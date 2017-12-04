# Airlfow Dag Datadog Agent Check
The purpose of this check is to use the Airlfow CLI to check and then report on the statuses of Dag Jobs. 

## Installation
checks.d/airflow_dag.py must be copied to the agent's checks.d directory.  On a linux system that is `/etc/dd-agent/checks.d`.

## Configuration
**TODO:** Add Configuration details once it exists

## Development

### Requirements
* [Vagrant](https://www.vagrantup.com/)
* Ansible
    * See installation instructions in the Server Playbooks repo

## Testing
### Setup
1. `vagrant ssh`
2. `airflow initdb`
3. `airflow unpause tutorial`

### Create Airflow Data
The Airflow Dag has been set up to be able to run via the Scheduler. To use it, run `airflow scheduler` from within the
Vagrant environment. This script expects to be run in a daemon-like setup, so you may wish to create another SSH session
to your Vagrant environment to run it.
