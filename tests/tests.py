from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from django.test.client import Client

from pgpdb import models
from pgpdb.admin import PGPKeyModelAdmin

import pgpdb

GPG_ALICE_KEY = """
Old: Public Key Packet(tag 6)(269 bytes)
    Ver 4 - new
    Public key creation time - Sun Jun 22 21:50:48 JST 2014
    Pub alg - RSA Encrypt or Sign(pub 1)
    RSA n(2048 bits) - ...
    RSA e(17 bits) - ...
Old: User ID Packet(tag 13)(36 bytes)
    User ID - alice (test key) <alice@example.com>
Old: Signature Packet(tag 2)(312 bytes)
    Ver 4 - new
    Sig type - Positive certification of a User ID and Public Key packet(0x13).
    Pub alg - RSA Encrypt or Sign(pub 1)
    Hash alg - SHA1(hash 2)
    Hashed Sub: signature creation time(sub 2)(4 bytes)
        Time - Sun Jun 22 21:50:48 JST 2014
    Hashed Sub: key flags(sub 27)(1 bytes)
        Flag - This key may be used to certify other keys
        Flag - This key may be used to sign data
    Hashed Sub: preferred symmetric algorithms(sub 11)(5 bytes)
        Sym alg - AES with 256-bit key(sym 9)
        Sym alg - AES with 192-bit key(sym 8)
        Sym alg - AES with 128-bit key(sym 7)
        Sym alg - CAST5(sym 3)
        Sym alg - Triple-DES(sym 2)
    Hashed Sub: preferred hash algorithms(sub 21)(5 bytes)
        Hash alg - SHA256(hash 8)
        Hash alg - SHA1(hash 2)
        Hash alg - SHA384(hash 9)
        Hash alg - SHA512(hash 10)
        Hash alg - SHA224(hash 11)
    Hashed Sub: preferred compression algorithms(sub 22)(3 bytes)
        Comp alg - ZLIB <RFC1950>(comp 2)
        Comp alg - BZip2(comp 3)
        Comp alg - ZIP <RFC1951>(comp 1)
    Hashed Sub: features(sub 30)(1 bytes)
        Flag - Modification detection (packets 18 and 19)
    Hashed Sub: key server preferences(sub 23)(1 bytes)
        Flag - No-modify
    Sub: issuer key ID(sub 16)(8 bytes)
        Key ID - 0xD5D7DA71C354960E
    Hash left 2 bytes - 04 5e
    RSA m^d mod n(2047 bits) - ...
        -> PKCS-1
Old: Public Subkey Packet(tag 14)(269 bytes)
    Ver 4 - new
    Public key creation time - Sun Jun 22 21:50:48 JST 2014
    Pub alg - RSA Encrypt or Sign(pub 1)
    RSA n(2048 bits) - ...
    RSA e(17 bits) - ...
Old: Signature Packet(tag 2)(287 bytes)
    Ver 4 - new
    Sig type - Subkey Binding Signature(0x18).
    Pub alg - RSA Encrypt or Sign(pub 1)
    Hash alg - SHA1(hash 2)
    Hashed Sub: signature creation time(sub 2)(4 bytes)
        Time - Sun Jun 22 21:50:48 JST 2014
    Hashed Sub: key flags(sub 27)(1 bytes)
        Flag - This key may be used to encrypt communications
        Flag - This key may be used to encrypt storage
    Sub: issuer key ID(sub 16)(8 bytes)
        Key ID - 0xD5D7DA71C354960E
    Hash left 2 bytes - 9a eb
    RSA m^d mod n(2047 bits) - ...
        -> PKCS-1

-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v1

mQENBFOm0SgBCAC8BH6U1HHzzL1SXWpvjhf3sfAFJ8ciw5E854f70AkOOvi+fllB
D2OzmDqVB7dhBFwRUQ5i9ajPvNwYCXakwiVze44G2FMfOMbqqZaVTVUhpnYyMfB8
K0NgXQUqvfOdbGaKyUvIn1QwUtBQUwxwxIpJqXCGfAAXj5B23Q4VHSVGMnZ7KSbp
uqIsbQwhPx9F3nSZE5bX6NEFCM9nkTlBCrMRsSed08DTf6zKVNUjzRSj30iOuPWS
xaGbz+3mfIFwgVxYit850YgZfaQEkqrFsYPDA/bvI7C15I/3Oy2AavsPtPFroydp
JJ06fKDvC5s9V4Utyal5ttVvPcFw4o3LLlNtABEBAAG0JGFsaWNlICh0ZXN0IGtl
eSkgPGFsaWNlQGV4YW1wbGUuY29tPokBOAQTAQIAIgUCU6bRKAIbAwYLCQgHAwIG
FQgCCQoLBBYCAwECHgECF4AACgkQ1dfaccNUlg4EXgf/aIoYolj4Zs9Q8ck43BWx
EpjaC/vWgCQfUlRa9QI3IoWM37V52iLmba423/moF/eXGS6VtwdLq0k4GsuDfxIW
1Ojjwt4vtVR6UVtSNoI7y0s7yhpoRV+phMTcIbGlryMIrqWAwK4so/XbNDvqpVlS
RwLQnkDRkjMU7w8VZGrOyRucbZy6nZuH+nhialIq4VIPCu02HfAPgZGp7LH7EnMu
n25eHEvs45fk3Pus1BkYiCwt+nW5i1RYfwzWEZW9zkG2kDKadGxuN7fi75sGIGvy
gP+T7AuJGSl5BJKplxrKqefhQVhcpBgA3UYrb4I1wPHgtpGlBU2o+QKV9ZSeIvte
XLkBDQRTptEoAQgA2YqsTj9JniJkrr1x6g59io1GkP9z0JElzRl4kvG7WUkrhSPc
XkoLngcCur9lpxET2Wp7ou43zcKuiwsDxnsWwSvWfmg15N4BzYS6ulP7PSIpQlLb
srqFTR/iX0c7asgUE5Jpe8YEnThl2aAPkJlx47GQN1jhGxOkZhz3kIC+rG2d25ET
36eI0vw4oHO40nF9DihyHzfcD3tuuaOJ+AUPrDh7o97a8yIQmVU031GImC1DHQ9t
k9qkixCuejN1cfi7zqWclnd4nu3C/PJXLz0qzprhK0gXqgjZVBpCPQ5g/WV/Myw/
5H7vJC5WcV0lQilxtjgaHmpSu65XTaAHf4OlNQARAQABiQEfBBgBAgAJBQJTptEo
AhsMAAoJENXX2nHDVJYOmusH/0VDpB6353RsZzCj+eoV9mpew8gPo7jdwMGFVW3r
7ZfwCCE+9hMqQAPU4ewTtpy9SrzynZCG02vycaBhLJwcP1dKtvae1y8B8zh7zo9F
eLTUewHuyFRpyM5/fj1Dou89AOvDRaiJPaO3RQOmjGG9+D5hDS03CHBXOg/P0gYv
lc1myZNfRtU5+ezMEWA+tqyjyjj3W6nyobtpVtwgpA/od47/UcdGqSkzkmr+zqqH
amPMgSaahcvqPw2VFt4fi00ShN9EguwiV2vJes6VvDq1qE5Ap/zWBn/B7xIc70jD
hHtoB2/2gM/blPn5EPrIht6Kh9njBFYVk+OrV96NpJl08lM=
=xJuO
-----END PGP PUBLIC KEY BLOCK-----
"""

