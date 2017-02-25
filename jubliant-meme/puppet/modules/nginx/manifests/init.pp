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
    service {'nginx_stopped':
        ensure => stopped,
        require => [Package['nginx'], Service['nginx']],
    }
    file {'/etc/nginx/sites-available':
        ensure => directory,
        require => Package['nginx'],
    }
    file {'/etc/nginx/sites-enabled':
        ensure => directory,
        require => File['/etc/nginx/sites-available'],
    }
    file {'/etc/nginx/sites-available/flaskapp.conf':
        ensure => present,
        source => "puppet:///modules/nginx/flaskapp.conf",
        notify => Service['nginx'],
        require => File['/etc/nginx/sites-enabled'],
    }
    file { '/etc/nginx/sites-enabled/flaskapp.conf':
        ensure => 'link',
        target => '/etc/nginx/sites-available/flaskapp.conf',
        require => File['/etc/nginx/sites-available/flaskapp.conf'],
    }
    file {'/etc/nginx/nginx.conf':
        ensure => present,
        source => "puppet:///modules/nginx/nginx.conf",
        require => File['/etc/nginx/sites-available/flaskapp.conf'],
        notify => Service['nginx'],
    }
    exec { 'run-gunicorn':
        command => 'gunicorn --bind localhost:5000 wsgi:app &',
        cwd => '/webapp/',
        path    => '/usr/bin/',
        require => [File['/etc/nginx/nginx.conf'], Exec['requirements']],
    }
}
