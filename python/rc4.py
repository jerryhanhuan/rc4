#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import codecs




def str2hex(s):
    b = codecs.decode(s,'hex_codec')
    return b

def hex2str(b):
    s = codecs.encode(b,'hex_codec')
    return s



MOD = 256

def KSA(key):
    '''
    Key Scheduling Algorithm (from wikipedia):
    for in from 0 to 255
        S[i] := i
    endfor
    j := 0
    for i from 0 to 255
        j := (j+S[i]+key[i mode keylength]) mod 256
        swap S[i] s[j]
    endfor
    '''
    keylen = len(key)
    # create the array S
    S = list(range(MOD))
    i = 0
    j = 0
    for i in range(MOD):
        j = (j+S[i]+key[i % keylen]) % MOD
        S[i],S[j] = S[j],S[i]
    return S

def PRGA(S):
    '''
    Psudo Random Generation Algorithm (from wikipedia):
    i := 0
    j := 0
    while GeneratingOutPut
        i := (i + 1)mod 256
        j := (j+S[i])mod 256
        swap S[i],S[j]
        K := S[(S[i]+S[j]) mod 256]
        output K
    endwhile
    '''
    i,j = 0,0
    while True:
        i = (i + 1)%MOD
        j = (j + S[i])%MOD
        S[i],S[j] = S[j],S[i]
        K = S[(S[i]+S[j])%MOD]
        yield K

def get_keystream(key):
    '''
    Takes the encryption key to get the keystream using PRGA
    return object is a generator
    '''
    S = KSA(key)
    return PRGA(S)

def encrypt(key,text):
    '''
    key is an array of  bytes
    text is an array of bytes
    '''
    keystream = get_keystream(key)
    res = []
    for c in text:
        val =( "%02X"% (c ^ next(keystream)))
        res.append(val)
    return codecs.decode(''.join(res),'hex_codec')


def str2hex(s):
    return codecs.decode(s,'hex_codec')

def hex2str(b):
    return codecs.encode(b,'hex-codec')



def main():
    while True:
        key = input('请输入密钥::')
        text = input('请输入待加密数据::')
        cipher_text = encrypt(str2hex(key),str2hex(text))
        print('cipher is:',hex2str(cipher_text))

        plain = encrypt(str2hex(key),cipher_text)
        print('plain is:',hex2str(plain))



if __name__ == '__main__':
    main()
