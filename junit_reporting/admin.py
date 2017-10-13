# pylint: disable=missing-docstring
from django.contrib import admin

from junit_reporting.models import (
    JUnitProblem,
    JUnitReport,
    JUnitSuite,
    JUnitTest,
)

MODELS = [
    JUnitProblem,
    JUnitReport,
    JUnitSuite,
    JUnitTest,
]

admin.site.register(MODELS)
