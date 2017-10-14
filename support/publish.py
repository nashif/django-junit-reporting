#!/usr/bin/env python3
"""
Publish test results to a 'JUnit Reporting' host
"""

from argparse import ArgumentParser
import os
import sys
import requests


ARGPARSE = ArgumentParser(
    description='Publish test results to a JUnit Reporting host'
)
ARGPARSE.add_argument('host', type=str,
                      help='The target host')
ARGPARSE.add_argument('project', type=str,
                      help='The target project')
ARGPARSE.add_argument('report', type=str,
                      help='The report to publish')
ARGPARSE.add_argument('buildid', type=int,
                      help='The build id of this report')
ARGPARSE.add_argument('token', type=str, nargs='?',
                      help='The authorization token')


ARGS = ARGPARSE.parse_args()


# pylint: disable=missing-docstring
def publish():
    token = (
        ARGS.token if 'token' in ARGS
        else os.environ['JUNIT_REPORTING_TOKEN']
    )
    if not token:
        sys.exit('Missing authorization token!')

    upload_url = ARGS.host + '/p/{0}/upload/{1}'.format(
        ARGS.project,
        ARGS.buildid
    )

    print(upload_url)

    headers = {
        'Authorization': 'Token {0}'.format(token),
        'Content-Disposition': 'attachement; filename=report.xml'
    }

    with open(ARGS.report, 'rb') as report:
        data = report.read()
        response = requests.put(upload_url,
                                data=data,
                                headers=headers)
        if not response.ok:
            print(response.text)
            sys.exit('Error during upload: {0}'.format(response.reason))


if __name__ == '__main__':
    publish()
