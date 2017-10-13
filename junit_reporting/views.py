# pylint: disable=missing-docstring,too-few-public-methods
from django.views.generic import DetailView, ListView
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from junit_reporting.models import JUnitReport, JUnitSuite, JUnitTest


class IndexView(ListView):
    template_name = "junit_reporting/index.html"
    model = JUnitReport


class ReportView(DetailView):
    template_name = 'junit_reporting/report.html'
    model = JUnitReport


class SuiteView(DetailView):
    template_name = 'junit_reporting/suite.html'
    model = JUnitSuite


class TestView(DetailView):
    template_name = 'junit_reporting/test.html'
    model = JUnitTest


class ReportUploadView(APIView):
    parser_classes = (FileUploadParser,)
    permission_classes = (IsAuthenticated,)

    def put(self, request, build_number, format=None):
        file_object = request.data['file']
        with open('reports/report_{0}.html'.format(build_number), 'wb') as file:
            for chunk in file_object.chunks():
                file.write(chunk)

        JUnitReport.objects.create(build_number=build_number)
        return Response(status=204)
