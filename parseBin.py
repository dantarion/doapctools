import os, struct
import string
import zlib
def doa_decrypt(s):
    xorkey  = "Except as expressly authorized, it is strictly prohibited to reproduce, distribute, exhibit or modify this software and any of its contents, including audio and visual contents. By way of example, to capture, copy or download any of the contents in this software, including audio and visual contents, onto any hardware or other software source media for any purpose, by the Internet or any other source, is strictly prohibited. Reversed engineering, decompiling or disassembly of this software is also strictly prohibited."
    dcounter = 0;
    ccounter = 0;
    doffset = 0;
    out = ""
    for doffset in range(0,len(s)):
      test = ord(xorkey[dcounter]);
      dcounter += 1
      if dcounter == 522:
          dcounter = 0
      test2 = ord(s[ccounter])
      ccounter += 1
      if test2 != 0 and test2 != test:
          test2 ^= test
      out +=  chr(test2)
    print s,out
    return s
def readString(f,off):
    f.seek(off)
    return f.read(255).split("\x00")[0]
def pad(offset):
    align = 0x800
    return offset + (align - (offset % align)) % align
def is_ascii(s):
    for c in s:
        if c not in string.ascii_letters+string.digits:
            return False
    return True
               
def dumpTextures(filename):
    f = open("../"+filename,"rb",819200)
    print filename,
    try:
        while True:
            test = f.read(4)
            if test == "DDS\x20":
                print f.tell()-4
            f.seek(12,1)
    except:
        pass
def parseLnk(filename):
    f = open("../"+filename,"rb")
    #print "%22s" % filename,
    s,entry_count,filesize,unk1 =  struct.unpack("8s3q",f.read(32))
    entries = []
    for i in range(0,entry_count):
        f.seek(32+i*32)
        offset,size1,size2,flags = struct.unpack("4q",f.read(32))
        f.seek(offset)
        
        tag = f.read(8).split("\x00")[0]
        if not is_ascii(tag):
               f.seek(offset)
               tag = doa_decrypt(f.read(4))
        if not is_ascii(tag):
               tag = "unk"
        entries.append((offset,size1,size2,flags,tag))
        


    
    return entries
def parseBin(filename):
    entries = parseLnk(filename.replace(".bin",".lnk"))
    
    f = open("../"+filename,"rb")
    f2 = open("../"+filename.replace(".bin",".lnk"),"rb")
    print "%22s" % filename,
    FILE_TYPE,ENTRY_COUNT,UNK1,UNK2,UNK3,UNK4,UNK6,UNK7,UNK8 = struct.unpack("4s4x8I",f.read(40))
    print (FILE_TYPE,ENTRY_COUNT,UNK1,UNK2,UNK3,UNK4,UNK6,UNK7,UNK8),

    
    
    for i in range(0,ENTRY_COUNT):
        f.seek(40+i*12)
        entry = struct.unpack("3I",f.read(12))
        print "\t",entry,readString(f,entry[2]),entries[i]
        fname = readString(f,entry[2])
        f2.seek(entries[i][0])
        data = f2.read(entries[i][1])
        dds = data.find("DDS\x20")
        tag = entries[i][4]
        if tag:
            if not os.path.exists("out/"+filename):
                os.makedirs("out/"+filename)
            out = open("out/"+filename+fname+"."+tag,"wb")
            out.write(data)
            out.close()
        if dds != -1:
            print "DDS TEXTURE FOUND"
            if not os.path.exists("out/"+filename):
                os.makedirs("out/"+filename)
            out = open("out/"+filename+fname+".dds","wb")
            out.write(data[dds:])
            out.close()
for filename in os.listdir("../"):
    if filename[-3:] == "bin":
        parseBin(filename)
#parseBin("chara_initial.bin")
