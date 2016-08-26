# Fabfile to:
#    - check the credentials for a certain user.
#    - to invoke: fab -f file func()
#    - $ fab -R local gen_key
#    - $ fab -R dev push_key
#    - $ fab -R dev test_key:username
# NOTE: http://docs.fabfile.org/en/1.12/usage/env.html#roles

# Import Fabric's API module#
#from fabric.api import *
from fabric.api import hosts, sudo, settings, hide, env, execute, prompt, run, local, task, put, cd
from fabric.contrib.files import append, exists
from termcolor import colored
import os
import sys
import logging
#import apt
import yum
import pwd
import iptools

# As a good practice we can log the state of each phase in our script.
#  https://docs.python.org/2.7/howto/logging.html
logging.basicConfig(filename='check_ssh.log', level=logging.DEBUG)
logging.info('LOG STARTS')
#logging.debug('This message should go to the log file')
#logging.warning('And this, too')

# Open the server list file and split the IP o each server.
# http://www.tutorialspoint.com/python/string_split.htm
# with open("./out_users_test.txt", "r") as f:
#    ServerList = [line.split()[0] for line in f]
with open("./out_users_test.txt", "r") as f:
    ServerList = [line.split()[0] for line in f]
    print(ServerList)

# In env.roledefs we define the remote servers. It can be IP Addrs or domain names.
env.roledefs = {
    'local': ['localhost'],
    'dev': ServerList,
    'staging': ['user@staging.example.com'],
    'production': ['user@production.example.com']
}

# Fabric user and pass.
env.user = "root"
env.password = "toor"
env.shell = "/bin/sh -c"

def apt_package(action,package):
    with settings(warn_only=False):
        hostvm = sudo('hostname')
        if (action =="install"  ):
            aptcache = apt.Cache()
            if aptcache[package].is_installed:
                print colored('###############################################################################', 'yellow')
                print colored(package + ' ALREADY INSTALLED in:' + hostvm + '- IP:' + env.host_string, 'yellow')
                print colored('###############################################################################', 'yellow')
            else:
                print colored('###############################################################################', 'blue')
                print colored(package + ' WILL BE INSTALLED in:' + hostvm + '- IP:' + env.host_string, 'blue')
                print colored('###############################################################################', 'blue')
                sudo('apt-get update')
                sudo('apt-get install '+package)
                aptcachenew = apt.Cache()
                if aptcachenew[package].is_installed:
                    print colored('##################################################################################', 'green')
                    print colored(package + 'SUCCESFULLY INSTALLED in:' + hostvm + '- IP:' + env.host_string, 'green')
                    print colored('##################################################################################', 'green')
                else:
                    print colored('#################################################################################', 'red')
                    print colored(package + 'INSTALLATION PROBLEM in:' + hostvm + '- IP:' + env.host_string, 'red')
                    print colored('#################################################################################', 'red')

        elif (action =="upgrade"  ):
            aptcache = apt.Cache()
            if aptcache[package].is_installed:
                print colored('############################################################################', 'yellow')
                print colored(package + ' TO BE UPGRADED in:' + hostvm + '- IP:' + env.host_string, 'yellow')
                print colored('############################################################################', 'yellow')
                sudo('apt-get update')
                sudo('apt-get install --only-upgrade '+package)
            else:
                print colored('###########################################################################', 'red')
                print colored(package + ' NOT INSTALLED in:' + hostvm + '- IP:' + env.host_string, 'red')
                print colored('###########################################################################', 'red')

        else:
            print colored('############################################################################', 'yellow')
            print colored('Usage eg1: $ fab -R dev apt_package:install,cron', 'red')
            print colored('Usage eg2: $ fab -R dev apt_package:upgrade,gcc', 'red')
            print colored('############################################################################', 'blue')

