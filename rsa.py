import math
import random
#choosing p and q atleast 10^200 big
hexalphabet = "0123456789ABCDEF"
alphabet = "abcdefghijklmnopqrstuvwxyz" #for p and q
alphabet2 = ".,?! \t\n\rabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"# encrpt decrypt

key1 = "once the lord of light banished dark and all that stemmed from humanity and men assumed a fleeting form these are the roots of our world men are props on the stage of life and no matter how tender how exquisite a lie will remain a lie"
key2 = "the dragons shall never be forgotten we knights fought valiantly but for every one of them we lost three score of our own exhiliration pride hatred rage the dragons teased out our dearest emotions thou will understand one day at thy twilight old thoughts return in great waves of nostalgia"
#from base 10 in the book section ch4.2 algorithm 1. example 6
def tobase10(alphabet, s): #string to number
	value = 0
	for c in s:
		if (c in alphabet):
			pos = alphabet.find(c)
			value *= len(alphabet)
			value += pos
	return value
	#if(value <= 10**200):
		#print("the value was below 10**200, try again")
		#return None
	#else:
		#value = value % 10**200
		#value = ToOddToPrime(value)
		#print(value)
		#return value

def frombase10(alphabet, num):
	z = []
	k = 0
	temp = ""
	while num != 0:
		z.append(num % len(alphabet))
		#print(z[k])
		num = num//len(alphabet)
		k += 1

	while k != 0:
		temp += alphabet[z[k-1]]
		k -= 1
	#print (temp)
	return temp


def ToOddToPrime(value):
	while(value % 2 == 0):
		value += 1
	#print("value turned odd")
	while(isPrime(value) == False):
		value += 2
	#print("value turned prime")
	return value

def GCD(a,b):
	if (b > a):
		return GCD(b,a)
	if (a % b == 0):
		return b
	return GCD(b, a%b)

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def generateKeys(Sp, Sq):
	p = tobase10(alphabet, Sp)
	q = tobase10(alphabet, Sq)
	#print("this is P before 10^200 ", p)
	if(p <= 10**200):
	 	print("the value was below 10**200, try again")
	 	return None
	else:
	 	p = p % 10**200
	 	p = ToOddToPrime(p)
	 	#print("this is P after 10^200 ", p)
	if(q <= 10**200):
	 	print("the value was below 10**200, try again")
	 	return None
	else:
	 	q = q % 10**200
	 	q = ToOddToPrime(q)
	 	#print("this is P after 10^200 ", p)
	n = p*q
	r = (p-1)*(q-1)
	e = 10**398 + 1
	while (GCD(r, e) != 1):
		e += 2
	d = modinv(e, r)
	#print("Public: \n", n, "\n", e, "\n")
	#save to a file Public.txt
	f = open("public.txt", "w")
	f.write(str(n))
	f.write("\n")
	f.write(str(e))
	f.close()

	#print("Private: \n", n, "\n", d, "\n")
	#save to a file Private.txt
	f = open("private.txt", "w")
	f.write(str(n))
	f.write("\n")
	f.write(str(d))
	f.close()
	#print("d*e%r is",d*e%r)

