from flask import Flask, request, session, redirect, url_for
from flask import render_template
import sqlite3
from datetime import datetime
import random
import sqlite3
import logging

app = Flask(__name__)
app.secret_key = "dskfjadsfjdslkfjasdflkdsajflasdfj"

@app.route("/",  methods = ['POST', 'GET'])
def index(nome_usuario=""):
    if request.method == "POST":
        if 'nome_usuario' not in session:
            print(f"usuario postado: {request.form.get('nome_usuario')}")
            session['nome_usuario'] = request.form.get('nome_usuario')
            return redirect(url_for('jogo'))
        else:
            return redirect(url_for('jogo'))
    if request.method == "GET":
        if 'nome_usuario'  in session:
            #print (f"conteudo da sessao: {session}")
            return redirect(url_for('jogo'))
    return render_template ('index.html')

@app.route("/jogo", methods = ['POST', 'GET'])
def jogo():
    mensagem={"type":"info","msg": "Boa Sorte"}
    if request.method == "POST":
        if "logout" in request.form:
            session.clear()
            print ("fazendo logout")
            if "partida" in session:
                print ("fazendo logout if")
                del session['partida']
                return redirect(url_for('index'))
            else:
                print ("fazendo logout else")
                return redirect(url_for('index'))
        palpite = request.form.get('palpite')
        print(f"session:{session}")
        print(f"palpite:{palpite}")
        try:
            if 'partida' not in session:
                session['partida'] = True
                session ['inicio'] = datetime.now()
                session['numero'] = random.randint(0,100)
                session ['tentativas'] = 0
            if 'reset' in request.form:
                print("reiniciando o jogo")
                session ['tentativas']=0
                session ['inicio']= datetime.now()
                session ['numero']=random.randint(0,100)
                mensagem ={"type":"info", "msg": "Você está em um novo jogo, boa sorte"}
            elif "envia_palpite" in request.form:
                try:
                    if int(palpite) < 0 or int(palpite) >100:
                        mensagem={"type":"danger", "msg": "SOMENTE NÚMEROS DE 0 A 100 >:("}
                    elif  int(session['numero']) == int(palpite):
                        mensagem={"type":"success", "msg":"Parabéns, você acertou."}
                        try:
                            conn = sqlite3.connect("../bancodedados.db")
                            print(f"conexao{conn}")
                            cursor = conn.cursor()
                            cursor.execute ("INSERT INTO partidas (nome_usuario, tentativas, inicio, fim) VALUES (?, ?, ?, ?);",
                                (session['nome_usuario'], session['tentativas'], session['inicio'], datetime.now()))
                            conn.commit()
                            print(f"conexao{cursor}")
                            conn.close() 
                        except (Exception) as e:
                            mensagem = {"type":"danger", "msg":e}
                    elif int(palpite) > session['numero']:
                        mensagem={"type":"info", "msg":"Tente um número menor"}
                    elif int (palpite) < session['numero']:
                        mensagem={"type":"info", "msg":"Tente um número maior"}
                    session ['tentativas']= int(session['tentativas']) +1
                except (ValueError) as e:
                    mensagem={"type":"danger", "msg":"Insira apenas números"}
                    session ['tentativas']= int(session['tentativas']) +1
        except (Exception) as e:
            mensagem = "Erro: {e}"
    return render_template ('jogo.html', mensagem=mensagem)

@app.route("/ranking")
def ranking():
    conn = sqlite3.connect("../bancodedados.db")
    cursor = conn.cursor()
    cursor.execute("""
        select nome_usuario, tentativas, strftime('%M:%S', strftime('%s', datetime(fim, 'localtime')) - strftime('%s', datetime(inicio, 'localtime')), 'unixepoch')  as tempo
        from partidas order by tentativas, tempo asc""")
    resultados = cursor.fetchall()
    cursor.execute("""select avg(tentativas) as media
          from partidas """)
    media = cursor.fetchone()
    cursor.execute("""SELECT nome_usuario, min(tentativas) as min, max(tentativas) as max, avg(tentativas) as media, count(*) as partidas FROM partidas GROUP by nome_usuario ORDER by min ASC LIMIT 10""")
    ranking = cursor.fetchall()
    conn.close()
    return render_template ('ranking.html', resultados = resultados, media=media, ranking=ranking)