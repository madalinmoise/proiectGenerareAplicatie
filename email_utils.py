# email_utils.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import logging
from config import config

logger = logging.getLogger('HRAudit')

def send_email_with_attachments(config, attachment_paths, log_queue=None, context=None):
    # Validare config
    required_fields = ['smtp_server', 'smtp_port', 'username', 'password', 'from', 'to', 'subject', 'body']
    for field in required_fields:
        if field not in config:
            err = f"Lipsește câmpul '{field}' din configurația email."
            if log_queue:
                log_queue.put(f"❌ {err}")
            return False
        if not config[field]:
            err = f"Câmpul '{field}' este gol în configurația email."
            if log_queue:
                log_queue.put(f"❌ {err}")
            return False
    """
    Trimite un email cu mai multe atașamente.
    config: dicționar cu cheile:
        - smtp_server: str
        - smtp_port: int
        - username: str
        - password: str
        - from: str
        - to: str (sau va fi înlocuit din context dacă există email)
        - subject: str
        - body: str
    attachment_paths: listă de căi către fișierele de atașat
    context: dicționar pentru înlocuirea placeholder-ilor în subiect și corp
    log_queue: coadă pentru mesaje de log (opțional)
    """
    # Validare adresă destinatar
    recipient = config.get('to', '')
    if not recipient or not isinstance(recipient, str) or '@' not in recipient:
        err = f"Adresă email invalidă: '{recipient}'"
        if log_queue:
            log_queue.put(f"❌ {err}")
        return False
    def log(msg):
        if log_queue:
            log_queue.put(msg)
        logger.info(msg)

    try:
        # Construim mesajul
        msg = MIMEMultipart()
        msg['From'] = config['from']

        # Determinăm destinatarul
        if context and 'email' in context:
            recipient = context['email']
        else:
            recipient = config['to']
        msg['To'] = recipient

        # Subiect personalizat
        subject = config['subject']
        if context:
            for key, val in context.items():
                subject = subject.replace('{' + key + '}', str(val))
        msg['Subject'] = subject
        log(f"Pregătire email către {recipient} cu subiectul: {subject}")

        # Corp personalizat
        body = config['body']
        if context:
            for key, val in context.items():
                body = body.replace('{' + key + '}', str(val))
        msg.attach(MIMEText(body, 'plain'))
        log("Corp mesaj construit.")

        # Atașamente
        for att_path in attachment_paths:
            if isinstance(att_path, (str, Path)):
                with open(att_path, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename="{Path(att_path).name}"')
                    msg.attach(part)
                    log(f"Atașament adăugat: {Path(att_path).name}")

        log(f"Conectare la serverul SMTP {config['smtp_server']}:{config['smtp_port']}...")

        # Alegem metoda de conectare în funcție de port
        if config['smtp_port'] == 465:
            # SSL
            server = smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port'])
            log("Conexiune SSL stabilită.")
        else:
            # TLS (port 587 de obicei)
            server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
            if not config.get('no_auth', False):
                server.starttls()
            log("Conexiune stabilită.")

        if not config.get('no_auth', False):
            server.login(config['username'], config['password'])
            log("Autentificare reușită.")
        else:
            log("Modul 'fără autentificare' activat (Relay local).")

        server.send_message(msg)
        server.quit()
        log(f"Email trimis cu succes către {recipient}.")
        return True

    except Exception as e:
        err_msg = f"Eroare la trimiterea emailului: {str(e)}"
        logger.error(err_msg, exc_info=True)
        if log_queue:
            log_queue.put(err_msg)
        return False