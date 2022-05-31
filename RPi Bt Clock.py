import utime
from machine import I2C, Pin, UART, ADC
from machine_i2c_lcd import I2cLcd
import _thread


sensor_temp = ADC(4)
convert = 3.3 / 65535

reset_button = Pin(10,Pin.IN, Pin.PULL_DOWN)

DEFAULT_I2C_ADDR = 0x27
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

uart = UART(1,9600)


def clock_logic():
    global seconds, minutes, hours, day, month, year
    if seconds == 60:
        seconds = 0
        minutes += 1
        if minutes == 60:
            minutes = 0
            hours += 1
            if hours == 24:
                hours = 0
                day += 1
                if month == 12:
                    if day == 31:
                        day = 1
                        month = 1
                        year += 1
                if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10:
                    if day == 31:
                        day = 1
                        month += 1
                if month == 4 or month == 6 or month == 9 or month == 11:
                    if day == 30:
                        day = 1
                        month += 1
                if month ==2:
                    if year % 4 == 0:
                        if day == 29:
                            day ==1
                            month += 1
                    else:
                        if day == 29:
                            day = 1
                            month += 1

def strings_to_display():
    global seconds, minutes, hours, day, month, year, secstr, minstr, hourstr, daystr, monthstr, yearstr, timestr, datestr, temperature, tempstr
    if seconds >= 10:
        secstr = str(seconds)
    else:
        secstr = "0" + str(seconds)
    if minutes >= 10:
        minstr = str(minutes)
    else:
        minstr = "0" + str(minutes)
    if hours >= 10:
        hourstr = str(hours)
    else:
        hourstr = "0" + str(hours)
    if day >= 10:
        daystr = str(day)
    else:
        daystr = "0" + str(day)
    if month >= 10:
        monthstr = str(month)
    else:
        monthstr = "0" + str(month)
    #year not needed
    yearstr = str(year)
    timestr = hourstr + ":" + minstr + ":" + secstr
    datestr = daystr + "/" + monthstr +"/" + yearstr
    tempstr = str(round(temperature,1)) + "C"

def get_temp():
    global reading, temperature
    reading = sensor_temp.read_u16() * convert
    temperature = 27 - (reading -0.706)/0.001721

def display():
    global timestr, tempstr, datestr
    lcd.putstr(timestr + "   " + tempstr + datestr)


def format_date():
    global day, month, year
    day = int(date[0:2])
    month = int(date[3:5])
    year = int(date[6:10])
    
    print("formatted date")
    
def format_time():
    global seconds, minutes, hours
    hours = int(time[0:2])
    minutes = int(time[3:5])
    seconds = int(time[6:8])
    print("formatted time")
    print("its"+ str(hours) + ":" +str(minutes)+":"+str(seconds))
a = 0



while True:
    seconds = 0
    minutes = 0
    hours = 0
    day = 0
    month = 0
    year = 0
    time = ""
    date = ""
    reading = 0
    temperature = 0
    secstr =""
    minstr=""
    hourstr=""
    daystr=""
    monthstr=""
    yearstr=""
    timestr=""
    datestr=""
    tempstr=""
    booltokill = False
    uart.write("Enter the date (format dd/mm/yyyy)\n")
    lcd.clear()
    lcd.putstr("Enter the date")

    while True:
        if uart.any():
            tempstr = str(uart.readline()).replace("b","")
            tempstr = tempstr.replace("'","")
            date += tempstr
            if len(date) == 10:
                
                break
    uart.write("Enter the time (format hh:mm:ss)")
    lcd.clear()
    lcd.putstr("Enter the time")

    while True:
        if uart.any():
            tempstr = str(uart.readline()).replace("b","")
            tempstr = tempstr.replace("'","")
            time += tempstr
            if len(time) == 8:
                
                break
            
    format_time()
    format_date()


    while True:
        start = utime.ticks_us()
        seconds += 1
        for i in range(900):
            utime.sleep_ms(1)
            if reset_button.value() == 1:
                booltokill = True
        if booltokill:
            uart.write("App was reset \n")
            lcd.clear()
            lcd.putstr("Resetting")
            utime.sleep(1)
            lcd.clear()
            break
        lcd.clear()
        clock_logic()
        get_temp()
        strings_to_display()
        display()
        
        while True:
            stop = utime.ticks_us()
            if stop-start >= 999990:
                break
        stop = utime.ticks_us()
        print(stop-start)
        

        
    
    
    
    
    
    

        
