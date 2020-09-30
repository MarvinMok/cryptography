import random
import math
import itertools
import operator
# Caesar Cipher
# Arguments: string, integer
# Returns: string
def encrypt_caesar(plaintext, offset):
    '''encrypted= ""
    for i in range (0, len(plaintext)):
        oldChar = plaintext[i]
        if(oldChar.isupper()):
            newChar = chr((ord(oldChar) + offset - 65) % 26 + 65)
        elif(oldChar.islower()):
            newChar = chr((ord(oldChar) + offset - 97) % 26 + 97)
        else:
            newChar = oldChar
       
        encrypted += newChar
    return encrypted'''
    return "".join([chr((ord(char) + offset - 65) % 26 + 65) if char.isupper() else char for char in plaintext])

# Arguments: string, integer
# Returns: string
def decrypt_caesar(ciphertext, offset):
    '''decrypted = ""
    for i in range (0, len(ciphertext)):
        oldChar = ciphertext[i]
        if(oldChar.isupper()):
            newChar = chr((ord(oldChar) - offset - 65) % 26 + 65)
        elif(oldChar.islower()):
            newChar = chr((ord(oldChar) - offset - 97) % 26 + 97)
        else:
            newChar = oldChar  
        decrypted += newChar
    return decrypted'''
    return "".join([chr((ord(char) - offset - 65) % 26 + 65) if char.isupper() else char for char in ciphertext])

# Vigenere Cipher
# Arguments: string, string
# Returns: string
def encrypt_vigenere(plaintext, keyword):
    '''encrypted= ""
    for i in range (0, len(plaintext)):
        oldChar = plaintext[i]
        offset = ord(keyword[i % len(keyword)]) - 65
        if(oldChar.isupper()):
            newChar = chr((ord(oldChar) + offset - 65) % 26 + 65)
        elif(oldChar.islower()):
            newChar = chr((ord(oldChar) + offset - 97) % 26 + 97)
        else:
            newChar = oldChar
       
        encrypted += newChar
    return encrypted'''
    return "".join([chr((ord(plaintext[i]) + ord(keyword[i % len(keyword)]) - 65 - 65) % 26 + 65) if plaintext[i].isupper() else plaintext[i] for i in range(0, len(plaintext)) ])

# Arguments: string, string
# Returns: string
def decrypt_vigenere(ciphertext, keyword):
    '''decrypted = ""
    for i in range (0, len(ciphertext)):
        oldChar = ciphertext[i]
        offset = ord(keyword[i % len(keyword)]) - 65
        if(oldChar.isupper()):
            newChar = chr((ord(oldChar) - offset - 65) % 26 + 65)
        elif(oldChar.islower()):
            newChar = chr((ord(oldChar) - offset - 97) % 26 + 97)
        else:
            newChar = oldChar  
        decrypted += newChar
    return decrypted'''
    return "".join([chr((ord(ciphertext[i]) - ord(keyword[i % len(keyword)]) - 65 - 65) % 26 + 65) if ciphertext[i].isupper() else ciphertext[i] for i in range(0, len(ciphertext))])

# Merkle-Hellman Knapsack Cryptosystem
# Arguments: integer
# Returns: tuple (W, Q, R) - W a length-n tuple of integers, Q and R both integers
def generate_private_key(n=8):
   

    W_as_list = [random.randint(0, 100)]
    total = W_as_list[0]
    for i in range(1, n):
        W_as_list.append(random.randint(total + 1, 2 * total))
        total += W_as_list[i]
    W = tuple(W_as_list)
    Q = random.randint(total + 1, 2 * total)

    done = 0
    while(not done):
        R = random.randint(2, Q - 1)
        if (math.gcd(R, Q) == 1):
            done = 1

    return (W, Q, R)
    #return tuple ([tuple(itertools.accumulate(sorted(random.sample(range(0, 10000), n))))] + (lambda Q:[Q, (lambda temp: (lambda Rs: Rs[random.randint(0, len(Rs))])(list(itertools.dropwhile(lambda x: x == 0, sorted([temp[i] if math.gcd(temp[i], Q) == 1 else 0 for i in range(0, len(temp))])))) )(list(range(2, Q - 1)))])(random.randint(n*10000, n*11000)))

# Arguments: tuple (W, Q, R) - W a length-n tuple of integers, Q and R both integers
# Returns: tuple B - a length-n tuple of integers
def create_public_key(private_key):
  
    return tuple([ private_key[2] * private_key[0][i] % private_key[1] for i in range(0, len(private_key[0])) ])

# Arguments: string, tuple (W, Q, R)
# Returns: list of integers
def encrypt_mhkc(plaintext, public_key):

    return [sum([ (not (ord(plaintext[i]) & (1 << j)) == 0) * public_key[j] for j in range(0, len(public_key)) ]) for i in range(0, len(plaintext))]

# Arguments: list of integers, tupledef encrypt_mhkc(plaintext, public_key):
# B - a length-n tuple of integers
# Returns: bytearray or str of plaintext
def decrypt_mhkc(ciphertext, private_key):
    W = private_key[0]
    Q = private_key[1]
    R = private_key[2]
    S = find_s(R,Q)
    plaintext = ''
    for i in range(0, len(ciphertext)):
        C = ciphertext[i] * S % Q
        charAsInt = 0
        for j in range(0, len(W)):
            #print(C)
            if C >= W[7 - j]:
                C = C - W[7 - j]
                charAsInt = (1 <<  (7 - j)) | charAsInt
            #print(C)
              
        plaintext += chr(charAsInt)
    return plaintext
    
    #return "".join( (lambda S, temp: [chr((lambda C: sorted([i if temp[i] == C else 0 for i in range(0, 2 ** len(private_key[0]))]).pop())(ciphertext[i] * S % private_key[1])) for i in range(0, len(ciphertext))]) (sorted([S if private_key[2] * S % private_key[1] == 1 else 0 for S in range(2, private_key[1] - 1 )]).pop(), ( [sum([ (not (i & (1 << j)) == 0) * private_key[0][j] for j in range(0,len(private_key[0]))]) for i in range(0, 2 ** len(private_key[0]))])))

  



def find_s(R, Q):
    for S in range(2,Q - 1):
        if (R * S % Q == 1):
            return S

    return 0;
    #return sorted([S if R * S % Q == 1 else 0 for S in range(2, Q -1 )]).pop()

def main():
    # Testing code here
    print (encrypt_caesar("ZABC?", 1))

    print (decrypt_caesar("ABC?", 1))

    print (encrypt_vigenere("ATTACKATDAWN", "AB")) 

    print (decrypt_vigenere("AUTBCLAUDBWO", "AB")) 

    priv = generate_private_key()
   
    print("priv")
    print(priv)
    

    pub = create_public_key(priv)
    print("pub")
    print(pub)

    e = encrypt_mhkc("ATTACKATDAWN", pub)
    print ("e")
    print (e)
   
    d = decrypt_mhkc(e, priv)
    print("d")
    print (d)




if __name__ == "__main__":
    main()
