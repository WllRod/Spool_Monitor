import os
import logging
import logging.handlers

def write_log():
    log_path    = os.getenv("LOCAL_PATH")+"\\logging.log"
    myLogger    = logging.getLogger("logging")
    
    handler     = logging.handlers.RotatingFileHandler(log_path)   
    myLogger.setLevel(logging.INFO)

    myLogger.addHandler(handler)

    return myLogger

