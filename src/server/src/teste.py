import os

arq = open("TESTE.txt", "r")
counter = ""
for x in arq.readlines():
    x = ''.join(x).replace("\n", "")
    
    if(x.find("=") > -1):
        (key, value) = x.split("=")
        if(key == "Value"):
            counter = value
arq.close()
arq = open("counter", "w")
arq.write(counter)
arq.close()