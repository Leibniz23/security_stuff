import random
import math

MODULUS_A = 2**16
MODULUS_B = 2**18
SECURITY = 10 # Security parameter of Miller–Rabin primality test
A_TEST = 100
B_TEST = 100000

def fast_exp(integer:int, exp:int, modulus:int)-> int:
    """ Calculates (integer^exp) % modulus in linear time with the bit-lenght of exp"""

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
    """ Return True if p is likely prime, False otherwise"""
    
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
    
  
def choose_prime(a:int, b:int, exception=0)-> int:
    """ Choose a (probably) prime p in range [a,b], and p != exception """
    find = False
    while not find:
        p = random.randint(a, b) | 1 # the bitwise-or guarantees that p is a odd number
        if isPrime(p) and p != exception:
            find = True
        
    return p

def gdc_inv(r0:int, r1:int)-> tuple:
    """ Calculates the greatest divisor commun (gdc) between r0 and r1
    Return the gdc and the modular inverse of r1"""
    
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
        
def slow_isprime(n):
  for i in range(2,int(math.sqrt(n))+1):
    if n % i == 0:
      return False
  
  return True

def choose_keys(p:int, q:int)-> int:
    """ Takes 2 primes p and q and returns a pair of public and private keys associated with them """
    phi = (p-1)*(q-1)
    used = {1}
    while True:
        e = random.randint(3, phi-1)
        if e in used:
            continue
        used.add(e)
        divisor, inv_e = gdc_inv(phi, e)
        if divisor == 1:
            break

    d = inv_e % phi
    
    return e, d

def encrypt(plaintext:int, key:int, n:int)-> int:
    try:
        assert(plaintext < n)
    except AssertionError:
        print("--------------------")
        print("Invalid message")
        print("--------------------")
        return
    
    return fast_exp(plaintext, key, n)

def decrypt(ciphertext:int, key:int, n:int)-> str:
    return fast_exp(ciphertext, key, n)

def test_fast_exp(n = 0, z = 10)-> None:
    i = 0
    while i < z:
        a = random.randint(A_TEST, B_TEST)
        b = random.randint(A_TEST, B_TEST)
        if n == 0:
            n = a 
        result = fast_exp(a, b, n)
        expected = pow(a, b, n)
        try:
            assert(result==expected)
        except AssertionError:
            print("fast_exp is not working")
        i+= 1
        
    print("fast_exp OK")
    
def test_prime(z = 50):
    for _ in range(z):
        p = choose_prime(A_TEST, B_TEST)
        try:
            assert(slow_isprime(p))
        except AssertionError:
            print("choose_prime is not working")
            return
            
    print("choose_prime OK")
    
def test_gdc_inv(z = 1000):
    for _ in range(z):
        p = choose_prime(MODULUS_A, MODULUS_B)
        q = choose_prime(MODULUS_A, MODULUS_B, p)
        e, d = choose_keys(p, q)
        phi = (p-1)*(q-1)
        divisor, inv = gdc_inv(phi, e)
        try:
            assert(divisor == 1)
            assert((e*inv) % phi) == 1
        except AssertionError:
            print("gdc_inv is not working")
            return
        
    print("gdc_inv OK")
        
    
def final_test(z = 100)-> None:
    for _ in range(SECURITY):
        p = choose_prime(MODULUS_A, MODULUS_B)
        q = choose_prime(MODULUS_A, MODULUS_B, p)
        modulus = p*q
        public, private = choose_keys(p, q)
        for _ in range(z):
            message = random.randint(0, modulus-1)
            assert decrypt(encrypt(message, public, modulus), private, modulus) == message
    
    return

def main():
    print("Welcome to RSA Manager Keys")
    while True:
        print("1 - Keys generator")
        print("2 - Function's test")
        print("0 - Exit")
        print("--------------------")
        print("What service do you need?")
        code = int(input())
        if code == 1:
            print("RSA-KEYS GENERATOR\n")
            print("Working...")
            p = choose_prime(MODULUS_A, MODULUS_B)
            q = choose_prime(MODULUS_A, MODULUS_B, p)
            n = p*q
            print("The RSA modulus is: "+ str(n))
            e, d = choose_keys(p, q)
            print("Your public-key is:")
            print(str(e)+"\n")
            print("Your private-key is:")
            print(str(d)+"\n")
            print("Enjoy!\n")
            continue
        
        if code == 2:
            print("--------------------")
            test_fast_exp()
            test_prime()
            test_gdc_inv()
            final_test()
            print("Everything OK!")
            print("--------------------")
            
        if code == 0:
            print("Goodbye!")
            break
    
main()
