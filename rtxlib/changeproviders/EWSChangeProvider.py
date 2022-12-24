from rtxlib.changeproviders.ChangeProvider import ChangeProvider
from rtxlib import info, error, debug
from colorama import Fore
from python_ews.server_interface import ewsRESTInterface as eRI

class EWSChangeProvider(ChangeProvider):
    def __init__(self, wf, cp):
        # load config
        try:
            info("> EWSChangePro  | ", Fore.CYAN)
        except KeyError:
            error("EWSChangePro was incomplete")
            exit(1)
       

    def applyChange(self, message):
        """ does a HTTP POST to the URL with the serialized message """
        eRI.change_configuration(message["config"])
