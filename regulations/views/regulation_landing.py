from django.views.generic.base import TemplateView

from regulations.generator.toc import fetch_toc
from regulations.views.reg_landing import regulation_exists, get_versions
from regulations.views import error_handling
from regulations.generator.section_url import SectionUrl


class RegulationLandingView(TemplateView):

    sectional_links = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reg_part = self.kwargs.get("part")
        current, _ = get_versions(reg_part)
        reg_version = current['version']

        toc = self.get_toc(reg_part, reg_version)
        c = {
            'TOC': toc,
            'part': reg_part,
        }
        return {**context, **c}

    def get_template_names(self):
        part = self.kwargs.get("part", None)
        return [
            'regulations/landing_%s.html' % part,
            'regulations/generic_landing.html',
        ]

    ### TODO move these to a mixin?
    def get_toc(self, reg_part, version):
        # table of contents
        toc = fetch_toc(reg_part, version)
        self.build_urls(toc, version)
        return toc

    def build_urls(self, toc, version):
        for el in toc:
            el['url'] = SectionUrl().of(
                el['index'], version, self.sectional_links)
            if 'sub_toc' in el:
                self.build_urls(el['sub_toc'], version)
