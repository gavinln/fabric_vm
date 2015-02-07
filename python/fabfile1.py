import os
import sys
import subprocess
import re
from collections import namedtuple

from fabric.api import run, local, sudo
from fabric.api import task, hide
from fabric.api import quiet
from fabric.api import execute
from fabric.utils import puts
from fabric.api import env, cd
from fabric.context_managers import settings
from fabric.colors import yellow, green, blue, red

#env.hosts = ['vagrant@127.0.0.1:2222']
env.user = 'vagrant'
env.password = 'vagrant'


env.roledefs = {
    'local': ['localhost:22'],
    'vm':    ['127.0.0.1:2222'],
}

# to get git working in color
# export TERM=ansi
# git config --global color.ui auto

env.repo_root = '/vagrant'
env.django_root = '/vagrant/python'
env.scripts_root = '/vagrant/vm'
env.jenkins_root = '/vagrant/jenkins'


def call_command_shell(command):
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True)
    return process.communicate()


def getVagrantSSH():
    output, err = call_command_shell(['vagrant', 'ssh-config'])
    lines = output.split(os.linesep)
    lines = [line.strip() for line in lines]
    paramNames = ['HostName ', 'Port ', 'User ', 'IdentityFile ']

    paramValues = [None] * len(paramNames)
    for line in lines:
        for index, param in enumerate(paramNames):
            if line.startswith(param):
                paramValues[index] = line[len(param):].strip()
                break
    ParamSSH = namedtuple('ParamSSH', ['host', 'port', 'username', 'keyFile'])
    # remove quotes for filename
    paramValues[3] = paramValues[3].replace('"', '')

    return ParamSSH._make(paramValues)


def setHosts():
    if sys.platform == 'win32':
        paramSSH = getVagrantSSH()
        env.roledefs['vm'] = ['{0}:{1}'.format(paramSSH.host, paramSSH.port)]
        env.key_filename = paramSSH.keyFile
        env.hosts = env.roledefs['vm']
    elif sys.platform == 'linux2':
        env.hosts = env.roledefs['local']

setHosts()

@task
def test_colors():
	puts('This word is ' + green('RUNNING', bold=True))


@task
def git_status():
    ''' status of git source code on local system '''
    local('git status')


@task
def runserver():
    ''' run Django web server '''
    with cd(env.django_root):
        # the colors generated by DJANGO webserver may not work correctly
        run('DJANGO_COLORS="nocolor" python manage.py runserver 0.0.0.0:8000')


@task
def collectstatic():
    ''' collect static Django files for web server '''
    with cd(env.django_root):
        run('python manage.py collectstatic --noinput')



@task
def nginx_start():
    ''' start nginx server for project '''
    with cd(env.repo_root):
        sudo('nginx -c django_nginx.conf -p /vagrant/')


@task
def nginx_stop():
    ''' stop default nginx server '''
    with cd(env.django_root):
        with settings(warn_only=True):
            # if nginx automatically starts the file /run/nginx.pid is created
            sudo('[ -f /run/nginx.pid ] && '
                 'kill -QUIT $( cat /run/nginx.pid )')

@task
def redis_server_start_DOES_NOT_WORK():
# does not work
    ''' start redis server for celery '''
    sudo('service redis-server start & sleep 2')

@task
def redis_server_stop_DOES_NOT_WORK():
# does not work
    ''' stop redis server for celery '''
    sudo('service redis-server stop')

def _service_started(service):
    ''' returns True if nginx is running, False otherwise '''
    with settings(hide('warnings', 'running', 'output'), warn_only=True):
        result = sudo('service {0} status'.format(service))
        if result.return_code != 0:
            return False 
    return True


def _supervisor_service_started(service):
    ''' returns True if service is running, False otherwise
        The service input is the name of a service managed by supervisor
    '''
    with settings(hide('warnings', 'running', 'output'), warn_only=True):
        cmd = 'supervisorctl -c /vagrant/vm/supervisor_mysite.conf status {0}'
        result = run(cmd.format(service))
        if 'RUNNING' not in result:
            return False 
    return True 


