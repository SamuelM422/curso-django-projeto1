import re
from django.core.exceptions import ValidationError

def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(
            'Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number and one special character.',
            code='invalid'
        )