from time import sleep

import logging

import requests
from colorama import Fore
from flask import json
from paho import mqtt
import paho.mqtt.client as mqtt

from rtxlib import info, error, debug, warn, direct_print, inline_print
from rtxlib.dataproviders.DataProvider import DataProvider
from python_ews.server_interface import ewsRESTInterface as eRI


class EWSDataProvider(DataProvider):
    """ implements a data provider based on http """

    def __init__(self, wf, dp):
        self.callBackFunction = None
        # load config
        try:
            self.chosen_metric = dp["chosen_metric"]
            info(">EWSDataPro    | Metric: " +  self.chosen_metric, Fore.CYAN)
        except KeyError as e:
            error("HTTPDataPro definition was incomplete: " + str(e))
            exit(1)

    def returnData(self):
        """Does a get_perception via the python_ews, and returns the metric contained within it corresponding to that chosen in definition.py"""
        perception = eRI.get_perception()
        
        metric = None

        if(self.chosen_metric in perception.metric_dict):
            metric = perception.metric_dict[self.chosen_metric]

        return metric

        
       
    def returnDataListNonBlocking(self):
        """ by logic this can not be non-blocking, so it is implemented as returnData """
        perception = eRI.get_perception()
        metric = perception.metric_dict[self.chosen_metric]
        return metric
        
