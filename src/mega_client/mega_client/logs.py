import logging
try:
    from setting import DEAFULT_LOG_DEBUG
    from setting import LOG_FILE_NAME
except:
    DEAFULT_LOG_DEBUG=False
    LOG_FILE_NAME='/tmp/mega_client.log'


class Logger:
    def __init__(self,model):
        if DEAFULT_LOG_DEBUG :
            self.level=0
        else:
            self.level=3    
        self.model=model
    def log(self):
        LEVELS = {0: logging.DEBUG,
                  3: logging.INFO,
                  2: logging.WARNING,
                  1: logging.ERROR}
        level=LEVELS.get(self.level,logging.NOTSET)   
        logging.basicConfig(level=level,
                            filename=LOG_FILE_NAME,
                            datefmt='%Y-%m-%d %H:%M:%S',
                            format='%(asctime)s %(name)-12s %(levelname)-5s %(message)s')
        logger=logging.getLogger(self.model)
        return logger

if __name__=="__main__":
    log=Logger('test').log()
    log.error("error")
