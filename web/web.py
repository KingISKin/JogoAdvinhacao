from flask import Flask
from flask import render_template
import sqlite3
app = Flask(__name__)

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

    return render_template ('index.html', resultados = resultados, media=media, ranking=ranking)