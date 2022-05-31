
import re
#regex to check if email is valid
email_match= re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
password_match = re.compile(r"""
    (?=^[a-zA-Z0-9]{6,}$)
    (?=\w*[a-z])
    (?=\w*[A-Z])
    (?=\w*\d)
""", re.X)


def validateEmail(email):
    if re.fullmatch(email_match,email):
        return True
    else:
        return False

def validatePassword(password):
    if re.fullmatch(password_match, password):
        return True
    else:
        return False