def yum_package(action, package):
    with settings(warn_only=False):
        hostvm = sudo('hostname')
        if(action =="install"):
            #yumcache = yum.YumBase()
            #print(yumcache.rpmdb.searchNevra(name=package))
            try:
                package_inst = sudo('yum list install '+package)
                print(package_inst)
                #if yumcache.rpmdb.searchNevra(name=package):
                # if not package_inst:
                if (package_inst == "" ):
                    print colored('###############################################################################', 'blue')
                    print colored(package + ' WILL BE INSTALLED in:' + hostvm + '- IP:' + env.host_string, 'blue')
                    print colored('###############################################################################', 'blue')
                    try:
                        sudo('yum install -y '+package)
                        #yumcache = yum.YumBase()
                        #if yumcache.rpmdb.searchNevra(name=package):
                        package_inst = sudo('yum list install ' + package)
                        if (package_inst == ""):
                            print colored('#################################################################################', 'red')
                            print colored(package + ' INSTALLATION PROBLEM in:' + hostvm + '- IP:' + env.host_string, 'red')
                            print colored('#################################################################################', 'red')
                        else:
                            print colored('##################################################################################', 'green')
                            print colored(package + ' SUCCESFULLY INSTALLED in:' + hostvm + '- IP:' + env.host_string, 'green')
                            print colored('##################################################################################', 'green')
                    except:
                            print colored('#################################################################################', 'red')
                            print colored(package + ' INSTALLATION PROBLEM in:' + hostvm + '- IP:' + env.host_string, 'red')
                            print colored('#################################################################################', 'red')
                else:
                    print colored('###############################################################################', 'yellow')
                    print colored(package + ' ALREADY INSTALLED in:' + hostvm + '- IP:' + env.host_string, 'yellow')
                    print colored('###############################################################################', 'yellow')
            except:
                print colored('#################################################################################', 'red')
                print colored(package + ' INSTALLATION PROBLEM in:' + hostvm + '- IP:' + env.host_string, 'red')
                print colored('#################################################################################', 'red')

        elif (action =="upgrade"  ):
            #yumcache = yum.YumBase()
            #print(yumcache.rpmdb.searchNevra(name=package))
            #if yumcache.rpmdb.searchNevra(name=package):
            try:
                package_inst = sudo('yum list install ' + package)
                print(package_inst)
                if (package_inst == ""):
                    print colored('###########################################################################', 'red')
                    print colored(package + ' NOT INSTALLED in:' + hostvm + '- IP:' + env.host_string, 'red')
                    print colored('###########################################################################', 'red')
                else:
                    print colored('############################################################################', 'yellow')
                    print colored(package + ' TO BE UPGRADED in:' + hostvm + '- IP:' + env.host_string, 'yellow')
                    print colored('############################################################################', 'yellow')
                    sudo('yum update -y '+package)
            except:
                print colored('###########################################################################', 'red')
                print colored(package + ' NOT INSTALLED in:' + hostvm + '- IP:' + env.host_string, 'red')
                print colored('###########################################################################', 'red')

        else:
            print colored('############################################################################', 'yellow')
            print colored('Usage eg1: $ fab -R dev yum_package:install,cron', 'red')
            print colored('Usage eg2: $ fab -R dev yum_package:upgrade,gcc', 'red')
            print colored('############################################################################', 'blue')

