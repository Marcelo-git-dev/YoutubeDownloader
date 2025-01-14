from flask import Flask, render_template, request, flash  
from flask_socketio import SocketIO, emit  
import subprocess  
import os  
import re  
import threading  

app = Flask(__name__)  
app.secret_key = 's3cr3t'  # Chave secreta para mensagens flash  
socketio = SocketIO(app)  

def validar_url(url):  
    """Valida a URL do YouTube."""  
    regex = r'^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$'  
    return re.match(regex, url) is not None  

def baixar_youtube(link, formato, pasta):  
    """Executa o comando para baixar o vídeo do YouTube."""  
    cmd = f"cd {pasta} && youtube-dl -f {formato} --write-thumbnail {link}"  
    
    try:  
        with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:  
            while True:  
                output = p.stdout.readline()  
                if output == b"" and p.poll() is not None:  
                    break  
                if output:  
                    socketio.emit('download_status', {'data': output.decode(errors='replace')})  
            return p.poll()  
    except Exception as e:  
        socketio.emit('download_status', {'data': f'Erro: {str(e)}'})  

@socketio.on('start_download')  
def handle_download(data):  
    link = data['link']  
    formato = data['formato']  
    pasta = data['pasta']  
    
    if not validar_url(link):  
        emit('download_status', {'data': 'Por favor, insira uma URL válida do YouTube.'})  
        return  

    threading.Thread(target=baixar_youtube, args=(link, formato, pasta)).start()  # Executa o download em uma nova thread  

@app.route('/', methods=['GET'])  
def index():  
    return render_template('index.html')  

if __name__ == '__main__':  
    socketio.run(app, debug=True)