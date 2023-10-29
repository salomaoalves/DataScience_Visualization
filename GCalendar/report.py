from datetime import timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl

import constants as cts
from Analytics import agg_colors, agg_report


DATA = cts.DATA

def send_mail(body_text, subject, receiver_email):
    '''Function to send a email for someone
        @body_text: string in html format
        @subject: email title - str
        @receiver_email: list of email to send the text - list of str'''

    with open('GetData/Database/email_credentials.txt', 'r') as f:
        credentials = f.read().split('\n')
    sender_email, password = credentials[0], credentials[1]

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message['To'] = ", ".join(receiver_email)

    part1 = MIMEText(body_text, "html")
    message.attach(part1)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


def get_report():
    '''Generate a txt or email report - use DISPLAY l01 or l02'''

    # Header info
    first_day = min(DATA["StartTimeStamp"]).date()
    last_day = max(DATA["StartTimeStamp"]).date()
    duration = (max(DATA["StartTimeStamp"]) + timedelta(days=1)).date() - first_day

    # Report header
    report = f'Report from {first_day} to {last_day} - with duration of {duration}.'
    if cts.DISPLAY=='l01':
        report += '\n\n'
    elif cts.DISPLAY=='l02':
        report = '<h1>'+report+'</h1>'

    # Free time - Sleep - Workout - Daily related
    nrm_evnts = 'DAY TO DAY' + cts.EVENTS_SEP
    if cts.DISPLAY=='l01':
        report += nrm_evnts
    elif cts.DISPLAY=='l02':
        report += '<h2><strong>'+nrm_evnts+'</strong></h2>'
    report += f'{agg_report.get_free(DATA)}\n{agg_report.get_sleep(DATA)}\n{agg_colors.get_blueberry(DATA)}\n{agg_colors.get_tangerine(DATA)}\n\n'

    # Main info - Earn $$ - Usefull stuffs
    res_evnts = 'RESUME' + cts.EVENTS_SEP
    if cts.DISPLAY=='l01':
        report += res_evnts
    elif cts.DISPLAY=='l02':
        report += '<h2><strong>'+res_evnts+'</strong></h2>'
    report += f'{agg_report.get_main(DATA)}\n{agg_colors.get_tomato(DATA)}\n\n'
    
    # Yellow stuffs
    impt_evnts = 'IMPORTANT' + cts.EVENTS_SEP
    if cts.DISPLAY=='l01':
        report += impt_evnts
    elif cts.DISPLAY=='l02':
        report += '<h2><strong>'+impt_evnts+'</strong></h2>'
    report += f'{agg_colors.get_banana(DATA)}\n\n'

    # Social events - Streaming time - All day events
    scial_evnts = 'Others' + cts.EVENTS_SEP
    if cts.DISPLAY=='l01':
        report += scial_evnts
    elif cts.DISPLAY=='l02':
        report += '<h2><strong>'+scial_evnts+'</strong></h2>'
    report += f'{agg_report.get_social(DATA)}\n{agg_colors.get_lavender(DATA)}\n{agg_report.get_all_day(DATA)}\n\n'

    # Transport/Travel time
    mov_evnts = 'MOVIMENT' + cts.EVENTS_SEP
    if cts.DISPLAY=='l01':
        report += mov_evnts
    elif cts.DISPLAY=='l02':
        report += '<h2><strong>'+mov_evnts+'</strong></h2>'
    report += f'{agg_colors.get_flamingo(DATA)}\n\n'

    return report


#output in terminal using layout 01
#print(get_report())

#output in txt file using layout 01
with open(cts.TXT_PATH, 'w') as f:
    f.write(get_report())

#output in email using layout 02
#send_mail(get_report(), 'GCalender Report 3', ['salomao.alves222@gmail.com'])
