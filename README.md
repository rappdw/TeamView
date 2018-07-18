# Team Viewer - *"Analytic Insights into your Software Development Team"*
Team Viewer is an application that provides insight into your software development team. It extracts data from
git (today) and other repositories (future) and makes that information available through Jupyter notebooks.

## Pre-requisites
1. You must provide an ssh key that has access to read from the git repos that comprise the work product of your team

    Run: `bin/create-repo-access-secret.py <path_to_private_key>`
    
    This is a one time only operation
2. Start the application

    Run: `bin/run.sh`
    
    This will stop any existing deployment and create a new deployment, opening a browser to
    the analytics notebook provided by the application
    
    **NOTE**: This is currently configured to run against a local kubernetes cluster