def add_user(usernamec):
    with settings(warn_only=False):
        #usernamep = prompt("Which USERNAME you like to CREATE & PUSH KEYS?")
        #user_exists = sudo('cat /etc/passwd | grep '+usernamep)
        #user_exists =sudo('grep "^'+usernamep+':" /etc/passwd')
        ##user_exists = sudo('cut -d: -f1 /etc/passwd | grep ' + usernamep)
        #print colored(user_exists, 'green')
        #print(env.host_string)
        #sudo('uname -a')

        try:
        ##if(user_exists != ""):
            user_exists = sudo('cut -d: -f1 /etc/passwd | grep '+usernamec)
            if (user_exists != ""):
                print colored('##############################', 'green')
                print colored('"' + usernamec + '" already exists', 'green')
                print colored('##############################', 'green')
                sudo('gpasswd -a ' + usernamep + ' wheel')
            else:
                print colored('#################################', 'green')
                print colored('"' + usernamec + '" doesnt exists', 'green')
                print colored('WILL BE CREATED', 'green')
                print colored('##################################', 'green')
                sudo('useradd ' + usernamec + ' -m -d /home/' + usernamec)
                #sudo('echo "' + usernamep + ':' + usernamep + '" | chpasswd')
                sudo('gpasswd -a ' + usernamep + ' wheel')
        except:
        ##else:
            print colored('#################################', 'green')
            print colored('"' + usernamec + '" doesnt exists', 'green')
            print colored('WILL BE CREATED', 'green')
            print colored('##################################', 'green')
            sudo('useradd ' + usernamec + ' -m -d /home/' + usernamec)
            #sudo('echo "'+usernamep+':'+usernamep+'" | chpasswd')
            sudo('gpasswd -a ' + usernamec + ' wheel')

def gen_key():
    with settings(warn_only=False):
        usernameg = prompt("Which USERNAME you like to GEN KEYS?")
        #user_exists = sudo('cut -d: -f1 /etc/passwd | grep '+usernameg)
        #user_exists = sudo('cat /etc/passwd | grep ' + usernameg)
        try:
            user_struct = pwd.getpwnam(usernameg)
            user_exists = user_struct.pw_gecos.split (",")[0]
            print colored(user_exists, 'green')
            if (user_exists == "root"):
                print colored('#######################################################', 'blue')
                print colored('ROOT user CANT be changed', 'blue')
                print colored('#######################################################', 'blue')

            elif os.path.exists('/home/'+usernameg+'/.ssh/id_rsa'):
                print colored(str(os.path.exists('/home/'+usernameg+'/.ssh/id_rsa')), 'blue')
                print colored('###########################################', 'blue')
                print colored('username: '+usernameg+' KEYS already EXISTS', 'blue')
                print colored('###########################################', 'blue')
            else:
                print colored('###########################################', 'blue')
                print colored('username: ' + usernameg + ' Creating KEYS', 'blue')
                print colored('###########################################', 'blue')
                sudo("ssh-keygen -t rsa -f /home/" + usernameg + "/.ssh/id_rsa -N ''", user=usernameg)
                # http://unix.stackexchange.com/questions/36540/why-am-i-still-getting-a-password-prompt-with-ssh-with-public-key-authentication
                # sudo('chmod 700 /home/' + usernameg)
                sudo('chmod 755 /home/' + usernameg)
                sudo('chmod 755 /home/' + usernameg + '/.ssh')
                sudo('chmod 600 /home/' + usernameg + '/.ssh/id_rsa')
                sudo('gpasswd -a ' + usernameg + ' wheel')
        except KeyError:
            print colored('User '+usernameg+' does not exist', 'red')
            print colored('#######################################################', 'blue')
            print colored('Consider that we generate user: username pass: username', 'blue')
            print colored('#######################################################', 'blue')

            sudo('useradd ' + usernameg + ' -m -d /home/' + usernameg)
            sudo('echo "' + usernameg + ':' + usernameg + '" | chpasswd')
            sudo("ssh-keygen -t rsa -f /home/" + usernameg + "/.ssh/id_rsa -N ''", user=usernameg)
            # http://unix.stackexchange.com/questions/36540/why-am-i-still-getting-a-password-prompt-with-ssh-with-public-key-authentication
            # sudo('chmod 700 /home/' + usernameg)
            sudo('chmod 755 /home/' + usernameg)
            sudo('chmod 755 /home/' + usernameg + '/.ssh')
            sudo('chmod 600 /home/' + usernameg + '/.ssh/id_rsa')
            sudo('gpasswd -a ' + usernameg + ' wheel')

