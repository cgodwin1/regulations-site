from importlib import import_module

import six
from django.conf import settings
from django.urls import reverse, NoReverseMatch

from regulations.generator import api_reader
from regulations.generator.toc import fetch_toc
from regulations.generator.section_url import SectionUrl
import logging
logger = logging.getLogger(__name__)


def build_citation(context):
        citation = []
        if 'part' in context:
            citation.append(context["part"])
        if 'section' in context:
            citation.append(context["section"])
        if 'subpart' in context:
            citation.append(context["subpart"])
        return "-".join(citation)


class CitationContextMixin:
    def get_context_data(self, **kwargs):
        context = super(CitationContextMixin, self).get_context_data(**kwargs)
        context['citation'] = build_citation(context)
        return context


class SidebarContextMixin():
    # contains either class paths or class objects (not instances)
    sidebar_classes = settings.SIDEBARS
    client = api_reader.ApiReader()

    def get_context_data(self, **kwargs):
        context = super(SidebarContextMixin, self).get_context_data(**kwargs)

        sidebars = []
        for class_or_class_path in self.sidebar_classes:
            sidebars.append(
                self.build_sidebar_context(
                    class_or_class_path,
                    build_citation(context),
                    context['version']))

        context['sidebars'] = sidebars

        return context

    def build_sidebar_context(self, sidebar_class, label_id, version):
        if isinstance(sidebar_class, six.string_types):
            module_name, class_name = sidebar_class.rsplit('.', 1)
            sidebar_class = getattr(import_module(module_name), class_name)
        sidebar = sidebar_class(label_id, version)
        return sidebar.full_context(self.client, self.request)


class TableOfContentsMixin:
    default_view = 'section_reader_view'

    def get_toc(self, reg_part, version):
        # table of contents
        toc = fetch_toc(reg_part, version)
        self.build_urls(toc, version)
        return toc

    def build_urls(self, toc, version, subpart=None):
        for el in toc:
            el['url'] = self.get_url(el['index'], version, subpart)
            if 'sub_toc' in el:
                if 'Subpart' in el['index']:
                    self.build_urls(el['sub_toc'], version, '-'.join(el['index'][1:]))
                else:
                    self.build_urls(el['sub_toc'], version)

    def get_url(self, citation, version, subpart):
        view_name = self.request.resolver_match.url_name
        part = citation[0]
        section = citation[1]

        if view_name == "subpart_reader_view" and subpart is not None:
            view = view_name
            args = (part, subpart, version)
        elif view_name == "part_reader_view":
            view = view_name
            args = (part, version)
        else:
            view = self.default_view
            args = (part, section, version)

        try:
            return reverse(view, args=args)
        except NoReverseMatch:
            return ''
