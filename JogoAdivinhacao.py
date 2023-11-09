#Imports
import pygame
import tkinter as tk
import random
import sqlite3
import os

def iniciar_jogo():
    global nickname
from datetime import datetime
import customtkinter
from CTkMessagebox import CTkMessagebox

pygame.init()
pygame.mixer.init()

#efeitos
#on = pygame.mixer.Sound("data/on.ogg")
#off = pygame.mixer.Sound("data/off.ogg")
#click = pygame.mixer.Sound("data/click_sound_1.mp3")

#importações: o codigo começa importando os módulos necessários para o jogo
#tkinter interface grafica do python.
#sqlite3 para interagir com um banco de dados SQLite
#datetime para trabalhar com datas e horas

#variavel de ambiente funciona como valores definidos no ambiente onde o programa está sendo executado
diretorio = os.getenv('JOGO_DB',f"{'/'.join(__file__.split('/')[1:-1])}") #obtem o caminho do banco de dados atraves da variavel de ambiente JOGO_DB, caso a variavel nao esteja definida, será criado no diretório atual.
db_path=f"/{diretorio}/bancodedados.db" 

def criar_tabela_partidas(): #função criar_tabela_partidas responsável por criar uma tabela chamada "partidas" no banco de dados SQLite 'exemplo.db', se ela ainda não existir.
    global db_path
        
    conn = sqlite3.connect(db_path) 
    cursor = conn.cursor() #é estabelecida uma conexão com o banco de dados SQLite 'bancodedados.db' usando a função 'connect' do módulo 'sqlite3'. Se o banco de dados não existir, ele será criado neste momento.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS partidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_usuario TEXT,
            tentativas INTEGER,
            inicio TIMESTAMP,
            fim DATETIME)""")
    # ^aqui foi feita uma instrução sql para criar uma tabela chamada 'partidas' caso ela nao exista. e a tabela tem as colunas: id, nome de usuario, tentativas, inicio e fim.
    conn.commit()
    conn.close()#após de criar a tabela no banco de dados, eu fecho a conexao com o banco de dados

def inserir_partida(nome_usuario, tentativas, inicio, fim):
    global db_path
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO partidas (nome_usuario, tentativas, inicio, fim) VALUES (?, ?, ?, ?)",
        (nome_usuario, tentativas, inicio, fim))
    conn.commit()
    conn.close()  # dps de inserir os dados, a conexão com o banco de dados é fechada.

def iniciar_jogo():
    global nickname
    nickname = entrada_nickname.get()
    if not nickname:
        CTkMessagebox(title="Não seja tímido", message="Digite um nome válido.", icon="cancel")
    else:
        criar_tabela_partidas() 
        frame_inicio.pack_forget()
        frame_jogo.pack()
        reiniciar_jogo()

def verificar_adivinhacao():
    try:
        palpite = int(entrada.get())
        if palpite < 0 or palpite > 100:
            CTkMessagebox(title="Palpite Inválido", message="Digite um número entre 0 e 100.", icon="cancel")
        else:
            comparar_palpite(palpite)
    except ValueError:
        CTkMessagebox(title="Caractere inválido", message="Digite um número válido.", icon="cancel")

def comparar_palpite(palpite):
    global tentativas, inicio_jogo, entrada, label_nickname, message_label
    tentativas += 1
    tentativas_label.configure(text=f"Tentativas: {tentativas}")
    
    if palpite == numero_secreto:
        CTkMessagebox(title="Parabéns!", message=f"{nickname}, você acertou em {tentativas} tentativas.")
        inserir_partida(nickname, tentativas, inicio_jogo, datetime.now())
        reiniciar_jogo()
    elif palpite < numero_secreto:
        message_label.configure(text=f"Tente um número maior")
        entrada.delete(0, 3)
        entrada.focus_set()

    else:
        message_label.configure(text=f"Tente um número menor")
        entrada.delete(0, 3)
        entrada.focus_set()
       
def reiniciar_jogo():
    global numero_secreto, tentativas, inicio_jogo
    numero_secreto = random.randint(1, 100) #aqui a funcao inicia definindo um numero aleatorio entre 1 e 100 e inicializa o contador de tentativas como 0.
    tentativas = 0
    entrada.delete(0, tk.END)
    tentativas_label.configure(text=f"Tentativas: {tentativas}")
    inicio_jogo = datetime.now() #obtida a data e hora atuais

def reply(name):
    global nickname
    nickname = name
    iniciar_jogo()

#INTERFACE GRAFICA
inicio_jogo = datetime.now() #incio do jogo
janela = customtkinter.CTk()
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
janela.title("Jogo de Adivinhação")
janela.geometry("900x550")
janela.maxsize(width=900, height=550)
janela.minsize(width=500, height=300)
janela.resizable(width=False, height=False)
frame_jogo = customtkinter.CTkFrame(janela)

frame_inicio = customtkinter.CTkFrame(master=janela,width=100,height=100)
frame_inicio.pack(padx=10, pady=90)

label_nickname = customtkinter.CTkLabel(frame_inicio, text="Bem vindo! Qual seu nome?")
label_nickname.pack(padx=25, pady=25)

entrada_nickname = customtkinter.CTkEntry(master=frame_inicio,width=250, placeholder_text="Nome")
entrada_nickname.bind("<Return>", (lambda event: reply(entrada_nickname.get())))
entrada_nickname.pack(padx=25, pady=25)

botao_iniciar = customtkinter.CTkButton(frame_inicio, text="Iniciar Jogo", command=iniciar_jogo)
botao_iniciar.pack(padx=25, pady=25)
#click.play()

label_instrucoes = customtkinter.CTkLabel(frame_jogo, text="Vamos lá. Tente adivinhar o número secreto entre 0 e 100:")
label_instrucoes.pack(padx=25, pady=25)
#click.play()
entrada = customtkinter.CTkEntry(frame_jogo, placeholder_text="Número")
entrada.bind("<Return>", (lambda event: verificar_adivinhacao()))
entrada.pack(pady=5)

message_label = customtkinter.CTkLabel(frame_jogo, text="Boa sorte!")
message_label.pack(padx=1, pady=1)

botao_palpite = customtkinter.CTkButton(frame_jogo, text="Palpite", command=verificar_adivinhacao)
botao_palpite.pack(padx=25, pady=25)

botao_reiniciar = customtkinter.CTkButton(frame_jogo, text="Reiniciar Jogo", command=reiniciar_jogo, fg_color="red")
botao_reiniciar.pack(padx=25, pady=25)

tentativas_label = customtkinter.CTkLabel(frame_jogo, text="Tentativas: 0")
tentativas_label.pack(padx=25, pady=25)

#switch de iluminação
frame_switch = customtkinter.CTkFrame(master=janela,width=50,height=50).place(x=850, y=550)

switch1 = customtkinter.StringVar(value="on")
switch2 = customtkinter.StringVar(value="off")

def acionamento_switch():
    if switch1.get() == "on" and switch2.get() == "off":
        customtkinter.set_appearance_mode("dark")
    #off.play()
    #click.play()
    if switch1.get() == "off" and switch2.get() == "off":
        customtkinter.set_appearance_mode("light") 
    #on.play()
    #click.play()

switch1 = customtkinter.CTkSwitch(master=janela, text="Modo Escuro", command=acionamento_switch, variable=switch1, onvalue="on", offvalue="off")
switch1.pack(padx=100,pady=5)

#musicaaaaaa
#pygame.mixer.music.load("data/8bit Bossa.mp3")
#pygame.mixer.music.play(-1)#-1 eh a quantidade de tempo que a musica vai repetir, pq o projeto entende q eu quero infinitamente

janela.mainloop()
pygame.quit()