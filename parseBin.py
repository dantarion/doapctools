import os, struct
def readString(f,off):
    f.seek(off)
    return f.read(255).split("\x00")[0]
def pad(offset):
    align = 0x800
    return offset + (align - (offset % align)) % align
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
        entries.append((offset,size1,size2,flags))



    
    return entries
def parseBin(filename):
    entries = parseLnk(filename.replace(".bin",".lnk"))
    
    f = open("../"+filename,"rb")
    f2 = open("../"+filename.replace(".bin",".lnk"),"rb")
    print "%22s" % filename,
    FILE_TYPE,ENTRY_COUNT,UNK1,UNK2,UNK3,UNK4,UNK6,UNK7,UNK8 = struct.unpack("4s4x8I",f.read(40))
    print (FILE_TYPE,ENTRY_COUNT,UNK1,UNK2,UNK3,UNK4,UNK6,UNK7,UNK8),
    print readString(f,UNK3),
    print readString(f,UNK4)
    
    for i in range(0,ENTRY_COUNT):
        f.seek(40+i*12)
        entry = struct.unpack("3I",f.read(12))
        print "\t",entry,readString(f,entry[2]),entries[i]
        f2.seek(entries[i][0])
        data = f2.read(entries[i][1])
        dds = data.find("DDS\x20")
        if dds != -1:
            print "DDS TEXTURE FOUND"
            if not os.path.exists(filename):
                os.makedirs(filename)
            out = open(filename+"/"+str(i)+".dds","wb")
            out.write(data[dds:])
            out.close()
for filename in os.listdir("../"):
    if filename[-3:] == "bin":
        parseBin(filename)
#parseBin("chara_common.bin")
