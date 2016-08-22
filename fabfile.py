from fabric.api import run, sudo, settings, hide, put
from termcolor import colored


def lxd():
    with settings(warn_only=True):
        print colored('##########################', 'blue')
        print colored('########### LXD ##########', 'blue')
        print colored('##########################', 'blue')

        # Add the PPA repository for LXD/LXC stable
        sudo('if [[ ! -e "/etc/apt/sources.list.d/ubuntu-lxc-lxd-stable-trusty.list" ]]; then '
            'sudo add-apt-repository -y ppa:ubuntu-lxc/lxd-stable; '
        'fi')

        #run('if [ ! -f "/home/vagrant/nagios-4.1.1.tar.gz" ]; then '
        #    'wget https://sourceforge.net/projects/nagios/files/nagios-4.x/nagios-4.1.1/nagios-4.1.1.tar.gz; '
        #    'fi')

        sudo('apt-get update')

        # Install LXC/LXD if not already installed
        sudo('if [[ ! -e "/usr/bin/lxd" ]]; then '
            'sudo apt-get -y install lxd; '
        'fi')

        #Add the public LinuxContainers.org image repository by running
        sudo('lxc remote add lxc-org images.linuxcontainers.org')

        #Copy the 32-bit Ubuntu 14.04 container image to your system with the command
        sudo('lxc image copy lxc-org:/ubuntu/trusty/i386 local: --alias=trusty32')

        #Launch a container based on this image with the command below.
        #This will start a container named "lxd-test-01" based on the "trusty32"
        # image (which is an alias for the image you copied in thre previous step).
        sudo('lxc launch trusty32 lxd-test-01')

        print colored('##########################', 'blue')
        print colored('########### LXD ##########', 'blue')
        print colored('##########################', 'blue')

        print colored('1) Run file /bin/ls and note the output. (You will use the output for comparison in just a moment.)', 'green')
        print colored('##########################', 'green')
        print colored('2) Open a shell in the 32-bit container you launched in step 8 with the command:', 'green')
        print colored('lxc exec lxd-test-01 bash', 'green')
        print colored('##########################', 'green')
        print colored('3) Inside the container, run file /bin/ls and compare the output to the output of the same command you ran', 'green')
        print colored('outside the container. You will see that inside the container the file is reported as a 32-bit ELF executable', 'green')
        print colored('outside the container the same file is listed as a 64-bit ELF executable.', 'green')
        print colored('##########################', 'green')
        print colored('4) Press Ctrl-D to exit the shell in the container.', 'green')
        print colored('##########################', 'green')
        print colored('5) The container is still running, so stop the container with:', 'green')
        print colored('lxc stop lxd-test-01.', 'green')

        #print colored('######################################', 'blue')
        #print colored('SERVER BASIC PROVISIONING:      ', 'blue')
        #print colored('######################################', 'blue')
        #sudo('cp /vagrant/fabric/fabfile.py /home/vagrant/fabfile.py')

        print colored('######################################', 'blue')
        print colored('FIREWALL - NAT TABLE STATUS:      ', 'blue')
        print colored('######################################', 'blue')
        with hide('output'):
            fw = sudo('iptables -t nat -L')
        print colored(fw, 'red')

        print colored('######################################', 'blue')
        print colored('FIREWALL - FILTER TABLE STATUS:   ', 'blue')
        print colored('######################################', 'blue')
        with hide('output'):
            fw = sudo('iptables -L')
        print colored(fw, 'red')

        print colored('##########################', 'blue')
        print colored('## NETWORK CONFIGURATION #', 'blue')
        print colored('##########################', 'blue')
        with hide('output'):
            netconf = sudo('ip addr show')
        print colored(netconf, 'green')
