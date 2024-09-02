#coding utf-8

import subprocess
import os
import sys


import tkinter as tk
from tkinter import messagebox

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def execute_script(script_name, filepath, output_folder, generate_table, generate_graph):
    script_path = get_resource_path(f"scripts\{script_name}")
    result = subprocess.run([
        "python", script_path, 
        filepath, 
        output_folder, 
        str(generate_table).lower(), 
        str(generate_graph).lower()
    ], capture_output=True, text=True)

    # Afficher la sortie et les erreurs
    #print("STDOUT:", result.stdout)
    #print("STDERR:", result.stderr)

    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, result.args)

def show_confirmation_message(output_folder):
    # Créer la fenêtre principale
    root = tk.Tk()
    root.withdraw()  # Masquer la fenêtre principale

    # Afficher un message de confirmation
    messagebox.showinfo("Confirmation", f"Data saved in {output_folder} with success!")

    # Détruire la fenêtre principale après que l'utilisateur ait cliqué sur "OK"
    root.destroy()
