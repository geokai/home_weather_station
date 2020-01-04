"""helper script that takes a str or bytes and always returns a bytes"""


def to_bytes(str_or_bytes):
    if isinstance(str_or_bytes, str):
        value = str_or_bytes.encode('utf-8')
    else:
        value = str_or_bytes
    return value    # instance of bytes
