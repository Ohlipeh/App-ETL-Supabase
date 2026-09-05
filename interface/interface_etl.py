# Para geração da intarface fiz importação do customtkinter
import customtkinter as ctk

# Optei por filedialog para abrir uma caixa de diálogo que permite ao usuário escolher arquivo e pasta no sistema operacional.
from tkinter import filedialog
import os

# importei o dotenv para ficar funcional.
from dotenv import load_dotenv

from vendas.etl_vendas import ExportadorDados, ExtratorDados, ProcessadorRegras

load_dotenv()


# Método para dar inicio a interface.
def iniciar_intarface():
    # Cria uma janela principal.
    root = ctk.CTk()
    root.title("Extrator CSV")
    root.geometry("500x500")

    # Gera um título para a janela principal.
    titulo = ctk.CTkLabel(root, text="Extrator CSV", font=("Arial", 28, "bold"))
    titulo.pack(pady=30)

    # Optei por colocar um Label logo a cima do botão
    lbl_planilha = ctk.CTkLabel(
        root, text="Aguardando planilha", font=("Arial", 12, "bold")
    )
    lbl_planilha.pack()

    # Criei um método selecionar_Arquivo para facíl leitura, optei por colocar um try/except/Exception para faciltar a leitura do cliente se errar ou colocar arquivos invalidos.
    def selecionar_arquivo():
        arquivo = filedialog.askopenfilename()
        if arquivo == "":
            print("Nenhum arquivo selecionado!")
            return
        else:
            print("Arquivo adicionado!")
        try:
            extrator = ExtratorDados(arquivo)
            host = os.getenv("DB_HOST")
            port = os.getenv("DB_PORT")
            database = os.getenv("DB_NAME")
            user = os.getenv("DB_USER")
            senha = os.getenv("DB_PASSWORD")
            dados = extrator.ler_arquivo()

            processador = ProcessadorRegras(dados)
            tabela_tratada = processador.limpar_nulos()

            exportador = ExportadorDados(
                tabela_tratada, host, port, database, user, senha
            )
            resultados = exportador.salvar_relatorio()
            lbl_planilha.configure(text=resultados)
            print(resultados)

        except FileNotFoundError:
            lbl_planilha.configure(text="ERRO: O arquivo não foi localizado!")

        except Exception as erro:
            lbl_planilha.configure(text=f"Ocorreu um erro inesperado: {erro}")

    # Função que cria os botões.
    btn_selecionar = ctk.CTkButton(
        root, text="Buscar Planilha", command=selecionar_arquivo
    )
    btn_selecionar.pack(pady=5)

    root.mainloop()