GPG_BOB_KEY = """
Old: Public Key Packet(tag 6)(269 bytes)
    Ver 4 - new
    Public key creation time - Sun Jun 22 21:55:43 JST 2014
    Pub alg - RSA Encrypt or Sign(pub 1)
    RSA n(2048 bits) - ...
    RSA e(17 bits) - ...
Old: User ID Packet(tag 13)(32 bytes)
    User ID - bob (test key) <bob@example.com>
Old: Signature Packet(tag 2)(312 bytes)
    Ver 4 - new
    Sig type - Positive certification of a User ID and Public Key packet(0x13).
    Pub alg - RSA Encrypt or Sign(pub 1)
    Hash alg - SHA1(hash 2)
    Hashed Sub: signature creation time(sub 2)(4 bytes)
        Time - Sun Jun 22 21:55:43 JST 2014
    Hashed Sub: key flags(sub 27)(1 bytes)
        Flag - This key may be used to certify other keys
        Flag - This key may be used to sign data
    Hashed Sub: preferred symmetric algorithms(sub 11)(5 bytes)
        Sym alg - AES with 256-bit key(sym 9)
        Sym alg - AES with 192-bit key(sym 8)
        Sym alg - AES with 128-bit key(sym 7)
        Sym alg - CAST5(sym 3)
        Sym alg - Triple-DES(sym 2)
    Hashed Sub: preferred hash algorithms(sub 21)(5 bytes)
        Hash alg - SHA256(hash 8)
        Hash alg - SHA1(hash 2)
        Hash alg - SHA384(hash 9)
        Hash alg - SHA512(hash 10)
        Hash alg - SHA224(hash 11)
    Hashed Sub: preferred compression algorithms(sub 22)(3 bytes)
        Comp alg - ZLIB <RFC1950>(comp 2)
        Comp alg - BZip2(comp 3)
        Comp alg - ZIP <RFC1951>(comp 1)
    Hashed Sub: features(sub 30)(1 bytes)
        Flag - Modification detection (packets 18 and 19)
    Hashed Sub: key server preferences(sub 23)(1 bytes)
        Flag - No-modify
    Sub: issuer key ID(sub 16)(8 bytes)
        Key ID - 0x3C8F7607CA580F9E
    Hash left 2 bytes - 5e 70
    RSA m^d mod n(2048 bits) - ...
        -> PKCS-1
Old: Public Subkey Packet(tag 14)(269 bytes)
    Ver 4 - new
    Public key creation time - Sun Jun 22 21:55:43 JST 2014
    Pub alg - RSA Encrypt or Sign(pub 1)
    RSA n(2048 bits) - ...
    RSA e(17 bits) - ...
Old: Signature Packet(tag 2)(287 bytes)
    Ver 4 - new
    Sig type - Subkey Binding Signature(0x18).
    Pub alg - RSA Encrypt or Sign(pub 1)
    Hash alg - SHA1(hash 2)
    Hashed Sub: signature creation time(sub 2)(4 bytes)
        Time - Sun Jun 22 21:55:43 JST 2014
    Hashed Sub: key flags(sub 27)(1 bytes)
        Flag - This key may be used to encrypt communications
        Flag - This key may be used to encrypt storage
    Sub: issuer key ID(sub 16)(8 bytes)
        Key ID - 0x3C8F7607CA580F9E
    Hash left 2 bytes - a8 60
    RSA m^d mod n(2046 bits) - ...
        -> PKCS-1

-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v1

mQENBFOm0k8BCAC1r3JzpCyUjSIMyDm35lOJItSe5hLK7aIHxscs5oxmQiLpR80d
6pisPWiwA9gMDs700LpE+m/QtR4y17MlNU2S1i1RLlt118SEnwD+g/fTBZrCOmuy
FWLizoRhtlLcu3ir4j47APfu1I3De5x3t1TeBuSY41rSkxXlZ8G9hlu2xAO6MmCE
fJpNc/tHt9cTXTMGKapVJK/F9dQZ+T2NgPf0nyr5EIfpx+GckZlx3qFT+SleN/UY
ETk2LL6ElpwARVmcyDv3J9BuLekA0aQSR9GqmDpQmMFBoXds69pBhWtXu228puop
8LSwO7ZF6c/flTp8xniRlpIEejk4WchhSYdlABEBAAG0IGJvYiAodGVzdCBrZXkp
IDxib2JAZXhhbXBsZS5jb20+iQE4BBMBAgAiBQJTptJPAhsDBgsJCAcDAgYVCAIJ
CgsEFgIDAQIeAQIXgAAKCRA8j3YHylgPnl5wCACvW5ihaa9Ovmh8hnpBzOdD9A0V
kTdXwHU0E2G4O0+jLxnbpP8s9apw8aYuOS7IlNBA0qoaCDQUU1XEs/TyZJNwVZww
FqwBSiAlxPR0ZBAVLGmuRPC/pA1LgFKEf95A3VKlqcOuFmBnA+o4FqUTHQ+hsXDs
icNflufWU/p0kAhP+8gAkrYdO2RTYqO9+qRFULb/U5/NX2iIIo+w7v8k3dVzDKD6
SQJ8IksFJ7iJb90zPu14xlWOHYZl9SPvD/hM+XwRdDRwnF2W1O1QT0+RZlbhZdB5
6opzVyonaVwSZ6X4wtIy9nhBVjHv9xaQKh7bYCtk9RAauDZ10R72KANdeoaQuQEN
BFOm0k8BCAC0xTBFoQ467Q0ye2tNQ1rUJ7xn6sQ03kiTUr7U+NLvJzKF2B6odGNA
Y+wBFAvkYDZ+AgzhfyWos3x+VuYulctPXR8KMUdbE4euoP+wu/jmXr5PocmxNQgg
92iHQ5hzxJXnBoDPAMSYl3Cux19+/jGoc44LgJP9Xm7gBwo7keq0+NhGlbCgGKKl
DxBr/Jqb87pa9Y+WBXN1LL1h8sLabAN6kEMx1GiAq3G8L9HEEAnOkXgn4vnQp+7s
KrSqxKEbqw28vB9FjPcC3ISzM5R/fGb1hanD/YAA5VEbZriUL9OnLN2AxNzfWQPI
1G3K1LcDGcrBo9FG8G0plulm93dorvvlABEBAAGJAR8EGAECAAkFAlOm0k8CGwwA
CgkQPI92B8pYD56oYAf+POvglwkna4396mqIAhhq7nozSbF26fX8fT3r7r2Hge+m
OgJZjLLVTKVtuUx1bb1SPaKdd+TW5A8xM1Nnjg1xB6WPaa3XXKkkd8Ty4kvrUqUk
yevXl0R/cBscnO04WeUic5ErHUaAo9NZH2smPaOcwW7zvIiYm8R6orb/zeXJqltn
2sVHuFNYjgcC8OxcreS5SQu/l6kfybRCKmdC7UaPfNNbesH+IuTwuLv5rQh125l2
Mpga1NHRG7vfaqDSp41mOel/Y1MbFgcFcs3Q274Olr9hxHeMIJAYow+RAOhgYXjQ
GeykHHGfctbPAwE/06+sspYamO7XjhmPcbdXd+fX9w==
=AXuc
-----END PGP PUBLIC KEY BLOCK-----
"""

