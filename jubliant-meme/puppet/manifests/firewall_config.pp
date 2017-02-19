firewall { '100 Allow http and https access':
  dport   => [80, 443],
  proto  => tcp,
  action => accept,
}
