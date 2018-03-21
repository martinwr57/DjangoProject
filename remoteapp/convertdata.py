#!/usr/bin/env python

__version__ = '1.0'



def convertBufToChar(buf):
    returnbuf = ""
    for j in range(0, len(buf)):
        if ((buf[j] >= 0x20) and (buf[j] < 0x7F)):
            returnbuf += "%c" % buf[j]
        else:
            returnbuf += "."  # eliminate non-printable characters
    return returnbuf                    
        
def xtod(c):
    if(c>='0' and c<='9'):
        return c-'0'
    elif(c>='A' or c>='a') and (c<='F' or c<='f'):
        return c-'A' + 10
    elif(c>='a' and c<='f'):
        return c-'a' + 10
    else:
        return 0

def HexToDec(hex, int):
    if(hex == 0):
        return int
    return HexToDec(hex+1, int*16+xtod(hex))
    
def xstrtoi(hex):
    return HexToDec(hex, 0)

def strtohex(strnumb):
    revstring = strnumb[::-1]
    holdnumber = []
    countpower = 0
    hexnumber = 0
    for c in revstring:
        holdnumber.append(int(c)*16^countpower)
    for item in holdnumber:
        hexnumber += item
    return hexnumber

        
        