GPG_CAROL_KEY = """
Old: Public Key Packet(tag 6)(51 bytes)
    Ver 4 - new
    Public key creation time - Fri Oct  9 14:41:17 +07 2020
    Pub alg - EdDSA Edwards-curve Digital Signature Algorithm(pub 22)
    Unknown public key(pub 22)
Old: User ID Packet(tag 13)(36 bytes)
    User ID - carol (test key) <carol@example.com>
Old: Signature Packet(tag 2)(144 bytes)
    Ver 4 - new
    Sig type - Positive certification of a User ID and Public Key packet(0x13).
    Pub alg - EdDSA Edwards-curve Digital Signature Algorithm(pub 22)
    Hash alg - SHA256(hash 8)
    Hashed Sub: issuer fingerprint(sub 33)(21 bytes)
     v4 -    Fingerprint - 5c b2 75 d4 49 c0 9c 30 28 fa ff 8d 7f a0 29 cf 20 39 d7 60
    Hashed Sub: signature creation time(sub 2)(4 bytes)
        Time - Fri Oct  9 14:41:17 +07 2020
    Hashed Sub: key flags(sub 27)(1 bytes)
        Flag - This key may be used to certify other keys
        Flag - This key may be used to sign data
    Hashed Sub: preferred symmetric algorithms(sub 11)(4 bytes)
        Sym alg - AES with 256-bit key(sym 9)
        Sym alg - AES with 192-bit key(sym 8)
        Sym alg - AES with 128-bit key(sym 7)
        Sym alg - Triple-DES(sym 2)
    Hashed Sub: preferred hash algorithms(sub 21)(5 bytes)
        Hash alg - SHA512(hash 10)
        Hash alg - SHA384(hash 9)
        Hash alg - SHA256(hash 8)
        Hash alg - SHA224(hash 11)
        Hash alg - SHA1(hash 2)
    Hashed Sub: preferred compression algorithms(sub 22)(3 bytes)
        Comp alg - ZLIB <RFC1950>(comp 2)
        Comp alg - BZip2(comp 3)
        Comp alg - ZIP <RFC1951>(comp 1)
    Hashed Sub: features(sub 30)(1 bytes)
        Flag - Modification detection (packets 18 and 19)
    Hashed Sub: key server preferences(sub 23)(1 bytes)
        Flag - No-modify
    Sub: issuer key ID(sub 16)(8 bytes)
        Key ID - 0x7FA029CF2039D760
    Hash left 2 bytes - ab 5a
    Unknown signature(pub 22)

-----BEGIN PGP PUBLIC KEY BLOCK-----

mDMEX4AUHRYJKwYBBAHaRw8BAQdAbzUUIywuir/IaG9JLGmMHKUwVhqiNgskyVXA
fVnpoHa0JGNhcm9sICh0ZXN0IGtleSkgPGNhcm9sQGV4YW1wbGUuY29tPoiQBBMW
CAA4FiEEXLJ11EnAnDAo+v+Nf6ApzyA512AFAl+AFB0CGwMFCwkIBwIGFQoJCAsC
BBYCAwECHgECF4AACgkQf6ApzyA512CrWgEAn8UlvGHQp+RLzNuXYU7E1ABdcbRL
nuXsvjXmL1k4doYBALSpvNzU6JavWxF79U41S3vOzYBi2x6rZCJ9FZHhyO0A
=jMet
-----END PGP PUBLIC KEY BLOCK-----
"""

