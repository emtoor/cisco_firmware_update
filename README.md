# cisco_firmware_update

Python script that uses Paramiko to upgrade the firmware on Cisco devices. It prompts the user for a range of IP addresses, the specific Cisco device model, the firmware version, the SSH username, and the password. The script then logs into each device, checks the device information, uploads the firmware to the device using FTP, and upgrades the firmware using the copy command. The script outputs the result of each device upgrade process, so the user can see if the upgrade was successful or not.
