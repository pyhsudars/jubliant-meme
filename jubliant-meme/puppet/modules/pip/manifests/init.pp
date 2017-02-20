class pip {
    package { 'python-pip':
        ensure => latest,
        require => Package['epel-release'],
    }
    exec { 'Install-pip-requirements':
        command => 'pip install -r requirements.txt',
        cwd => '/webapp/FlaskApp/',
        path    => '/usr/bin/',
        require => Package['python-pip']
    }
}
