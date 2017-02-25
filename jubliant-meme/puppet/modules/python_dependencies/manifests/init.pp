class python_dependencies {
  exec { 'python-dev':
    command => 'yum install -y python-devel',
    path    => '/usr/bin/',
  }

  exec { 'python-pip':
    command => 'yum install -y python-pip',
    path    => '/usr/bin/',
  }

  exec { 'upgrade-python-pip':
    command => 'pip install --upgrade pip',
    path    => '/usr/bin/',
    require => [Exec['python-dev'], Exec['python-pip']]
  }

  exec { 'requirements':
    command => 'sudo pip install -r requirements.txt',
    cwd => '/webapp/FlaskApp/',
    path    => '/usr/bin/',
    require => Exec['upgrade-python-pip'],
  }
}