def read_key_file(key_file):
    with settings(warn_only=False):
        key_file = os.path.expanduser(key_file)
        if not key_file.endswith('pub'):
            raise RuntimeWarning('Trying to push non-public part of key pair')
        with open(key_file) as f:
            return f.read()

def append_key(usernamea):
    with settings(warn_only=False):
        if(usernamea == "root"):
            key_file = '/'+ usernamea+'/.ssh/id_rsa.pub'
            key_text = read_key_file(key_file)
            if exists('/'+usernamea+'/.ssh/authorized_keys', use_sudo=True):
                local('sudo chmod 701 /home/' + usernamea)
                local('sudo chmod 741 /home/' + usernamea + '/.ssh')
                local('sudo chmod 604 /home/' + usernamea + '/.ssh/id_rsa.pub')
                print colored('#########################################', 'blue')
                print colored('##### authorized_keys file exists #######', 'blue')
                print colored('#########################################', 'blue')
                append('/'+usernamea+'/.ssh/authorized_keys', key_text, use_sudo=True)
                sudo('chown -R ' + usernamea + ':' + usernamea + ' /home/' + usernamea + '/.ssh/')
                local('sudo chmod 700 /home/' + usernamea)
                local('sudo chmod 700 /home/' + usernamea + '/.ssh')
                local('sudo chmod 600 /home/' + usernamea + '/.ssh/id_rsa.pub')
            else:
                sudo('mkdir -p /'+usernamea+'/.ssh/')
                sudo('touch /'+usernamea+'/.ssh/authorized_keys')
                append('/'+ usernamea+'/.ssh/authorized_keys', key_text, use_sudo=True)
                sudo('chown -R ' + usernamea + ':' + usernamea + ' /home/' + usernamea + '/.ssh/')
                # put('/home/'+usernamea+'/.ssh/authorized_keys', '/home/'+usernamea+'/.ssh/')
                local('sudo chmod 700 /home/' + usernamea)
                local('sudo chmod 700 /home/' + usernamea + '/.ssh')
                local('sudo chmod 600 /home/' + usernamea + '/.ssh/id_rsa.pub')

        else:
            key_file = '/home/'+usernamea+'/.ssh/id_rsa.pub'
            local('sudo chmod 701 /home/' + usernamea)
            local('sudo chmod 741 /home/' + usernamea + '/.ssh')
            local('sudo chmod 604 /home/' + usernamea + '/.ssh/id_rsa.pub')
            key_text = read_key_file(key_file)
            local('sudo chmod 700 /home/' + usernamea)
            local('sudo chmod 700 /home/' + usernamea + '/.ssh')
            local('sudo chmod 600 /home/' + usernamea + '/.ssh/id_rsa.pub')
            if exists('/home/'+usernamea+'/.ssh/authorized_keys', use_sudo=True):
                print colored('#########################################', 'blue')
                print colored('##### authorized_keys file exists #######', 'blue')
                print colored('#########################################', 'blue')
                append('/home/'+usernamea+'/.ssh/authorized_keys', key_text, use_sudo=True)
                sudo('chown -R ' + usernamea + ':' + usernamea + ' /home/' + usernamea + '/.ssh/')
            else:
                sudo('mkdir -p /home/'+usernamea+'/.ssh/')
                sudo('touch /home/' + usernamea + '/.ssh/authorized_keys')
                append('/home/'+usernamea+'/.ssh/authorized_keys', key_text, use_sudo=True)
                sudo('chown -R ' + usernamea + ':' + usernamea + ' /home/' + usernamea + '/.ssh/')
            #put('/home/'+usernamea+'/.ssh/authorized_keys', '/home/'+usernamea+'/.ssh/')

