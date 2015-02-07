# install python
class python_setup {
    case $operatingsystem {
        ubuntu: {
            package { "python-pip":
                ensure => installed
            }
            package { 'fabric':
                ensure => installed,
                provider => pip,
                require => Package['python-pip']
            }
            package { 'ipython':
                ensure => installed,
                provider => pip,
                require => Package['python-pip']
            }
        }
    }
}
