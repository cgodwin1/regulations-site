from django.conf.urls import url

from regulations.url_caches import daily_cache, lt_cache
from regulations.views.about import about
from regulations.views.chrome_breakaway import ChromeSXSView
from regulations.views.chrome import (
    ChromeView, ChromeLandingView,
    ChromeSearchView,
    ChromeSubterpView)
from regulations.views.diff import ChromeSectionDiffView
from regulations.views.diff import PartialSectionDiffView
from regulations.views.partial import PartialDefinitionView
from regulations.views.partial import PartialParagraphView
from regulations.views.partial import PartialRegulationView, PartialSectionView
from regulations.views import partial_interp
from regulations.views.partial_search import PartialSearch
from regulations.views.partial_sxs import ParagraphSXSView
from regulations.views.preamble import (
    CFRChangesView, PreambleView, ChromePreambleSearchView
)
from regulations.views.redirect import (
    diff_redirect,
    redirect_by_current_date,
    redirect_by_date,
    redirect_by_date_get
)
from regulations.views.sidebar import SideBarView
from regulations.views.universal_landing import universal

urlpatterns = [
    # Index page
    # Example http://.../
    url(r'^$', universal, name='universal_landing'),

    # About page
    # Example http://.../about
    url(r'^about$', about, name='about'),

    # Redirect to version by date (by GET)
    # Example http://.../regulation_redirect/201-3-v
    url(r'^regulation_redirect/(?P<label_id>[-\w]+)$',
        redirect_by_date_get, name='redirect_by_date_get'),

    # Redirect to a diff based on GET params
    # Example http://.../diff_redirect/201-3/old_version?new_version=new
    url(r'^diff_redirect/(?P<label_id>[\d]+[-][\w]+)/(?P<version>[-\d\w_]+)$',
        diff_redirect, name='diff_redirect'),

    # A section by section paragraph with chrome
    # Example: http://.../sxs/201-2-g/2011-1738
    url(r'^sxs/(?P<label_id>[-\w]+)/(?P<notice_id>[-\d\w_]+)$',
        lt_cache(ChromeSXSView.as_view()), name='chrome_sxs_view'),

    # Search results for non-JS viewers
    # Example: http://.../search?q=term&version=2011-1738
    url(r'^search(?:/cfr)?/(?P<label_id>[\d]+)$',
        ChromeSearchView.as_view(),
        name='chrome_search',
        kwargs={'doc_type': 'cfr'}),
    url(r'^search/preamble/(?P<label_id>[\w]+)$',
        ChromePreambleSearchView.as_view(),
        name='chrome_search_preamble',
        kwargs={'doc_type': 'preamble'}),
 
    # Diff view of a section for non-JS viewers (or book markers)
    # Example: http://.../diff/201-4/2011-1738/2013-10704
    url(r'^diff/(?P<label_id>[\d]+[-][\w]+)/(?P<version>[-\d\w_]+)/(?P<newer_version>[-\d\w_]+)$',
        lt_cache(ChromeSectionDiffView.as_view()), name='chrome_section_diff_view'),
    url(r'^preamble/(?P<doc_number>[\w-]+)/cfr_changes/(?P<section>[\w-]+)$',
        daily_cache(CFRChangesView.as_view()), name='cfr_changes'),
    url(r'^preamble/(?P<paragraphs>[-\w]+(/[-\w]+)*)$',
        daily_cache(PreambleView.as_view()), name='chrome_preamble'),

    # Redirect to version by date
    # Example: http://.../201-3-v/1999/11/8
    url(r'^(?P<label_id>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})$',
        redirect_by_date, name='redirect_by_date'),
 
    # Redirect to version by current date
    # Example: http://.../201-3-v/CURRENT
    url(r'^(?P<label_id>[-\w]+)/CURRENT$',
        redirect_by_current_date, name='redirect_by_current_date'),

    # A regulation section with chrome
    # Example: http://.../201-4/2013-10704
    url(r'^(?P<label_id>[\d]+[-][\w]+)/(?P<version>[-\d\w_]+)$',
        lt_cache(ChromeView.as_view(partial_class=PartialSectionView)),
        name='chrome_section_view'),
        
    # Subterp, interpretations of a while subpart, emptypart or appendices
    # Example: http://.../201-Subpart-A-Interp/2013-10706
    #          http://.../201-Subpart-Interp/2013-10706
    #          http://.../201-Appendices-Interp/2013-10706
    url(r'^(?P<label_id>[\d]+-(Appendices|Subpart(-[A-Z]+)?)-Interp)/(?P<version>[-\d\w_]+)$',
        lt_cache(ChromeSubterpView.as_view()), name=ChromeSubterpView.version_switch_view),

    # Interpretation of a section/paragraph or appendix
    # Example: http://.../201-4-Interp/2013-10704
    url(r'^(?P<label_id>[-\w]+[-]Interp)/(?P<version>[-\d\w_]+)$',
        lt_cache(ChromeView.as_view(partial_class=partial_interp.PartialInterpView)),
        name='chrome_interp_view'),

    # The whole regulation with chrome
    # Example: http://.../201/2013-10704
    url(r'^(?P<label_id>[\d]+)/(?P<version>[-\d\w_]+)$',
        lt_cache(ChromeView.as_view(
            partial_class=PartialRegulationView,
            version_switch_view='chrome_regulation_view')),
         name='chrome_regulation_view'),

    # A regulation paragraph with chrome
    # Example: http://.../201-2-g/2013-10704
    url(r'^(?P<label_id>[-\w]+)/(?P<version>[-\d\w_]+)$',
        lt_cache(ChromeView.as_view(
            partial_class=PartialParagraphView,
            version_switch_view='chrome_paragraph_view')),
        name='chrome_paragraph_view'),

    # A regulation landing page
    # Example: http://.../201
    url(r'^(?P<label_id>[\d]+)$',
        ChromeLandingView.as_view(), name='regulation_landing_view'),

    # Load just the sidebar
    # Example: http://.../partial/sidebar/201-2/2013-10704
    url(r'^partial/sidebar/(?P<label_id>[-\w]+)/(?P<version>[-\d\w_]+)$',
        SideBarView.as_view(), name='sidebar'),

    # Load just search results
    url(r'^partial/search(?:/cfr)?/(?P<label_id>[\d]+)$',
        PartialSearch.as_view(),
        name='partial_search',
        kwargs={'doc_type': 'cfr'}),
    url(r'^partial/search/preamble/(?P<label_id>[\w]+)$',
        PartialSearch.as_view(),
        name='partial_search',
        kwargs={'doc_type': 'preamble'}),

    # A diff view of a section (without chrome)
    url(r'^partial/diff/(?P<label_id>[\d]+[-][\w]+)/(?P<version>[-\d\w_]+)/(?P<newer_version>[-\d\w_]+)$',
        lt_cache(PartialSectionDiffView.as_view()), name='partial_section_diff_view'),

    # A section by section paragraph (without chrome)
    # Example: http://.../partial/sxs/201-2-g/2011-1738
    url(r'^partial/sxs/(?P<label_id>[-\w]+)/(?P<notice_id>[-\d\w_]+)$',
        lt_cache(ParagraphSXSView.as_view()), name='paragraph_sxs_view'),

    # A definition templated to be displayed in the sidebar (without chrome)
    # Example: http://.../partial/definition/201-2-g/2011-1738
    url(r'^partial/definition/(?P<label_id>[-\w]+)/(?P<version>[-\d\w_]+)$',
        lt_cache(PartialDefinitionView.as_view()), name='partial_definition_view'),

    # A regulation section without chrome
    # Example: http://.../partial/201-4/2013-10704
    url(r'^partial/(?P<label_id>[\d]+[-][\w]+)/(?P<version>[-\d\w_]+)$',
        lt_cache(PartialSectionView.as_view()), name='partial_section_view'),

    # Subterp, interpretations of a whole subpart, emptypart or appendices
    # Example: http://.../partial/201-Subpart-A-Interp/2013-10706
    #          http://.../partial/201-Subpart-Interp/2013-10706
    #          http://.../partial/201-Appendices-Interp/2013-10706
    url(r'^partial/(?P<label_id>[\d]+-(Appendices|Subpart(-[A-Z]+)?)-Interp)/(?P<version>[-\d\w_]+)$',
        lt_cache(partial_interp.PartialSubterpView.as_view()), name='partial_subterp_view'),

    # An interpretation of a section/paragraph or appendix without chrome.
    # Example: http://.../partial/201-2-Interp/2013-10704
    url(r'^partial/(?P<label_id>[-\w]+[-]Interp)/(?P<version>[-\d\w_]+)$',
        lt_cache(partial_interp.PartialInterpView.as_view()), name='partial_interp_view'),

    # The whole regulation without chrome; not too useful; added for symmetry
    # Example: http://.../partial/201/2013-10704
    url(r'^partial/(?P<label_id>[\d]+)/(?P<version>[-\d\w_]+)$',
        lt_cache(PartialRegulationView.as_view()), name='partial_regulation_view'),

    # A regulation paragraph without chrome.
    # Example: http://.../partial/201-2-g/2013-10704
    url(r'^partial/(?P<label_id>[-\w]+)/(?P<version>[-\d\w_]+)$',
        lt_cache(PartialParagraphView.as_view()), name='partial_paragraph_view'),
]
