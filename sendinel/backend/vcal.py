﻿from datetime import datetime

import settings

def create_vcal_string(start_date, end_date, location, content, uid):
    """
        @param  start_date:  Start Date of the appointment
        @type   start_date:  Datetime
        
        @param  end_date:    End Date of the appointment
        @type   end_date:    Datetime
        
        @param  location:   Location for the appointment
        @type   location:   String
        
        @param  content:    Subject of the appointment
        @type   content:    String
        
        @param  uid:        UID for the vcal entry
        @type   uid:        String
        
        @return:    Plain text version of the vcal entry
    """
    time_delta = settings.REMINDER_TIME_BEFORE_APPOINTMENT
    #need time difference in minutes for alarm
    alarm_time = (time_delta.days * 1440) + (time_delta.seconds/60)
    
    vcal_data = \
"""BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
UID:%(uid)d
SUMMARY:%(content)s
DTSTAMP:%(stamp)s
DTSTART:%(start)s
DTEND:%(end)s
LOCATION:%(location)s
BEGIN:VALARM
TRIGGER:-PT%(alarm)dM
ACTION:DISPLAY
DESCRIPTION:%(content)s
END:VALARM
END:VEVENT
END:VCALENDAR""" % {\
    'uid': uid,
    'content': content,
    'location': location,
    'start': start_date.strftime("%Y%m%dT%H%M%SZ"),
    'end': end_date.strftime("%Y%m%dT%H%M%SZ"),
    'stamp': datetime.now().strftime("%Y%m%dT%H%M%SZ"),    
    'alarm': alarm_time}
    
    return vcal_data
    