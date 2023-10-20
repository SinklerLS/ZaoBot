import validators


def is_string_an_url(url_string: str) -> bool:
    return validators.url(url_string)


