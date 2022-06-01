from requests import post
from getpass import getpass

headers = {
    'content-type': 'application/json'
}

email = input('Email > ')
password = getpass('Password > ')

def invalid_password_email():
    print('Invalid password/email.')
    input()
    exit()

def captcha_required():
    print('Captcha required.')
    input()
    exit()


def mfa(ticket):

    code = input('Code > ')
    
    payload = {
        'code': code,
        'gift_code_sku_id': None,
        'login_source': None,
        'ticket': ticket
    }

    url = 'https://discord.com/api/v9/auth/mfa/totp'

    resp = post(url, json=payload, headers=headers)

    try: json = resp.json()
    except: invalid_password_email()

    if not json['token']: invalid_password_email()

    return json['token']



payload = {
    'captcha_key': None,
    'gift_code_sku_id': None,
    'login': email,
    'login_source': None,
    'password': password,
    'undelete': False
}

url = 'https://discord.com/api/auth/login'

resp = post(url, json=payload, headers=headers)

try: json = resp.json()
except: invalid_password_email()

if resp.status_code != 200:
    if json["captcha_key"]:
        captcha_required()
    else:
        invalid_password_email()

if not json['token']:
    if json['mfa']:
        mfa(json['ticket'])
    else:
        invalid_password_email()
