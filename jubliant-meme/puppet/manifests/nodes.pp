node 'flask-backend-app' {
    include nginx
    include epel
    include python_dependencies
}
