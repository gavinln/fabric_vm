from __future__ import print_function
from fabric.api import run, env, task, roles, local
from gitric.api import git_seed, git_reset


import os
import shutil
import yaml


script_dir = os.path.dirname(__file__)
with open(os.path.join(script_dir, "config.yaml"), "r") as f:
    config = yaml.load(f)


env.roledefs['master'] = config['master']
env.roledefs['workers'] = config['workers']
env.use_ssh_config = True


@task(name='host-type')
@roles('master')
def host_type():
    ''' display os name for master hosts '''
    run('uname -a')


@task(name='ssh-config')
def ssh_config():
    ''' set up ssh config file '''
    user_root = os.path.expanduser('~')
    ssh_root = os.path.join(user_root, '.ssh')
    ssh_config = os.path.join(ssh_root, 'config')
    if not os.path.exists(ssh_root):
        os.makedirs(ssh_root)
    if not os.path.exists(ssh_config):
        shutil.copy(os.path.join(script_dir, 'config'), ssh_root)
        local('chmod 600 {0}'.format(os.path.join(ssh_root, 'config')))
    key_file = '~/.ssh/insecure_private_key'
    key_url = 'https://raw.githubusercontent.com/mitchellh/vagrant/master/keys/vagrant'
    local('wget -O {0} {1} && chmod 600 {0}'.format(
        key_file, key_url))


@task
@roles('master')
def deploy(commit=None):
    ''' Deployment using git '''
    repo_path = '/home/vagrant/test_deploy'
    git_seed(repo_path, commit)
    # stop your service here
    git_reset(repo_path, commit)
    # restart your service herec
