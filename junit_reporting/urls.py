# pylint: disable=missing-docstring
from os.path import join
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from junit_reporting.views import IndexView, ReportUploadView

# pylint: disable=invalid-name
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^upload/(?P<build_number>[1-9][0-9]+)$', ReportUploadView.as_view()),
]
