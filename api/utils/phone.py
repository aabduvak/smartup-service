import re


def validate_phone_number(phone_number):
    pattern = r"^\+998[1-9]\d\d{3}\d{2}\d{2}$"
    return re.match(pattern, phone_number) is not None


def format_phone_number(phone_number):
    phone_number = re.sub(r"\D", "", str(phone_number))
    if len(phone_number) not in (9, 12):
        return None

    if len(phone_number) == 9:
        phone_number = "998" + phone_number

    if len(phone_number) == 12 and not phone_number.startswith("+"):
        phone_number = "+" + phone_number

    return phone_number
