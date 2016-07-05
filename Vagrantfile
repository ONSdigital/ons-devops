# Provision ONS Environments in Vagrant

VAGRANTFILE_API_VERSION = "2"
require 'yaml'
nodes = YAML.load_file('nodes.yaml')

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "geerlingguy/centos7"
  config.ssh.insert_key = false
  nodes.each do |server,cfgOptions|

    config.vm.define server do |node|

      node.vm.hostname = cfgOptions['hostname']
      node.vm.network "private_network", type: "dhcp"
      node.vm.provision "shell", path: "setup.sh"

      node.vm.provider "virtualbox" do |v|
        v.name = cfgOptions['hostname']
        v.memory = cfgOptions['memory']
      end

      node.vm.provision "ansible_local" do |ansible|
        ansible.verbose = "v"
        ansible.sudo = true
        ansible.galaxy_role_file = "requirements.yml"
        ansible.playbook = "ons-automation/#{cfgOptions['role']}.yml"
      end

    end

  end

end
