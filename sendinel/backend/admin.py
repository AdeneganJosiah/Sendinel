from django.contrib import admin

from sendinel.backend.models import *

admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Hospital)
admin.site.register(Sendable)
admin.site.register(HospitalAppointment)
admin.site.register(TextMessage)
admin.site.register(ScheduledEvent)
