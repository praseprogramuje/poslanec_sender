import smtplib
import ssl
from time import sleep
import logging


class Sender:
    SSL_PORT = 465
    SUBJECT = 'Subject: '

    def __init__(self):
        self.file_with_pms = ''
        self.login = ''
        self.password = ''
        self.file_with_text_name = ''
        self.message = ''
        self.pms_list = []
        self.log = logging.getLogger(__name__)

    def create_recipients_list(self):
        try:
            with open(self.file_with_pms, 'r', encoding='utf-8') as reader:
                for line in reader:
                    if line[0] != '#':
                        words = line.split(";")
                        self.pms_list.append(words)
        except Exception as exception:
            self.log.error('Chyba pri cteni souboru s emailem ' + repr(exception))
            quit()

    def compose_email_message_from_file(self):
        text = ''.encode('utf-8')
        try:
            with open(self.file_with_text_name, 'r', encoding='utf-8') as reader:
                for line in reader:
                    text += line.encode('utf-8')
        except Exception as exception:
            self.log.error('Chyba pri cteni souboru kde je obsah emailu ' + repr(exception))
            quit()

        self.message = text.decode('utf-8')

    def gather_input(self):
        self.login = input("Zadejte prosim svoji emailovou adresu a stisknete enter: ")
        if not self.login:
            self.log.error('Bez emailu to nepujde, zkuste prosim znova')
            quit()

        self.password = input("Zadejte heslo k svoji emailové adrese a stisknete enter: ")
        if not self.password:
            self.log.error('Bez hesla k emailu to nepujde, zkuste prosim znova')
            quit()

        self.file_with_text_name = input(
            "Zadejte jméno souboru kde je text ktery chcete zaslat a stiskněte enter: ")
        if not self.file_with_text_name:
            self.log.error('Bez textu k zaslani to nepujde, zkuste prosim znova')
            quit()

        self.file_with_pms = input(
            "Zadejte jmeno souboru kde je seznam osob kterym chcete zaslat email a stisknete enter: ")
        if not self.file_with_pms:
            self.log.error('Seznam osob nenalezen')
            quit()

    def send_email(self, pm, ssl_context):
        complete_text = (self.SUBJECT + ' ' + pm[0] + '\n' + pm[1] + '\n' + self.message).encode('utf-8')
        receiver_email = pm[2].strip()
        sleep(5)  # do not overwhelm ssl connection :-D
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", self.SSL_PORT, context=ssl_context) as server:
                server.login(self.login, self.password)
                server.sendmail(self.login, receiver_email, complete_text)
                self.log.info("Poslano na " + receiver_email)
        except Exception as exception:
            self.log.error('Chyba pri odesilani emailu ' + repr(exception))
            quit()

    def send_emails(self):
        ssl_context = ssl.create_default_context()
        for pm in self.pms_list:
            self.send_email(pm, ssl_context)

    def send(self):
        self.gather_input()
        self.create_recipients_list()
        self.compose_email_message_from_file()
        self.send_emails()


if __name__ == '__main__':
    logging.basicConfig(filename='chyby.log', filemode='w', level=logging.INFO)
    sender = Sender()
    sender.send()
