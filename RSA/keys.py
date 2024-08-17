import random

MODULUS_A = 2**512
MODULUS_B = 2**514
SECURITY = 5 # Security parameter of Miller–Rabin primality test 

def trunc(a:float)-> int:
    b = str(a).split('.')
    return int(b[0])

def fast_exp(integer:int, exp:int, modulus:int):
    num = bin(exp)
    m = len(num) - 2
    result = integer % modulus
    for i in range(3, m): # the binary representation starts with '0b', and the first bit is always 1
        bit = num[i]
        result = (result * result) % modulus
        if bit == '1':
            result = (result * result) % modulus
            
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
    
  
def choose_prime(a, b):
    find = False
    while not find:
        p = random.randint(a, b) | 1 # the bitwise-or guarantees thats a odd number
        if isPrime(p):
            find = True
        
    return p

def Ext_euclidian_alg(a,b)-> tuple:
    pass
    # Extended Euclidean algorithm
    # result = [1, 0, 0]
	# if b==0:
    #     result = [a, 1, 0]
    #     return result

	# }
	# Triplet smallAns = gcdExtendedEuclid(b,a%b);
	# // Algoritmo de Euclides estendido

	# Triplet myAns;
	# myAns.gcd = smallAns.gcd;
	# myAns.x  = smallAns.y;
	# myAns.y = (smallAns.x - ((a/b)*(smallAns.y)));
	# return myAns

def gdc(a,b)->int:
    pass

    
def choose_keys(phi, modulus):
    while True:
        e = random.randint(3, phi-1)
        if gdc(e, phi) == 1:
            break
        
    s, t = Ext_euclidian_alg(phi, e) # s is not used
    d = t % phi
    
    return e, d

def main():
    p = choose_prime(MODULUS_A, MODULUS_B)
    q = choose_prime(MODULUS_A, MODULUS_B)
    n = p*q
    phi = (p-1)*(q-1)
    e, d = choose_keys(phi, n)
    # encontrar d tq. d*e = 1 mod (phi)  (Usando Algoritmo euclidiano estendido)
    
main()
