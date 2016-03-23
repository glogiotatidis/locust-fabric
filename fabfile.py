import os
from fabric.api import cd, env, run, sudo
from fabric.contrib.files import append, exists
from fabric.operations import put

env.user = 'ubuntu'

PACKAGES = [
    'vim',
    'python-pip',
    'python-virtualenv',
    'python-dev',
    'build-essential',
    'git',
    'python-zmq',
    'iftop',
]


def install_packages():
    packages = ' '.join(PACKAGES)
    sudo('apt-get update')
    sudo('apt-get install -y {}'.format(packages))


def install_locust():
    sudo('pip install locustio')

    with cd('~'):
        if not exists('load_test'):
            run('git clone {} load_test'.format(env.load_test_repo))


def master():
    MASTER_CMD = 'locust -f locust_file.py --master --host={host} DesktopLocust MobileLocust'.format(host=env.target)
    with cd('~/load_test'):
        run(MASTER_CMD)


def slave():
    ssh_cmd = ("ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no "
                   "-o 'ExitOnForwardFailure yes' -fNL {port}:localhost:{port} {host} || true")
    run(ssh_cmd.format(port=5557, host=env.master_host))
    run(ssh_cmd.format(port=5558, host=env.master_host))

    SLAVE_CMD = 'locust -f locust_file.py --slave --master-host={master} DesktopLocust MobileLocust'.format(master='localhost')
    with cd('~/load_test'):
        run(SLAVE_CMD)
