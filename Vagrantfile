# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

    config.ssh.forward_agent = true
    config.vm.hostname = "devmeter"
    config.vm.box = "ubuntu/xenial64"
    config.vm.network :private_network, ip: "192.168.100.100"

    config.vm.provider :virtualbox do |v|
        v.name = "devmeter"
        v.customize ["modifyvm", :id, "--memory", 6144]
        v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
        v.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
    end

end
