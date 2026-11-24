import secrets

SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32,
]


def parse_kplus(text):
    bits = "".join(text.split())
    if len(bits) == 56 and set(bits) <= {"0", "1"}:
        return bits
    if len(bits) == 14 and all(c in "0123456789abcdefABCDEF" for c in bits):
        return format(int(bits, 16), "056b")
    raise ValueError("K+ trebuie să aibă 56 de biți: 56 de cifre 0/1 sau 14 cifre hexazecimale (0-9, A-F).")


def round_keys(kplus):
    c, d = kplus[:28], kplus[28:]
    rounds = []
    for shift in SHIFTS:
        c, d = c[shift:] + c[:shift], d[shift:] + d[:shift]
        rounds.append((shift, c, d, "".join((c + d)[p - 1] for p in PC2)))
    return rounds


def groups(bits, size):
    return " ".join(bits[i:i + size] for i in range(0, len(bits), size))


def show_tables():
    print("Tabelul deplasărilor la stânga (runda: nr. de deplasări)")
    print("  Runda:       " + " ".join(f"{i:2}" for i in range(1, 17)))
    print("  Deplasări:   " + " ".join(f"{s:2}" for s in SHIFTS))
    print("\nTabelul PC-2 (bitul j al lui Ki = bitul PC-2[j] al lui CiDi)")
    for row in range(8):
        print("  " + " ".join(f"{p:2}" for p in PC2[row * 6:row * 6 + 6]))


def show_schedule(kplus):
    print(f"\nK+ = {groups(kplus, 7)}")
    print(f"C0 = {groups(kplus[:28], 7)}")
    print(f"D0 = {groups(kplus[28:], 7)}")
    for i, (shift, c, d, k) in enumerate(round_keys(kplus), 1):
        print(f"\nRunda {i}: C{i-1} și D{i-1} se deplasează ciclic la stânga cu {shift} {'poziție' if shift == 1 else 'poziții'}")
        print(f"  C{i} = {groups(c, 7)}")
        print(f"  D{i} = {groups(d, 7)}")
        print(f"  C{i}D{i} = {groups(c + d, 7)}")
        if i == 1:
            print("  PC-2 aplicat pe C1D1, rând cu rând (poziție -> bit):")
            for row in range(8):
                cells = PC2[row * 6:row * 6 + 6]
                print("    " + "  ".join(f"{p:2}->{(c + d)[p - 1]}" for p in cells))
        print(f"  K{i} = {groups(k, 6)}   (hex {int(k, 2):012X})")


def main():
    print("DES: generarea celor 16 chei de rundă K1..K16 din K+ (sarcina 2.5)\n")
    show_tables()
    while True:
        choice = input("\n1 - introduc K+, 2 - K+ aleatoriu, 0 - ieșire: ").strip()
        if choice == "0":
            break
        if choice == "1":
            try:
                kplus = parse_kplus(input("K+ (56 biți sau 14 cifre hex): "))
            except ValueError as error:
                print(error)
                continue
        elif choice == "2":
            kplus = format(secrets.randbits(56), "056b")
        else:
            print("Alegeți 1, 2 sau 0.")
            continue
        show_schedule(kplus)


if __name__ == "__main__":
    main()
