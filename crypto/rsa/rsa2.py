import binascii

import gmpy2
import hashlib

N = 101991809777553253470276751399264740131157682329252673501792154507006158434432009141995367241962525705950046253400188884658262496534706438791515071885860897552736656899566915731297225817250639873643376310103992170646906557242832893914902053581087502512787303322747780420210884852166586717636559058152544979471
e = 46731919563265721307105180410302518676676135509737992912625092976849075262192092549323082367518264378630543338219025744820916471913696072050291990620486581719410354385121760761374229374847695148230596005409978383369740305816082770283909611956355972181848077519920922059268376958811713365106925235218265173085


p=9046853915223503351787031888977627106934564043204783593118678181991596316582877057556463152579621699010610569526573031954779520781448550677767565207407183
q=11273732364123571293429600400343309403733952146912318879993851141423284675797325272321856863528776914709992821287788339848962916204774010644058033316303937

phi=(p-1)*(q-1)
d=gmpy2.invert(e,phi)
flag = "flag{" + hashlib.md5(hex(d).encode('utf-8')).hexdigest() + "}"

print(flag)

#flag = "flag{" + hashlib.md5(hex(d)).hexdigest() + "}"

