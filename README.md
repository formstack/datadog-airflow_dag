# Airlfow Dag Datadog Agent Check
The purpose of this check is to use the Airlfow CLI to check and then report on the statuses of Dag Jobs. 

## Installation
checks.d/airflow_dag.py must be copied to the agent's checks.d directory.  On a linux system that is `/etc/dd-agent/checks.d`.

## Configuration
### All Environments
* A config file needs to be defined for the Agent
    * An example config file for the Agent can be found in conf.d/airflow_dag.yaml.example
### Development Envrionment Only
* The Datadog API key needs to be defined in playbooks/roles/datadog/vars/main.yml
    * An example of the variable file can be found in playbooks/roles/datadog/vars/main.yml.example

## Development
### Requirements
* [Vagrant](https://www.vagrantup.com/)
* Ansible
    * This was built and tested using Ansible 2.2.0.0.
* A Datadog account and API Key
    * To keep namespaces for the checks as clean as possible, setting up a free trial is advised

## Testing
### Generating Airflow Data to be Detected
The Airflow Dag has been set up to be able to run via the Scheduler. To use it, run `airflow scheduler` from within the
Vagrant environment. This script expects to be run in a daemon-like setup, so you may wish to create another SSH session
to your Vagrantenvironment to run it.
