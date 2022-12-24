from rtxlib import error

from rtxlib.changeproviders.DummyChangeProvider import DummyChangeChangeProvider
from rtxlib.changeproviders.HTTPRequestChangeProvider import HTTPRequestChangeProvider
from rtxlib.changeproviders.KafkaProducerChangeProvider import KafkaProducerChangeProvider
from rtxlib.changeproviders.MQTTPublisherChangeProvider import MQTTPublisherChangeProvider
#from rtxlib.changeproviders.EWSChangeProvider import EWSChangeProvider
from rtxlib.changeproviders.SWIMChangeProvider import SWIMChangeProvider
def init_change_provider(wf):
    """ loads the specified change provider into the workflow """
    cp = wf.change_provider
    if cp["type"] == "kafka_producer":
        cp["instance"] = KafkaProducerChangeProvider(wf, cp)
    elif cp["type"] == "mqtt_publisher":
        cp["instance"] = MQTTPublisherChangeProvider(wf, cp)
    elif cp["type"] == "http_request":
        cp["instance"] = HTTPRequestChangeProvider(wf, cp)
    elif cp["type"] == "dummy":
        cp["instance"] = DummyChangeChangeProvider(wf, cp)
    # elif cp["type"] == "ews_change":
    #     cp["instance"] = EWSChangeProvider(wf,cp)
    elif cp["type"] == "swim_change":
        cp["instance"] = SWIMChangeProvider(wf,cp)
    elif cp["type"] == "local_hook":
        cp["instance"] = LocalHookChangeProvider(wf, cp)
    else:
        error(cp["type"])
        error("Not a valid changeProvider")
        exit(1)

