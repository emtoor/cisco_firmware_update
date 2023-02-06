import paramiko
import ftplib

def upgrade_firmware(device_ip, model, firmware_version, username, password, firmware_file):
    # Connect to the device using SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(device_ip, username=username, password=password)

    # Check the device information
    if check_device_info(ssh, model, firmware_version):
        # Upload the firmware to the device using FTP
        ftp = ftplib.FTP(device_ip)
        ftp.login(username, password)
        ftp.cwd('/')
        with open(firmware_file, 'rb') as f:
            ftp.storbinary('STOR ' + firmware_file, f)
        ftp.quit()

        # Upgrade the firmware on the device
        upgrade_command = "copy tftp://" + device_ip + "/" + firmware_file + " flash:\n"
        ssh.exec_command(upgrade_command)

        # Check if the upgrade was successful
        stdin, stdout, stderr = ssh.exec_command("show version")
        output = stdout.read().decode()
        if firmware_version in output:
            print(f"Upgrade to {firmware_version} successful on device with IP: {device_ip}")
        else:
            print(f"Upgrade to {firmware_version} failed on device with IP: {device_ip}")
    else:
        print(f"Device information does not match for device with IP: {device_ip}")

def check_device_info(ssh, model, firmware_version):
    stdin, stdout, stderr = ssh.exec_command("show version")
    output = stdout.read().decode()
    if model in output and firmware_version in output:
        return True
    return False

if __name__ == '__main__':
    # Ask the user for the range of IP addresses, the device model and firmware version, the SSH username and password, and the firmware file
    ip_range = input("Enter the range of IP addresses (separated by commas): ")
    device_ips = ip_range.split(',')
    model = input("Enter the device model: ")
    firmware_version = input("Enter the firmware version: ")
    username = input("Enter the SSH username: ")
    password = input("Enter the SSH password: ")
    firmware_file = input("Enter the firmware file name: ")

    # Loop through the range of IP addresses and upgrade the firmware on each device
    for device_ip in device_ips:
        upgrade_firmware(device_ip.strip(), model, firmware_version, username, password, firmware_file)
