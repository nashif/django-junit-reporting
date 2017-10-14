# pylint: disable=missing-docstring
from django.conf.urls import url

from junit_reporting.views import (
    IndexView,
    ProjectView,
    ReportView,
    ReportUploadView,
    SuiteView,
    TestView,
)

PROJECT_URL = (
    r'^p/(?P<slug>[-0-9a-z_]+)/?$'
)

UPLOAD_URL = (
    r'^p/(?P<project_slug>[-0-9a-z_]+)/'
    r'upload/(?P<build_number>[1-9][0-9]*)$'
)


REPORT_URL = (
    r'^p/(?P<project_slug>[-0-9a-z_]+)/'
    r'report/(?P<build_number>[1-9][0-9]*)/?$'
)

SUITE_URL = (
    r'^p/(?P<project_slug>[-0-9a-z_]+)/'
    r'report/(?P<build_number>[1-9][0-9]*)/'
    r'(?P<suite_name>[.a-zA-Z]+)/?$'
)

TEST_URL = (
    r'^p/(?P<project_slug>[-0-9a-z_]+)/'
    r'report/(?P<build_number>[1-9][0-9]*)/'
    r'(?P<suite_name>[.a-zA-Z]+)/'
    r'(?P<test_name>[.a-zA-Z]+)/?$'
)

# pylint: disable=invalid-name
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(UPLOAD_URL, ReportUploadView.as_view(), name='upload'),
    url(PROJECT_URL, ProjectView.as_view(), name='project'),
    url(REPORT_URL, ReportView.as_view(), name='report'),
    url(SUITE_URL, SuiteView.as_view(), name='suite'),
    url(TEST_URL, TestView.as_view(), name='test'),
]