PGPDB_ALICE_KEY = '''-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: django-pgpdb {0}

mQENBFOm0SgBCAC8BH6U1HHzzL1SXWpvjhf3sfAFJ8ciw5E854f70AkOOvi+fllB
D2OzmDqVB7dhBFwRUQ5i9ajPvNwYCXakwiVze44G2FMfOMbqqZaVTVUhpnYyMfB8
K0NgXQUqvfOdbGaKyUvIn1QwUtBQUwxwxIpJqXCGfAAXj5B23Q4VHSVGMnZ7KSbp
uqIsbQwhPx9F3nSZE5bX6NEFCM9nkTlBCrMRsSed08DTf6zKVNUjzRSj30iOuPWS
xaGbz+3mfIFwgVxYit850YgZfaQEkqrFsYPDA/bvI7C15I/3Oy2AavsPtPFroydp
JJ06fKDvC5s9V4Utyal5ttVvPcFw4o3LLlNtABEBAAG0JGFsaWNlICh0ZXN0IGtl
eSkgPGFsaWNlQGV4YW1wbGUuY29tPokBOAQTAQIAIgUCU6bRKAIbAwYLCQgHAwIG
FQgCCQoLBBYCAwECHgECF4AACgkQ1dfaccNUlg4EXgf/aIoYolj4Zs9Q8ck43BWx
EpjaC/vWgCQfUlRa9QI3IoWM37V52iLmba423/moF/eXGS6VtwdLq0k4GsuDfxIW
1Ojjwt4vtVR6UVtSNoI7y0s7yhpoRV+phMTcIbGlryMIrqWAwK4so/XbNDvqpVlS
RwLQnkDRkjMU7w8VZGrOyRucbZy6nZuH+nhialIq4VIPCu02HfAPgZGp7LH7EnMu
n25eHEvs45fk3Pus1BkYiCwt+nW5i1RYfwzWEZW9zkG2kDKadGxuN7fi75sGIGvy
gP+T7AuJGSl5BJKplxrKqefhQVhcpBgA3UYrb4I1wPHgtpGlBU2o+QKV9ZSeIvte
XLkBDQRTptEoAQgA2YqsTj9JniJkrr1x6g59io1GkP9z0JElzRl4kvG7WUkrhSPc
XkoLngcCur9lpxET2Wp7ou43zcKuiwsDxnsWwSvWfmg15N4BzYS6ulP7PSIpQlLb
srqFTR/iX0c7asgUE5Jpe8YEnThl2aAPkJlx47GQN1jhGxOkZhz3kIC+rG2d25ET
36eI0vw4oHO40nF9DihyHzfcD3tuuaOJ+AUPrDh7o97a8yIQmVU031GImC1DHQ9t
k9qkixCuejN1cfi7zqWclnd4nu3C/PJXLz0qzprhK0gXqgjZVBpCPQ5g/WV/Myw/
5H7vJC5WcV0lQilxtjgaHmpSu65XTaAHf4OlNQARAQABiQEfBBgBAgAJBQJTptEo
AhsMAAoJENXX2nHDVJYOmusH/0VDpB6353RsZzCj+eoV9mpew8gPo7jdwMGFVW3r
7ZfwCCE+9hMqQAPU4ewTtpy9SrzynZCG02vycaBhLJwcP1dKtvae1y8B8zh7zo9F
eLTUewHuyFRpyM5/fj1Dou89AOvDRaiJPaO3RQOmjGG9+D5hDS03CHBXOg/P0gYv
lc1myZNfRtU5+ezMEWA+tqyjyjj3W6nyobtpVtwgpA/od47/UcdGqSkzkmr+zqqH
amPMgSaahcvqPw2VFt4fi00ShN9EguwiV2vJes6VvDq1qE5Ap/zWBn/B7xIc70jD
hHtoB2/2gM/blPn5EPrIht6Kh9njBFYVk+OrV96NpJl08lM=
=xJuO
-----END PGP PUBLIC KEY BLOCK-----'''.format(pgpdb.__version__)

PGPDB_BOB_KEY = '''-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: django-pgpdb {0}

mQENBFOm0k8BCAC1r3JzpCyUjSIMyDm35lOJItSe5hLK7aIHxscs5oxmQiLpR80d
6pisPWiwA9gMDs700LpE+m/QtR4y17MlNU2S1i1RLlt118SEnwD+g/fTBZrCOmuy
FWLizoRhtlLcu3ir4j47APfu1I3De5x3t1TeBuSY41rSkxXlZ8G9hlu2xAO6MmCE
fJpNc/tHt9cTXTMGKapVJK/F9dQZ+T2NgPf0nyr5EIfpx+GckZlx3qFT+SleN/UY
ETk2LL6ElpwARVmcyDv3J9BuLekA0aQSR9GqmDpQmMFBoXds69pBhWtXu228puop
8LSwO7ZF6c/flTp8xniRlpIEejk4WchhSYdlABEBAAG0IGJvYiAodGVzdCBrZXkp
IDxib2JAZXhhbXBsZS5jb20+iQE4BBMBAgAiBQJTptJPAhsDBgsJCAcDAgYVCAIJ
CgsEFgIDAQIeAQIXgAAKCRA8j3YHylgPnl5wCACvW5ihaa9Ovmh8hnpBzOdD9A0V
kTdXwHU0E2G4O0+jLxnbpP8s9apw8aYuOS7IlNBA0qoaCDQUU1XEs/TyZJNwVZww
FqwBSiAlxPR0ZBAVLGmuRPC/pA1LgFKEf95A3VKlqcOuFmBnA+o4FqUTHQ+hsXDs
icNflufWU/p0kAhP+8gAkrYdO2RTYqO9+qRFULb/U5/NX2iIIo+w7v8k3dVzDKD6
SQJ8IksFJ7iJb90zPu14xlWOHYZl9SPvD/hM+XwRdDRwnF2W1O1QT0+RZlbhZdB5
6opzVyonaVwSZ6X4wtIy9nhBVjHv9xaQKh7bYCtk9RAauDZ10R72KANdeoaQuQEN
BFOm0k8BCAC0xTBFoQ467Q0ye2tNQ1rUJ7xn6sQ03kiTUr7U+NLvJzKF2B6odGNA
Y+wBFAvkYDZ+AgzhfyWos3x+VuYulctPXR8KMUdbE4euoP+wu/jmXr5PocmxNQgg
92iHQ5hzxJXnBoDPAMSYl3Cux19+/jGoc44LgJP9Xm7gBwo7keq0+NhGlbCgGKKl
DxBr/Jqb87pa9Y+WBXN1LL1h8sLabAN6kEMx1GiAq3G8L9HEEAnOkXgn4vnQp+7s
KrSqxKEbqw28vB9FjPcC3ISzM5R/fGb1hanD/YAA5VEbZriUL9OnLN2AxNzfWQPI
1G3K1LcDGcrBo9FG8G0plulm93dorvvlABEBAAGJAR8EGAECAAkFAlOm0k8CGwwA
CgkQPI92B8pYD56oYAf+POvglwkna4396mqIAhhq7nozSbF26fX8fT3r7r2Hge+m
OgJZjLLVTKVtuUx1bb1SPaKdd+TW5A8xM1Nnjg1xB6WPaa3XXKkkd8Ty4kvrUqUk
yevXl0R/cBscnO04WeUic5ErHUaAo9NZH2smPaOcwW7zvIiYm8R6orb/zeXJqltn
2sVHuFNYjgcC8OxcreS5SQu/l6kfybRCKmdC7UaPfNNbesH+IuTwuLv5rQh125l2
Mpga1NHRG7vfaqDSp41mOel/Y1MbFgcFcs3Q274Olr9hxHeMIJAYow+RAOhgYXjQ
GeykHHGfctbPAwE/06+sspYamO7XjhmPcbdXd+fX9w==
=AXuc
-----END PGP PUBLIC KEY BLOCK-----'''.format(pgpdb.__version__)

