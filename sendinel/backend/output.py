from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class OutputData(object):
    """
    Define an interface for OutputData.
    """
    data = None
    def __str__(self):
        return str(self.data)

class BluetoothOutputData(OutputData):
    """
    Define necessary OutputData for sending via bluetooth.
    """
    url = None

class SMSOutputData(OutputData):
    """
    Define necessary OutputData for sending via sms.
    """
    phone_number = None

class VoiceOutputData(OutputData):
    """
    Define necessary OutputData for sending via voice.
    """
    phone_number = None
    
    
def send(data_object):
    """
    Take an OutputData and send this to the specified Output
    """
    print 'sending data: %s' % data_object