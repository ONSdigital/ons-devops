if [ -f /etc/yum.repos.d/epel.repo ]
  then
    echo "epel repo already installed - skipping"
  else
    yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
fi
