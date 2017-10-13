# pylint: disable=missing-docstring,too-few-public-methods
from rest_framework import serializers
from junit_reporting.models import JUnitReport


class JUnitReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = JUnitReport
        fields = ('id', 'build_number')
