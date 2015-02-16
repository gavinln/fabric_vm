# Commands to run before all others in puppet.
class init {
    $git_cmd = "git config --global"
    group { "puppet":
        ensure => "present",
    }
    case $operatingsystem {
        ubuntu: {
            exec { "apt-update":
                command => "sudo apt-get update",
            }
            Exec["apt-update"] -> Package <| |>
            $misc_packages = ['git-core']
            package { $misc_packages:
                ensure => present,
            }
            exec { 'setup-git-user':
                command => "$git_cmd user.name $::git_name",
                environment => "HOME=/home/vagrant",
                require => Package['git-core'],
            } 
            exec { 'setup-git-email':
                command => "$git_cmd user.email $::git_email",
                environment => "HOME=/home/vagrant",
                require => Package['git-core']
            } 
        }
    }
}
