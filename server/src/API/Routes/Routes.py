
from API import app
from Models import Users
from flask import jsonify, request
from Controllers import PrinterData
from Models import returnTraceFile
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename
import sys
import requests

@app.route("/quit", methods=['Get'])
def stop_service():
    shutdown_hook = request.environ.get('werkzeug.server.shutdown')
    if shutdown_hook is not None:
        shutdown_hook()
    return "Tchau"

@app.route("/setData", methods=["Post"])
def insert_product():
    load_dotenv()
    
    content = request.json
    print(content)
    user = Users.InsertUser()
    verifyUser = user.insert_user(content['User'])[0].ID

    printer = PrinterData(verifyUser)
    printer.get_db_data(content['Printer'], content)
    # printerData = PrinterData()
    # content = request.json
    # printerData.set_data(content)
    # arq = open('.env', 'r')
    # read = arq.read()
    # (key, value) = read.split("=")
    # arq.close()
    # printerData.set_new_counter(int(value))
    

    # printerData.return_ip()
    return content

@app.route("/verifyTracerFile", methods=["Get"])
def tracerFile():
    content = request.query_string
    (key, value) = content.decode('utf8').split("=")
    response = returnTraceFile(value)
    return jsonify(response), 200

@app.route('/uploadedFile', methods=['Post'])
def uploadedFile():
    files = request.files['upload_file']
    fileName = request.files['Name'].read().decode('utf-8')
    files.save(os.path.join(app.config['UPLOAD_FOLDER'], fileName))
    #print(request.json)
    #filename = secure_filename(files.filename)
    
    return 'Ok'