import datetime
now = datetime.datetime.now()
def getshift():
    if int(now.hour) in (6,7,8,9,10,11,12,13):
        return 'shift1'
    if  int(now.hour)  in (14,15,16,17,18,19,20,21):
        return 'shift2'
    if  int(now.hour)  in (22,23,0,1,2,3,4,5) :
        return 'shift3'
    
    