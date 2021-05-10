from datetime import date
from requests import HTTPError
from django.views.generic.base import TemplateView
from django.http import Http404
from django.urls import reverse

from regulations.views.mixins import TableOfContentsMixin
from regulations.generator import api_reader

client = api_reader.ApiReader()


class RegulationLandingView(TableOfContentsMixin, TemplateView):

    template_name = "regulations/regulation_landing.html"

    sectional_links = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reg_part = self.kwargs.get("part")

        try:
            current = client.v2_structure(date.today(), 42, reg_part)
        except HTTPError:
            raise Http404

        reg_version = current['date']
        structure = current['structure']

        c = {
            'structure': structure,
            'version': reg_version,
            'part': reg_part,
            'content': [
                'regulations/partials/landing_%s.html' % reg_part,
                'regulations/partials/landing_default.html',
            ],
        }

        self.build_toc_urls(c, structure)

        return {**context, **c}

    def build_toc_url(self, context, node):
        url_kwargs = {
            'part': context['part'],
            'version': context['version'],
        }

        if node['type'] == 'subpart':
            url_kwargs['subpart'] = 'Subpart-{}'.format(node['identifier'][0])
        elif node['parent_subpart'] is not "":
            url_kwargs['subpart'] = 'Subpart-{}'.format(node['parent_subpart'])

        return reverse('reader_view', kwargs=url_kwargs)
