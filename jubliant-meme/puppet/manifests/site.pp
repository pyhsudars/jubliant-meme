import 'nodes.pp'
import 'firewall_config.pp'

exec { 'run-gunicorn':
    command => 'gunicorn --bind localhost:5000 wsgi:app &',
    cwd => '/webapp/',
    path    => '/usr/bin/:/bin',
    require => [File['/etc/nginx/nginx.conf'], Exec['requirements']],
}
