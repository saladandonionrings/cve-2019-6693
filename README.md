# FortiGate Password Decrypt Script - CVE-2019-6693

![cve](https://github.com/saladandonionrings/cve-2019-6693/assets/61053314/861fc896-eb4a-4030-b7ea-51934993eadd)

---

🔐 An authorized remote user with access or knowledge of the standard encryption key could gain access and decrypt the FortiOS backup files and all non-administrator passwords, private keys, and High Availability (HA) passwords.

---

## Overview

This Python script is designed to recover passwords encrypted using FortiGate's encryption method. It can be used to decrypt both user passwords and High Availability (HA) configuration passwords stored in FortiOS configuration files.

## Usage
### Prerequisites

- Python 3.x
```bash
git clone https://github.com/saladandonionrings/cve-2019-6693.git
cd cve-2019-6693
pip3 install pycryptodome
```

### Decrypting Users Passwords
1. Have "admin read access" at least to Fortigate.
2. Go to "CLI Console" > `show user local` and download
3. Place the FortiOS user data in a text file named `data.txt`. Ensure that the data file contains user information in the FortiOS format.

### Decrypting HA Configuration Passwords
1. Go to "CLI Console" >  `show system ha`and download
2. Place the FortiOS user data in a text file named `ha_config.txt`. Ensure that the data file contains HA information in the FortiOS format.
3. Run the script using the following command:
   ```bash
   python3 fortigate-decrypt.py
   ```
   
# Disclaimer
⚠️ This script is provided for educational and awareness purposes only. Use this script responsibly and in compliance with all applicable laws and regulations. The authors are not responsible for any misuse or unauthorized access.
