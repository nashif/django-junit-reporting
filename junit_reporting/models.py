# pylint: disable=missing-docstring,too-few-public-methods
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import permalink
from rest_framework.authtoken.models import Token


# pylint: disable=unused-argument
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class JUnitReport(models.Model):
    build_number = models.IntegerField(unique=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'JUnit Test Report'

    @permalink
    def get_absolute_url(self):
        return ('report', [self.build_number])

    def __str__(self):
        return 'Report for build #{0}'.format(self.build_number)

    @property
    def test_count(self):
        count = 0
        for suite in self.junitsuite_set.all():
            count += suite.junittest_set.count()
        return count

    @property
    def skip_count(self):
        count = 0
        for suite in self.junitsuite_set.all():
            count += suite.skipped
        return count

    @property
    def failure_count(self):
        count = 0
        for suite in self.junitsuite_set.all():
            for test in suite.junittest_set.all():
                failures = test.junitproblem_set.filter(type='F')
                count += failures.count()
        return count

    @property
    def error_count(self):
        count = 0
        for suite in self.junitsuite_set.all():
            for test in suite.junittest_set.all():
                failures = test.junitproblem_set.filter(type='E')
                count += failures.count()
        return count

    @property
    def runtime(self):
        time = 0
        for suite in self.junitsuite_set.all():
            time += suite.runtime
        return '{0} s'.format(time)

    @property
    def status(self):
        return (
            "success" if self.error_count == 0 and self.failure_count == 0
            else "problem"
        )


class JUnitSuite(models.Model):
    report = models.ForeignKey(JUnitReport, on_delete=models.CASCADE)
    name = models.CharField(max_length=512)
    runtime = models.FloatField()
    skipped = models.IntegerField()

    class Meta:
        verbose_name = 'JUnit Test Suite'

    @permalink
    def get_absolute_url(self):
        return ('suite', [self.report.build_number, self.name])

    def __str__(self):
        return '{0} - Build #{1}'.format(self.name, self.report.build_number)


class JUnitTest(models.Model):
    suite = models.ForeignKey(JUnitSuite, on_delete=models.CASCADE)
    name = models.CharField(max_length=512)
    classname = models.CharField(max_length=512)
    runtime = models.FloatField()

    class Meta:
        verbose_name = 'JUnit Test Case'

    @permalink
    def get_absolute_url(self):
        return ('test', [
            self.suite.report.build_number,
            self.suite.name,
            self.name
        ])

    def __str__(self):
        return '{0}::{1} - Suite {2} - Build #{3}'.format(
            self.classname,
            self.name,
            self.suite.name,
            self.suite.report.build_number
        )


class JUnitProblem(models.Model):
    TYPES = (
        ('E', 'Error'),
        ('F', 'Failure'),
    )

    test = models.ForeignKey(JUnitTest, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TYPES, default='F')
    message = models.TextField()

    class Meta:
        verbose_name = 'JUnit Test Case Problem'
