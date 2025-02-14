import os
import tkinter as tk
from tkinter import filedialog, messagebox
import winreg  # Módulo para manipular o registro do Windows

def adicionar_menu_contexto():
    try:
        # Caminho para o executável
        caminho_exe = os.path.abspath(__file__)  # Pega o caminho do script atual
        if caminho_exe.endswith('.exe'):
            caminho_exe = os.path.abspath(sys.argv[0])  # Pega o caminho do executável

        # Cria a chave no registro
        chave = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\JuntarArquivos\command")
        winreg.SetValue(chave, '', winreg.REG_SZ, f'"{caminho_exe}" "%1"')
        winreg.CloseKey(chave)

        messagebox.showinfo("Sucesso", "Opção 'Juntar Arquivos' adicionada ao menu de contexto!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao adicionar ao menu de contexto: {e}")

def juntar_arquivos(primeira_parte):
    try:
        # Verifica se o arquivo é uma parte válida
        if not primeira_parte.endswith(".part000"):
            messagebox.showerror("Erro", "Selecione a primeira parte do arquivo (extensão .part000).")
            return

        # Define o nome base do arquivo original (remove ".part000")
        diretorio = os.path.dirname(primeira_parte)
        nome_base = os.path.basename(primeira_parte)[:-8]  # Remove ".part000"

        # Encontra todas as partes do arquivo
        partes = sorted(
            [f for f in os.listdir(diretorio) if f.startswith(nome_base) and f.endswith((".part000", ".part001", ".part002", ".part003"))],
            key=lambda x: int(x[-3:])  # Ordena pelas últimas 3 dígitos (000, 001, 002, etc.)
        )

        if not partes:
            messagebox.showerror("Erro", "Nenhuma parte do arquivo foi encontrada.")
            return

        # Pergunta ao usuário onde salvar o arquivo recombinado
        output_path = filedialog.asksaveasfilename(
            title="Salvar arquivo recombinado como",
            defaultextension=".*",
            initialfile=nome_base
        )

        if not output_path:
            return  # Usuário cancelou

        # Junta as partes
        with open(output_path, 'wb') as arquivo_final:
            for parte in partes:
                parte_path = os.path.join(diretorio, parte)
                with open(parte_path, 'rb') as arquivo_parte:
                    arquivo_final.write(arquivo_parte.read())

        messagebox.showinfo("Sucesso", f"Arquivo recombinado com sucesso em:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao juntar os arquivos: {e}")

def selecionar_primeira_parte():
    primeira_parte = filedialog.askopenfilename(
        title="Selecione a primeira parte do arquivo (.part000)",
        filetypes=(("Partes de arquivo", "*.part000"),)
    )
    if primeira_parte:
        juntar_arquivos(primeira_parte)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal do tkinter

    # Adiciona a opção ao menu de contexto (se não estiver presente)
    try:
        winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\JuntarArquivos")
    except FileNotFoundError:
        adicionar_menu_contexto()

    selecionar_primeira_parte()