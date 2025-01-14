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
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    output = ""
    for line in p.stdout:
        line = line.decode(
            errors="replace" if (sys.version_info) < (3, 5) else "backslashreplace"
        ).rstrip()
        output += line
        print(line)
        window.Refresh() if window else None  # yes, a 1-line if, so shoot me
    retval = p.wait(timeout)
    return (retval, output)
    
    try:  
        with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:  
            while True:  
                output = p.stdout.readline()  
                if output == b"" and p.poll() is not None:  
                    break  
                if output:  
                    socketio.emit('download_status', {'data': output.decode(errors='replace')})  

        # Verificação do resultado do download  
        if p.returncode == 0:  
            socketio.emit('download_completed', {'data': 'Download concluído com sucesso!'})  
        else:  
            socketio.emit('download_failed', {'data': 'Erro ao baixar o vídeo.'})  

    except Exception as e:  
        socketio.emit('download_failed', {'data': f'Erro: {str(e)}'})  

@socketio.on('start_download')  
def handle_download(data):  
    link = data['link']  
    formato = data['formato']  
    pasta = data['pasta']  
    
    if not validar_url(link):  
        emit('download_failed', {'data': 'Por favor, insira uma URL válida do YouTube.'})  
        return  

    threading.Thread(target=baixar_youtube, args=(link, formato, pasta)).start()  # Executa o download em uma nova thread  

@app.route('/', methods=['GET'])  
def index():  
    return render_template('index.html')  

if __name__ == '__main__':  
    socketio.run(app, debug=True)  