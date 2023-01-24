import base64
# from sendgrid.helpers.mail import Mail
from django.conf import settings
# from contract_project.settings import SEND_GRID_API_key
# import sendgrid



class StringEncoder:
    "This is  encoder decoder class"

    def encode(self, value):
        byte_msg = str(value).encode('ascii')
        base64_value = base64.b64encode(byte_msg)
        idDecoded = base64_value.decode('ascii')
        idDecoded = idDecoded.strip()
        return idDecoded

    def decode(self, value):
        byte_msg = value.encode('ascii')
        base64_val = base64.b64decode(byte_msg)
        encoded_id = base64_val.decode('ascii')
        return encoded_id




# def send_email(from_email, to_email, subject, content):
#     try:
#         sg = sendgrid.SendGridAPIClient(api_key=SEND_GRID_API_key)
#         mail = Mail(from_email, to_email, subject, content)
#         mail_json = mail.get()
#         response = sg.client.mail.send.post(request_body=mail_json)
#         return True
#     except Exception as e:
#         print("here error")
#         print(e)
#         return False