def test_key(usernamet):
    with settings(warn_only=False):
        hostvm = sudo('hostname')
        local('sudo chmod 701 /home/' + usernamet)
        local('sudo chmod 741 /home/' + usernamet + '/.ssh')
        local_user=getpass.getuser()
        if (os.path.exists('/home/'+local_user+'/temp/')):
            print colored('##################################', 'blue')
            print colored('##### Directory Exists ###########', 'blue')
            print colored('##################################', 'blue')
        else:
            local('mkdir ~/temp')

        local('sudo cp /home/'+usernamet+'/.ssh/id_rsa ~/temp/id_rsa')
        local('sudo chown -R '+local_user+':'+local_user+' ~/temp/id_rsa')
        #local('sudo chmod 604 /home/' + usernamet + '/.ssh/id_rsa')

        # FIX DONE! - Must copy the key temporaly with the proper permissions
        # in the home directory of the current user executing fabric to use it.
        # Temporally we comment the line 379 and the script must be run by
        # user that desires to test it keys
        #[ntorres@jumphost fabric]$ ssh -i /home/ntorres/.ssh/id_rsa ntorres@10.0.3.113   Warning: Permanently added '10.0.3.113' (ECDSA) to the list of known hosts.
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        #@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        #Permissions 0604 for '/home/ntorres/.ssh/id_rsa' are too open.
        #It is required that your private key files are NOT accessible by others.
        #This private key will be ignored.
        #bad permissions: ignore key: /home/ntorres/.ssh/id_rsa
        #Permission denied (publickey).
        #NOTE:
        #there is no way to bypass the keyfile permission check with ssh or ssh-add
        #(and you can't trick it with named pipe or such). Besides, you do not actually want to trick ssh,' \
        #' but just to be able to use your key files.

        if (os.path.exists('/home/'+usernamet+'/.ssh/')):
            ssh_test = local('ssh -i ~/temp/id_rsa -o "StrictHostKeyChecking no" -q '+usernamet+'@'+env.host_string+' exit')
            if (ssh_test.succeeded):
                print colored('###################################################', 'blue')
                print colored(usernamet+' WORKED! in:'+hostvm+' IP:'+env.host_string, 'blue')
                print colored('###################################################', 'blue')
                local('sudo chmod 700 /home/'+usernamet)
                local('sudo chmod 700 /home/'+usernamet+'/.ssh')
                #local('sudo chmod 600 /home/'+usernamet+'/.ssh/id_rsa')
                local('sudo rm ~/temp/id_rsa')
        else:
            print colored('###################################################', 'red')
            print colored(usernamet+' FAIL! in:'+hostvm+'- IP:'+env.host_string, 'red')
            print colored('###################################################', 'red')

def ruby_install_centos():
    with settings(warn_only=False):
        # sudo('yum ruby ruby-devel rubygems')
        # yum groupinstall -y development
        # yum groupinstall -y 'development tools'
        sudo('yum groupinstall "Development Tools"')
        sudo('yum install -y git-core zlib zlib-devel gcc-c++ patch readline readline-devel')
        sudo('yum install -y libyaml-devel libffi-devel openssl-devel make bzip2 autoconf automake libtool bison curl sqlite-devel')

        #with cd('/home/'+usernamei+'/'):
        with cd('~'):
            run('gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3')
            run('\curl -sSL https://get.rvm.io | bash -s stable --ruby')
            run('source ~/.rvm/scripts/rvm')
            run('gem install bundler')

def chefzero_install_centos():
    with settings(warn_only=False):
        run('wget -P /tmp/ https://packages.chef.io/stable/el/7/chefdk-0.17.17-1.el7.x86_64.rpm')
        run('rpm -Uvh /tmp/chefdk-0.17.17-1.el7.x86_64.rpm')

        knifezero_inst = run('chef gem list | grep knife-zero')
        if(knifezero_inst ==""):
            run('chef gem install knife-zero')
        else:
            print colored('##############################################', 'blue')
            print colored('##### knife-zero already installed ###########', 'blue')
            print colored('##############################################', 'blue')

        if exists('/opt/chefdk/embedded/bin/knife', use_sudo=True):
            print colored('###########################################', 'blue')
            print colored('##### Knife-zero correctly installed ######', 'blue')
            print colored('###########################################', 'blue')
        else:
            print colored('###########################################', 'red')
            print colored('###### Check chef-zero installation #######', 'red')
            print colored('###########################################', 'red')

