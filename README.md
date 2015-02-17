ubuntu_docker
=============

* Source code - [Github][1]
* Author - Gavin Noronha - <gavinln@hotmail.com>

[1]: https://github.com/gavinln/fabric_vm.git

About
-----

This project provides a [Ubuntu (14.04)][2] [Vagrant][3] Virtual Machine (VM)
with [Fabric][4], a ssh multiplexers.

[2]: http://releases.ubuntu.com/14.04/
[3]: http://www.vagrantup.com/
[4]: https://TODO/
[5]: http://TODO

There are [Puppet][6] scripts that automatically install the software when the VM is started.

[6]: http://puppetlabs.com/

Running
-------

1. To start the virtual machine(VM) type

    ```
    vagrant up
    ```

2. Connect to the VM

    ```
    vagrant ssh
    ```

3. Go to the Fabric directory

    ```bash
    cd /vagrant/python
    ```

4. View the available fabric commands

    ```bash
    fab -l
    ```

5. Setup zsh to improve fabric prompts

    ```bash
    /vagrant/scripts/setup_zsh.sh
    ```

6. Startup zsh

    ```
    zsh
    ```

7. To display fabric commands type: fab<tab><tab>

8. Create alias to view commands from any directory

    ```bash
    source env.sh
    ```

9. Display the list of commands

    ```bash
    si -l
    ```

10. Setup the ssh private key login

    ```bash
    si-ssh-config
    ```

11. Run fabric task to view host type

    ```bash
    si-host-type
    ```

Requirements
------------

The following software is needed to get the software from github and run
Vagrant. The Git environment also provides an [SSH client][7] for Windows.

* [Oracle VM VirtualBox][8]
* [Vagrant][9]
* [Git][10]

[7]: http://en.wikipedia.org/wiki/Secure_Shell
[8]: https://www.virtualbox.org/
[9]: http://vagrantup.com/
[10]: http://git-scm.com/

