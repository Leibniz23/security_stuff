from sage.all import *

class Prover():
    def __init__(self, public, private):
        self.public = public
        self.private = private
        self.k = None
        self.r = None
        
    def firstStep(self):
        group, g, q, y = self.public
        k = randint(1, q-1)
        self.k = k
        I = g*k
        return I
    
    def finalStep(self):
        group, g, q, y = self.public
        s = ((self.r*self.private) + self.k) % q
        return s
    
    def setR(self, r):
        self.r = r
    
class Verifier():
    def __init__(self, public):
        self.public = public
        self.s = None
        self.r = None
        self.I = None
        
    def challenge(self):
        group, g, q, y = self.public
        r = randint(1, q-1)
        self.r = r
        return r
    
    def finalCheck(self, s):
        group, g, q, y = self.public
        aux1 = g*s
        aux2 = y*(-self.r)
        result = aux1+aux2
        if result == self.I:
            return True
        else:
            return False
    
    def setI(self, I):
        self.I = I
    

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
    # Gerando chaves
    public, private = genKeys()
    
    # Criando o prover e verifier
    prover = Prover(public, private)
    verifier = Verifier(public)
    
    # Protocolo de Schnorr
    I = prover.firstStep()
    verifier.setI(I)
    
    r = verifier.challenge()
    prover.setR(r)

    s = prover.finalStep()
    response = verifier.finalCheck(s)
    
    if response:
        print("Everything OK")
    else:
        print("Not accepted, try again")
        
main()