def nfs_server(nfs_dir):
    with settings(warn_only=False):
        sudo('yum install -y nfs-utils libnfsidmap libnfsidmap-devel nfs4-acl-tools')

        if exists('/var/'+nfs_dir, use_sudo=True):
            print colored('###########################################', 'blue')
            print colored('####### Directory already created #########', 'blue')
            print colored('###########################################', 'blue')
        else:
            print colored('###########################################', 'red')
            print colored('###### Creating NFS share Directory #######', 'red')
            print colored('###########################################', 'red')
            sudo('mkdir /var/'+nfs_dir)
            sudo('chmod -R 777 /var/'+nfs_dir+'/')

        ip_addr=sudo('ifconfig eth0 | awk \'/inet /{print substr($2,1)}\'')
        netmask=sudo('ifconfig eth0 | awk \'/inet /{print substr($4,1)}\'')
        subnet_temp = iptools.ipv4.subnet2block(str(ip_addr) + '/' + str(netmask))
        subnet = subnet_temp[0]
        #sudo('echo "/var/' + nfs_dir + '     ' + subnet + '/' + netmask + '(rw,sync,no_root_squash,no_all_squash)" > /etc/exports')
        sudo('echo "/var/'+nfs_dir+'     *(rw,sync,no_root_squash)" > /etc/exports')

        #sudo('sudo exportfs -a')

        sudo('systemctl enable rpcbind')
        sudo('systemctl start rpcbind')

        sudo('systemctl enable nfs-server')
        sudo('systemctl start nfs-server')

        #sudo firewall-cmd --zone=public --add-service=nfs --permanent
        #sudo firewall-cmd --zone=public --add-service=rpc-bind --permanent
        #sudo firewall-cmd --zone=public --add-service=mountd --permanent
        #sudo firewall-cmd --reload

def nfs_client(nfs_dir,nfs_server_ip):
    with settings(warn_only=False):
        sudo('yum install -y nfs-utils')
        sudo('mkdir -p /mnt/nfs/var/'+nfs_dir)
        sudo('mount -t nfs '+nfs_server_ip+':/var/'+nfs_dir+' /mnt/nfs/var/'+nfs_dir+'/')
        run('df - kh | grep nfs')
        run('mount | grep nfs')

        try:
            run('touch /mnt/nfs/var/nfsshare/test_nfs')

        except:
            print colored('###########################################', 'red')
            print colored('###### Check chef-zero installation #######', 'red')
            print colored('###########################################', 'red')


