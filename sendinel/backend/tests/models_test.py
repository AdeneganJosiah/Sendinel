from datetime import datetime

from django.test import TestCase

from sendinel import settings
from sendinel.backend.models import *
from sendinel.backend.output import *
import sendinel.backend.tests.contenttype_helper


class ScheduledEventTest(TestCase):

    fixtures = ['backend']

    def setUp(self):
        self.event = ScheduledEvent.objects.get(pk=1)
    
    def test_sendable_polymorphic(self):
        appointment = self.event.sendable
        self.assertEquals(type(appointment),
                            HospitalAppointment,
                            'Sendable polymorphic type is wrong')

    def test_sendable_get_data_for_sending(self):
        appointment = self.event.sendable
        appointment.way_of_communication="sms"
        data = OutputData()
        appointment.get_data_for_sms = lambda: data
        self.assertEquals(appointment.get_data_for_sending(), data)
        

class HospitalAppointmentTest(TestCase):
    fixtures = ['backend']
    
    def setUp(self):
      self.appointment = HospitalAppointment.objects.get(pk=2)

    def test_create_scheduled_event(self):
        number_of_events = ScheduledEvent.objects.count()
        appointment_date = datetime(2010, 02, 24, 13, 43, 59)
        self.appointment.date = appointment_date
        self.appointment.create_scheduled_event()

        self.assertEquals(ScheduledEvent.objects.count(),
                            number_of_events + 1)

        scheduled_event = ScheduledEvent.objects \
                            .order_by('pk').reverse()[:1][0]
        send_time_should = appointment_date - \
                            settings.REMINDER_TIME_BEFORE_APPOINTMENT
        self.assertEquals(scheduled_event.send_time,
                            send_time_should)

class ModelsSMSTest(TestCase):
    
    fixtures = ['backend']
    
    def test_hospital_appointment_get_data_for_sms(self):
        data = HospitalAppointment.objects.get( pk = 2).get_data_for_sms()
        self.assertions_for_sms_output_object(data)
        
    def test_text_message_get_data_for_sms(self):
        data = TextMessage.objects.get(pk = 1).get_data_for_sms()
        self.assertions_for_sms_output_object(data)
        
    def assertions_for_sms_output_object(self, data):
        self.assertEquals(type(data), SMSOutputData)
        self.assertEquals(data.phone_number, "12345")
        self.assertEquals(type(data.data), unicode)

