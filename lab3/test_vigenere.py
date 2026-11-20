from vigenere import ALPHABET, check_key, clean, decrypt, encrypt

LATIN = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

assert len(ALPHABET) == 31 and len(set(ALPHABET)) == 31
assert encrypt("Per aspera ad astra", "SUPER", LATIN) == "HYGEJHYGERVUHXIS"
assert decrypt("HYGEJHYGERVUHXIS", "SUPER", LATIN) == "PERASPERAADASTRA"

message = "Întâlnirea secretă are loc mâine la ora şapte lângă ţărmul lacului"
key = "criptografie"
assert clean(message) == "ÎNTÂLNIREASECRETĂARELOCMÂINELAORAȘAPTELÂNGĂȚĂRMULLACULUI"
assert decrypt(encrypt(message, key), key) == clean(message)
assert encrypt("Z", "Ă") == "A" and decrypt("A", "Ă") == "Z"

for bad in ("ora 7", "salut!", "café"):
    try:
        clean(bad)
        raise AssertionError(bad)
    except ValueError:
        pass
try:
    check_key("cheie")
    raise AssertionError("short key accepted")
except ValueError:
    pass

print("all tests passed")
