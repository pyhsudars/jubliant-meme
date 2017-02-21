#!/bin/bash
# provision_puppet.sh (09/24/2015 smithr)

TARGET_VERSION=${1:?}

function puppet_ok () {
  VERSION=$(puppet --version 2>&1)
  if [[ $? -eq 0 ]]; then
    echo "Puppet Version = $VERSION"
    if [[ $VERSION == $TARGET_VERSION* ]]; then
      return 0
    fi
  fi
  return 1
}

echo "Running Puppet Provisioner script"

if puppet_ok; then
  echo "Provisioner script OK"
  exit
fi

LOG_DIR=$HOME/logs
mkdir -p $LOG_DIR

NOW=$(date "+%Y_%m%d_%H%M%S")
LOG=$LOG_DIR/provision.$NOW.txt
echo "Logging to: $LOG"

exec 3>&1 4>&2
exec 1>$LOG 2>&1

if [[ -x /usr/bin/dpkg ]]; then
  TARGET=puppetlabs-release-trusty.deb
  rm -f $TARGET

  wget https://apt.puppetlabs.com/$TARGET
  dpkg -i $TARGET

  apt-get update
  apt-get -y install puppet
fi

if [[ -x /usr/bin/yum ]]; then
  TARGET=puppetlabs-release-el-6.noarch.rpm

  yum -y update --exclude='kernel*'

  if [[ ! -e /etc/yum.repos.d/puppetlabs.repo ]]; then
    yum -y install https://yum.puppetlabs.com/$TARGET
  fi

  yum -y install puppet
fi

exec 1>&3 2>&4

if puppet_ok; then
  echo "Provisioner script OK"
  puppet module install puppetlabs-firewall --version 1.8.2
else
  echo "Provisioner script encountered an error"
  echo "Logs are in: $LOG"
  exit 1
fi

#
# provision_puppet.sh ends here
