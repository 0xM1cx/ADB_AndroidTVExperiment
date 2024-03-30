from adb_shell.auth.keygen import keygen
from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
import os
import urllib.request
import ctypes
from time import sleep


# print("HEllo...")
def genkeys():
    """
    Ine na function generates an ADB key pair (public tas private keys) na gagamiton para mag connect ha Android TV Device 
    """
    print('Generating ADB keys...')
    current_path = os.getcwd()
    keys_folder = os.path.join(current_path, 'keys')

    
    if not os.path.exists(keys_folder):
        os.makedirs(keys_folder)
        priv = os.path.join(keys_folder, 'adbkey')
        keygen(priv)
        print('Na generate na successfully an keys')
    else:
        print('Na exist na it keys')


def connect(ip):
    print(f'Connecting to {ip}:5555')
    current_path = os.getcwd()
    keys_folder = os.path.join(current_path, 'keys')

    with open(os.path.join(keys_folder, 'adbkey.pub'), 'rb') as f:
        pub = f.read()
    with open(os.path.join(keys_folder, 'adbkey'), 'rb') as f:
        priv = f.read()

    # Create a PythonRSASigner object using the loaded keys
    signer = PythonRSASigner(pub, priv)

    try:
        # Create an AdbDeviceTcp object and connect to the Android TV device using the signer object
        device = AdbDeviceTcp(ip.strip(), 5555, default_transport_timeout_s=9.)
        device.connect(rsa_keys=[signer], auth_timeout_s=0.1)
        print(f'Connected to {ip}:5555 successfully')
        return device
    except Exception as e:
        print(e)
        print('Make sure to grant ADB permission to your device (check always allow from X device and click allow),'
              ' then try again')
        print('If the above not worked, check the IP and try again')
        print('Click any key to exit & re-run it again...')
        input()
        exit(1)

def do_shit(dev):
    dev.shell('adb shell am start -n com.android.tv.settings/com.android.tv.settings.MainSettings')

if __name__ == '__main__':
    print(f"Setting up", end="")
    for i in range(3):
        sleep(1)
        print(".", end="")

    print()
    genkeys()
    ip = input("Ig surat an IP address han im TV: ")
    device = connect(ip)
    do_shit(device)
