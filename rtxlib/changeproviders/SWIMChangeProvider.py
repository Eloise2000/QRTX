from rtxlib.changeproviders.ChangeProvider import ChangeProvider
from rtxlib import info, error, debug
from colorama import Fore
import socket

class SWIMChangeProvider(ChangeProvider):
    def __init__(self, wf, cp):
        # load config
        self.host = wf.host
        self.port = wf.port
        self.send_message = wf.send_message
        try:
            info("> SWIMChangePro  | ", Fore.CYAN)
        except KeyError:
            error("SWIMChangePro was incomplete")
            exit(1)
       

    def applyChange(self, message):
        """ does a HTTP POST to the URL with the serialized message """
        if(message == "initial" or message == "data"):
            return

        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # s.connect((self.host, self.port))
        resp = self.send_message(message)
        print("applied change, response: " + resp)


        # s.sendall(message.encode('UTF-8'))

        # s.close()