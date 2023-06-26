import string

alphabet = [' '] + list(string.ascii_lowercase)
print(alphabet)
positions = {}
for i in range(len(alphabet)):
    positions[alphabet[i]] = i

print(positions)

message = "hi my name is caesar"
def encoding(message, key):
    encoded_message = ""
    for letter in message:
            for letter2, index in positions.items():
                ciphered = positions[letter] + key
                if ciphered > 26:
                    ciphered -= 27
                elif ciphered < 0:
                    ciphered += 27
                if index == ciphered:
                    encoded_message += letter2
    return encoded_message

print(message)
encoded_message = encoding(message, 3)
print(encoded_message)

decoded_message = encoding(encoded_message, -3)
print(decoded_message)
print(encoding(message, 1))
