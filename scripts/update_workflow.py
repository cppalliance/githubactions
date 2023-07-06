#!/usr/bin/python3

# 
# update_workflow.py
# 
# Modifies github actions workflows to use self-hosted runners.
#
# python3 update_workflow.py __path_to_ci_file__
#

quote_os=True

import sys
import re
import shutil

targetfile=sys.argv[1]

shutil.copyfile(targetfile, targetfile + '.orig')

with open(targetfile, 'r') as file:
    data = file.read()

# Add single quotes around operating system names if they are missing. 'ubuntu-latest'

if quote_os:
    data=re.sub(
        pattern=r'([^"\'])(\S*)-latest([^"\'])',
        repl='\\1\'\\2-latest\'\\3',
        string=data
    )

    data=re.sub(
        pattern=r'([^"\'])ubuntu-(\d\d)\.(\d\d)([^"\'])',
        repl='\\1\'ubuntu-\\2.\\3\'\\4',
        string=data
    )

    data=re.sub(
        pattern=r'([^"\'])windows-(\d{4})([^"\'])',
        repl='\\1\'windows-\\2\'\\3',
        string=data
    )

    data=re.sub(
        pattern=r'([^"\'])macos-(\d{2})([^"\'])',
        repl='\\1\'macos-\\2\'\\3',
        string=data
    )

data=re.sub(
    pattern=r'([^\S\r\n]*)runs-on: \${{\s*matrix.os\s*}}',
    repl='\\1needs: [runner-selection]\n\\1runs-on: ${{ fromJSON(needs.runner-selection.outputs.labelmatrix)[matrix.os] }}',
    string=data
)

data=re.sub(
    pattern=r"([^\S\r\n]*)runs-on:(\s*)('ubuntu.*').*",
    repl='\\1needs: [runner-selection]\n\\1runs-on: ${{ fromJSON(needs.runner-selection.outputs.labelmatrix)[\\3] }}',
    string=data
)

data=re.sub(
    pattern=r"([^\S\r\n]*)runs-on:(\s*)('windows.*').*",
    repl='\\1needs: [runner-selection]\n\\1runs-on: ${{ fromJSON(needs.runner-selection.outputs.labelmatrix)[\\3] }}',
    string=data
)

data=re.sub(
    pattern=r"([^\S\r\n]*)runs-on:(\s*)('mac.*').*",
    repl='\\1needs: [runner-selection]\n\\1runs-on: ${{ fromJSON(needs.runner-selection.outputs.labelmatrix)[\\3] }}',
    string=data
)

job_to_include="""
  runner-selection:
    # runs-on: ubuntu-latest
    runs-on: ${{ github.repository_owner == 'boostorg' && fromJSON('[ "self-hosted", "linux", "x64", "ubuntu-latest-aws" ]') || 'ubuntu-latest' }}
    outputs:
      labelmatrix: ${{ steps.aws_hosted_runners.outputs.labelmatrix }}
    steps:
      - name: AWS Hosted Runners
        id: aws_hosted_runners
        uses: cppalliance/aws-hosted-runners@v1.0.0
"""

data=re.sub(
    pattern=r'(jobs:)',
    repl='\\1' + job_to_include,
    string=data
)

f = open(targetfile, "w")
f.write(data)
f.close()
