# -*- coding: utf-8 -*-
from six import text_type
from six.moves import urllib
from zerver.lib.test_helpers import WebhookTestCase

class TravisHookTests(WebhookTestCase):
    STREAM_NAME = 'travis'
    URL_TEMPLATE = u"/api/v1/external/travis?stream={stream}&api_key={api_key}&topic=builds"
    FIXTURE_DIR_NAME = 'travis'

    def test_travis_message(self):
        # type: () -> None
        """
        Build notifications are generated by Travis after build completes.

        The subject describes the repo and Stash "project". The
        content describes the commits pushed.
        """
        expected_message = (u"Author: josh_mandel\nBuild status: Passed :thumbsup:\n"
                            u"Details: [changes](https://github.com/hl7-fhir/fhir-sv"
                            u"n/compare/6dccb98bcfd9...6c457d366a31), [build log](ht"
                            u"tps://travis-ci.org/hl7-fhir/fhir-svn/builds/92495257)")

        self.send_and_test_stream_message(
            'build',
            'builds',
            expected_message,
            content_type="application/x-www-form-urlencoded"
        )

    def get_body(self, fixture_name):
        # type: (text_type) -> text_type
        return urllib.parse.urlencode({'payload': self.fixture_data("travis", fixture_name, file_type="json")})