'''
def push_key(usernamep):
    with settings(warn_only=False):
        #usernamep = prompt("Which USERNAME you like to CREATE & PUSH KEYS?")
        #user_exists = sudo('cat /etc/passwd | grep '+usernamep)
        #user_exists =sudo('grep "^'+usernamep+':" /etc/passwd')
        ##user_exists = sudo('cut -d: -f1 /etc/passwd | grep ' + usernamep)
        #print colored(user_exists, 'green')
        #print(env.host_string)
        #sudo('uname -a')

        try:
        ##if(user_exists != ""):
            user_exists = sudo('cut -d: -f1 /etc/passwd | grep '+usernamep)
            if (user_exists != ""):
                print colored('##############################', 'green')
                print colored('"' + usernamep + '" already exists', 'green')
                print colored('PUSHING KEYS', 'green')
                print colored('##############################', 'green')
                local('sudo chmod 701 /home/' + usernamep)
                local('sudo chmod 741 /home/' + usernamep + '/.ssh')
                local('sudo chmod 604 /home/' + usernamep + '/.ssh/id_rsa')
                local('sudo chmod 604 /home/' + usernamep + '/.ssh/id_rsa.pub')

                local('ssh-copy-id -i /home/' + usernamep + '/.ssh/id_rsa.pub ' + usernamep + '@' + env.host_string)
                sudo('chmod 700 /home/' + usernamep + '/.ssh/authorized_keys')
                sudo('gpasswd -a ' + usernamep + ' wheel')

                local('sudo chmod 700 /home/' + usernamep)
                local('sudo chmod 700 /home/' + usernamep + '/.ssh')
                local('sudo chmod 600 /home/' + usernamep + '/.ssh/id_rsa')
                local('sudo chmod 600 /home/' + usernamep + '/.ssh/id_rsa.pub')
            else:
                print colored('#################################', 'green')
                print colored('"' + usernamep + '" doesnt exists', 'green')
                print colored('PUSHING KEYS', 'green')
                print colored('##################################', 'green')
                local('sudo chmod 701 /home/' + usernamep)
                local('sudo chmod 741 /home/' + usernamep + '/.ssh')
                local('sudo chmod 600 /home/' + usernamep + '/.ssh/id_rsa')
                local('sudo chmod 604 /home/' + usernamep + '/.ssh/id_rsa.pub')

                sudo('useradd ' + usernamep + ' -m -d /home/' + usernamep)
                sudo('echo "' + usernamep + ':' + usernamep + '" | chpasswd')

                # Remember that the usernamep is not in the remote server
                # Then you are gona be ask the pass of this user.
                # To avoid this you must use a user that it's already created
                # in the local and remote host with the proper permissions.
                local('ssh-copy-id -i /home/' + usernamep + '/.ssh/id_rsa.pub ' + usernamep + '@' + env.host_string)
                sudo('chmod 700 /home/' + usernamep + '/.ssh/authorized_keys')
                sudo('gpasswd -a ' + usernamep + ' wheel')

                local('sudo chmod 700 /home/' + usernamep)
                local('sudo chmod 700 /home/' + usernamep + '/.ssh')
                local('sudo chmod 600 /home/' + usernamep + '/.ssh/id_rsa')
                local('sudo chmod 600 /home/' + usernamep + '/.ssh/id_rsa.pub')
        except:
        ##else:
            print colored('#################################', 'green')
            print colored('"' + usernamep + '" doesnt exists', 'green')
            print colored('PUSHING KEYS', 'green')
            print colored('##################################', 'green')
            local('sudo chmod 701 /home/' + usernamep)
            local('sudo chmod 741 /home/' + usernamep + '/.ssh')
            local('sudo chmod 604 /home/' + usernamep + '/.ssh/id_rsa')
            local('sudo chmod 604 /home/' + usernamep + '/.ssh/id_rsa.pub')
            sudo('useradd ' + usernamep + ' -m -d /home/' + usernamep)
            sudo('echo "'+usernamep+':'+usernamep+'" | chpasswd')
            # Remember that the usernamep is not in the remote server
            # Then you are gona be ask the pass of this user.
            # To avoid this you must use a user that it's already created
            # in the local and remote host with the proper permissions.
            local('ssh-copy-id -i /home/'+usernamep+'/.ssh/id_rsa.pub '+usernamep+'@'+env.host_string)
            sudo('chmod 700 /home/'+usernamep+'/.ssh/authorized_keys')
            sudo('gpasswd -a ' + usernamep + ' wheel')
            local('sudo chmod 700 /home/' + usernamep)
            local('sudo chmod 700 /home/' + usernamep + '/.ssh')
            local('sudo chmod 600 /home/' + usernamep + '/.ssh/id_rsa')
            local('sudo chmod 600 /home/' + usernamep + '/.ssh/id_rsa.pub')
'''