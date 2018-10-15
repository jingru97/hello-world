# This is a script to automate the BIN file hacking process

#input file here
filename = input('Enter your file name here')

# Step 1: Append 0s (in hexadecimal format) to the end of the BIN file


# Step 2: Prepend MD-5 hash to the front of the BIN file
# Step 3: Prepend signature after MD-5 hash

#MD5 hasher
import hashlib
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

MD5_hash = md5(filename)
print(MD5_hash)
input('MD5 hash is done')
MD5_ascii = bytes.fromhex(MD5_hash)
print (MD5_ascii)
input('ascii is done')

#Prepend
f = open(filename, 'r')
temp = f.read()
f.close()

f = open(filename, 'w')
f.write(MD5_ascii)
f.write("TM3BUSCOUPLEREIP")
f.write(temp)
f.close()

#pause before exiting
input('Hacking is done. Press any key to continue')

#References
#MD5 hasher https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
#Prepend https://stackoverflow.com/questions/4454298/prepend-a-line-to-an-existing-file-in-python