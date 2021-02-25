from django.http import HttpResponse
from django.template.loader import select_template

from regulations.generator import api_reader
from regulations.generator.versions import fetch_grouped_history
from regulations.views import utils


def regulation_exists(label_id):
    client = api_reader.ApiReader()
    vr = client.regversions(label_id)
    return (vr and len(vr) > 0)


def get_versions(label_id):
    """ Get the current and next version of the regulation. """
    history = fetch_grouped_history(label_id)
    if history:
        future = [h for h in history if h['timeline'].is_future()]
        if len(future) > 0:
            next_version = future[-1]
        else:
            next_version = None

        current = [h for h in history if h['timeline'].is_present()]
        current_version = current[0]
        return (current_version, next_version)
