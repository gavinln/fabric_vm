'''
This tests using Win32 open ssh on Windows.
https://github.com/PowerShell/Win32-OpenSSH
'''
from fabric.api import run, local, sudo
from fabric.api import env, cd
from fabric.api import task, hide


# env.hosts = ['beth-pc2']
env.hosts = ['192.168.0.137']
env.user = 'beth'

# fab -f fabfile5.py --port 443 dir
# env.hosts = ['192.168.0.100']
# env.user = 'gavin'

# working commands
# ssh beth@beth-pc2 "cmd /c dir"
# ssh beth@beth-pc2 "c:\windows\system32\tree.com /A"

# powershell jobs
# powershell -Command "& { Start-Job -ScriptBlock { gci -Recurse c:\sw }; Receive-Job -Id 1 }"
# powershell -Command "& { Start-Job -ScriptBlock { gci -Recurse c:\ }; Receive-Job -Id 1 -Keep }"
# powershell -Command "& {  Get-Job }"
# Start-Job -ScriptBlock { gci -Recurse c:\ }; Receive-Job -Id 1 -Keep


@task
def dir():
    ' dir using cmd '
    run('cmd /c "dir c:\sw"', shell=False)


@task
def dir2():
    ' dir using powershell '
    run('powershell -Command "& {gci c:\sw }"', shell=False)


@task
def info():
    run('cmd /c systeminfo', shell=False)
