import requests

from django.core.exceptions import ValidationError


def validate_breed(value):
    response = requests.get(f'https://api.thecatapi.com/v1/breeds/search?q={value}')
    if not response.json():
        raise ValidationError('Breed is not found.')
    return value
