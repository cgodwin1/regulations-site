from unittest import TestCase
from mock import patch

from django.test import RequestFactory

from regulations.views import errors


class ErrorHandlingTest(TestCase):

    @patch('regulations.views.errors.api_reader')
    def test_check_regulation_none(self, api_reader):
        api_reader.ApiReader.return_value.regversions.return_value = None

        self.assertRaises(
            errors.MissingContentException,
            errors.check_regulation, '204')

    @patch('regulations.views.errors.api_reader')
    def test_check_regulation_exists(self, api_reader):
        api_reader.ApiReader.return_value.regversions.return_value = [1]

        result = errors.check_regulation('204')
        self.assertEqual(result, None)

    @patch('regulations.views.errors.api_reader')
    def test_check_version(self, api_reader):
        api_reader.ApiReader.return_value.regversions.return_value =\
            {'versions': [{'version': '2'}]}
        result = errors.check_version('204', '2')
        self.assertTrue(result)

    @patch('regulations.views.errors.api_reader')
    def test_check_no_version(self, api_reader):
        api_reader.ApiReader.return_value.regversions.return_value =\
            {'versions': [{'version': '3'}]}
        result = errors.check_version('204', '2')
        self.assertFalse(result)

    def test_handle_generic_404(self):
        request = RequestFactory().get('/fake-path')
        result = errors.handle_generic_404(request)
        self.assertEqual(result.status_code, 404)
        self.assertTrue(b'Regulation content not found' in result.content)

    @patch('regulations.views.errors.add_to_chrome')
    @patch('regulations.views.errors.api_reader')
    def test_handle_missing_section_404(self, api_reader, add_to_chrome):
        api_reader.ApiReader.return_value.regversions.return_value =\
            {'versions': [{'version': '2', 'by_date': '2013-03-26'}]}
        add_to_chrome.return_value = None

        request = RequestFactory().get('/fake-path')

        extra_content = {'passed': 1, 'env': 'source'}
        response = errors.handle_missing_section_404(
            request, '204-1', '2', extra_content)
        self.assertEqual(response, None)
        self.assertTrue(add_to_chrome.called)
