""""
DESCRIÇÃO: NESTE FONTE ESTÃO AS ROTAS DA API
----------------------------------------------
AUTOR: WILLIAM RODRIGUES
----------------------------------------------
DATA: 08/07/2021
"""

import requests
from API import app
from Models import Users, returnTraceFile, InsertPrinter
from flask import jsonify, request, Flask
from Controllers import PrinterData
from dotenv import load_dotenv
import os
from Error import ErrorLog
import sys
import socket

def generate_error(error):
    """Função chamada em exceções de erros, gera os dados necessários para ser enviado o Log de erro"""
    exc_type, exc_obj, exc_tb = sys.exc_info()
    filename = os.path.basename(os.path.dirname(__file__))+"\\"+os.path.basename(__file__)
    
    ErrorLog(
        Error=error,
        Script=filename,
        Line=exc_tb.tb_lineno
    )

@app.route("/", methods=['Get'])
def returnIP():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return f"IP: {ip_address}"

@app.route("/quit", methods=['Get'])
def stop_service():
    """Função para tombar a execução da API, chamada atraves da Rota /quit"""

    shutdown_hook = request.environ.get('werkzeug.server.shutdown')
    if shutdown_hook is not None:
        shutdown_hook()
    return "Tchau"

@app.route("/setData", methods=["Post"])
def insertData():
    """Função responsável por receber os dados dos client's e chamar as devidas funções para registro"""

    try:
        load_dotenv()
        
        content = request.json
        
        user = Users.InsertUser()
        printer = InsertPrinter()
        verifyUser = user.insert_user(content['User'])[0].ID
        printer.insert_printer(content['IP'], content['Printer'])
        printer = PrinterData(verifyUser, app.config['UPLOAD_FOLDER'])
        printer.get_db_data(content['Printer'], content)
       
        return content
    except Exception as e:
        generate_error(e)
        return jsonify(), 404
        

@app.route("/verifyTracerFile", methods=["Get"])
def tracerFile():
    """Função responsável por verificar se é necessário monitorar o arquivo do que o usuário esta imprimindo"""

    try:
        
        content = request.query_string
        (key, value) = content.decode('utf8').split("=")
        user = Users.InsertUser()
        verifyUser = user.insert_user(value)
        response = returnTraceFile(value)
        return jsonify(response), 200
    except Exception as e:
        generate_error(e)
        return jsonify(), 404

@app.route('/uploadedFile', methods=['Post'])
def uploadedFile():
    """Função responsável por salvar o arquivo impresso, caso seja necessário"""

    try:
        files = request.files['upload_file']
        fileName = request.files['Name'].read().decode('utf-8')
        files.save(os.path.join(app.config['UPLOAD_FOLDER'], fileName))
        
        return 'Ok'
    except Exception as e:
        generate_error(e)
        return jsonify(), 404