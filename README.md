# Team Viewer - *"Analytic Insights into your Software Development Team"*
Team Viewer is an application that provides insight into your software development team. It extracts data from
git (today) and other repositories (future) and makes that information available through Jupyter notebooks.

## Pre-requisites
You have to define secrets and configuration to the kubernetes cluster

Run: `bin/create-config.py -k <private_key_file> -c <config_file>`

This is a one time only operation

## Starting the Application
Run: `bin/run.sh`

This will stop any existing kubernetes deployment and create a new deployment, opening a browser to
the analytics notebook provided by the application

**NOTE**: This is currently configured to run against a local kubernetes cluster
    
## Configuration
A configuration file must be provided that describes the projects for which Team View will etract data for analysis.
Each project defines the repositories, the date span for the project, and, optionally, any adjustments that should be
made to the extract to correct any biases present in the data, e.g. copying significant code blocks from another project,
etc.

A sample configuration file is:

```json
{
  "extracts": [
    {
      "name": "TeamView",
      "repos": [
        {
          "name": "TeamView",
          "remote": "git@github.com:rappdw/TeamView.git"
        },
        {
          "name": "team-view-extract",
          "remote": "git@github.com:rappdw/team-view-extract.git"
        },
        {
          "name": "team-view-notebook",
          "remote": "git@github.com:rappdw/team-view-notebook.git"
        },
        {
          "name": "tv-extract",
          "remote": "git@github.com:rappdw/tv-extract.git"
        }
      ],
      "start_date": "2018-07-18",
      "end_date": "2018-08-31"
    }
  ],
  "output_path": "/root/.local/share/cache/TeamView",
  "mailmap_file": "/root/extract/.mailmap",
  "logging": 20
}
```

This configuration file and .mailmap file (if specified) are added to a Kubenetes configmap which is mounted into
containers at the mountpoint `/root/extract`. Because of this, if you use a mailmap file, it should be specified as 
`/root/extract/.mailmap` in your configuration file. Also, because of volume definitions in `team-view.yaml`, the output
path in your configuration should be `/root/.local/share/cache/TeamView`.
