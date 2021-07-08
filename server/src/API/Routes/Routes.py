
from API import app
from Models import Users, returnTraceFile, InsertPrinter
from flask import jsonify, request
from Controllers import PrinterData
from dotenv import load_dotenv
import os
from Error import ErrorLog
import sys

def generate_error(error):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    filename = os.path.basename(os.path.dirname(__file__))+"\\"+os.path.basename(__file__)
    
    ErrorLog(
        Error=error,
        Script=filename,
        Line=exc_tb.tb_lineno
    )

@app.route("/isRunning", methods=["Get"])
def isRunning():
    data = { "isRunning": True }
    return jsonify(data)

@app.route("/quit", methods=['Get'])
def stop_service():
    
    shutdown_hook = request.environ.get('werkzeug.server.shutdown')
    if shutdown_hook is not None:
        shutdown_hook()
    return "Tchau"

@app.route("/setData", methods=["Post"])
def insert_product():
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
    try:
        content = request.query_string
        (key, value) = content.decode('utf8').split("=")
        response = returnTraceFile(value)
        return jsonify(response), 200
    except Exception as e:
        generate_error(e)
        return jsonify(), 404

@app.route('/uploadedFile', methods=['Post'])
def uploadedFile():

    try:
        files = request.files['upload_file']
        fileName = request.files['Name'].read().decode('utf-8')
        files.save(os.path.join(app.config['UPLOAD_FOLDER'], fileName))
        #print(request.json)
        #filename = secure_filename(files.filename)
        
        return 'Ok'
    except Exception as e:
        generate_error(e)
        return jsonify(), 404