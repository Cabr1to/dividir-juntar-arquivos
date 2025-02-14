import os
import tkinter as tk
from tkinter import filedialog

DVD_SIZE = 4300 * 1024 * 1024  # 4.3 GB em bytes

def dividir_arquivo(file_path):
    try:
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
        print(f"Arquivo dividido em {part_num} partes de ~4.3GB")
        tk.messagebox.showinfo("Sucesso", f"Arquivo dividido em {part_num} partes!")
    except Exception as e:
        tk.messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def selecionar_arquivo():
    file_path = filedialog.askopenfilename(
        title="Selecione o arquivo para dividir",
        filetypes=(("Todos os arquivos", "*.*"),)
    )
    if file_path:
        dividir_arquivo(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal do tkinter
    selecionar_arquivo()