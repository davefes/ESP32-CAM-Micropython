#  Image should be base64 encoded.
#  Thanks to pm4r at https://github.com/shawwwn/uMail/issues/2


import my_umail as umail
import utime
import machine
import config
import uos
import gc
import ubinascii
import urandom as random


smtp_config = {'host' : 'smtp.gmail.com',
                'port' : 587,
                'username' : 'your_email@gmail.com',
                'password' : '2 factor password'}


def boundary():
    return ''.join(random.choice('0123456789ABCDEFGHIJKLMNOUPQRSTUWVXYZ') for i in range(15))


def send_mail(email, attachment = None):
    smtp = umail.SMTP(**smtp_config)
    smtp.to(email['to'])
    smtp.write("From: {0} <{0}>\n".format(email.get('from', smtp_config['username'])))
    smtp.write("To: {0} <{0}>\n".format(email['to']))
    smtp.write("Subject: {0}\n".format(email['subject']))
    if attachment:
        text_id = boundary()
        attachment_id = boundary()
        smtp.write("MIME-Version: 1.0\n")
        smtp.write('Content-Type: multipart/mixed;\n boundary="------------{0}"\n'.format(attachment_id))
        smtp.write('--------------{0}\nContent-Type: multipart/alternative;\n boundary="------------{1}"\n\n'.format(attachment_id, text_id))
        smtp.write('--------------{0}\nContent-Type: text/plain; charset=utf-8; format=flowed\nContent-Transfer-Encoding: 7bit\n\n{1}\n\n--------------{0}--\n\n'.format(text_id, email['text']))
        smtp.write('--------------{0}\nContent-Type: image/jpeg;\n name="{1}"\nContent-Transfer-Encoding: base64\nContent-Disposition: attachment;\n  filename="{1}"\n\n'.format(attachment_id, attachment['name']))
        b64 = ubinascii.b2a_base64(attachment['bytes'])
        smtp.write(b64)
        smtp.write('--------------{0}--'.format(attachment_id))
    else:
        smtp.send(email['text'])
    smtp.send()
    smtp.quit()


