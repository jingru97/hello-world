#=======================================================+
#=====This script performs hacking of a binary file=====#
#=======================================================#

#Step 1: Perform Zero Padding to end of bin file
#Step 2: Obtain MD5 checksum
#Step 3: Add MD5 checksum to beginning
#Step 4: Add "TM3BUSCOUPLEREIP" after checksum
#Step 5: save hacked bin file (under original file name)

#=======================================================#

import os,hashlib

filename = input('Please Enter your filename: ')
byteSizeLimit = input('Please enter number of bytes to pad to: ') 

print("File chosen: " + filename)
print("N.o of bytes to pad to: " + str(byteSizeLimit))


# open file from os
f = os.fdopen(os.open(filename , os.O_RDWR | os.O_CREAT), 'rb+')

#====Step1: Perform zero padding==========#

fileByteSize = os.path.getsize(filename)
nBytes= byteSizeLimit % fileByteSize

f.seek(0,2)
f.write(bytearray(nBytes))

print('zero padding done')
print(nBytes)

#====Step2: Obtain MD5 checksum===========#
 
# read contents of the file
f.seek(0,0)
data = f.read() 
  
# pipe contents of the file through
md5_returned = hashlib.md5(data).digest()

# check that MD5 value is successfully generated

print('MD5 obtained: '+ hashlib.md5(data).hexdigest())


#====Step3: Add MD5 checksum to start of file=====#

f.seek(0,0)
f.write(md5_returned)

print('checksum added')


#=====Step4: Add signature after=========#

f.seek(16,0)
f.write('TM3BUSCOUPLEREIP')

print('signature added')


#=====Step 5: Save hacked bin file=========#

f.seek(32,0)
f.write(data)
f.close()

print('hack successful!')





