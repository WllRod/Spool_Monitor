import smtplib
from email.mime.text import MIMEText
from datetime import date, datetime
import requests, sys

def send_email(texto):
# conexão com os servidores do google
    smtp_ssl_host = 'smtp.gmail.com'
    smtp_ssl_port = 465
    # username ou email para logar no servidor
    username = 'relatorioscda@gmail.com'
    password = '$2@cda123'

    from_addr = 'relatorioscda@gmail.com'
    to_addrs = ['william.rodrigues@casadoalemao.com.br', 'alexandre.delgado@casadoalemao.com.br']

    # a biblioteca email possuí vários templates
    # para diferentes formatos de mensagem
    # neste caso usaremos MIMEText para enviar
    # somente texto
    message = MIMEText(texto)
    message['subject'] = "XML's Download Log"
    message['from'] = from_addr
    message['to'] = ', '.join(to_addrs)

    # conectaremos de forma segura usando SSL
    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    # para interagir com um servidor externo precisaremos
    # fazer login nele
    server.login(username, password)
    server.sendmail(from_addr, to_addrs, message.as_string())
    server.quit()

def ErrorLog(**kwargs):
    data_atual = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    text = f"[{data_atual}]\n"
    for keys, values in kwargs.items():
        text += f"{keys}: {values}\n"
    
    print(text)
    try:
        requests.get('http://localhost:5000/quit')
    except requests.exceptions.ConnectionError:
        sys.exit(0)
    #sys.exit(0)
    #