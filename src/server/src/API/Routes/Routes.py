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
from Error import ErrorLog, send_email
import sys
import socket
from datetime import datetime
from Log import write_log

hostname    = socket.gethostname()
ip_address  = socket.gethostbyname(hostname)
data        = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
myLogger    = write_log()

myLogger.info(f"[{data}] - Server is running on IP: {ip_address}")
def generate_error(error):
    """Função chamada em exceções de erros, gera os dados necessários para ser enviado o Log de erro"""
    exc_type, exc_obj, exc_tb = sys.exc_info()
    filename = os.path.basename(os.path.dirname(__file__))+"\\"+os.path.basename(__file__)
    
    ErrorLog(
        Error=error,
        Script=filename,
        Line=exc_tb.tb_lineno,
        User=ip_address
    )

@app.route("/", methods=['Get'])
def returnIP():
    
    return f"IP: {ip_address}"

@app.route("/quit", methods=['Get'])
def stop_service():
    """Função para tombar a execução da API, chamada atraves da Rota /quit"""

    data        = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    shutdown_hook = request.environ.get('werkzeug.server.shutdown')
    if shutdown_hook is not None:
        myLogger.info(f"[{data}] - CLient IP:{request.remote_addr} - Route:/quit")
        shutdown_hook()
    return "Tchau"

@app.route("/setData", methods=["Post"])
def insertData():
    """Função responsável por receber os dados dos client's e chamar as devidas funções para registro"""

    try:
        load_dotenv()
        data        = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        content = request.json
        
        user = Users.InsertUser()
        printer = InsertPrinter()
        verifyUser = user.insert_user(content['User'])[0].ID
        #printer.insert_printer(content['IP'], content['Printer'])
        printer = PrinterData(verifyUser, app.config['UPLOAD_FOLDER'])
        printer.get_db_data(content['Printer'], content)
        for keys, values in content.items():
            myLogger.info(f"[{data}] - Client IP:{request.remote_addr} - Route:/setData - Params: [{keys}] - {values}")
        return content
    except Exception as e:
        generate_error(e)
        return jsonify(), 404
        

@app.route("/verifyTracerFile", methods=["Get"])
def tracerFile():
    """Função responsável por verificar se é necessário monitorar o arquivo do que o usuário esta imprimindo"""

    try:
        data        = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        content = request.query_string
        (key, value) = content.decode('utf8').split("=")
        user = Users.InsertUser()
        verifyUser = user.insert_user(value)
        response = returnTraceFile(value)
        myLogger.info(f"[{data}] - Client IP:{request.remote_addr} - Route:/verifyTracerFile - Params:{content.decode('utf-8')}")
        return jsonify(response), 200
    except Exception as e:
        generate_error(e)
        return jsonify(), 404

@app.route('/uploadedFile', methods=['Post'])
def uploadedFile():
    """Função responsável por salvar o arquivo impresso, caso seja necessário"""

    try:
        data        = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        files = request.files['upload_file']
        fileName = request.files['Name'].read().decode('utf-8')
        files.save(os.path.join(app.config['UPLOAD_FOLDER'], fileName))
        myLogger.info(f"[{data}] - Client IP:{request.remote_addr} - Route:/uploadedFile - Params:{fileName}")
        return 'Ok'
    except Exception as e:
        generate_error(e)
        return jsonify(), 404

@app.route("/sendClientErrorLog", methods=["Get"])
def sendErrorLog():
    """Função responsavel por enviar log de erro dos Client's"""
    try:
        data        = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        content = request.json
        myLogger.info(f"[{data}] - Client IP:{request.remote_addr} - Route:/sendClientErrorLog - Params:{content['Message']}")

        send_email(content['Message'], 'SpoolMonitorClient Error')
        return jsonify(), 200
    except Exception as e:
        generate_error(str(e))
        return jsonify(), 404