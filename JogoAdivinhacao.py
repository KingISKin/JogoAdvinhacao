#Imports
import tkinter as tk
from tkinter import messagebox
import random
import sqlite3

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
