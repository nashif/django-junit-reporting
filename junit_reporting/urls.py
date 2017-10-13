# pylint: disable=missing-docstring
from django.conf.urls import url

from junit_reporting.views import (
    IndexView,
    ReportView,
    ReportUploadView,
    SuiteView,
    TestView,
)


REPORT_URL = (
    r'^report/(?P<build_number>[1-9][0-9]+)/?$'
)
SUITE_URL = (
    r'^report/(?P<build_number>[1-9][0-9]+)/'
    r'(?P<suite_name>[.a-zA-Z]+)/?$'
)
TEST_URL = (
    r'^report/(?P<build_number>[1-9][0-9]+)/'
    r'(?P<suite_name>[.a-zA-Z]+)/'
    r'(?P<test_name>[.a-zA-Z]+)/?$'
)

# pylint: disable=invalid-name
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^upload/(?P<build_number>[1-9][0-9]+)$', ReportUploadView.as_view()),
    url(REPORT_URL, ReportView.as_view(), name='report'),
    url(SUITE_URL, SuiteView.as_view(), name='suite'),
    url(TEST_URL, TestView.as_view(), name='test'),
]
