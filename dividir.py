import ctypes
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import winreg

def is_admin():
    """Verifica se o script está sendo executado como administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def adicionar_menu_contexto():
    try:
        # Caminho para o executável
        if getattr(sys, 'frozen', False):
            caminho_exe = os.path.abspath(sys.argv[0])
        else:
            caminho_exe = os.path.abspath(__file__)

        # Cria a chave no registro
        chave = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\DividirArquivo\command")
        winreg.SetValue(chave, '', winreg.REG_SZ, f'"{caminho_exe}" "%1"')
        winreg.CloseKey(chave)

        messagebox.showinfo("Sucesso", "Opção 'Dividir Arquivo' adicionada ao menu de contexto!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao adicionar ao menu de contexto: {e}")

def dividir_arquivo(file_path):
    try:
        # Lógica para dividir o arquivo
        DVD_SIZE = 4300 * 1024 * 1024  # 4.3 GB em bytes
        with open(file_path, 'rb') as f:
            part_num = 0
            while True:
                chunk = f.read(DVD_SIZE)
                if not chunk:
                    break
                part_name = f"{file_path}.part{part_num:03d}"
                with open(part_name, 'wb') as part_file:
                    part_file.write(chunk)
                part_num += 1
        messagebox.showinfo("Sucesso", f"Arquivo dividido em {part_num} partes de ~4.3GB!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao dividir o arquivo: {e}")

def selecionar_arquivo():
    file_path = filedialog.askopenfilename(
        title="Selecione o arquivo para dividir",
        filetypes=(("Todos os arquivos", "*.*"),)
    )
    if file_path:
        dividir_arquivo(file_path)

if __name__ == "__main__":
    if is_admin():
        # Se estiver rodando como administrador, executa o script normalmente
        root = tk.Tk()
        root.withdraw()  # Oculta a janela principal do tkinter

        # Adiciona a opção ao menu de contexto (se não estiver presente)
        try:
            winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\DividirArquivo")
        except FileNotFoundError:
            adicionar_menu_contexto()

        selecionar_arquivo()
    else:
        # Se não estiver rodando como administrador, solicita elevação
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)