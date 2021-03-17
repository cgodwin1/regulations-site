# -*- coding: utf-8 -*-
from collections import namedtuple

import six
from django.urls import reverse

from regulations.generator import generator
from regulations.generator.html_builder import CFRHTMLBuilder
from regulations.generator.layers.toc_applier import TableOfContentsLayer
from regulations.generator.node_types import EMPTYPART, REGTEXT
from regulations.generator.section_url import SectionUrl
from regulations.generator.sidebar.diff_help import DiffHelp
from regulations.generator.toc import fetch_toc
from regulations.views import error_handling, utils
from regulations.views.partial import PartialView


class Versions(namedtuple('Versions', ['older', 'newer', 'return_to'])):
    def __new__(cls, older, newer, return_to=None):
        if return_to is None:
            return_to = older
        return super(Versions, cls).__new__(cls, older, newer, return_to)


def reverse_chrome_diff_view(sect_id, left_ver, right_ver, from_version):
    """ Reverse the URL for a chromed diff view. """

    diff_url = reverse(
        'chrome_section_diff_view',
        args=(sect_id, left_ver, right_ver))
    diff_url += '?from_version=%s' % from_version
    return diff_url


def extract_sections(toc):
    compiled_toc = []
    for i in toc:
        if 'Subpart' in i['index'] or 'Subjgrp' in i['index']:
            compiled_toc.extend(i['sub_toc'])
        else:
            compiled_toc.append(i)
    return compiled_toc


def diff_toc(versions, old_toc, diff):
    # We work around Subparts in the TOC for now.
    compiled_toc = extract_sections(old_toc)

    for node in (v['node'] for v in diff.values() if v['op'] == 'added'):
        if len(node['label']) == 2 and node['title']:
            element = {
                'label': node['title'],
                'index': node['label'],
                'section_id': '-'.join(node['label']),
                'op': 'added'
            }
            data = {'index': node['label'], 'title': node['title']}
            TableOfContentsLayer.section(element, data)
            TableOfContentsLayer.appendix_supplement(element, data)
            compiled_toc.append(element)

    modified, deleted = modified_deleted_sections(diff)
    for el in compiled_toc:
        if 'Subpart' not in el['index'] and 'Subjgrp' not in el['index']:
            el['url'] = reverse_chrome_diff_view(el['section_id'], *versions)
        # Deleted first, lest deletions in paragraphs affect the section
        if tuple(el['index']) in deleted and 'op' not in el:
            el['op'] = 'deleted'
        if tuple(el['index']) in modified and 'op' not in el:
            el['op'] = 'modified'

    return sorted(compiled_toc, key=normalize_toc)


def normalize_toc(toc_element):
    """Return a sorting order for a TOC element, primarily based on the
    index, and the type of content. General order is regulation text,
    appendices, then interpretations."""

    sortable_index = tuple(utils.make_sortable(l)
                           for l in toc_element['index'])
    if toc_element.get('is_section'):
        return (0,) + sortable_index
    elif toc_element.get('is_appendix'):
        return (1,) + sortable_index
    elif toc_element.get('is_supplement'):
        return (2,) + sortable_index
    else:
        return (3,) + sortable_index


def modified_deleted_sections(diff):
    modified, deleted = set(), set()
    for label, diff_value in six.iteritems(diff):
        label = tuple(label.split('-'))
        if 'Interp' in label:
            section_label = (label[0], 'Interp')
        else:
            section_label = tuple(label[:2])

        # Whole section was deleted
        if diff_value['op'] == 'deleted' and label == section_label:
            deleted.add(section_label)
        # Whole section added/modified or paragraph added/deleted/modified
        else:
            modified.add(section_label)
    return modified, deleted
