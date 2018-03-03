import time,datetime,ttTools,json,operator,os.path

fullScheduleJson=ttTools.loadJson(ttTools.getFull())

shows=fullScheduleJson['upcomingAirings']['shows']
if os.path.isfile("old.json"):
    old=ttTools.loadJson("old.json")
else:
    old=[]
if os.path.isfile("nep.json"):
    old_nep=ttTools.loadJson("nep.json")
else:
    old_nep=[]

zero=[]
for x in old_nep:
    if x[0]==0:
        zero.append(x)

nep=[]
for x in shows:
    title=x['title']
    for y in x['programs']:
        episodeTitle=y.setdefault('episodeTitle', 'Unnamed '+title)
        description=y.setdefault('description', 'No Description.')
        # for z in y['schedules']:
        z=y['schedules'][0]
        if z['isNew']:
            stationName=z['station']['name']
            date=z['date']
            timee=z['time']
            endTime=z['endTime']
            tvRating=z.setdefault('tvRating', 'Unrated')
            airInfo=[0]
            airInfo += ttTools.splitDate(date)
            airInfo += ttTools.splitTime(timee)
            airInfo += ttTools.splitTime(endTime)
            airInfo[0]=time.mktime(datetime.datetime(airInfo[1],airInfo[2],airInfo[3],airInfo[4],airInfo[5],0).timetuple())+18000
            stationName=ttTools.stationNameAlias(stationName)
            if stationName == "Cartoon Network" and (airInfo[4] < 6 or airInfo[4]>= 20 ):
                stationName="Adult Swim"
            airInfo.append(stationName)
            airInfo.append(title)
            airInfo.append(episodeTitle)
            airInfo.append(description)
            date = z['date']

            if bool(zero):
                for i in zero:
                    if airInfo[10]==i[10]:
                        airInfo[0]=0
                        nep.append(airInfo)
                        break

            if airInfo[0]<time.time()+60:
                oldlen=len(old)
                for x in range(1,oldlen):
                    if old[-x][10]==airInfo[10]:
                        break
                else:
                    old.append(airInfo)
            else:
                nep.append(airInfo)
        else:
            continue
nep.sort(key=operator.itemgetter(0))



ttTools.storeJson(nep,"nep.json")
ttTools.storeJson(old,"old.json")
print(time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()+28800)))
