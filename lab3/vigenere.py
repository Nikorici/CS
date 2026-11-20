ALPHABET = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"
CEDILLA = str.maketrans("ŞŢşţ", "ȘȚșț")
MIN_KEY = 7


def clean(text, alphabet=ALPHABET):
    text = "".join(text.translate(CEDILLA).split()).upper()
    bad = sorted({c for c in text if c not in alphabet})
    if bad:
        raise ValueError(
            f"Caractere nepermise: {' '.join(bad)}. Sunt permise doar literele alfabetului român: "
            f"A-Z, a-z și Ă Â Î Ș Ț, ă â î ș ț."
        )
    return text


def shift(text, key, sign, alphabet):
    n = len(alphabet)
    return "".join(
        alphabet[(alphabet.index(c) + sign * alphabet.index(key[i % len(key)])) % n]
        for i, c in enumerate(text)
    )


def encrypt(message, key, alphabet=ALPHABET):
    return shift(clean(message, alphabet), clean(key, alphabet), 1, alphabet)


def decrypt(cryptogram, key, alphabet=ALPHABET):
    return shift(clean(cryptogram, alphabet), clean(key, alphabet), -1, alphabet)


def ask(prompt, check):
    while True:
        value = input(prompt)
        try:
            return check(value)
        except ValueError as error:
            print(error)


def check_key(value):
    key = clean(value)
    if len(key) < MIN_KEY:
        raise ValueError(f"Cheia are {len(key)} litere. Lungimea cheii trebuie să fie de cel puțin {MIN_KEY} litere.")
    return key


def check_text(value):
    text = clean(value)
    if not text:
        raise ValueError("Textul nu poate fi gol.")
    return text


def main():
    print("Cifrul Vigenère pentru alfabetul român (31 de litere, codificate 0..30)")
    while True:
        choice = input("\n1 - criptare, 2 - decriptare, 0 - ieșire: ").strip()
        if choice == "0":
            break
        if choice not in ("1", "2"):
            print("Alegeți 1, 2 sau 0.")
            continue
        key = ask("Cheia: ", check_key)
        if choice == "1":
            message = ask("Mesajul: ", check_text)
            print("Mesajul pregătit:", message)
            print("Criptograma:     ", encrypt(message, key))
        else:
            cryptogram = ask("Criptograma: ", check_text)
            print("Mesajul decriptat:", decrypt(cryptogram, key))


if __name__ == "__main__":
    main()
