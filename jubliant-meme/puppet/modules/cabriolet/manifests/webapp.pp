class cabriolet::webapp {
  class { "cabriolet::webapp::nginxSetup": } ->
  class { "cabriolet::webapp::nginxConfigure": } ->
  class { "cabriolet::webapp::nginxSitesEnabled": }
}

#
# Declare contained classes
#

class cabriolet::webapp::nginxSetup {
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

class cabriolet::webapp::nginxConfigure {
  if $operatingsystem == 'CentOS'{
    file { "nginx.conf":
      path   => "/etc/nginx/nginx.conf",
      ensure => file,
      mode   => 0644,
      owner  => root,
      group  => root,
      source => "puppet:///modules/cabriolet/nginx/cabriolet-nginx-CentOS.conf",
      }
    } else {
      file { "nginx.conf":
        path   => "/etc/nginx/nginx.conf",
        ensure => file,
        mode   => 0644,
        owner  => root,
        group  => root,
        source => "puppet:///modules/cabriolet/nginx/cabriolet-nginx-debian.conf",
      }
    }
}

class cabriolet::webapp::nginxSitesEnabled {
  file {'create-sites-available-directory':
    ensure => directory,
    path => "/etc/nginx/sites-available",
  }

  file { "sites-available.conf":
    path   => "/etc/nginx/sites-available/sites-available.conf",
    ensure => file,
    mode   => 0644,
    owner  => root,
    group  => root,
    source => "puppet:///modules/cabriolet/nginx/nginx-sites-available.conf",
    require => File['create-sites-available-directory'],
  }

  file {'create-sites-enabled-directory':
    ensure => directory,
    path => "/etc/nginx/sites-enabled",
  }

  file { "sites-enabled.conf":
    path   => "/etc/nginx/sites-enabled/sites-enabled.conf",
    ensure => link,
    mode   => 0644,
    owner  => root,
    group  => root,
    target => "/etc/nginx/sites-available/sites-available.conf",
    require => File['sites-available.conf'],
  }
}
