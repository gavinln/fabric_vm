from __future__ import print_function
from fabric.api import run, env, task, roles, local, hosts
from fabric.colors import red

import os
import shutil
import yaml

from textwrap import dedent

# need to make Virtualbox Host-Only Network adapter private
# See: http://sharepoint.smayes.com/2012/02/virtualbox-unidentified-network/
# also need to run: winrm quickconfig
powershell_cmd = """powershell -NoProfile -NonInteractive
        \"$secure_password = ConvertTo-SecureString '{1}' -asPlainText -Force;
        $credentials = New-Object Management.Automation.PSCredential('{0}', $secure_password);
        $remote_session = New-PSSession -ComputerName {2} -Credential $credentials;
        Invoke-Command -Session $remote_session -ScriptBlock {{ {3} }};
        $remote_last_exit_code = Invoke-Command -Session $remote_session -ScriptBlock {{ $LastExitCode }};
        Remove-PSSession -Session $remote_session;
        exit $remote_last_exit_code\" """


def remote_sh(target_host, command_text, ignore_error=False):
    print('run PowerShell script block at {0}: {1}'.format(
        target_host, command_text))

    command_text = command_text.replace('"', '\'')

    # -NoProfile -NonInteractive PowerShell parameters decrease execution time
    power_shell_text = """powershell -NoProfile -NonInteractive
        $remote_session = New-PSSession -ComputerName {0};
        Invoke-Command -Session $remote_session -ScriptBlock {{ {1} }};
        $remote_last_exit_code = Invoke-Command -Session $remote_session -ScriptBlock {{ $LastExitCode }};
        Remove-PSSession -Session $remote_session;
        exit $remote_last_exit_code\" """.format(
            target_host,
            command_text)

    power_shell_text = dedent(power_shell_text).replace('\n', ' ')

    # This print call could be uncommented for debugging purposes
    # print('run shell command: {0}'.format(power_shell_text))

    error_code = os.system(power_shell_text)

    if error_code and not ignore_error:
        errMsg = 'Failed to execute PowerShell script block on host {0}.' + \
            ' Actual return code was {1} ' + \
            'but only zero value is expected. ' + \
            'Script block is "{2}".'
        raise Exception(err.format(target_host, error_code, command_text))

    return error_code


script_dir = os.path.dirname(__file__)
with open(os.path.join(script_dir, "config.yaml"), "r") as f:
    config = yaml.load(f)


env.roledefs['master'] = config['master']
env.roledefs['workers'] = config['workers']


@task
def ps():
    print('Executing on %s' % env.host)
    if env.host:
        remote_sh(env.host, "Get-Process", ignore_error=False)
    else:
        print(red('Host not specified\nUsage: psh -H nearretiree-980 ps'))
