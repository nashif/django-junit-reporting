# pylint: disable=missing-docstring
from django.contrib import admin

from junit_reporting.models import (
    JUnitProject,
    JUnitProblem,
    JUnitReport,
    JUnitSuite,
    JUnitTest,
)

MODELS = [
    JUnitProject,
    JUnitProblem,
    JUnitReport,
    JUnitSuite,
    JUnitTest,
]

admin.site.register(MODELS)