PGPDB_MULTI_KEY = '''-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: django-pgpdb {0}

mQENBFOm0SgBCAC8BH6U1HHzzL1SXWpvjhf3sfAFJ8ciw5E854f70AkOOvi+fllB
D2OzmDqVB7dhBFwRUQ5i9ajPvNwYCXakwiVze44G2FMfOMbqqZaVTVUhpnYyMfB8
K0NgXQUqvfOdbGaKyUvIn1QwUtBQUwxwxIpJqXCGfAAXj5B23Q4VHSVGMnZ7KSbp
uqIsbQwhPx9F3nSZE5bX6NEFCM9nkTlBCrMRsSed08DTf6zKVNUjzRSj30iOuPWS
xaGbz+3mfIFwgVxYit850YgZfaQEkqrFsYPDA/bvI7C15I/3Oy2AavsPtPFroydp
JJ06fKDvC5s9V4Utyal5ttVvPcFw4o3LLlNtABEBAAG0JGFsaWNlICh0ZXN0IGtl
eSkgPGFsaWNlQGV4YW1wbGUuY29tPokBOAQTAQIAIgUCU6bRKAIbAwYLCQgHAwIG
FQgCCQoLBBYCAwECHgECF4AACgkQ1dfaccNUlg4EXgf/aIoYolj4Zs9Q8ck43BWx
EpjaC/vWgCQfUlRa9QI3IoWM37V52iLmba423/moF/eXGS6VtwdLq0k4GsuDfxIW
1Ojjwt4vtVR6UVtSNoI7y0s7yhpoRV+phMTcIbGlryMIrqWAwK4so/XbNDvqpVlS
RwLQnkDRkjMU7w8VZGrOyRucbZy6nZuH+nhialIq4VIPCu02HfAPgZGp7LH7EnMu
n25eHEvs45fk3Pus1BkYiCwt+nW5i1RYfwzWEZW9zkG2kDKadGxuN7fi75sGIGvy
gP+T7AuJGSl5BJKplxrKqefhQVhcpBgA3UYrb4I1wPHgtpGlBU2o+QKV9ZSeIvte
XLkBDQRTptEoAQgA2YqsTj9JniJkrr1x6g59io1GkP9z0JElzRl4kvG7WUkrhSPc
XkoLngcCur9lpxET2Wp7ou43zcKuiwsDxnsWwSvWfmg15N4BzYS6ulP7PSIpQlLb
srqFTR/iX0c7asgUE5Jpe8YEnThl2aAPkJlx47GQN1jhGxOkZhz3kIC+rG2d25ET
36eI0vw4oHO40nF9DihyHzfcD3tuuaOJ+AUPrDh7o97a8yIQmVU031GImC1DHQ9t
k9qkixCuejN1cfi7zqWclnd4nu3C/PJXLz0qzprhK0gXqgjZVBpCPQ5g/WV/Myw/
5H7vJC5WcV0lQilxtjgaHmpSu65XTaAHf4OlNQARAQABiQEfBBgBAgAJBQJTptEo
AhsMAAoJENXX2nHDVJYOmusH/0VDpB6353RsZzCj+eoV9mpew8gPo7jdwMGFVW3r
7ZfwCCE+9hMqQAPU4ewTtpy9SrzynZCG02vycaBhLJwcP1dKtvae1y8B8zh7zo9F
eLTUewHuyFRpyM5/fj1Dou89AOvDRaiJPaO3RQOmjGG9+D5hDS03CHBXOg/P0gYv
lc1myZNfRtU5+ezMEWA+tqyjyjj3W6nyobtpVtwgpA/od47/UcdGqSkzkmr+zqqH
amPMgSaahcvqPw2VFt4fi00ShN9EguwiV2vJes6VvDq1qE5Ap/zWBn/B7xIc70jD
hHtoB2/2gM/blPn5EPrIht6Kh9njBFYVk+OrV96NpJl08lOZAQ0EU6bSTwEIALWv
cnOkLJSNIgzIObfmU4ki1J7mEsrtogfGxyzmjGZCIulHzR3qmKw9aLAD2AwOzvTQ
ukT6b9C1HjLXsyU1TZLWLVEuW3XXxISfAP6D99MFmsI6a7IVYuLOhGG2Uty7eKvi
PjsA9+7UjcN7nHe3VN4G5JjjWtKTFeVnwb2GW7bEA7oyYIR8mk1z+0e31xNdMwYp
qlUkr8X11Bn5PY2A9/SfKvkQh+nH4ZyRmXHeoVP5KV439RgROTYsvoSWnABFWZzI
O/cn0G4t6QDRpBJH0aqYOlCYwUGhd2zr2kGFa1e7bbym6inwtLA7tkXpz9+VOnzG
eJGWkgR6OThZyGFJh2UAEQEAAbQgYm9iICh0ZXN0IGtleSkgPGJvYkBleGFtcGxl
LmNvbT6JATgEEwECACIFAlOm0k8CGwMGCwkIBwMCBhUIAgkKCwQWAgMBAh4BAheA
AAoJEDyPdgfKWA+eXnAIAK9bmKFpr06+aHyGekHM50P0DRWRN1fAdTQTYbg7T6Mv
Gduk/yz1qnDxpi45LsiU0EDSqhoINBRTVcSz9PJkk3BVnDAWrAFKICXE9HRkEBUs
aa5E8L+kDUuAUoR/3kDdUqWpw64WYGcD6jgWpRMdD6GxcOyJw1+W59ZT+nSQCE/7
yACSth07ZFNio736pEVQtv9Tn81faIgij7Du/yTd1XMMoPpJAnwiSwUnuIlv3TM+
7XjGVY4dhmX1I+8P+Ez5fBF0NHCcXZbU7VBPT5FmVuFl0HnqinNXKidpXBJnpfjC
0jL2eEFWMe/3FpAqHttgK2T1EBq4NnXRHvYoA116hpC5AQ0EU6bSTwEIALTFMEWh
DjrtDTJ7a01DWtQnvGfqxDTeSJNSvtT40u8nMoXYHqh0Y0Bj7AEUC+RgNn4CDOF/
JaizfH5W5i6Vy09dHwoxR1sTh66g/7C7+OZevk+hybE1CCD3aIdDmHPElecGgM8A
xJiXcK7HX37+MahzjguAk/1ebuAHCjuR6rT42EaVsKAYoqUPEGv8mpvzulr1j5YF
c3UsvWHywtpsA3qQQzHUaICrcbwv0cQQCc6ReCfi+dCn7uwqtKrEoRurDby8H0WM
9wLchLMzlH98ZvWFqcP9gADlURtmuJQv06cs3YDE3N9ZA8jUbcrUtwMZysGj0Ubw
bSmW6Wb3d2iu++UAEQEAAYkBHwQYAQIACQUCU6bSTwIbDAAKCRA8j3YHylgPnqhg
B/486+CXCSdrjf3qaogCGGruejNJsXbp9fx9PevuvYeB76Y6AlmMstVMpW25THVt
vVI9op135NbkDzEzU2eODXEHpY9prddcqSR3xPLiS+tSpSTJ69eXRH9wGxyc7ThZ
5SJzkSsdRoCj01kfayY9o5zBbvO8iJibxHqitv/N5cmqW2faxUe4U1iOBwLw7Fyt
5LlJC7+XqR/JtEIqZ0LtRo9801t6wf4i5PC4u/mtCHXbmXYymBrU0dEbu99qoNKn
jWY56X9jUxsWBwVyzdDbvg6Wv2HEd4wgkBijD5EA6GBheNAZ7KQccZ9y1s8DAT/T
r6yylhqY7teOGY9xt1d359f3
=Nkr1
-----END PGP PUBLIC KEY BLOCK-----'''.format(pgpdb.__version__)

