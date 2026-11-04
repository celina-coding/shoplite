import smtplib
from application.place_order import Notifier

class SmtpNotifier(Notifier):
    def __init__(self, host="localhost"):
        self.host = host

    def notify(self, to: str, msg: str) -> None:
        try:
            smtplib.SMTP(self.host).sendmail('shop@x.fr', to, msg)
        except Exception:
            pass
