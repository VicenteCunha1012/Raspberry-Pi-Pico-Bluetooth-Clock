# Raspberry-Pi-Pico-Bluetooth-Clock
Raspberry Pi Pico Clock/Thermometer/Calendar made with Circuitpython
LCD API for LCD1602 made by T-622 at https://github.com/T-622/RPI-PICO-I2C-LCD                              
From https://github.com/T-622/RPI-PICO-I2C-LCD lcd_api.py and lcd_i2c_lcd.py are required to run this program
___________________________
GPIO -SCL-    -I2C Adapter                                                
GPI1 -SDA-    -I2C Adapter                                              
GPI3 -RX(HC06)                                                         
GPI4 -TX(HC06)                                                        
GPI10-Button                                                           
___________________________
All VCC pins are on 5V (VBUS)
All GND pins can be connected to any GND on the pico

Hardware:
-Raspberry Pi Pico                                                  
-LCD 1602 16x2                                                  
-HC06 Bluetooth Module                                                  
-I2C Adapter for LCD1602                                                  