PGPDB_CAROL_KEY = '''-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: django-pgpdb {0}

mDMEX4AUHRYJKwYBBAHaRw8BAQdAbzUUIywuir/IaG9JLGmMHKUwVhqiNgskyVXA
fVnpoHa0JGNhcm9sICh0ZXN0IGtleSkgPGNhcm9sQGV4YW1wbGUuY29tPoiQBBMW
CAA4FiEEXLJ11EnAnDAo+v+Nf6ApzyA512AFAl+AFB0CGwMFCwkIBwIGFQoJCAsC
BBYCAwECHgECF4AACgkQf6ApzyA512CrWgEAn8UlvGHQp+RLzNuXYU7E1ABdcbRL
nuXsvjXmL1k4doYBALSpvNzU6JavWxF79U41S3vOzYBi2x6rZCJ9FZHhyO0A
=jMet
-----END PGP PUBLIC KEY BLOCK-----'''.format(pgpdb.__version__)

MACHINE_READABLE_INDEX1 = '''info:1:1
pub:d5d7da71c354960e:1:2048:1403441448::
uid:alice (test key) <alice@example.com>:1403441448::'''

MACHINE_READABLE_INDEX2 = '''info:1:2
pub:d5d7da71c354960e:1:2048:1403441448::
uid:alice (test key) <alice@example.com>:1403441448::
pub:3c8f7607ca580f9e:1:2048:1403441743::
uid:bob (test key) <bob@example.com>:1403441743::'''


class MockRequest(object):
    def __init__(self, user=None):
        self.user = user


