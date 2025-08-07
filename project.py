#RSA em pequena escala

# encrypter, p, q, decrypter, n,  message

# Encontra divisores primos de um número n
def findPrimeDivisors(n):
    primeDivisors = []
    for i in range(2, n+1):
        totalDiv = 0
        if n%i == 0:
            #verifica se o numero é primo
            for j in range(2, int(i**0.5)+1):
                #para testar um número primo, precisamos apenas checar até a raiz quadrada do número
                if i%j == 0:
                    totalDiv +=1        
            totalDiv +=2 #para não rodar desnecessariamente no 1 e no numero(ja sabemos que é divisível)
            if totalDiv == 2:
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

#Loop para enviar ou receber mensagens
# Variáveis: e, d, n
#variaveis publicas: e, n

#enviar

def enviarMSG():
    msg = int(input("MSG: "))
    n = int(input("N = "))
    e = calc_e(n, phi(n))
    print(f"Possíveis valores de e: {e}")
    el = int(input("E = e[?]: "))
    enc = encrypt(e[el], n, msg)
    print(f"Mensagem encriptada: {enc}")
    return enc, n

#receber: usar mensagem recebida, encriptador e n para desencriptar
def receberMSG():
    msg = int(input("MSG encriptada: "))
    n = int(input("N = "))
    e = calc_e(n, phi(n))
    print(f"Possíveis valores de e: {e}")
    el = int(input("E = e[?]: "))
    d = calc_d(e[el], phi(n))
    dec = decrypt(d, n, msg)
    print(f"Mensagem desencriptada: {dec}")



enviarMSG()
receberMSG()

# results = calcP_Q(n)

# phi_n = phi(n)

# e = calc_e(n, phi_n)

# for el in e:
#     enc = encrypt(el, n, msg)
#     d = calc_d(el, phi_n)
    

#     dec = decrypt(d, n, enc)

#     print(f"|e| \t |d| \t |msg| \t |enc| \t |dec|")
#     print(f"|{el}| \t |{d}| \t |{msg}| \t |{enc}| \t |{dec}|")
#     print('\n')
