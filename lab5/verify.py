import random
import re
import sys
from math import gcd

GIVEN_P = int(open(__file__.rsplit("/", 1)[0] + "/given_p.txt" if "/" in __file__ else "given_p.txt").read())


def is_prime(n, rounds=40):
    if n < 2:
        return False
    for small in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % small == 0:
            return n == small
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for _ in range(rounds):
        x = pow(random.randrange(2, n - 1), d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def parse(path):
    values, key = {}, None
    for line in open(path, encoding="utf-8"):
        match = re.match(r"^([a-zA-Z][\w.()*, ]*?) = (.*)$", line.rstrip("\n"))
        if match:
            key = match.group(1)
            values[key] = match.group(2).strip()
        elif key and line.strip():
            values[key] += line.strip()
    return values


v = parse(sys.argv[1] if len(sys.argv) > 1 else "report/output.txt")
num = lambda key: int(re.sub(r"[^0-9]", "", v[key]))
checks = []
check = lambda name, ok: checks.append((name, bool(ok)))

msg = v["msg"]
m = num("m")
check("ASCII codes of the message", v["ascii"].replace(" ", "") == "{" + ",".join(str(b) for b in msg.encode()) + "}")
check("hex = ASCII bytes in hexadecimal", v["hex"].lower() == msg.encode().hex())
check("m = hex read as a number", m == int(v["hex"], 16))

p, q, n, phi, e, d, c = (num("rsa." + k) for k in ("p", "q", "n", "phi", "e", "d", "c"))
check("RSA: p and q are prime and different", is_prime(p) and is_prime(q) and p != q)
check("RSA: n = p*q has 2048 bits", n == p * q and n.bit_length() == 2048 == num("rsa.bits(n)"))
check("RSA: phi = (p-1)(q-1), gcd(e, phi) = 1", phi == (p - 1) * (q - 1) and gcd(e, phi) == 1)
check("RSA: e*d = 1 mod phi", e * d % phi == 1)
check("RSA: c = m^e mod n", c == pow(m, e, n))
check("RSA: c^d mod n = m, text matches", pow(c, d, n) == num("rsa.decrypted") == m and v["rsa.text"] == msg)

pp, g = num("p"), num("g")
check("p is the handout's 2048-bit safe prime, g = 2", pp == GIVEN_P and is_prime(pp) and is_prime((pp - 1) // 2) and g == 2)

x, beta, k, y1, y2 = (num("elgamal." + key) for key in ("x", "beta", "k", "y1", "y2"))
check("ElGamal: 1 < x < p-1, beta = g^x mod p", 1 < x < pp - 1 and beta == pow(g, x, pp))
check("ElGamal: y1 = g^k, y2 = m*beta^k mod p", y1 == pow(g, k, pp) and y2 == m * pow(beta, k, pp) % pp)
check("ElGamal: y2 * y1^(p-1-x) mod p = m, text matches",
      y2 * pow(y1, pp - 1 - x, pp) % pp == num("elgamal.decrypted") == m and v["elgamal.text"] == msg)

a, b, ka, kb = num("dh.a"), num("dh.b"), num("dh.keyAlice"), num("dh.keyBob")
check("DH: 1 < a, b < p-1, A = g^a, B = g^b mod p",
      1 < a < pp - 1 and 1 < b < pp - 1 and num("dh.A") == pow(g, a, pp) and num("dh.B") == pow(g, b, pp))
check("DH: B^a = A^b mod p (same shared key)", ka == pow(num("dh.B"), a, pp) == pow(num("dh.A"), b, pp) == kb and v["dh.equal"] == "True")
aes = ka >> (2048 - 256)
check("AES-256 key = top 256 bits of the shared key",
      num("aes.key") == aes and v["aes.hex"].lower() == format(aes, "064x") and v["aes.binary"] == format(aes, "0256b"))

for name, ok in checks:
    print(("OK    " if ok else "FAIL  ") + name)
print(f"{sum(ok for _, ok in checks)}/{len(checks)} checks passed")
if not all(ok for _, ok in checks):
    sys.exit(1)
if len(sys.argv) > 2:
    with open(sys.argv[2], "w", encoding="utf-8") as out:
        for key, value in v.items():
            compact = re.sub(r"\s", "", value)
            out.write(f"{key} = {compact if compact.isdigit() else value}\n")
