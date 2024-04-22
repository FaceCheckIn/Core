from rest_framework_simplejwt.tokens import RefreshToken
import re

user_messages = {
    "password": "Your identification_code or password is incorrect.",
    "identification_code_not_exists": "This identification code is not exists.",
    "identification_code_exists": "This identification code was taken.",
    "identification_invalid": "This identification code is invalid.",
    "equal_passwords": "Your new_password and confirm password isn't equal.",
    "successful_change_password": "Your password changed.",
    "wrong_password": "Your input password is incorrect.",
}


def get_user_messages(title: str):
    return user_messages.get(title, "")


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def is_valid_iran_code(input: str) -> bool:
    if not re.search(r'^\d{10}$', input):
        return False
    check = int(input[9])
    s = sum(int(input[x]) * (10 - x) for x in range(9)) % 11
    return check == s if s < 2 else check + s == 11
