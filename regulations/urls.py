from django.urls import path, register_converter
from django.conf.urls import url

from regulations.url_caches import daily_cache, lt_cache
from regulations.views.partial import PartialDefinitionView
from regulations.views.partial import PartialRegulationView
from regulations.views.reader import SubpartReaderView, SectionReaderView, PartReaderView
from regulations.views import partial_interp
from regulations.views.partial_sxs import ParagraphSXSView
from regulations.views.goto import GoToRedirectView
from regulations.views.regulation_landing import RegulationLandingView
from regulations.views.homepage import HomepageView
from regulations.views import converters

# Reusable pattern matching constants to improve readability
match_version = match_notice = r'[-\d\w_]+'
match_section = r'[\d]+[-][\w]+'
match_paragraph = r'[-\w]+'
match_reg = r'[\d]+'
match_preamble = r'[\w]+'
match_paragraphs = r'[-\w]+(/[-\w]+)*'
match_year = r'\d{4}'
match_day = match_month = r'\d{2}'
match_interp = r'[-\w]+[-]Interp'
match_sub_interp = r'[\d]+-(Appendices|Subpart(-[A-Z]+)?)-Interp'

register_converter(converters.NumericConverter, 'numeric')
register_converter(converters.SubpartConverter, 'subpart')
register_converter(converters.VersionConverter, 'version')

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('<numeric:part>/<version:version>/', PartReaderView.as_view(), name='part_reader_view'),
    path('<numeric:part>/<numeric:section>/<version:version>/', SectionReaderView.as_view(), name='section_reader_view'),
    path('<numeric:part>/<subpart:subpart>/<version:version>/', SubpartReaderView.as_view(), name="subpart_reader_view"),
    path('goto/', GoToRedirectView.as_view(), name='goto'),
    path('<part>/', RegulationLandingView.as_view(), name="regulation_landing_view"),

    # A section by section paragraph (without chrome)
    # Example: http://.../partial/sxs/201-2-g/2011-1738
    url(rf'^partial/sxs/(?P<label_id>{match_paragraph})/(?P<notice_id>{match_notice})$',
        lt_cache(ParagraphSXSView.as_view()), name='paragraph_sxs_view'),

    # A definition templated to be displayed in the sidebar (without chrome)
    # Example: http://.../partial/definition/201-2-g/2011-1738
    url(rf'^partial/definition/(?P<label_id>{match_paragraph})/(?P<version>{match_version})$',
        lt_cache(PartialDefinitionView.as_view()), name='partial_definition_view'),

    # An interpretation of a section/paragraph or appendix without chrome.
    # Example: http://.../partial/201-2-Interp/2013-10704
    url(rf'^partial/(?P<label_id>{match_interp})/(?P<version>{match_version})$',
        lt_cache(partial_interp.PartialInterpView.as_view()), name='partial_interp_view'),

    # The whole regulation without chrome; not too useful; added for symmetry
    # Example: http://.../partial/201/2013-10704
    url(rf'^partial/(?P<label_id>{match_reg})/(?P<version>{match_version})$',
        lt_cache(PartialRegulationView.as_view()), name='partial_regulation_view'),
]
