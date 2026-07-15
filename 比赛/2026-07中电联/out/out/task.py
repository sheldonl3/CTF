g = 916143391925527262831875920931
p = 14396524142538228424993723224595141948383030778566133225922417832357880258148761185020930195532450742879746914027266864394266451377581759004827248578768524336431104

from Crypto.Cipher import AES
from hashlib import sha256
def gen_pub(x,g,p):
    return pow(g,x,p)

def gen_sharekey(A,b):
    share = pow(A,b,p)
    sharekey =  sha256(str(share)).hexdigest()[:16]
    return sharekey

def pad(msg):
    l = 16-(len(msg)%16)
    return  msg+'\x00'*l
def encrypt(sharekey,msg):
    msg = pad(msg)
    aes = AES.new(key,AES.MODE_ECB)
    return aes.encrypt(msg)
