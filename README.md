# Github Actions Self-Hosted Runners

[The C++ Alliance](https://cppalliance.org/) is offering a service to Boost C++ repositories, enabling Github Actions workflows to be processed on AWS hosted runners.

Often the standard Github runners are slow and unresponsive. Github throttles the number of simultaneous jobs. The monthly quota gets used up. By switching to self-hosted runners, CI can continue at a faster pace.

We have implemented a feature to globally switch the service ON or OFF. At the beginning of the month, or when Github is running smoothly, the jobs may be hosted on the normal Github runners. If things are moving slowly we will switch to the AWS machines. There is an opportunity to fine-tune the switch by adding logic that queries the Github API and makes intelligent decisions based on when the queues are busy.   

## Instructions

Modify your github actions workflow file, usually located at .github/workflows/ci.yml. A script has been provided in this repository [scripts/update_workflow.py](scripts/update_workflow.py) that will do most of the work if the ci.yml has a common format similar to boostorg/system. Otherwise, the updates can be made without using the script.  

LINUX:  

Copy the script into your $PATH. For example:  

```
cp scripts/update_workflow.py /usr/local/bin/update_workflow.py
``` 

Run the script:

```
update_workflow.py .github/workflows/ci.yml
```

WINDOWS:  

It may be necessary on Windows to execute the script with the `python` executable:

```
python update_workflow.py _target_file_
```

In either case, it should create a .orig backup file. After running the script, check the updates, and fix anything that's missing.  

```
diff .github/workflows/ci.yml.orig .github/workflows/ci.yml
```

These modifications should have been made in the workflow file:  

- In the matrix section, quote the operating system labels. That is 'ubuntu-latest' or 'ubuntu-22.04'. Don't leave them as plain text ubuntu-latest. (The need for this change may depend on whether you have sections of json in the workflow or it is completely yaml format).  

- Add a `runner-selection` job:

```
jobs:
  runner-selection:
    # runs-on: ubuntu-latest
    runs-on: ${{ github.repository_owner == 'boostorg' && fromJSON('[ "self-hosted", "linux", "x64", "ubuntu-latest-aws" ]') || 'ubuntu-latest' }}
    outputs:
      labelmatrix: ${{ steps.aws_hosted_runners.outputs.labelmatrix }}
    steps:
      - name: AWS Hosted Runners
        id: aws_hosted_runners
        uses: cppalliance/aws-hosted-runners@v1.0.0
```

The initial runner-selection job may run on either a self-hosted or GitHub host. There are pros and cons to each. Consider both options and set the one you prefer. If GitHub is being responsive and everything is pointed to using GitHub, a self-hosted runner at the first step causes a delay. If GitHub is slow and everything is pointed to AWS, then it's faster to use self-hosted.  

- Set the `runs-on` and `needs` configuration in all jobs:  

```
needs: [runner-selection]
runs-on: ${{ fromJSON(needs.runner-selection.outputs.labelmatrix)[matrix.os] }}
```

In the above example, notice where it says "matrix.os". That is whatever the runner label had been before.  

If a job specified the exact label 'ubuntu-22.04', then the section should be:  

```
needs: [runner-selection]
runs-on: ${{ fromJSON(needs.runner-selection.outputs.labelmatrix)['ubuntu-22.04'] }}
```

After `update_workflow.py` has completed you may modify ci.yml manually to adjust anything.  

If specific jobs should be excluded add '-no-aws' to the label, such as 'ubuntu-latest-no-aws'. `runner-selection` will resolve that back to 'ubuntu-latest'.  

## Supported Runners

The list of runner images and installed packages may be found at https://github.com/cppalliance/terraform-aws-github-runner/blob/cppal/images in the *-cppal files.

| AMI Images |
| ---------- |
| ubuntu-bionic-arm64-cppal |
| ubuntu-bionic-cppal |
| ubuntu-focal-arm64-cppal |
| ubuntu-focal-cppal |
| ubuntu-jammy-arm64-cppal |
| ubuntu-jammy-cppal |
| windows-2019-cppal |
| windows-2022-cppal |

Linux:

| Runner Label  |
| ------------- |
| ubuntu-20.04 |
| ubuntu-22.04, ubuntu-latest |

Windows:

| Runner Label  | Visual Studio |
| ------------- | ------------- |
| windows-2019 | msvc-14.0 |
| windows-2019 | msvc-14.1 |
| windows-2019 | msvc-14.2 |
| windows-2022, windows-latest | msvc-14.3 |

Mac:

| Runner Label  |
| ------------- |
| macos-11 |
| macos-12, macos-latest |

MacOS is not being hosted currently. Those jobs will continue to use Github runners instead of AWS.

## GitHub App

A "GitHub App" called "Terraform-AWS-Runners-Boost" should already be installed at the Organization level. However, it must also be installed to each repository that will use self-hosted runners. Contact an organization-level administrator so they can modify the install settings of the GitHub App and include the repository.  Admin instructions are covered in [docs/admin-guide.md](docs/admin-guide.md)

## Advanced Configuration  

### Temporarily disable self-hosted runners

To ensure self-hosted runners are not used, modify the runner selection:  
- `run-on` a GitHub runner 
- self_hosted_runners_override set to 'false'

```
jobs:
  runner-selection:
    runs-on: ubuntu-latest
    # runs-on: [ self-hosted, linux, x64, ubuntu-latest-aws ]
    outputs:
      labelmatrix: ${{ steps.aws_hosted_runners.outputs.labelmatrix }}
    steps:
      - name: AWS Hosted Runners
        id: aws_hosted_runners
        uses: cppalliance/aws-hosted-runners@v1.0.0
          with:
          self_hosted_runners_override: 'false'
```
