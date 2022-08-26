import conf, json,time,math,statistics,requests
from boltiot import Sms,Bolt

def compute_bounds(history_data,frame_size,factor):
    if len(history_data)<frame_size:
        return None
    if len(history_data)>frame_size:
        del history_data[0:len(history_data)-frame_size]

    Mn=statistics.mean(history_data)
    Variance=0
    for data in history_data:
        Variance+=math.pow((data-Mn),2)
    Zn=factor*math.sqrt(Variance/frame_size)
    High_bound =history_data[frame_size-1]+Zn
    Low_bound=history_data[frame_size-1]-Zn
    return [High_bound,Low_bound]
def get_sensor_value_from_pin(pin):
    """Return the sensor value .return -999 if request fails"""
    try:
        response =mybolt.analogRead(pin)
        data =json.loads(response)
        if data["success"]!=1:
            print("Request not successfull

mybolt=Bolt(conf.API_KEY,conf.DEVICE_ID)
sms= Sms(conf.SSID,conf.AUTH_TOKEN,conf.TO_NUMBER,conf.FROM_NUMBER)
history_data=[]

while True:
    response=mybolt.analogRead('A0')
    data=json.loads(response)
    if data['success']!=1:
        print("There was an error while retriving the data.")
        print("This is the error:"+data['value'])
        time.sleep(5)
        continue
    print("This is the vallue "+data['value'])
    sensor_value=0
    try:
        sensor_value=int(data['value'])
    except e:
        print("There was an error while parsing the response:",e)
        continue
    bound=compute_bounds(history_data,conf.FRAME_SIZE,conf.MUL_FACTOR)
    if not bound:
        required_data_count=conf.FRAME_SIZE-len(history_data)
        print("Not enough data to compute Z-score. Need ",required_data_count," more data points")
        history_data.append(int(data['value']))
        time.sleep(10)
        continue
    try:
        if sensor_value>bound[0]:
            response=mybolt.digitalWrite('1', 'HIGH' )
            print(response)
            print("The light level incresed suddenly. Sending  an SMS.")
            response=sms.send_sms("SOMEONE UNLOCKED YOUR LOCKER!!!")
            print("This is the reponse",reponse)
        elif sensor_value<bound[1]:
            print ("The light level decresed suddenly. Sending an SMS.")
            response=sms.send_sms("Someone locked your locker!!")
            print("This the the response",response)
        history_data.append(sensor_value);
    except Exception as e:
        print ("Error",e)
    time.sleep(4)