def Encrypt(inputFile, outputFile):
	fin = open(inputFile,"rb")
	PlainTextBinary = fin.read()
	PlainText = PlainTextBinary.decode("utf-8")
	fin.close()

	n = 0
	e = 0
	fin = open("public.txt","rb")
	publicTextBinary = fin.readlines()
	fin.close()
	for x in range(len(publicTextBinary)):
		temp = publicTextBinary[x].decode("utf-8")
		temp.strip("\n")
		if(x == 0):
			n = int(temp)
		else:
			e = int(temp)

	#print(n)
	#print(e)
	f = open(outputFile, "wb")
	#Convert the resulting integers back to the base 70 alphabet,(from base 10)
	blocks = (len(PlainText) - 1)/ 216 + 1 
	blocks = int(blocks)
	subBlocks = [] #Treat the input file text as a base 70 integer, 216cha

	start = 0
	end = 215
	incrament = 215
	#print("PlainText: \n",PlainText)
	#print(blocks)
	for i in range(blocks): 								# i = 0-3 #for each block 
		#print("start:", start)
		#print("end", end)
		#print(PlainText[630:850])
		subBlocks.append(PlainText[start:end])
		#print(len(subBlocks))
		#print(subBlocks[i], "\n") 				#grab the 216cha
		M = tobase10(alphabet2, subBlocks[i])
		#print(M)
		if(M > n):								#make sure the value is less than n
			print("error the sub block was greater than N")
			return None
		E = pow(M,e,n) 					#Encode each block using the rules of RSA. m^e%n
		#print(E)
		Etext = frombase10(alphabet2, E)#Convert the resulting integers back to the base 70 alphabet,(from base 10)
		Etext += "$"
		#print(Etext)
		temp = Etext.encode("utf-8")
		f.write(temp)
		start += incrament
		end += incrament
		#print(subBlocks[i], "\n")

		#print(subBlocks[j])
	f.close()

	#and write to the output file.  Put a $ after each block to indicate where each block ends. 
	#Note that the output file should also be opened in binary mode, so to write text to it, 
	#the text must first be converted to binary as follows:
	#fout.write( stringMessage.encode("utf-8") )

def Decrypt(inputFile, outputFile):
	fin = open(inputFile,"rb")
	PlainTextBinary = fin.read()
	PlainText = PlainTextBinary.decode("utf-8")
	fin.close()
	subBlocks = PlainText.split("$")
	#print(subBlocks)

	n = 0
	d = 0
	fin = open("private.txt","rb")
	privateTextBinary = fin.readlines()
	fin.close()
	for x in range(len(privateTextBinary)):
		temp = privateTextBinary[x].decode("utf-8")
		temp.strip("\n")
		if(x == 0):
			n = int(temp)
			#print (n)
		else:
			d = int(temp)
			#print(d)

	f = open(outputFile, "wb")
	for i in range(len(subBlocks)):
		#print("---------------------------\n")
		#print(subBlocks[i])
		E = tobase10(alphabet2, subBlocks[i])
		#print (E)
		D = pow(E,d,n)
		#print(D)
		M = frombase10(alphabet2, D)
		#print(M)
		temp = M.encode("utf-8")
		f.write(temp)
	f.close()
		#print(subBlocks[i])
	#Use the same alphabet as above.

	#Treat the input file text as a base 70 integer, 
	#and convert it to base 10, using block sizes as indicated by the $ signs.

	#Decode each block using the rules of RSA.  (Read n and d from private.txt)

	#Convert the resulting integers back to the base 70 alphabet, 
	#and write to the output file, again converting to binary mode as explained above.

def MillersTest(N):
	b = random.randrange(2, N)
	T = N - 1
	s = 0
	for i in range(N):
		if(T % 2 == 0):
			s += 1
			T = T//2
		else:
			break

	if (pow(b,T,N) == 1):
		return True

	for j in range(0,s):
		power = (2**j)*T
		if (pow(b,power,N) == N - 1):
			return True # 3/4 chance prime

	return False # for sure composite



def isPrime(N):
	for i in range(20):
		ok = MillersTest(N)
		if(ok == False):
			return False #composite
		
	return True #almost surely Prime

def main():
	generateKeys(key1, key2)
	#Make a plain text file consisting of only letters in the alphabet.
	#It should be long enough to require multiple encoding blocks.
	
	#Encrypt("plaintext.txt","en_output.txt")#Call your Encrypt method.

	Decrypt("BlakeEncrypted.txt", "de_output.txt")#Call your Decrypt method.

	#Verify that the decoded output file exactly matches the original plain text file.
	fin = open("plaintext.txt","rb")
	PlainTextBinary = fin.read()
	PlainText = PlainTextBinary.decode("utf-8")
	fin.close()

	fin = open("de_output.txt","rb")
	PlainTextBinary = fin.read()
	endText = PlainTextBinary.decode("utf-8")
	fin.close()

	if(PlainText == endText):
		print("The files matche, congradulations")
	else:
		print("FAIL")
		print("this is plain text \n", PlainText)
		print("this is endText \n", endText)

main()