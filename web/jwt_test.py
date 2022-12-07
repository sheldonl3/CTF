import jwt

public = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAs+/Ju0JZqKk5Y6EslP+r
KYo01bNzBqK3m3QgD9hgSbLOg0vNUKlYRaCXzQAcavRrjG+GkT2siIcVJmkaI7ij
PRjh0YHOMnacKuLfthYP4X0b3+lxNtAKjDMhEMHXHZdmIz9zPilILCd7DDko8ICF
ebuptjjP0OVNLeXvgVVvgPPPw9tLKda0yae8LNxeq0MHU/fFhAohLYAjqwG9t16m
RWDeKdUTayZMRTPFSnfbbQqCO+ct0GTPkgpbb5Xh1HaYf/aRmcOOBmumZ87UywEY
JWaCxlY00xInuhNw+lDoqY+peAvgY2KMll7jtwKJNK88GuNPx/CDTg6l50Xy0tVU
twIDAQAB
-----END PUBLIC KEY-----
"""

payload = {
    "username": "admin",
    "role": "admin"
}
print(jwt.encode(payload, key=public, algorithm='HS256'))