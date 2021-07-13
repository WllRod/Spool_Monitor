"""
DESCRIÇÃO: IRÁ GERAR E ENVIAR O LOG DE ERRO E FINALIZARÁ A EXECUÇÃO DA API
_____________________________________________________________________________
AUTOR: WILLIAM RODRIGUES
_____________________________________________________________________________
DATA: 08/07/2021
"""


import smtplib
from email.mime.text import MIMEText
from datetime import date, datetime
from components.Config import returnConfig

def send_email(texto, assunto):
    
    """
    ENVIARÁ O TEXTO DE LOG PARA OS EMAILS CADASTRADOS NO config.json
    param:  texto -> TEXTO DE LOG A SER ENVIADO
    """

    emailConfig = returnConfig()['EMAIL_CONFIG']
    print(emailConfig)

    smtp_ssl_host = 'smtp.gmail.com'
    smtp_ssl_port = 465
    
    username = emailConfig['From']['Username']
    password = emailConfig['From']['Password']

    from_addr = emailConfig['From']['Email']
    to_addrs = emailConfig['To']

    print(username, password)
    
    message = MIMEText(texto)
    message['subject'] = "TESTE"
    message['from'] = from_addr
    message['to'] = ', '.join(to_addrs)

    
    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    
    server.login(username, password)
    server.sendmail(from_addr, to_addrs, message.as_string())
    server.quit()

def ErrorLog(**kwargs):
    """
    Gerará o texto de log e tombará a execução da API
    params: **kwargs -> dicionario de dados
    """
    data_atual = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    text = f"[{data_atual}]\n"
    for keys, values in kwargs.items():
        text += f"{keys}: {values}\n"
    
    send_email(text, "Monitorador De Spool - Client")
    

