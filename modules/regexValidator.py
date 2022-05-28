
import re
#regex to check if email is valid
email_match= re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

def validateEmail(input):
    if re.fullmatch(email_match,input):
        return('Valid Email')
    else:
        return('Invalid Email')