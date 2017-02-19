class nginx {
    package {'apache':
        ensure => absent,
    }
    package { 'epel-release':
        ensure => installed,
    }
    package {'nginx':
        ensure => installed,
        require => [Package['apache'], Package['epel-release']],
    }
    service {'nginx':
        ensure => running,
        enable => true,
        require => Package['nginx'],
    }
}
