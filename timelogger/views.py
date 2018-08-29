from django.shortcuts import render, get_object_or_404, redirect

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.multipart import MIMEBase
from email.mime.text import MIMEText
#from django.conf import config
from constance import config

def call_the_cops(exception):
    msg = MIMEMultipart()
    msg['From'] = config.EMAIL_HOST_USER
    msg['To'] = config.ADMIN_CONTACT_EMAIL
    msg['Subject'] = "Time Tracker Server Problem"
    body = "Sorry to trouble you but, there is a problem on timetracker.spsradiology.com. Got this exception:\n"+str(exception)
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP(config.EMAIL_HOST, config.EMAIL_PORT)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(config.EMAIL_HOST_USER, config.EMAIL_HOST_PASSWORD)
    text = msg.as_string()
    print(text)
    server.sendmail(config.EMAIL_HOST_USER, config.ADMIN_CONTACT_EMAIL, text)
    server.quit()

def handler404(request, exception):
    #print('I am here')
    #call_the_cops('404 error')
    data = {"name": "spstimetracker.com"}
    return render(request,'errors/404.html', data)

def handler500(request, exception):
    #call_the_cops(exception)
    return render(request, 'errors/500.html', locals())

def handler403(request, exception):
    #call_the_cops(exception)
    return render(request, 'errors/403.html', locals())

def handler400(request, exception):
    #call_the_cops(exception)
    return render(request, 'errors/400.html', locals())
