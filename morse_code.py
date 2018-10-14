# Dictionary representing the morse code chart 
# Blink: '.'; Brow_raise:'-'

morseAlphabet = {
	'A': '.-', 'B': '-...',
	'C': '-.-.', 'D': '-..', 'E': '.',
	'F': '..-.', 'G': '--.', 'H': '....',
	'I': '..', 'J': '.---', 'K': '-.-.',
	'L': '.-..', 'M':'--', 'N':'-.', 
	'O':'---', 'P':'.--.', 'Q':'--.-', 
    'R':'.-.', 'S':'...', 'T':'-', 
    'U':'..-', 'V':'...-', 'W':'.--', 
    'X':'-..-', 'Y':'-.--', 'Z':'--..', 
    '1':'.----', '2':'..---', '3':'...--', 
    '4':'....-', '5':'.....', '6':'-....', 
    '7':'--...', '8':'---..', '9':'----.', 
    '0':'-----', ', ':'--..--', '.':'.-.-.-', 
    '?':'..--..', '/':'-..-.', '-':'-....-', 
    '(':'-.--.', ')':'-.--.-',' ':'.-.-' ,'@':'..--'
}

inverseMorseAlphabet=dict((v,k) for (k,v) in morseAlphabet.items())

def decrypt(message): 
  
    # extra space added at the end to access the 
    # last morse code 
    if message == '':return ''
    message += ' '

    decipher = '' 
    citext = '' 
    for letter in message: 
  
        # checks for space 
        if (letter != ' '): 
  
            # counter to keep track of space 
            i = 0
  
            # storing morse code of a single character 
            citext += letter 
  
        # in case of space 
        else: 
            # if i = 1 that indicates a new character 
            i += 1
  
            # if i = 2 that indicates a new word 
            if i == 2 : 
  
                 # adding space to separate words 
                decipher += ' '
            else: 
  
                # accessing the keys using their values (reverse of encryption) 
                decipher += list(morseAlphabet.keys())[list(morseAlphabet 
                .values()).index(citext)] 
                citext = '' 
  
    return decipher 