class PGPKeyModelTest(TestCase):

    def setUp(self):
        self.ALICE = models.PGPKeyModel.objects.save_to_storage(None, GPG_ALICE_KEY)
        self.CAROL = models.PGPKeyModel.objects.save_to_storage(None, GPG_CAROL_KEY)

    def tearDown(self):
        self.ALICE.delete()
        self.CAROL.delete()

    def test_adminlist(self):
        self.CLIENT = Client()
        my_model_admin = PGPKeyModelAdmin(model=models.PGPKeyModel, admin_site=AdminSite())
        super_user = User.objects.create_superuser(username='super', email='super@email.org', password='pass')
        self.CLIENT.force_login(user=super_user)
        my_model_admin.save_model(obj=self.ALICE, request=MockRequest(user=super_user), form=None, change=None)

        resp = self.CLIENT.get(reverse('admin:pgpdb_pgpkeymodel_changelist'))
        self.assertEqual(resp.context['results'][1][3], '<td class="field-user_ids">&lt;ul&gt;&lt;li&gt;&lt;a href=&quot;../pgpuseridmodel/1/&quot;&gt;alice (test key) &lt;alice@example.com&gt;&lt;/a&gt;&lt;/li&gt;&lt;/ul&gt;</td>')


    def test_save_to_storage(self):
        self.BOB = models.PGPKeyModel.objects.save_to_storage(None, GPG_BOB_KEY)

        self.assertNotEqual(self.ALICE.uid, self.BOB.uid)
        self.assertNotEqual(self.ALICE.file, self.BOB.file)
        self.assertEqual(self.ALICE.user, None)
        self.assertEqual(self.BOB.user, None)
        self.assertEqual(self.ALICE.crc24, 'xJuO')
        self.assertEqual(self.BOB.crc24, 'AXuc')
        self.assertEqual(self.ALICE.is_revoked, False)
        self.assertEqual(self.BOB.is_revoked, False)

        self.BOB.delete()

    def test_publickey(self):
        self.assertEqual(self.ALICE.public_keys.count(), 2)
        keys = self.ALICE.public_keys.all()
        sign = keys[0]
        enc = keys[1]
        self.assertTrue(sign.is_public_key())
        self.assertFalse(sign.is_userid())
        self.assertFalse(sign.is_signature())
        self.assertEqual(sign.index, 1)
        self.assertEqual(sign.key, self.ALICE)
        self.assertEqual(sign.is_sub, False)
        creation_time = sign.creation_time.strftime('%Y-%m-%dT%H:%M:%S')
        self.assertEqual(creation_time, '2014-06-22T12:50:48')
        self.assertEqual(sign.expiration_time, None)
        self.assertEqual(sign.algorithm, 1)  # RSA_ENC_SIGN
        self.assertEqual(sign.bits, 2048)
        self.assertEqual(sign.fingerprint, '4b3292e956b577ad703443f4d5d7da71c354960e')
        self.assertEqual(sign.keyid, 'd5d7da71c354960e')

        self.assertTrue(enc.is_public_key())
        self.assertFalse(enc.is_userid())
        self.assertFalse(enc.is_signature())
        self.assertEqual(enc.index, 4)
        self.assertEqual(enc.key, self.ALICE)
        self.assertEqual(enc.is_sub, True)
        creation_time = enc.creation_time.strftime('%Y-%m-%dT%H:%M:%S')
        self.assertEqual(creation_time, '2014-06-22T12:50:48')
        self.assertEqual(enc.expiration_time, None)
        self.assertEqual(enc.algorithm, 1)  # RSA_ENC_SIGN
        self.assertEqual(enc.bits, 2048)
        self.assertEqual(enc.fingerprint, '089d58a247da0553a46ff04c9f0ff40fd27061e1')
        self.assertEqual(enc.keyid, '9f0ff40fd27061e1')

    def test_userid(self):
        self.assertEqual(self.ALICE.userids.count(), 1)
        userid = self.ALICE.userids.all()[0]
        self.assertFalse(userid.is_public_key())
        self.assertTrue(userid.is_userid())
        self.assertFalse(userid.is_signature())
        self.assertEqual(userid.index, 2)
        self.assertEqual(userid.key, self.ALICE)
        self.assertEqual(userid.userid, 'alice (test key) <alice@example.com>')

    def test_signature(self):
        keys = self.ALICE.public_keys.all()
        pkey = keys[0]
        skey = keys[1]
        userid = self.ALICE.userids.all()[0]

        self.assertEqual(self.ALICE.signatures.count(), 2)
        sigs = self.ALICE.signatures.all()
        pub = sigs[0]
        sub = sigs[1]
        self.assertFalse(pub.is_public_key())
        self.assertFalse(pub.is_userid())
        self.assertTrue(pub.is_signature())
        self.assertEqual(pub.index, 3)
        self.assertEqual(pub.key, self.ALICE)
        self.assertEqual(pub.pkey, pkey)
        self.assertEqual(pub.userid, userid)
        self.assertEqual(pub.type, 0x13)  # Positive key sign
        self.assertEqual(pub.pka, 1)
        self.assertEqual(pub.hash, 2)
        creation_time = pub.creation_time.strftime('%Y-%m-%dT%H:%M:%S')
        self.assertEqual(creation_time, '2014-06-22T12:50:48')
        self.assertEqual(pub.expiration_time, None)
        self.assertEqual(pub.keyid, 'd5d7da71c354960e')

        self.assertFalse(sub.is_public_key())
        self.assertFalse(sub.is_userid())
        self.assertTrue(sub.is_signature())
        self.assertEqual(sub.index, 5)
        self.assertEqual(sub.key, self.ALICE)
        self.assertEqual(sub.pkey, skey)
        self.assertEqual(sub.userid, userid)
        self.assertEqual(sub.type, 0x18)  # Subkey binding sign
        self.assertEqual(sub.pka, 1)
        self.assertEqual(sub.hash, 2)
        creation_time = sub.creation_time.strftime('%Y-%m-%dT%H:%M:%S')
        self.assertEqual(creation_time, '2014-06-22T12:50:48')
        self.assertEqual(sub.expiration_time, None)
        self.assertEqual(sub.keyid, 'd5d7da71c354960e')

    def test_first(self):
        first = self.ALICE.first()
        self.assertEqual(sorted(first.keys()), ['public_key', 'userid'])
        self.assertEqual(first['public_key'], self.ALICE.public_keys.first())
        self.assertEqual(first['userid'], self.ALICE.userids.first())

    def test_packets(self):
        packets = self.ALICE.packets()
        index = [x.index for x in packets]
        self.assertEqual(index, [1, 2, 3, 4, 5])

    def test_ascii_armor(self):
        data = self.ALICE.ascii_armor()
        self.assertEqual(data, PGPDB_ALICE_KEY)

    def test_algorithm_str(self):
        first = self.ALICE.public_keys.first()
        algorithm_str = first.algorithm_str()
        PKA_MAP = models.PGPPublicKeyModel.PKA_MAP
        rsa_enc_sign = PKA_MAP[models.PGPPublicKeyModel.RSA_ENC_SIGN]
        self.assertEqual(algorithm_str, str(rsa_enc_sign))

    def test_simple_algorithm_str(self):
        first = self.ALICE.public_keys.first()
        simple_str = first.simple_algorithm_str()
        SIMPLE_PKA_MAP = models.PGPPublicKeyModel.SIMPLE_PKA_MAP
        simple_rsa = SIMPLE_PKA_MAP[models.PGPPublicKeyModel.RSA_ENC_SIGN]
        self.assertEqual(simple_str, str(simple_rsa))

    def test_type_str(self):
        first = self.ALICE.signatures.first()
        type_str = first.type_str()
        SIG_MAP = models.PGPSignatureModel.SIG_MAP
        key_positive = SIG_MAP[models.PGPSignatureModel.KEY_POSITIVE]
        self.assertEqual(type_str, str(key_positive))

    def test_pka_str(self):
        first = self.ALICE.signatures.first()
        pka_str = first.pka_str()
        PKA_MAP = models.PGPSignatureModel.PKA_MAP
        rsa_enc_sign = PKA_MAP[models.PGPSignatureModel.RSA_ENC_SIGN]
        self.assertEqual(pka_str, str(rsa_enc_sign))

    def test_simple_pka_str(self):
        first = self.ALICE.signatures.first()
        simple_pka_str = first.simple_pka_str()
        SIMPLE_PKA_MAP = models.PGPSignatureModel.SIMPLE_PKA_MAP
        simple_rsa = SIMPLE_PKA_MAP[models.PGPSignatureModel.RSA_ENC_SIGN]
        self.assertEqual(simple_pka_str, str(simple_rsa))

    def test_hash_str(self):
        first = self.ALICE.signatures.first()
        hash_str = first.hash_str()
        HASH_MAP = models.PGPSignatureModel.HASH_MAP
        sha1 = HASH_MAP[models.PGPSignatureModel.SHA1]
        self.assertEqual(hash_str, str(sha1))

    def test_eddsa_algorithm_str(self):
        first = self.CAROL.public_keys.first()
        algorithm_str = first.algorithm_str()
        PKA_MAP = models.PGPPublicKeyModel.PKA_MAP
        eddsa_enc_sign = PKA_MAP[models.PGPPublicKeyModel.EDDSA]
        self.assertEqual(algorithm_str, str(eddsa_enc_sign))

    def test_simple_eddsa_algorithm_str(self):
        first = self.CAROL.public_keys.first()
        simple_str = first.simple_algorithm_str()
        SIMPLE_PKA_MAP = models.PGPPublicKeyModel.SIMPLE_PKA_MAP
        simple_eddsa = SIMPLE_PKA_MAP[models.PGPPublicKeyModel.EDDSA]
        self.assertEqual(simple_str, str(simple_eddsa))

    def test_pka_eddsa_str(self):
        first = self.CAROL.signatures.first()
        pka_str = first.pka_str()
        PKA_MAP = models.PGPSignatureModel.PKA_MAP
        eddsa_enc_sign = PKA_MAP[models.PGPSignatureModel.EDDSA]
        self.assertEqual(pka_str, str(eddsa_enc_sign))

    def test_simple_pka_eddsa_str(self):
        first = self.CAROL.signatures.first()
        simple_pka_str = first.simple_pka_str()
        SIMPLE_PKA_MAP = models.PGPSignatureModel.SIMPLE_PKA_MAP
        simple_eddsa = SIMPLE_PKA_MAP[models.PGPSignatureModel.EDDSA]
        self.assertEqual(simple_pka_str, str(simple_eddsa))


