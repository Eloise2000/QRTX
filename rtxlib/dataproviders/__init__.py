from logging import error

from rtxlib.dataproviders.HTTPRequestDataProvider import HTTPRequestDataProvider
from rtxlib.dataproviders.IntervalDataProvider import IntervalDataProvider
from rtxlib.dataproviders.KafkaConsumerDataProvider import KafkaConsumerDataProvider
from rtxlib.dataproviders.MQTTListenerDataProvider import MQTTListenerDataProvider
# from rtxlib.dataproviders.EWSDataProvider import EWSDataProvider
from rtxlib.dataproviders.SWIMDataProvider import SWIMDataProvider


def init_data_providers(wf):
    """ creates the required data providers """
    createInstance(wf, wf.primary_data_provider)
    if hasattr(wf, "secondary_data_providers"):
        for cp in wf.secondary_data_providers:
            createInstance(wf, cp)


def createInstance(wf, cp):
    """ creates a single instance of a data provider and stores the instance as reference in the definition """
    if cp["type"] == "kafka_consumer":
        cp["instance"] = KafkaConsumerDataProvider(wf, cp)
    elif cp["type"] == "mqtt_listener":
        cp["instance"] = MQTTListenerDataProvider(wf, cp)
    elif cp["type"] == "http_request":
        cp["instance"] = HTTPRequestDataProvider(wf, cp)
    elif cp["type"] == "interval":
        cp["instance"] = IntervalDataProvider(wf, cp)
    # elif cp["type"] == "ews_data":
    #     cp["instance"] = EWSDataProvider(wf,cp)
    elif cp["type"] == "swim_data":
        cp["instance"] = SWIMDataProvider(wf,cp)
    elif cp["type"] == "local_hook":
        cp["instance"] = LocalHookChangeProvider(wf, cp)
    else:
        error("Not a valid data_provider")
