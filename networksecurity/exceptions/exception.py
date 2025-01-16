import sys
import traceback
from networksecurity.logging import logger

class NetworkSecurityException(Exception):

    def __init__(self,error_message,error_details:sys):

        self.error_message=error_message

        _,_,exc_traceback=error_details.exc_info()

        
        tracebacks=traceback.extract_tb(exc_traceback)
        last_traceback = tracebacks[-1]  # Get the last frame

        # Store filename and line number from the last traceback frame
        self.filename = last_traceback.filename
        self.line_no = last_traceback.lineno

    def __str__(self):

        return "Error Occured in Python Script name [{0}] line number [{1}] error message[{2}]".format(
            self.filename,self.line_no,str(self.error_message))
        
if __name__=="__main__":
    try:
        logger.logger.info("Try Block executed")
        a=1/0
        print("These will not be printed",a)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
        


