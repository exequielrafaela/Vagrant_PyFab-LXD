from fabric.api import run, sudo, settings, hide, put
from fabric.contrib.files import exists
from termcolor import colored


def lxd():
    with settings(warn_only=True):
        print colored('##################################', 'blue')
        print colored('########### LXD INSTALL ##########', 'blue')
        print colored('##################################', 'blue')

        # Add the PPA repository for LXD/LXC stable


        if exists('/etc/apt/sources.list.d/ubuntu-lxc-lxd-stable-trusty.list', use_sudo=True):
            print colored('##################################', 'blue')
            print colored('##### LDX repo already add #######', 'blue')
            print colored('##################################', 'blue')
        else:
            sudo('add-apt-repository -y ppa:ubuntu-lxc/lxd-stable')


        #sudo('if [[ ! -e "/etc/apt/sources.list.d/ubuntu-lxc-lxd-stable-trusty.list" ]]; then '
        #    'sudo add-apt-repository -y ppa:ubuntu-lxc/lxd-stable; '
        #'fi')

        sudo('apt-get update')

        # Install LXC/LXD if not already installed

        if exists('/usr/bin/lxd', use_sudo=True):
            print colored('##################################', 'blue')
            print colored('##### LDX repo already add #######', 'blue')
            print colored('##################################', 'blue')
        else:
            sudo('add-apt-repository -y ppa:ubuntu-lxc/lxd-stable')

        #sudo('if [[ ! -e "/usr/bin/lxd" ]]; then '
        #    'sudo apt-get -y install lxd; '
        #'fi')

        #Add the public LinuxContainers.org image repository by running
        sudo('lxc remote add lxc-org images.linuxcontainers.org')

        #Copy the 32-bit Ubuntu 14.04 container image to your system with the command
        #Copy the 64-bit Centos 7.0 container image to your system with the command
        #https: // images.linuxcontainers.org /
        sudo('lxc image copy lxc-org:/ubuntu/trusty/i386 local: --alias=trusty32')
        sudo('lxc image copy lxc-org:/centos/7/amd64 local: --alias=centos764')

        print colored('##########################', 'blue')
        print colored('###### LXD PROVISION #####', 'blue')
        print colored('##########################', 'blue')
        #Launch a container based on this image with the command below.
        #This will start a container named "lxd-test-01" based on the "trusty32"
        # image (which is an alias for the image you copied in thre previous step).
        #sudo('lxc launch trusty32 lxd-ubuntu-01')
        #sudo('lxc launch images:centos/7/amd64 my-container')
        sudo('lxc launch centos764 lxd-centos-01')
        sudo('lxc launch centos764 lxd-centos-02')
        sudo('lxc launch centos764 lxd-centos-03')

        sudo('lxc images list')

        sudo('dpkg-reconfigure -p medium lxd')

        sudo('lxc list')

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

        print colored('###########################', 'blue')
        print colored('## JUMPHOST PROVISIONING ##', 'blue')
        print colored('###########################', 'blue')

        sudo('lxc exec lxd-centos-01 -- echo root:toor | chpasswd')
        sudo('lxc exec lxd-centos-01 -- dhclient eth0 -r')
        sudo('lxc exec lxd-centos-01 -- dhclient eth0')
        sudo('lxc exec lxd-centos-01 -- yum clean all')
        sudo('lxc exec lxd-centos-01 -- yum install -y gcc glibc glibc-common gd gd-devel')
        sudo('lxc exec lxd-centos-01 -- yum install -y python-devel vim net-tools sudo openssh-server openssh-clients')
        sudo('lxc exec lxd-centos-01 -- yum install -y epel-release')
        sudo('lxc exec lxd-centos-01 -- yum install -y python-pip')
        sudo('lxc exec lxd-centos-01 -- pip install --upgrade pip')
        sudo('lxc exec lxd-centos-01 -- pip install fabric')
        sudo('lxc exec lxd-centos-01 -- pip install termcolor')
        sudo('lxc exec lxd-centos-01 -- chkconfig sshd on')
        sudo('lxc exec lxd-centos-01 -- service sshd start')

        sudo('lxc file push /vagrant/scripts/* lxd-centos-01/root/')
        #sudo('lxc file push /vagrant/scripts/out_users_test.txt lxd-centos-01/root/')

        print colored('###########################', 'blue')
        print colored('### CLIENT PROVISIONING ###', 'blue')
        print colored('###########################', 'blue')

        sudo('lxc exec lxd-centos-02 -- echo root:toor | chpasswd')
        sudo('lxc exec lxd-centos-02 -- dhclient eth0 -r')
        sudo('lxc exec lxd-centos-02 -- dhclient eth0')
        sudo('lxc exec lxd-centos-02 -- yum clean all')
        sudo('lxc exec lxd-centos-02 -- yum install -y python-devel vim net-tools sudo openssh-server openssh-clients')
        sudo('lxc exec lxd-centos-02 -- chkconfig sshd on')
        sudo('lxc exec lxd-centos-02 -- service sshd start')

        sudo('lxc exec lxd-centos-03 -- echo root:toor | chpasswd')
        sudo('lxc exec lxd-centos-03 -- dhclient eth0 -r')
        sudo('lxc exec lxd-centos-03 -- dhclient eth0')
        sudo('lxc exec lxd-centos-03 -- yum clean all')
        sudo('lxc exec lxd-centos-03 -- yum install -y python-devel vim net-tools sudo openssh-server openssh-clients')
        sudo('lxc exec lxd-centos-03 -- chkconfig sshd on')
        sudo('lxc exec lxd-centos-03 -- service sshd start')

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
