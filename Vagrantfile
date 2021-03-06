# Provision ONS Environments in Vagrant

VAGRANTFILE_API_VERSION = "2"
require 'yaml'
nodes = YAML.load_file('nodes.yml')

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.ssh.insert_key = false
  nodes.each do |server,cfgOptions|

    config.vm.define server do |node|
      node.vm.box = cfgOptions['box']

      node.vm.hostname = cfgOptions['server']['hostname']

      cfgOptions['forwarded_ports'].each do |guest, host|
        node.vm.network 'forwarded_port', guest: guest, host: host
      end if cfgOptions['forwarded_ports']

      if cfgOptions['server']['ip']
        node.vm.network 'private_network', ip: cfgOptions['server']['ip']
      else
        node.vm.network "private_network", type: "dhcp"
      end

      node.vm.provider "virtualbox" do |v|
        v.name = cfgOptions['server']['hostname'] if cfgOptions['server']['hostname']
        v.memory = cfgOptions['server']['memory'] if cfgOptions['server']['memory']
        v.cpus = cfgOptions['server']['vcpu'] if cfgOptions['server']['vcpu']
      end

      node.vm.provision "ansible_local" do |ansible|
        ansible.verbose = "v"
        ansible.sudo = true
        ansible.galaxy_roles_path = "ons-automation/roles/"
        ansible.galaxy_role_file = "requirements.yml"
        ansible.inventory_path = "ons-automation/#{cfgOptions['provisioning']['environment']}/"
        ansible.playbook = "ons-automation/#{cfgOptions['provisioning']['role']}/playbook.yml"
      end if cfgOptions['provisioning']

    end

  end

end
