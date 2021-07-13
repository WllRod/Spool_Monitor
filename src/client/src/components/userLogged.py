import subprocess
import os, sys

def return_loggedUser():
    cLoggedUser = subprocess.Popen(
            'cd {} && powershell ./CLU.ps1'.format(os.path.dirname(sys.argv[0])), 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            stdin=subprocess.DEVNULL, 
            shell=True
        )

    array = []
    text = ""
    for lines in cLoggedUser.stdout.readlines():
        lines = lines.decode('windows-1252')
        lines = lines.replace("\n", "").replace("\r", "")
        lines = lines.split(":")
        if(lines == ['']):
            pass
        else:
            format_key = lines[0].replace(" ", "")
            format_value = lines[1].replace(" ", "")
            
            if(format_key == "USERNAME"):
                dictUser = {"USERNAME": format_value}
                
            elif(format_key == "SESSIONNAME"):
                dictUser['SESSIONNAME'] = format_value
                array.append(dictUser)
            
            text += format_value
            text += "\n"
    
    arq = open('USER.txt','w')
    arq.write(text)
    arq.close()
    user = ""     
    for x in range(len(array)):
        if(array[x]['SESSIONNAME'] == "console"):
            user = array[x]['USERNAME'].replace(">", "")
            break
    return user
