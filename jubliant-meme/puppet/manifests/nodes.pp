## Select the node - hostname ##

node 'flask-backend-app' {
    if $operatingsystem == 'CentOS' {
      include 'epel'
      include cabriolet::webapp
      include cabriolet::common
    }
}
