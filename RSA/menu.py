import random

MODULUS_A = 2**16
MODULUS_B = 2**18
SECURITY = 5 # Security parameter of Miller–Rabin primality test 

def fast_exp(integer:int, exp:int, modulus:int)-> int:
    num = bin(exp)
    m = len(num)
    result = integer
    for i in range(3, m): # the binary representation starts with '0b', and the first bit is always 1
        bit = num[i]
        result = (result * result) % modulus
        if bit == '1':
            result = (result * integer) % modulus
            
    return result

def isPrime(p:int)-> bool:
    # Factoring p - 1 = (2^u).r
    p_ = p-1
    u = 0
    while p_ % 2 == 0:
        u += 1
        p_ >>= 1
    r = p_
    
    # Miller–Rabin primality test
    for i in range(SECURITY):
        a = random.randint(2, p-2)
        z = fast_exp(a, r, p)
        if z != 1 and z != (p - 1):
            for j in range(u-1):
                z = (z**2) % p
                if z == 1:
                    return False
            if z != p-1:
                return False
    
    return True 
    
  
def choose_prime(a, b, exception):
    find = False
    while not find:
        p = random.randint(a, b) | 1 # the bitwise-or guarantees that p is a odd number
        if isPrime(p) and p != exception:
            find = True
        
    return p

def gdc(r0,r1)-> tuple:
    # Extended Euclidian Algorithm
    s0, t0 = 1, 0 
    s1, t1 = 0, 1
    i = 1

    while True:
        i += 1
        try:
            ri = r0 % r1  
        except ZeroDivisionError:
            return r0, t0  # s is not useful
        qi_1 = (r0 - ri) // r1  
        si = s0 - (qi_1 * s1)
        ti = t0 - (qi_1 * t1)

        if ri == 0:
            break
        
        # Updating variables
        r0, s0 = r1, s1
        r1, s1 = ri, si
        t0 = t1
        t1 = ti
    
    return r1, t1  # s is not useful
        
    
def choose_keys(phi):
    used = {1}
    while True:
        e = random.randint(3, phi-1)
        if e in used:
            continue
        used.add(e)
        divisor, inv_e = gdc(e, phi)
        if divisor == 1:
            break

    d = inv_e % phi
    
    return e, d

def encrypt(plaintext, key, n):
    cipher = ""
    for letter in plaintext:
        code = ord(letter)
        cipher += (str(fast_exp(code, key, n))+'.')
        
    return cipher

def decrypt(ciphertext, key, n):
    char = ciphertext.split(".")
    plain = ""
    i = 0
    while char[i] != "" and i < len(char):
        code = int(char[i])
        try:
            plain += chr(fast_exp(code, key, n))
        except ValueError:
            print("Something was wrong! Check out your keys and try again")
            return "\0"
        i += 1
            
    return plain

def main():
    print("Welcome to RSA Manager Keys")
    while True:
        print("1 - Keys generator")
        print("2 - Encryption")
        print("3 - Decryption")
        print("0 - Exit")
        print("--------------------")
        print("What service do you need?")
        code = int(input())
        if code == 1:
            print("RSA-KEYS GENERATOR\n")
            print("Working...")
            p = choose_prime(MODULUS_A, MODULUS_B, 0)
            q = choose_prime(MODULUS_A, MODULUS_B, p)
            n = p*q
            phi = (p-1)*(q-1)
            print("The RSA modulus is: "+ str(n))
            e, d = choose_keys(phi)
            print("Your public-key is:")
            print(str(e)+"\n")
            print("Your private-key is:")
            print(str(d)+"\n")
            print("Enjoy!\n")
            continue
        
        if code == 2:
            print("Insert the ciphertext to encryption:")
            plaintext = input()
            print("Insert your RSA public key:")
            key = int(input())
            print("Insert your RSA key modulus:")
            n = int(input())
            ciphertext = encrypt(plaintext, key, n)
            print("Your ciphertext is as follows:\n")
            print(ciphertext)
            continue
            
        if code == 3:
            print("Feature not developed... coming soon")
            # print("Insert the plaintext to decryption:")
            # ciphertext = input()
            # print("Insert your RSA private key:")
            # key = int(input())
            # print("Insert your RSA key modulus:")
            # n = int(input())
            # plaintext = decrypt(ciphertext, key, n)
            # if plaintext != "\0":
            #     print("Your plaintext is as follows:\n")
            #     print(plaintext)
            # continue
            
        if code == 0:
            lista = encrypt("plaintext", 3, 33)
            novo = decrypt(lista, 7, 33)
            print("Goodbye!")
            break
    
main()
