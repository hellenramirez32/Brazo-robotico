#De la función machine importamos PIN, TIMER,PWM
#De time importamos sleep_ms
# Y por último importamos la función ubluetooth

from machine import Pin, Timer, PWM 
from time import sleep_ms
import ubluetooth


#   4.Declaramos 3 variables, las cuales le asignamos los pines de conexión que
#tenemos en la ESP32 y la frecuencia con la que se trabaja con los servomotores.

servobase = PWM(Pin(14), freq = 50)        
servocodo= PWM(Pin(12), freq = 50)
servomano = PWM(Pin(13), freq = 50)

#  5.Definimos la función map, en la cual creamos una fórmula que nos permite
#llegar con exactitud a los diferentes ángulos o GDL, que estemos configurando a los servomotores.
def map(x):
    return int((x - 0) * (130- 34) / (180 - 0) + 34)


#.En este apartado podemos ver la configuración del interprete en este caso la aplicación móvil
#que descarguemos y que posea conexión a bluetooth, con el fin de empalmar con la ESP32.
class BLE():
    def __init__(self, name):   
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)

        self.led = Pin(2, Pin.OUT)
        self.timer1 = Timer(0)
        self.timer2 = Timer(1)
        
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

    def connected(self):        
        self.timer1.deinit()
        self.timer2.deinit()

    def disconnected(self):        
        self.timer1.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(1))
        sleep_ms(200)
        self.timer2.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(0))   

    def ble_irq(self, event, data):
        if event == 1:
            '''Central disconnected'''
            self.connected()
            self.led(1)
        
        elif event == 2:
            '''Central disconnected'''
            self.advertiser()
            self.disconnected()
        
        elif event == 3:
            '''New message received'''
          
            buffer = self.ble.gatts_read(self.rx)
            message = buffer.decode('UTF-8').strip()
            ble.send('Esp dice:' + str(message))
            ble.send('Esp dice:' + str("bienvenidos:"))
            print(message)
            
            
    #Insertamos la sentencia if, que se utiliza para ejecutar un bloque
    #de código si, que nos permita enviar un ángulo al momento de escribir
    #una letra en la aplicación móvil, esto los hacemos con cada una de las
    #partes del brazo, indicando que ángulos va a ejecutar según la función que realice.
            
            if message == 'c':
                m = map(45)
                servobase.duty(m)
                print(m)
                ble.send(str('Angulo de 45 Grados'))
                
            if message == 'b':
                m = map(90)
                servobase.duty(m)
                print(m)
                ble.send(str('Angulo de 90 Grados'))
            
                
                '''servouno'''
                
                
            if message == 'a':
                m = map(0)
                servocodo.duty(m)
                print(m)
                ble.send(str('Angulo de 0 Grados'))
            
            if message == 'e':
                m = map(45)
                servocodo.duty(m)
                print(m)
                ble.send(str('Angulo de 45 Grados'))
                
            if message == 'f':
                m = map(90)
                servocodo.duty(m)
                print(m)
                ble.send(str('Angulo de 90 Grados'))
            
            if message == 'd':
                m = map(125)
                servocodo.duty(m)
                print(m)
                ble.send(str('Angulo de 125 Grados'))
            
                    
                
                '''servodos'''
                
            if message == 'g':
                m = map(0)
                servomano.duty(m)
                print(m)
                ble.send(str('Angulo de 0 Grados'))
            
            if message == 'h':
                m = map(45)
                servomano.duty(m)
                print(m)
                ble.send(str('Angulo de 45 Grados'))
                
#De las líneas de register , el servicio NUS es el servicio bluethooth LE GATT
#Nordic UART es un servicio personalizado que recibe y escribe datos y sirve como puente a la interfaz UART.
#El UUID de servicio específico del proveedor de 128 bits es el numero en verde, propio de las tarjetas.
#El RX escribe datos para enviarlos a la interfaz UART
     
          
           
    def register(self):        
        # Nordic UART Service (NUS)   
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
            
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)
            
        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART, )
        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        self.ble.gatts_notify(0, self.tx, data + '\n')

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        self.ble.gap_advertise(100, bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name)
        


ble = BLE("ESP32Hellen")
