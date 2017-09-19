Vagrant.configure("2") do |config|

    config.vm.box = "scotch/box"
    config.vm.network "private_network", ip: "192.168.33.10"
    config.vm.hostname = "scotchbox"
    config.vm.synced_folder "./crawler", "/home/vagrant/crawler", :mount_options => ["dmode=777", "fmode=666"]
    
    # Optional NFS. Make sure to remove other synced_folder line too
    #config.vm.synced_folder ".", "/var/www", :nfs => { :mount_options => ["dmode=777","fmode=666"] }

    # Fix for the "==> default: stdin: is not a tty" bug.
    config.vm.provision "fix-no-tty", type: "shell" do |s|
        s.privileged = false
        s .inline = "sudo sed -i '/tty/!s/mesg n/tty -s \\&\\& mesg n/' /root/.profile"
    end

    # - install python3.6
    config.vm.provision :shell do |sh|
        sh.privileged = true # this means it runs as 'root'
        sh.path = "tools/install_python.sh"
    end

    # - install R
    config.vm.provision :shell do |sh|
        sh.privileged = true # this means it runs as 'root'
        sh.path = "tools/install_r.sh"
    end

end