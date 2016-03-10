'''
This tests using Win32 open ssh on Windows.
https://github.com/PowerShell/Win32-OpenSSH
'''
from fabric.api import run, local, sudo
from fabric.api import env, cd
from fabric.api import task, hide


env.hosts = ['beth-pc2']
env.user = 'beth'

# fab -f fabfile5.py --port 443 dir
# env.hosts = ['192.168.0.100']
# env.user = 'gavin'

# working commands
# ssh beth@beth-pc2 "cmd /c dir"
# ssh beth@beth-pc2 "c:\windows\system32\tree.com /A"


@task
def dir():
    run('cmd /c dir', shell=False)


@task
def info():
    run('cmd /c systeminfo', shell=False)