class PGPDBViewTest(TestCase):
    def setUp(self):
        self.CLIENT = Client()

    def test_index(self):
        uri = reverse('pgpdb:index')
        resp = self.CLIENT.get(uri)
        self.assertTemplateUsed(resp, 'pgpdb/index.html')

    def test_add(self):
        uri = reverse('pgpdb:add')

        data = {
            'keytext': GPG_ALICE_KEY,
        }
        resp = self.CLIENT.post(uri, data=data)
        self.assertTemplateUsed(resp, 'pgpdb/added.html')

        # invalid post
        data = {
            'keytext': 'INVALID_POST',
        }
        resp = self.CLIENT.post(uri, data=data)
        self.assertTemplateUsed(resp, 'pgpdb/add_invalid_post.html')

        # GET method
        resp = self.CLIENT.get(uri)
        self.assertTemplateUsed(resp, 'pgpdb/add_method_not_allowed.html')

    def test_add_multi(self):
        uri = reverse('pgpdb:add')

        self.assertEqual(models.PGPKeyModel.objects.all().count(), 0)

        data = {
            'keytext': PGPDB_MULTI_KEY,
        }
        resp = self.CLIENT.post(uri, data=data)
        self.assertTemplateUsed(resp, 'pgpdb/added.html')

        self.assertEqual(models.PGPKeyModel.objects.all().count(), 2)
        first = models.PGPKeyModel.objects.all().first()
        last = models.PGPKeyModel.objects.all().last()
        self.assertEqual(first.ascii_armor(), PGPDB_ALICE_KEY)
        self.assertEqual(last.ascii_armor(), PGPDB_BOB_KEY)

    def test_lookup(self):
        uri = reverse('pgpdb:lookup')

        data = {
            'op': 'index',
            'search': '0xd5d7da71c354960e',
        }
        resp = self.CLIENT.get(uri, data=data)
        self.assertTemplateUsed(resp, 'pgpdb/lookup_not_found.html')

        models.PGPKeyModel.objects.save_to_storage(None, GPG_ALICE_KEY)

        data = {
            'op': 'index',
            'search': '0xd5d7da71c354960e',
        }
        resp = self.CLIENT.get(uri, data=data)
        self.assertTemplateUsed(resp, 'pgpdb/lookup_index.html')

        data = {
            'op': 'vindex',
            'search': '0xd5d7da71c354960e',
        }
        resp = self.CLIENT.get(uri, data=data)
        self.assertTemplateUsed(resp, 'pgpdb/lookup_vindex.html')

        data = {
            'op': 'get',
            'search': '0xd5d7da71c354960e',
        }
        resp = self.CLIENT.get(uri, data=data)
        self.assertTemplateUsed(resp, 'pgpdb/lookup_get.html')

    def test_lookup_mr(self):
        uri = reverse('pgpdb:lookup')

        data = {
            'op': 'index',
            'options': 'mr',
            'search': '0xd5d7da71c354960e',
        }
        resp = self.CLIENT.get(uri, data=data)
        self.assertEqual(resp.status_code, 404)

        models.PGPKeyModel.objects.save_to_storage(None, GPG_ALICE_KEY)

        data = {
            'op': 'index',
            'options': 'mr',
            'search': '0xd5d7da71c354960e',
        }
        resp = self.CLIENT.get(uri, data=data)
        self.assertEqual(resp['Content-Type'], 'text/plain')
        self.assertEqual(resp.content.decode("ascii"), MACHINE_READABLE_INDEX1)

        data = {
            'op': 'get',
            'options': 'mr',
            'search': '0xd5d7da71c354960e',
        }
        resp = self.CLIENT.get(uri, data=data)
        self.assertEqual(resp['Content-Type'], 'application/pgp-keys')
        self.assertEqual(resp.content.decode("ascii"), PGPDB_ALICE_KEY)

        models.PGPKeyModel.objects.save_to_storage(None, GPG_BOB_KEY)

        data = {
            'op': 'index',
            'options': 'mr',
            'search': 'example',
        }
        resp = self.CLIENT.get(uri, data=data)
        self.assertEqual(resp['Content-Type'], 'text/plain')
        self.assertEqual(resp.content.decode("ascii"), MACHINE_READABLE_INDEX2)

        data = {
            'op': 'get',
            'options': 'mr',
            'search': 'example',
        }
        resp = self.CLIENT.get(uri, data=data)
        self.assertEqual(resp['Content-Type'], 'application/pgp-keys')
        self.assertEqual(resp.content.decode("ascii"), PGPDB_MULTI_KEY)
