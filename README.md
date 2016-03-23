# locust swarm

[Fabric](http://docs.fabfile.org/) script to deploy and run a [locust](http://locust.io/) swarm

## Setup

`fab -H [IP][,IP][,IP] install_packages install_locust`

## Master

`fab -H [IP] --set target=[TARGET],load_test_repo=[LOCUSTFILE GIT REPO] run_master`

## Slaves

`fab -P -A -H [IP][,IP][,IP] --set target=[TARGET] run_slave`


Note that the master process only schedules jobs and it does not
execute them. You probably want to include master node IP address in
the slave list as well.
