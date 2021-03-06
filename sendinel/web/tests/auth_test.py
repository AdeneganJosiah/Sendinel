from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
from django.test import TestCase

from sendinel.backend.models import AuthenticationCall
from sendinel.backend import authhelper
from sendinel.notifications.models import NotificationType
from sendinel.notifications import views as notification_views
from sendinel.web import views as web_views


class AuthenticateViewTests(TestCase):
    fixtures = ['backend_test']
    urls = "urls"

    def test_authenticate_phonenumber_messages(self):
        # TODO test
        # infoservice = Infoservice(name="tesstinfoservice")
        # infoservice.save()
        # info_text = "You want to register for" + str(infoservice)
        # self.client.post(reverse('web_authenticate_phonenumber') +"?next=" + 
                                 # reverse('groups_register', \
                                          # kwargs={'id': infoservice.id}), \
                                # {'infoservice_text' : info_text})
        # self.assertContains(response, 
        # infoservice.delete()
        pass
        
    def test_authenticate_phonenumber(self):
        
        notification_type = NotificationType.objects.get(pk=1)
        self.client.get(reverse('notifications_create', \
                kwargs={"notification_type_name": notification_type.name })) 
        data = {'date': '2012-08-12',
                'phone_number': '01733685224',
                'way_of_communication': 1}
        self.client.post(reverse('notifications_create', \
                kwargs = {"notification_type_name": notification_type.name }),\
                          data)
     
        response = self.client.post(reverse("web_authenticate_phonenumber"))

        self.failUnlessEqual(response.status_code, 200)
        self.assertEquals(response.template[0].name,
                          "web/authenticate_phonenumber_call.html")
        self.assertContains(response, "auth.js")
        self.assertContains(response, "<noscript>")
        
        session_data = self.client.session['authenticate_phonenumber']
        self.assertEquals(session_data['number'], "01733685224")
        self.assertTrue(isinstance(session_data['start_time'], datetime))

        # TODO check delete_timed_out_authentication_calls gets called
        
        self.assertTemplateUsed(response,'web/authenticate_phonenumber_call.html')
    
    def test_check_call_received(self):        
        # settings up the environment
        notification_type = NotificationType.objects.get(pk=1)
        original_value = authhelper.AUTHENTICATION_ENABLED
        authhelper.AUTHENTICATION_ENABLED = True
        
        self.client.get(reverse('notifications_create', \
                kwargs={"notification_type_name": notification_type.name })) 
        data = {'date': '2012-08-12',
                'phone_number': '0123456789012',
                'way_of_communication': 1}
        self.client.post(reverse('notifications_create', \
                kwargs = {"notification_type_name": notification_type.name }), data)
                
        # make sure there are no AuthenticationCall objects in the db
        AuthenticationCall.objects.all().delete()
                
        self.client.post("/web/authenticate_phonenumber/", 
            {'number':'01234 / 56789012'})
    
        response = self.client.post("/web/check_call_received/")
    
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, "waiting")
    
        AuthenticationCall(number = "0123456789012").save()
    
        response = self.client.post("/web/check_call_received/")
        
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, "received")
    
        # make sure timeout is over
        real_timeout = web_views.AUTHENTICATION_CALL_TIMEOUT
        web_views.AUTHENTICATION_CALL_TIMEOUT = timedelta(minutes = -1)
    
        response = self.client.post("/web/check_call_received/")  
    
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, "failed")      
    
        web_views.AUTHENTICATION_CALL_TIMEOUT = real_timeout
        
        authhelper.AUTHENTICATION_ENABLED = original_value
