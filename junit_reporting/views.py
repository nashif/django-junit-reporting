# pylint: disable=missing-docstring,too-few-public-methods,too-many-ancestors
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from junit_reporting.models import (
    JUnitProblem,
    JUnitReport,
    JUnitSuite,
    JUnitTest,
)

import junitparser


class IndexView(ListView):
    template_name = "junit_reporting/index.html"
    model = JUnitReport


class ReportView(DetailView):
    template_name = 'junit_reporting/report.html'

    def get_object(self):
        print(self.request)


class SuiteView(DetailView):
    template_name = 'junit_reporting/suite.html'
    model = JUnitSuite

    def get_object(self):
        print(self.request)
        report = get_object_or_404(
            JUnitReport,
            build_number=self.kwargs['build_number']
        )
        return get_object_or_404(
            JUnitSuite,
            report=report,
            name=self.kwargs['suite_name']
        )


class TestView(DetailView):
    template_name = 'junit_reporting/test.html'
    model = JUnitTest


class ReportUploadView(APIView):
    parser_classes = (FileUploadParser,)
    permission_classes = (IsAuthenticated,)

    # pylint: disable=unused-argument
    def put(self, request, build_number, fmt=None):
        file = request.data['file']
        report, _ = JUnitReport.objects.get_or_create(
            build_number=build_number
        )

        junit = junitparser.JUnitXml().fromfile(file)
        self._handle_junit_report(report, junit)

        return Response(status=204)


def handle_junit_report(report, junit):
    if isinstance(junit, junitparser.TestSuite):
        handle_junit_suite(report, junit)


def handle_junit_suite(report, junit):
    suite, _ = JUnitSuite.objects.get_or_create(
        report=report,
        name=junit.name,
        runtime=junit.time,
        skipped=junit.skipped
    )

    for test in junit:
        handle_junit_test(suite, test)


def handle_junit_test(suite, junit):
    test, _ = JUnitTest.objects.get_or_create(
        suite=suite,
        name=junit.name,
        classname=junit.classname,
        runtime=junit.time
    )
    result = junit.result
    if isinstance(result, junitparser.Error):
        JUnitProblem.objects.get_or_create(
            test=test,
            type='E',
            message=junit.message
        )
    elif isinstance(result, junitparser.Failure):
        JUnitProblem.objects.get_or_create(
            test=test,
            type='F',
            message=junit.message
        )
