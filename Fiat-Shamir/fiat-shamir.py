from sage.all import *

class Prover():
    def __init__(self, public, private):
        self.public = public
        self.private = private
        
    def sign(self, message):
        # Gerando I
        group, g, q, y = self.public
        k = randint(1, q-1)
        I = g*k
        
        # Gerando r e s, a assinatura
        before_hash = str(I) + str(message)
        r = hash(before_hash)
        s = ((r*self.private) + k) % q
        
        return (r, s)
    
class Verifier():
    def __init__(self, public):
        self.public = public
        
    def verify(self, signature, message):
        r, s = signature
        group, g, q, y = self.public
        aux1 = g*s
        aux2 = y*(-r)
        new_I = aux1+aux2
        new_hash = str(new_I) + str(message)
        new_r = hash(new_hash)
        if r == new_r:
            return True
        else:
            return False

def genKeys():
    # Para fins didáticos, vou usar a curva elíptica Curve25519, que garante 128-bits de segurança
    
    # Definindo os parâmetros
    p = 2**255 - 19  # Primo gerador para essa curva
    field = GF(p)  # Corpo finito com o primo 2**255 - 19
    parameter = field(486662)  # Parâmetro da Curve25519
    
    # Definindo a curva
    group = EllipticCurve(field, [0, parameter, 0, 1, 0])  # Definição da Curve25519
    g = group.lift_x(field(9))  # x = 9 é a coordenada do gerador padrão da Curve25519
    q = int(g.order()) # Ordem do grupo (nesse caso, um número primo conhecido)
    
    # Gerando as chaves pública e privada
    x = randint(1, q - 1)  # Chave privada uniforme em Z_q
    y = g*x  # y = g^x da chave pública basta multiplicar, por ser uma curva elíptica
    
    return ((group, g, q, y), x)

def main():
    pk, sk = genKeys()
    message = "aaa"
    prover = Prover(pk, sk)
    verifier = Verifier(pk)
    
    # Inicio do protocolo
    signature = prover.sign(message)
    result = verifier.verify(signature, "message")
    if result:
        print("Accepted!")
    else:
        print("Not accepted...")
    
main()
