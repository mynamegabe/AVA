import re
ports1 = []
with open('testxml.txt','r') as r:
    content = r.read()
    print(content)
    ports = re.findall(r'portid=\"[\d]*\"',content)
    print(ports)
    for i in ports:
        ports1.append(re.findall(r'\d+',i)[0])
    print(ports1)
    r.close()
