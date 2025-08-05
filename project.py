#RSA em pequena escala
#Usando num = alg

# encrypter, p, q, decrypter, n,  message

def findPrimeDivisors(n):
    primeDivisors = []
    for i in range(2, n+1):
        totalDiv = 0
        if n%i == 0:
            for j in range(2, i):
                if i%j == 0:
                    totalDiv +=1        
            totalDiv +=2 #para não rodar desnecessariamente no 1 e no numero(ja sabemos que é divisível)
            if totalDiv == 2:
                primeDivisors.append(i)

    return primeDivisors

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

def phi(n):
    results = calcP_Q(n)
    
    p = results[0][0]
    q = results[0][1]

    phiResult = (p-1)*(q-1)

    return phiResult

def calc_e(n, phi_n):
    numeros = [i for i in range(2, n+1)]

    divisors_n = findPrimeDivisors(n)
    divisors_phi_n = findPrimeDivisors(phi_n)

    divisors_prob = divisors_phi_n + divisors_n

    for i in divisors_prob:
        if i in numeros:
            numeros.remove(i)

    listaRem = []
    for i in numeros:
        divisors_i = findPrimeDivisors(i)

        if len(divisors_i) == 1:
            if divisors_i[0] in divisors_prob:
                listaRem.append(i)
        else:
            print(divisors_i)
            for j in range(len(divisors_i)):
                if divisors_i[j] in divisors_prob:
                    if i not in listaRem:
                        listaRem.append(i)
                        break
        if i < 1 or i > phi_n:
            if i not in listaRem:
                listaRem.append(i)
    for i in listaRem:
        numeros.remove(i)

    return numeros

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

msg = int(input("MSG: "))

n = int(input("N = "))
results = calcP_Q(n)

phi_n = phi(n)

e = calc_e(n, phi_n)

for el in e:
    enc = encrypt(el, n, msg)
    d = calc_d(el, phi_n)
    

    dec = decrypt(d, n, enc)

    print(f"|e| \t |d| \t |msg| \t |enc| \t |dec|")
    print(f"|{el}| \t |{d}| \t |{msg}| \t |{enc}| \t |{dec}|")
    print('\n')
