from django import http
from django.template import loader

from regulations.generator import api_reader


class MissingContentException(Exception):
    """ This is essentially a generic 404. """
    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "MissingContentException"