def _supervisor_started(service):
    ''' returns True if supervisor is running, False otherwise
    '''
    with settings(hide('warnings', 'running', 'output'), warn_only=True):
        cmd = 'supervisorctl -c /vagrant/vm/supervisor_mysite.conf pid'
        result = run(cmd)
        if re.match('\d+', str(result)):
            return True 
    return False 


def _supervisor_service_command(service, command):
    ''' runs command on supervisor managed service '''
    isRunning = _supervisor_service_started(service)
    if command == 'start' and isRunning:
        _puts_service_status(service, True)
        return
    elif command == 'stop' and not isRunning:
        _puts_service_status(service, False)
        return

    if command == 'start':
        isSupervisorRunning = _supervisor_started('supervisor')
        if not isSupervisorRunning:
            run('supervisord -c /vagrant/vm/supervisor_mysite.conf')
    cmd = 'supervisorctl -c /vagrant/vm/supervisor_mysite.conf {0} {1}' 
    run(cmd.format(command, service))



templates = {
    'nginx': {
        'status': _service_started,
    },
    'redis-server': {
        'status': _service_started,
    },
    'gunicorn': {
        'status': _supervisor_service_started,
        'start': _supervisor_service_command,
    },
    'celery': {
        'status': _supervisor_service_started,
    },
    'supervisor': {
        'status': _supervisor_started,
    }
}


def _puts_service_status(service, started):
    ''' display the status of the service '''
    if started:
        puts('{0} is '.format(service) + green('RUNNING', bold=True))
    else:
        puts('{0} is '.format(service) + red('STOPPED', bold=True))


@task
def all_status():
    ''' status of all services used in the project '''
    for service in templates:
        operation = templates[service]
        result = operation['status'](service)
        _puts_service_status(service, result)


@task
def supervisor_start():
    ''' starts supervisor and all configured programs '''
    if _supervisor_started('supervisor'):
        _puts_service_status('supervisor', True)
    else:
        run('supervisord -c /vagrant/vm/supervisor_mysite.conf')


@task
def gunicorn_start():
    ''' start gunicorn server '''
    _supervisor_service_command('gunicorn', 'start')


@task
def gunicorn_stop():
    ''' stop gunicorn processes '''
    _supervisor_service_command('gunicorn', 'stop')


@task
def celery_start():
    ''' start celery workers '''
    _supervisor_service_command('celery', 'start')


@task
def celery_stop():
    ''' stop celery workers '''
    _supervisor_service_command('celery', 'stop')


@task
def jenkins_stop():
    ' stop jenkins service '
    sudo('service jenkins stop')


@task
def jenkins_start():
    ' start jenkins service '
    sudo('service jenkins start')


@task
def ipynb_run():
    ' start ipython notebook '
    with cd(env.django_root):
        ipy_cmd = 'ipython notebook --port=8002 --ip=0.0.0.0 --no-browser ' \
            '--notebook-dir=/vagrant/notebooks'
        run('PYTHONPATH=/vagrant/python '
            'DJANGO_SETTINGS_MODULE=mysite.settings {0}'.format(
            ipy_cmd))


@task
def jenkins_job_run():
    ' runs Jenkins jobs for testing '
    run('curl http://localhost:8080/job/django_jenkins/build')


@task
def git_commit(message):
    ' commit code with a message and run jenkins test '
    with cd(env.repo_root):
        local('git commit -a -m "{}"'.format(message))


@task
def supervisor_shell():
    ''' starts supervisor shell '''
    run('supervisorctl -c /vagrant/vm/supervisor_mysite.conf')


@task
def supervisor_stop():
    ''' stops supervisor and all configured programs '''
    run('supervisorctl -c /vagrant/vm/supervisor_mysite.conf shutdown')


@task
def flower_run():
    ''' runs flower monitor for celery '''
    run(' PYTHONPATH=/vagrant/python '
        ' celery flower --broker=redis://localhost:6379/0 ')


@task
def jenkins_get_jobs():
    ''' gets the configuration of all jenkins jobs '''
    jenkins_cmd = 'java -jar jenkins-cli.jar -s http://localhost:8080 get-job'

    with cd(env.jenkins_root):
        run('{0} {1} > config/{1}.xml'.format(jenkins_cmd, 'jenkins_job'))
        run('{0} {1} > config/{1}.xml'.format(jenkins_cmd, 'django_jenkins'))
