from django import http
from django.template import loader

from regulations.generator import api_reader
from regulations.generator.layers.utils import convert_to_python


class MissingContentException(Exception):
    """ This is essentially a generic 404. """
    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "MissingContentException"


class MissingSectionException(Exception):
    """" This is for when we suspect that we have the version requested, but
    maybe just not the label_id. """

    def __init__(self, label_id, version, context):
        self.label_id = label_id
        self.version = version
        self.context = context

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "MissingSectionException(%s, %s)" % (
            self.label_id, self.version)


def handle_generic_404(request):
    template = loader.get_template('regulations/generic_404.html')
    context = {'request_path': request.path}
    body = template.render(context, request)
    return http.HttpResponseNotFound(body, content_type='text/html')


def check_regulation(reg_part):
    """ If versions of the reg_part given don't exist, raise
    a MissingContentException(). """

    client = api_reader.ApiReader()
    vr = client.regversions(reg_part)

    if not vr:
        raise MissingContentException()


def check_version(label_id, version):
    """ We check if the version of this regulation exists, and the user is only
    referencing a section that does not exist. """

    reg_part = label_id.split('-')[0]
    client = api_reader.ApiReader()
    vr = client.regversions(reg_part)

    requested_version = [v for v in vr['versions'] if v['version'] == version]

    if len(requested_version) > 0:
        requested_version = convert_to_python(requested_version)
        return requested_version[0]


def handle_missing_section_404(
        request, label_id, version, extra_context=None):

    req_version = check_version(label_id, version)
    if not req_version:
        return handle_generic_404(request)

    reg_section = label_id.split('-')[1]

    context = {
        'request_path': request.path,
        'reg_section': reg_section,
        'effective_date': req_version['by_date']
    }
    context.update(extra_context)

    template = loader.get_template('regulations/missing_section_404.html')
    body = template.render(context, request)

    return add_to_chrome(body, context, request)
