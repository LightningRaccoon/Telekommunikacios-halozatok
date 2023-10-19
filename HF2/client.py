import os.path
import sys
import struct

packer1 = struct.Struct('f ? s')
packer2 = struct.Struct('s 9s i')
packer3 = struct.Struct('i ? f')
packer4 = struct.Struct('s f 9s')

with open(sys.argv[1], 'wb') as f:
    f.seek(packer1.size)
    f.write(packer1.pack(5.6, True, 'c').encode())
    f.close()

with open(sys.argv[1], 'rb') as f:
    f.seek(packer1.size)
    data = f.read(packer1.size)
    print("Parameter1 formatuma: " + str(packer1.unpack(data)))
    #print("A tms errort ad vissza")

with open(sys.argv[2], 'rb') as f2:
    f2.seek(packer2.size)
    data2 = f2.read(packer2.size)
    print(packer2.unpack(data2))
    #print("A tms errort ad vissza")

with open(sys.argv[3], 'rb') as f3:
    f3.seek(packer3.size)
    data3 = f3.read(packer3.size)
    print(packer3.unpack(data3))
    #print("A tms errort ad vissza")

with open(sys.argv[4], 'rb') as f4:
    f4.seek(packer4.size)
    data4 = f4.read(packer4.size)
    print(packer4.unpack(data4))
    #print("A tms errort ad vissza")


def convertToInt(s):
    try:
        toFloat = float(s)
        toInt = int(toFloat)
    except (TypeError, ValueError):
        return False
    else:
        return toFloat == toInt


def convertToFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def makeStruct(inp):
    structString = ''
    inp = inp.split(",")
    for dat in inp:
        dat = dat.strip(" ")
        if dat[0] == '"':
            dat = dat[len(dat) - 4:]
            dat = dat.strip("()")
            structString += str(dat) + 's'
        elif dat[0] == "'":
            structString += 's'
        elif dat == "True" or dat == "False":
            structString += '?'
        elif convertToInt(dat):
            structString += "i"
        elif convertToFloat(dat):
            structString += 'f'

        structString += ' '
    #print(structString)
    return structString[:-1]


def removeStringLegth(inp):
    list = []
    inp = inp.split(",")
    for dat in inp:
        dat = dat.strip(" ")
        # print(data)
        if dat[0] == '"':
            dat = dat[:len(dat) - 4]
            dat = dat.strip('"')
            # print(data)
            list.append(dat.encode())
        elif dat[0] == "'":
            dat = dat[1:-1]
            list.append(dat.encode())
        elif dat == "True" or dat == "False":
            dat = bool(dat)
            list.append(dat)
        elif convertToInt(dat):
            list.append(int(dat))
        elif convertToFloat(dat):
            list.append(float(dat))

    return list


values = removeStringLegth('\"elso\"(13), 53, True')
packerStruct = struct.Struct(makeStruct('"elso"(13), 53, True'))
packed_data = packerStruct.pack(*values)
print(packed_data)

values2 = removeStringLegth("56.5, False, 'X'")
packerStruct2 = struct.Struct(makeStruct("56.5, False, 'X'"))
packed_data2 = packerStruct2.pack(*values2)
print(packed_data2)

values3 = removeStringLegth("44, \"masodik\"(11), 63.9")
packerStruct3 = struct.Struct(makeStruct("44, \"masodik\"(11), 63.9"))
packed_data3 = packerStruct3.pack(*values3)
print(packed_data3)

values4 = removeStringLegth("'Z', 75, \"harmadik\"(14)")
packerStruct4 = struct.Struct(makeStruct("'Z', 75, \"harmadik\"(14)"))
packed_data4 = packerStruct4.pack(*values4)
print(packed_data4)
