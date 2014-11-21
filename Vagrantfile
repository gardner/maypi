# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # From https://gist.github.com/millisami/3798773
  def local_cache(box_name)
    cache_dir = File.join(File.expand_path('~/.vagrant.d'), 'cache', 'apt', box_name)
    partial_dir = File.join(cache_dir, 'partial')
    FileUtils.mkdir_p(partial_dir) unless File.exists? partial_dir
    cache_dir
  end


  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "trusty32"
  
  # custom baked ubuntu vm that hass updates applied and packages applied
  config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-i386-vagrant-disk1.box"

  cache_dir = local_cache(config.vm.box)
  
  config.vm.synced_folder cache_dir, "/var/cache/apt/archives/"

  # accessing "localhost:31337" will access port 3133 on the guest machine.
  config.vm.network :forwarded_port, guest: 3133, host: 3133

  # If true, then any SSH connections made will enable agent forwarding.
  # Default value: false
  config.ssh.forward_agent = true
  
$rootScript = <<SCRIPT
  set -x
  apt-get update -y 
  # apt-get upgrade -y 
  apt-get install python-software-properties libxml2-dev libxslt1-dev mercurial -y
  apt-get install git vim python-dev curl vim screen gunicorn nginx -y

  apt-get purge python-pip -y

  cd /tmp
  curl -LO https://raw.github.com/pypa/pip/master/contrib/get-pip.py
  python get-pip.py
  pip --version
  pip install virtualenv
  pip install virtualenvwrapper  
SCRIPT

$userScript = <<SCRIPT

  git config --global url."https://".insteadOf git://
  
  echo export WORKON_HOME="/home/vagrant/envs" >> /home/vagrant/.bashrc
  export WORKON_HOME="/home/vagrant/envs"
  echo source /usr/local/bin/virtualenvwrapper.sh >> /home/vagrant/.bashrc
  source /usr/local/bin/virtualenvwrapper.sh
  cd /vagrant

  mkvirtualenv maypi
  yes | pip install -r requirements.txt
  yes | pip install --index-url https://code.stripe.com --upgrade stripe

  if [ ! -f modernomad/local_settings.py ]; then
  	SECURE_RANDOM=$(dd if=/dev/urandom count=1 bs=28 2>/dev/null | od -t x1 -A n)
  	SECRET_KEY="${SECURE_RANDOM//[[:space:]]/}"
  	sed "s/^SECRET_KEY.*$/SECRET_KEY = '$SECRET_KEY'/" maypi/local_settings.example.py > maypi/local_settings.py
  fi
  
  echo workon maypi >> /home/vagrant/.bashrc
  workon maypi
  ./manage.py syncdb --noinput
  ./manage.py migrate
SCRIPT


  config.vm.provision "shell",
    privileged: true,
    inline: $rootScript

  config.vm.provision "shell",
    privileged: false,
    inline: $userScript
    
end
