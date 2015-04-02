import os, struct
def readString(f,off):
    f.seek(off)
    return f.read(255).split("\x00")[0]
def parseBin(filename):
    f = open("../"+filename,"rb")
    print "%22s" % filename,
    FILE_TYPE,ENTRY_COUNT,UNK1,UNK2,UNK3,UNK4,UNK6,UNK7,UNK8 = struct.unpack("4s4x8I",f.read(40))
    print (FILE_TYPE,ENTRY_COUNT,UNK1,UNK2,UNK3,UNK4,UNK6,UNK7,UNK8),
    print readString(f,UNK3),
    print readString(f,UNK4)
    
    for i in range(0,ENTRY_COUNT):
        f.seek(40+i*12)
        entry = struct.unpack("3I",f.read(12))
        print "\t",entry,readString(f,entry[2])
#for filename in os.listdir("../"):
#    if filename[-3:] == "bin":
#        parseBin(filename)
parseBin("patch_02_catalog.bin")
