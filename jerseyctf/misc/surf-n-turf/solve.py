import subprocess
from string import printable, digits, ascii_lowercase, punctuation 
password = "EQNQTCFQTKXGT" 
encrypted_file = "location.txt.aes"
for x in ascii_lowercase:
    for y in digits:
        for z in punctuation:
            new_pass = password + x + y +z
            command = f"pyAesCrypt -p '{new_pass}' -d {encrypted_file} -o {x+y+z}"

            try:
               subprocess.run(command, shell=True, check=True)
               print("File decrypted successfully")
               print(x+y+z)
            except subprocess.CalledProcessError:
               print("Decryption failed")