show[label_, value_] := Print[label, " = ", If[IntegerQ[value], IntegerString[value], value]];

msg = "Nicorici Daniel";
codes = ToCharacterCode[msg];
hex = StringJoin[IntegerString[codes, 16, 2]];
m = FromDigits[hex, 16];
show["msg", msg];
show["ascii", codes];
show["hex", hex];
show["m", m];
show["bits(m)", IntegerLength[m, 2]];

e = 65537;
While[True,
  p = RandomPrime[{2^1023, 2^1024 - 1}];
  q = RandomPrime[{2^1023, 2^1024 - 1}];
  If[p != q && IntegerLength[p q, 2] == 2048 && GCD[e, (p - 1) (q - 1)] == 1, Break[]]];
n = p q;
phi = (p - 1) (q - 1);
d = PowerMod[e, -1, phi];
c = PowerMod[m, e, n];
mRSA = PowerMod[c, d, n];
show["rsa.p", p];
show["rsa.q", q];
show["rsa.n", n];
show["rsa.bits(n)", IntegerLength[n, 2]];
show["rsa.phi", phi];
show["rsa.e", e];
show["rsa.gcd(e,phi)", GCD[e, phi]];
show["rsa.d", d];
show["rsa.e*d mod phi", Mod[e d, phi]];
show["rsa.c", c];
show["rsa.decrypted", mRSA];
show["rsa.text", FromCharacterCode[IntegerDigits[mRSA, 256]]];

pp = ToExpression[StringJoin[
  "32317006071311007300153513477825163362488057133489075174588434139269806834136210",
  "00279205636264016468545855635793533081692882902308057347262527355474246124574102",
  "62025279165729728627063003252634282131457669314142236542209411113486299916574782",
  "68034230553086349050635557712219187890332729569696129743856241741236237225197346",
  "40269185579776797682301462539793305801522685873076119753243646747585546071504389",
  "68449403661304976978128542959586595975670512838521327844685229255045682728791137",
  "20098931873959143374175837826000278034973198552060607533234122603254684088120031",
  "105907484281003994966956119696956248629032338072839127039"]];
g = 2;
show["p", pp];
show["bits(p)", IntegerLength[pp, 2]];
show["g", g];

x = RandomInteger[{2, pp - 2}];
beta = PowerMod[g, x, pp];
k = RandomInteger[{2, pp - 2}];
y1 = PowerMod[g, k, pp];
y2 = Mod[m PowerMod[beta, k, pp], pp];
mElGamal = Mod[y2 PowerMod[y1, pp - 1 - x, pp], pp];
show["elgamal.x", x];
show["elgamal.beta", beta];
show["elgamal.k", k];
show["elgamal.y1", y1];
show["elgamal.y2", y2];
show["elgamal.decrypted", mElGamal];
show["elgamal.text", FromCharacterCode[IntegerDigits[mElGamal, 256]]];

a = RandomInteger[{2, pp - 2}];
b = RandomInteger[{2, pp - 2}];
alicePublic = PowerMod[g, a, pp];
bobPublic = PowerMod[g, b, pp];
aliceKey = PowerMod[bobPublic, a, pp];
bobKey = PowerMod[alicePublic, b, pp];
aesKey = Quotient[aliceKey, 2^(2048 - 256)];
show["dh.a", a];
show["dh.b", b];
show["dh.A", alicePublic];
show["dh.B", bobPublic];
show["dh.keyAlice", aliceKey];
show["dh.keyBob", bobKey];
show["dh.equal", aliceKey == bobKey];
show["aes.key", aesKey];
show["aes.hex", IntegerString[aesKey, 16, 64]];
show["aes.binary", IntegerString[aesKey, 2, 256]];
