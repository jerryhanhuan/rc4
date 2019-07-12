# rc4
rc4 算法的实现，使用 C、Python、Go 实现
### RC4 特点

* 流密码
* key 的长度[1,256]
* 加密数据长度没什么限制


### 基本步骤

1. 利用Key生成S盒——The key-scheduling algorithm (KSA)
2. 利用S盒生成密钥流——The pseudo-random generation algorithm(PRGA)
3. 密文=密钥流 xor 明文，那么 明文 = 密钥流 xor 密文,明文和密文的长度是一样的

```
key-scheduling algorithm (KSA)

for i from 0 to 255
    S[i] := i
endfor
j := 0
for i from 0 to 255
    j := (j + S[i] + key[i mod keylength]) mod 256
    swap values of S[i] and S[j]
endfor


Pseudo-random generation algorithm (PRGA)

i := 0
j := 0
while GeneratingOutput:
    i := (i + 1) mod 256
    j := (j + S[i]) mod 256
    swap values of S[i] and S[j]
    K := S[(S[i] + S[j]) mod 256]
    output K
endwhile

encrypt_data = data xor K

```
