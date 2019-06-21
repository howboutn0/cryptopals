
#!/usr/bin/python3

string = "YELLOW SUBMARINE"

def pad(string, blocklength):
    n = (blocklength - (len(string) % blocklength)) % blocklength
    print(string + n*chr(n))
    print(repr(string + n*chr(n)))
    return string + n*chr(n)

#(pad(string, 20))
#(pad(string, 10))
#(pad(string, 15))

print(len(pad(string, 20)))
