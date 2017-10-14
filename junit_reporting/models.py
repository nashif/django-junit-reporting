# pylint: disable=missing-docstring,too-few-public-methods
from autoslug import AutoSlugField
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


class JUnitProject(models.Model):
    name = models.CharField(max_length=128)
    repo_url = models.URLField()
    ci_url_pattern = models.CharField(max_length=256)
    slug = AutoSlugField(populate_from='name')

    class Meta:
        verbose_name = 'JUnit Project'

    @permalink
    def get_absolute_url(self):
        return ('project', [self.slug])

    def __str__(self):
        return self.name

    @property
    def status(self):
        reports = self.junitreport_set.all()
        if not reports:
            return 'unknown'

        return (
            'success' if all(r.status == 'success' for r in reports)
            else 'problem'
        )


class JUnitReport(models.Model):
    build_number = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(
        JUnitProject,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'JUnit Test Report'
        unique_together = (('build_number', 'project'))

    @permalink
    def get_absolute_url(self):
        return ('report', [self.project.slug, self.build_number])

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
        return time

    @property
    def status(self):
        return (
            "success" if self.error_count == 0 and self.failure_count == 0
            else "problem"
        )

    @property
    def suites(self):
        return self.junitsuite_set.all()


class JUnitSuite(models.Model):
    report = models.ForeignKey(JUnitReport, on_delete=models.CASCADE)
    name = models.CharField(max_length=512)
    runtime = models.FloatField(default=0)
    skipped = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'JUnit Test Suite'

    @permalink
    def get_absolute_url(self):
        return ('suite', [
            self.report.project.slug,
            self.report.build_number,
            self.name
        ])

    def __str__(self):
        return '{0} - Build #{1}'.format(self.name, self.report.build_number)

    @property
    def test_count(self):
        return self.junittest_set.count()

    @property
    def skip_count(self):
        return self.skipped

    @property
    def failure_count(self):
        count = 0
        for test in self.junittest_set.all():
            failures = test.junitproblem_set.filter(type='F')
            count += failures.count()
        return count

    @property
    def error_count(self):
        count = 0
        for test in self.junittest_set.all():
            failures = test.junitproblem_set.filter(type='E')
            count += failures.count()
        return count

    @property
    def status(self):
        return (
            "success" if self.error_count == 0 and self.failure_count == 0
            else "problem"
        )

    @property
    def tests(self):
        return self.junittest_set.all()


class JUnitTest(models.Model):
    suite = models.ForeignKey(JUnitSuite, on_delete=models.CASCADE)
    name = models.CharField(max_length=512)
    classname = models.CharField(max_length=512)
    runtime = models.FloatField(default=0)

    class Meta:
        verbose_name = 'JUnit Test Case'

    @permalink
    def get_absolute_url(self):
        return ('test', [
            self.suite.report.project.slug,
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

    @property
    def status(self):
        return "success" if self.junitproblem_set.count() == 0 else "problem"


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
