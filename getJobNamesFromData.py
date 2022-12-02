
rawFile = open("./data/data.txt", "r")
rawFile.read()
i = rawFile.tell()
rawFile.seek(0)

rawFile.readline() # date
f = open("./data/jobnames.txt","w")
print(rawFile.readline(), file=f)

while i> rawFile.tell():
    l = rawFile.readline()
    if l == "--------------------------------------\n":
        l = rawFile.readline()
        l = rawFile.readline()
        print(l,file=f)
f.close()
