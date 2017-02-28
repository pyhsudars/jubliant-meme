class cabriolet::common {
  class { "cabriolet::common::dependencies": }
}

class cabriolet::common::dependencies {
  $deb_pkg = [
              "coreutils",
              "curl",
              "git",
              "htop",
              "ntp",
              "tzdata",
              ]

  firewall { '100 Allow http and https access':
    dport   => [80, 443],
    proto  => tcp,
    action => accept,
  }

  exec { 'python-dev':
    command => 'sudo yum install -y python-devel',
    path    => '/usr/bin/',
  }

  exec { 'python-pip':
    command => 'sudo yum install -y python-pip',
    path    => '/usr/bin/',
  }

  exec { 'upgrade-python-pip':
    command => 'sudo pip install --upgrade pip',
    path    => '/usr/bin/',
    require => [Exec['python-dev'], Exec['python-pip']]
  }
  exec { 'requirements':
    command => 'sudo pip install -r requirements.txt',
    cwd => '/webapp/FlaskApp/',
    path    => '/usr/bin/',
    require => [Exec['python-dev'], Exec['upgrade-python-pip']]
  }
}
