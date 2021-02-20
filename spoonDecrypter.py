import argparse, os, struct, random, getpass
from Crypto.Cipher import AES

username = getpass.getuser()	
localRoot = r'/Users/' + username + r'/'

def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)
    return out_filename









key = open("SPNCRYPT.key", "rb")
key = key.read()

if os.path.exists("SPNCRYPT.key"):
  os.remove("SPNCRYPT.key")

system = os.walk(localRoot, topdown=True)
for root, dir, files in system:
    for file in files:
        file_path = os.path.join(root, file)
        if not file.split('.')[-1] in 'SPNCRYPT':
            continue
        else:
            try:
                decrypt_file(key, file_path)
                os.remove(file_path)
                print(f'Decrypting: {file_path}')
            except:
                continue

print('\n\nYour files have been decrypted successfully!')
print('Thank you for chosing SpoonCrypter and have a nice day!')