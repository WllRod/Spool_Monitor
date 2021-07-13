import os, sys
from components import userLogged

def WriteEnviroments():
    os.environ['CURRENT_PATH'] = os.path.dirname(sys.agrv[0])
    
    os.environ['CURRENT_USER'] = userLogged.return_loggedUser()