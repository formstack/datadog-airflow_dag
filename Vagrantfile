# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
    config.vm.box = "centos/7"

    config.vm.provision "ansible" do |ansible|
        ansible.playbook = "./playbooks/vagrant.yml"
        ansible.become = true
        ansible.become_user = 'root'
        ansible.compatibility_mode = "2.0"
    end
end