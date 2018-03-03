import json
import urllib.request
import codecs

def storeJson(data,a):
    with open(a, 'w+') as json_file:
        json_file.write(json.dumps(data))

def loadJson(a):
        with open(a) as json_file:
            data = json.load(json_file)
            return data

def makeUrl(fileName="EPlist.txt"):
    f=open(fileName,"r")
    all=f.readlines()
    f.close()
    url="http://api.zap2it.com/tvlistings/webservices/upcomingAirings?sid="
    for x in all:
        url+=x.strip().split('#')[0]
        if x!=all[-1]:
            url += ","
        else:
            url += "&zip=10003"
    return url

def getFull(url=makeUrl(),fileName="schedule.json"):
    f=codecs.open(fileName,"w+","utf-8")
    a=urllib.request.urlopen(url).read().decode('utf-8','strict')
    print(a)
    f.write(a)
    f.close()
    return fileName

def to24(h,ap):
    h=int(h)
    if h==12:
        if ap.upper()=="AM":
            return 0
        if ap.upper()=="PM":
            return 12
    else:
        if ap.upper()=="AM":
            return h
        if ap.upper()=="PM":
            return h+12

def splitDate(date):
    return [int(each) for each in date.split("-")]

def splitTime(time):
    return [to24(time.split(" ")[0].split(":")[0],time.split(" ")[1]),int(time.split(" ")[0].split(":")[1])]

def stationNameAlias(name,file="alias.txt"):
    f=open(file,"r+");
    all=f.readlines();
    f.close();
    dic={}
    for x in all:
        x=x.strip().split('#')
        dic[x[0]]=x[1]
    return dic.setdefault(name,name)



