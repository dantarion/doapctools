import os, struct
def readString(f,off):
    f.seek(off)
    return f.read(255).split("\x00")[0]
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
    s,entry_count,filesize,unk1,unk2 =  struct.unpack("8s4q",f.read(40))
    entries = []
    for i in range(0,entry_count):
        f.seek(40+i*32)
        size1,size2,flags,offset = struct.unpack("4q",f.read(32))
        f.seek(offset)
        tag = f.read(4)
        entries.append((size1,size2,flags,offset,tag))
        #print "\t",i,"\t",size1,size2,flags,offset
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
        if entries[i][4] == "dlic" and entries[i][0] > 4160:
            if not os.path.exists(filename):
                os.makedirs(filename)
            out = open(filename+"/"+str(i)+".dds","wb")
            f2.seek(entries[i][3]+4160)
            out.write(f2.read(entries[i][0]-4160))
            out.close()
#for filename in os.listdir("../"):
#    if filename[-3:] == "lnk":
#        dumpTextures(filename)
dumpTextures("chara_initial.bin")
