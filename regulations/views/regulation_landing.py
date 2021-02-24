from django.views.generic.base import TemplateView


class RegulationLandingView(TemplateView):
    def get_template_names(self):
        part = self.kwargs.get("part", None)
        return [
            'regulations/landing_%s.html' % part,
            'regulations/landing_base.html',
            'regulations/generic_landing.html'
        ]
