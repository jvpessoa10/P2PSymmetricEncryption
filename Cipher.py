import string

alphabet = string.printable
class Vignere:

    @staticmethod
    def encrypt(key, plaintext):
        ciphertext = ""
        for i, letter in enumerate(plaintext):
            offset = (alphabet.index(letter) + alphabet.index(key[i % len(key)]) + 1) % len(alphabet)
            ciphertext += alphabet[offset]
        return ciphertext

    @staticmethod
    def decrypt(key, cyphertext):
        plaintext = ""
        for i, letter in enumerate(cyphertext):
            offset = (alphabet.index(letter) - alphabet.index(key[i % len(key)]) - 1) % len(alphabet)
            plaintext += alphabet[offset]
        return plaintext


def main():
    plaintext = "teste"
    key = "chavesimetricadoservidor"
    cyphertext = Vignere.encrypt(key, plaintext)
    print(cyphertext)
    print(Vignere.decrypt(key, cyphertext))


if __name__ == "__main__":
    main()