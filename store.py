#very simple syntax
# CREATE|filename
# OPEN|filename
# KEY|VALUE
# DELETE|KEY
# KEY
# CLOSE

import struct

open_file = ""
dictionary = {}

def encode(key, value) -> bytes:
    key = key.encode()
    value = value.encode()
    return struct.pack('>QQ', len(key), len(value)) + key + value

def append(key, value, filename):
    with open(filename, "ab") as f:
        f.write(encode(key, value))

def decode(filename):
    global open_file 
    open_file = filename
    store = {}
    print(filename)
    with open(filename, "rb") as f:
        while True:
            header = f.read(16)
            if len(header) < 16:
                break
            keylen, valuelen = struct.unpack('>QQ', header)
            key = f.read(keylen).decode()
            value = f.read(valuelen).decode()
            if value == "0x00000000":
                del store[key]
            else:
                store[key] = value
    return store


def parse(line):
    global open_file
    global dictionary
    line = line.split("|")
    if len(line) > 1:
        if line[0].lower().strip() == "open":
            dictionary = decode(line[1].strip())
        elif line[0].lower().strip() == "create":
            with open("./"+line[1], 'wb') as f:
                open_file = line[1]
                print("created database " +line[1])
        elif(open_file == ""):
            print("error: please open database")
        elif (line[0].lower().strip() == "delete"):
            if line[1] in dictionary:
                del dictionary[line[1]]
            append(line[0], "0x00000000", open_file)
        else:
            append(line[0], line[1], open_file)
            dictionary[line[0]] = line[1]
    else:
        if line[0].lower().strip() == "close":
            open_file = ""
            dictionary = {}
            print("database closed")
        else:
            if line[0] in dictionary:
                print(dictionary[line[0]])
            else:
                "key "+line[0]+ "not found"

def input_loop():
    user_input = input()
    parse(user_input)

print("welcome!!")
while True:
    input_loop()
