
## Admin Instructions

The project is based on "Terraform module for scalable self hosted GitHub action runners" https://github.com/philips-labs/terraform-aws-github-runner . CPPAlliance is maintaining a fork of that repo with updated AMI images and runner configurations at https://github.com/cppalliance/terraform-aws-github-runner

### Create a GitHub App  

This is a one-time action. Replace "boostorg" in the following steps if another organization is being used.  

Go to the GitHub Apps setting page https://github.com/organizations/boostorg/settings/apps (This page may also be reached from Settings https://github.com/organizations/boostorg/settings and then navigate to Developer Settings -> GitHub Apps)

In the Management section, add other admin users. Most steps can be done by a delegated user, except the final installation.  

Click "New GitHub App" to create a new GitHub App.  

On the "General" page of the app:  

Name: Terraform-AWS-Runners-Boost  
Description: Self-hosted github actions runners  
Homepage URL: https://github.com/cppalliance/githubactions  
  
Webhook:  
Active: Check this box  
Webhook URL: fill in the value from Terraform  
Webhook secret: fill in the value from Terraform  

Under Private Keys click "Generate a private key". Download a private key. The key and the "App ID:" at the top of the page will be entered in Terraform.

Click "Save Changes"  

On the "Permissions and Events" page of the app, under Repository Permissions:  
Actions: Read-Only  
Administration: Read and Write  
Checks: Read-Only  
Metadata: Read-Only  

Subscribe to Events:  
choose Workflow Job  

Click "Save Changes"  

## Install the App

In the "Install App" page of the app configuration, choose the Organization and then the target repositories. This step must be done by an organization administrator.  

Only apply the app to selected repositories, not the entire organization. Whenever a repository will add self-hosted runners the organization administrator must modify the installation setting.  

