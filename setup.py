import subprocess
import os 
import time
import pwd
import threading
import sys
if not sys.platform.lower().startswith('l'):
    print("for linux platforms only")
    exit()
try:
    import tqdm
except ModuleNotFoundError:
    os.system("pip3 install tqdm")
    time.sleep(2)
finally:
    from tqdm import tqdm


has_args = True
try:
    args = sys.argv[1:]
except IndexError:
    has_args = False
if has_args == False:
    website = args[0] if not args[0].startswith("www.") else args[0][4:]
    WEBSITE = website
else:
    print("\033[43m      ***      ATTENTION    ***           \033[0m")
    print("\033[42m      Script Requires Website Name        \033[0m")
    website = input("\n\tPlease enter your website:\n\n\t\033[32mwww\033[0m.\033[31m")
    print("\033[0m")
    if website == "":
        exit()
    WEBSITE = website
uid = os.getuid()
try:
    USER = os.getlogin()
except FileNotFoundError:
    USER = pwd.getpwuid(uid).pw_name
FILEPATH = os.path.abspath(__file__)
DIRECTORY = os.path.dirname(FILEPATH)
NEW_PATH = os.path.join(DIRECTORY,"master.py")


commands = [
    "sudo apt update && sudo apt upgrade", 
    "sudo apt install -y openssh-server", 
    "sudo systemctl enable --now ssh", 
    "sudo apt-get install -y apache2", 
    "sudo apt-get install -y ufw", 
    "sudo ufw allow http", 
    "sudo ufw allow https", 
    "sudo apt-get install -y mysql-server", 
    "sudo apt-get install -y php libapache2-mod-php php-mysql php-cgi php-curl php-json", 
    f"sudo mkdir -p /var/www/{WEBSITE}/", 
    f"sudo chown -R {USER}:{USER} /var/www/{WEBSITE}", 
    f"sudo chmod -R 755 /var/www/{WEBSITE}"
    ]
steps = ["update and upgrading", "installing openssh-server", "enabling openssh-server", "installing apache 2", "installing ufw", "Enabling http and https", "installing mysql-server",
         "installing php", "making directory", "changing ownerships", "changing permissions"]

def is_sudo():
    return os.geteuid() == 0

def ran_sudo():
    if not is_sudo():
        print(f"\n\033[31m \tThis script must be run with sudo\033[0m\n")
        exit()
    
def setup_website_enviroment() -> None:
    sindex = 0
    failed_to = []
    
    for status in tqdm(range(len(steps))):
        
        try:
            cmd = commands.pop(0)
        except IndexError:
            continue
        except KeyboardInterrupt:
            exit()
        finally:
            
            try:
                stat = steps[sindex]
            except IndexError:
                stat = ""
            finally:
                print(stat)
                sindex+=1
            
            silent_command = f"{cmd} > /dev/null 2>&1"
            scmd = subprocess.run(silent_command, shell=True)
            if scmd.returncode == 0:
                os.sync()
            else:
                failed_to.append(cmd)
    
    if not failed_to is None:
        print("failed commands:")
        for cmd in failed_to:
            print(f"\t{cmd}")
            scheduled_command(cmd)

def shell_command(command: str, delay=0):
    time.sleep(delay)
    subprocess.run(command, shell=True)

def ensure_thread(thread):
    thread.join()
        
def scheduled_command(command, delay: int=1):
    new_thread = threading.Thread(target=shell_command, args=(command, delay))
    new_thread.start()
    ensurethread = threading.Thread(target=ensure_thread, args=(new_thread, ))
    ensurethread.run()

def main():
    
    ran_sudo()
    
    setup_website_enviroment()
    
    print("Done!")


if __name__ == "__main__":
    main()
            