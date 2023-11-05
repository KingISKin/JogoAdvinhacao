#-*- coding: utf-8 -*-

#Imports
import tkinter as tk
from tkinter import messagebox
import random
import sqlite3
import os
from datetime import datetime

#sqlite3 para poder interagir com o banco de dados sqlite
#os para realizar a execução de comandos do S.O ('clear' para Linux e Mac, 'cls' para windows)
#datetime para trabalhar com datas e horas

def criar_tabela_partidas():
    try:
        conn = sqlite3.connect("bancodedados.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS partidas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_usuario TEXT,
                tentativas INTEGER,
                inicio DATETIME,
                fim DATETIME)""")

        conn.close()  #dps de criar a tabela no banco de dados, eu fecho a conexao com o banco de dados
    except sqlite3.Error as e:
        print("Erro ao criar o banco de dados:", e)

def iniciar_jogo():
    global nickname
    nickname = entrada_nickname.get()
    if not nickname:
        messagebox.showerror("Nickname Inválido", "Digite um nickname válido.")
    else:
        criar_tabela_partidas()  # Chame a função para criar a tabela no início do jogo
        frame_inicio.pack_forget()
        frame_jogo.pack()
        reiniciar_jogo()

# ^aqui foi feita uma instrução sql para criar uma tabela chamada 'partidas' caso ela nao exista. e a tabela tem as colunas: id, nome de usuario, tentativas, inicio e fim.

def iniciar_jogo():
    global nickname
    nickname = entrada_nickname.get()
    if not nickname:
        messagebox.showerror("Nickname Inválido", "Digite um nickname válido.")
    else:
        frame_inicio.pack_forget()
        frame_jogo.pack()
        reiniciar_jogo()

def verificar_adivinhacao():
    try:
        palpite = int(entrada.get())
        if palpite < 0 or palpite > 100:
            messagebox.showerror("Palpite Inválido", "Digite um número entre 0 e 100.")
        else:
            comparar_palpite(palpite)
    except ValueError:
        messagebox.showerror("Entrada Inválida", "Digite um número válido.")

def comparar_palpite(palpite):
    global tentativas
    tentativas += 1
    tentativas_label.config(text=f"Tentativas: {tentativas}")
    
    if palpite == numero_secreto:
        messagebox.showinfo("Parabéns!", f"{nickname}, você acertou em {tentativas} tentativas.")
        reiniciar_jogo()
    elif palpite < numero_secreto:
        messagebox.showinfo("Palpite Baixo", "Tente um número maior.")
    else:
        messagebox.showinfo("Palpite Alto", "Tente um número menor.")
        
def reiniciar_jogo():
    global numero_secreto, tentativas
    numero_secreto = random.randint(0, 100)
    tentativas = 0
    entrada.delete(0, tk.END)
    tentativas_label.config(text=f"Tentativas: {tentativas}")

numero_secreto = random.randint(0, 100)
tentativas = 0
nickname = ""

#interface grafica
root = tk.Tk()
root.title("Jogo de Adivinhação")
root.geometry("300x300")
root.configure(bg="gray")

frame_inicio = tk.Frame(root, bg="gray")
frame_inicio.pack(pady=50)

label_nickname = tk.Label(frame_inicio, text="Digite seu nickname:", bg="gray", fg="black")
label_nickname.pack(pady=5)

entrada_nickname = tk.Entry(frame_inicio, width=20)
entrada_nickname.pack(pady=5)

botao_iniciar = tk.Button(frame_inicio, text="Iniciar Jogo", command=iniciar_jogo, bg="black", fg="white")
botao_iniciar.pack(pady=5)

frame_jogo = tk.Frame(root, bg="gray")

label_instrucoes = tk.Label(frame_jogo, text="Tente adivinhar o número secreto entre 0 e 100:", bg="gray", fg="black")
label_instrucoes.pack(pady=10)

entrada = tk.Entry(frame_jogo, width=5)
entrada.pack(pady=5)

botao_palpite = tk.Button(frame_jogo, text="Palpite", command=verificar_adivinhacao, bg="black", fg="white")
botao_palpite.pack(pady=5)

botao_reiniciar = tk.Button(frame_jogo, text="Reiniciar Jogo", command=reiniciar_jogo, bg="black", fg="white")
botao_reiniciar.pack(pady=5)

tentativas_label = tk.Label(frame_jogo, text="Tentativas: 0", bg="gray", fg="black")
tentativas_label.pack(pady=10)

root.mainloop()
