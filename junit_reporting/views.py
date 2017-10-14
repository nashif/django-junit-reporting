# pylint: disable=missing-docstring,too-few-public-methods,too-many-ancestors
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from xml.etree.ElementTree import ParseError

from junit_reporting.models import (
    JUnitProject,
    JUnitProblem,
    JUnitReport,
    JUnitSuite,
    JUnitTest,
)

import junitparser


class IndexView(ListView):
    template_name = "junit_reporting/index.html"
    model = JUnitProject
    queryset = model.objects.exclude(name__exact='_').order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view'] = {
            'title': 'Projects',
        }
        return context


class ProjectView(DetailView):
    template_name = 'junit_reporting/project.html'
    model = JUnitProject

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reports = self.object.junitreport_set.order_by('-submitted_at')
        context['latest_report'] = reports.first()
        context['reports'] = reports[1:]
        context['view'] = {
            'title': self.object.name,
        }
        return context


class ReportView(DetailView):
    template_name = 'junit_reporting/report.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            JUnitReport,
            build_number=self.kwargs['build_number']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view'] = {
            'title': '{0} (#{1})'.format(
                self.object.project,
                self.object.build_number
            ),
        }
        return context


class SuiteView(DetailView):
    template_name = 'junit_reporting/suite.html'
    model = JUnitSuite

    def get_object(self, queryset=None):
        report = get_object_or_404(
            JUnitReport,
            build_number=self.kwargs['build_number']
        )
        return get_object_or_404(
            JUnitSuite,
            report=report,
            name=self.kwargs['suite_name']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view'] = {
            'title': '{0} ({1})'.format(
                self.object.report.project,
                self.object.name,
            )
        }
        return context


class TestView(DetailView):
    template_name = 'junit_reporting/test.html'
    model = JUnitTest

    def get_object(self, queryset=None):
        print(self.request)
        report = get_object_or_404(
            JUnitReport,
            build_number=self.kwargs['build_number']
        )
        suite = get_object_or_404(
            JUnitSuite,
            report=report,
            name=self.kwargs['suite_name']
        )
        return get_object_or_404(
            JUnitTest,
            suite=suite,
            name=self.kwargs['test_name']
        )


class ReportUploadView(APIView):
    parser_classes = (FileUploadParser,)
    permission_classes = (IsAuthenticated,)

    # pylint: disable=unused-argument,no-self-use
    def put(self, request, build_number, fmt=None, **kwargs):
        file = request.data['file']
        report, _ = JUnitReport.objects.get_or_create(
            project=JUnitProject.objects.get(slug=self.kwargs['project_slug']),
            build_number=build_number
        )

        try:
            junit = junitparser.JUnitXml().fromfile(file)
            handle_junit_report(report, junit)
        except ParseError:
            return Response(status=400)

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
