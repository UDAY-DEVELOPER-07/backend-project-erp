import re
from django.http import JsonResponse

def check_regex(regex, value):
    x = re.fullmatch(regex, value)
    return x

