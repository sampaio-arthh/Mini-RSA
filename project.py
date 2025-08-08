import tkinter as tk

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

### Funções do algoritmo RSA

# Encontra divisores primos de um número n
def findPrimeDivisors(n):
    primeDivisors = []
    
    # 2<={i}<=n
    # Verifica se o número i é divisor de n
    for i in range(2, n):
        totalDiv = 0
        
        if n%i == 0:
            # Se {i} divisor de n, então verifica se {i} é primo
            for j in range(2, int(i**0.5)+1):
                #para testar um número primo, precisamos apenas checar até a raiz quadrada do número
                if i%j == 0:
                    totalDiv += 1
                    break

            #Se {i} não tem divisores de 2 a n-1, então é primo pois já excluímos 1 e o próprio número
            if totalDiv == 0:
                primeDivisors.append(i)

    return primeDivisors

# Encontra p e q tais que n = p * q
def calcP_Q(n):
    primeDivisors = findPrimeDivisors(n)
    primePair = []
    for i in range(len(primeDivisors)):
        for j in range(i+1, len(primeDivisors)):
            if primeDivisors[i]*primeDivisors[j] == n:
                primePair.append((primeDivisors[i],primeDivisors[j]))
    if primePair == []:
        return "Número primo resultante de mais de dois termos"

    return primePair

# Calcula o valor de phi(n) = (p-1)(q-1)
def phi(n):
    results = calcP_Q(n)
    
    p = results[0][0]
    q = results[0][1]

    phiResult = (p-1)*(q-1)

    return phiResult

# Calcula os valores de e que são coprimos com phi(n) e n
# e deve ser menor que phi(n)
def calc_e(n, phi_n):
    numeros2aN = [i for i in range(2, n+1)]

    divisors_n = findPrimeDivisors(n)
    divisors_phi_n = findPrimeDivisors(phi_n)

    divisors_prob = divisors_phi_n + divisors_n

    #Usando o inverso da interseção
    divisors_prob = set(divisors_prob)
    numeros2aN = set(numeros2aN)

    numeros2aN.symmetric_difference_update(divisors_prob)

    #limpar listas desnecessárias, apagando da memória
    del divisors_n
    del divisors_phi_n

    listaRem = []

    # Verifica se os números restantes são coprimos com phi(n)
    for i in numeros2aN:
        divisors_i = findPrimeDivisors(i)

        if len(divisors_i) == 1:
            if divisors_i[0] in divisors_prob:
                listaRem.append(i)
        else:
            for j in range(len(divisors_i)):
                if divisors_i[j] in divisors_prob:
                    if i not in listaRem:
                        listaRem.append(i)
                        break
        if i < 1 or i > phi_n:
            if i not in listaRem:
                listaRem.append(i)
    
    numeros2aN.symmetric_difference_update(set(listaRem))

    return list(numeros2aN)

def encrypt(e, n, msg):
    enc = msg**e
    enc%=n
    return enc

def calc_d(e, phi_n):
    cont = 0
    i = 1
    while cont !=2:
        if i % e == 0 and i % phi_n == 1:
            cont+=1
            i+=1
        else:
            i+=1
    return int((i-1)/e)
        
def decrypt(d, n, enc):
    dec = enc**d
    dec %= n
    return dec
#######

### Funções extras
def letterToNumber(text):
    #para cada letra, verifica se é válida
    #for letter in text:
        #if letter.upper() not in LETTERS:
            #raise ValueError(f"Caractere inválido: {letter}. Apenas letras de A a Z são permitidas.")
    
    # Lista para armazenar os números correspondentes
    textRet = []
    # Converte cada letra para seu número
    for letter in text:
        textRet.append(LETTERS.index(letter.upper()) + 1)
    return textRet

def numberToLetter(text):
    #para 2 digitos, se <= 26, então é 1 letra
    if len(text) % 2 != 0:
        text = "0" + text  # Adiciona um zero à esquerda se o comprimento for ímpar
    text = [text[i:i+2] for i in range(0, len(text), 2)]
    # Converte cada par de números para letras
    text = [LETTERS[int(i)-1] for i in text]
    return "".join(text)


#### Ciclo principal do programa

#Enviar: aplicar na mensagem e exibir mensagem encriptada
def enviarMSG():
    msg = input("MSG: ")
    n = int(input("N = "))
    e = calc_e(n, phi(n))
    print(f"Possíveis valores de e: {e}")
    el = int(input("{e} escolhido = e[?]: "))

    # Converter mensagem para lista de números
    msg = letterToNumber(msg)
    result = ""
    for i in range(len(msg)):
        enc = encrypt(e[el], n, msg[i])
        # Converter mensagem encriptada para letras
        enc = str(enc)
        enc = numberToLetter(enc)
        result+=enc    

    print(f"Mensagem encriptada: \"{result}\" | e:{e} | n:{n}")



#Receber: aplicar na mensagem encriptada e exibir mensagem desencriptada
def receberMSG():
    msg = int(input("MSG encriptada: "))
    n = int(input("N = "))
    e = calc_e(n, phi(n))
    print(f"Possíveis valores de e: {e}")
    el = int(input("E = e[?]: "))
    d = calc_d(e[el], phi(n))
    dec = decrypt(d, n, msg)
    print(f"Mensagem desencriptada: {dec}")


##GUI
#base
ROOT_L = 1000
ROOT_A = 800

root = tk.Tk()

#classe para padronizar a GUI e seus itens

class JanelaPrincipal:
    def __init__(self, root, name):
        self.tela = root
        self.tela.geometry(f"{ROOT_L}x{ROOT_A}")
        self.tela.title(name)

        self.labelEscolha = tk.Label(self.tela, text="Qual função deseja executar ?")
        self.labelEscolha.pack(pady=20)

        self.buttonEscolhaEnc = tk.Button(self.tela, command=JanelaEnc(root, "Tela Encriptar"))
        self.buttonEscolhaEnc.pack(padx=10)

        self.buttonEscolhaDec = tk.Button(self.tela, anchor="center", command=JanelaDec(root, "Tela Decriptar"))
        
        self.tela.mainloop()


class JanelaEnc:
    def __init__(self, root, name):
        self.tela = root
        self.tela.title(name)
        self.labelMensagem = tk.Label(self.tela)
        self.entryMensagem = tk.Entry(self.tela, width=80)

class JanelaDec:
    def __init__(self, root, name):
        self.tela = root
        self.tela.title(name)
        self.labelMensagem = tk.Label(self.tela)
        self.entryMensagem = tk.Entry(self.tela, width=80)

JanelaPrincipal(root, "RSA")