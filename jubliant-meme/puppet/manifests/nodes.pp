node 'flask-backend-app' {
    include nginx
    include epel
    include python_dependencies

    Exec { environment => [ "sigPassPhrase=development-signature-passphrase", "encryptionPassPhrase=development-encryption-passphrase" ] }
}
