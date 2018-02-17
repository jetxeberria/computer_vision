import time

class Logger(object):
    
    def __init__(self, logger_file):
        self.logger_file = logger_file
        with open(self.logger_file,"w") as container:
            hour = time.strftime("%H:%M:%S")
            date = time.strftime("%d/%m/%Y")
            message = date+"-"+hour+"[log]<<Log start>>\n"
            container.write(message)



    def write_log(self, level, message):
        with open(self.logger_file,"a") as container:
            hour = time.strftime("%H:%M:%S")
            date = time.strftime("%d/%m/%Y")

            message = date+"-"+hour+"["+level+"]<<"+message+">>\n"
            container.write(message)

# CUANDO CIERRO EL ARCHIVO, DONDE SE QUEDA EL CURSOR
# log
# warn
# error
# (opcional) critical 
        
