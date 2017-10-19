import os
import glob
import RPi.GPIO as GPIO

class Device:
    (IN,OUT,IO) = [0,1,2]
    def __init__(self, direction=0, gpio=None):
        self._direction = direction
        if gpio is not None:
            self.set_gpio(gpio,direction)

    def update(self):
        raise NotImplementedError('This method has to be implemented within a subclass!')

    def set_gpio(self, gpio, direction):
        if gpio in range(2,28):
            GPIO.setmode(GPIO.BCM)
            if direction == self.IN:
                GPIO.setup(gpio, GPIO.IN)
            elif direction == self.OUT:
                GPIO.setup(gpio, GPIO.OUT)
            self._gpio = gpio
        else:
            raise ValueError('Not a valid GPIO number. Available GPIO pins are <2;27>.')

    def get_value(self):
        return self._value

class W1Sensor(Device):
    def __init__(self, gpio=4, path=None):
        Device.__init__(self, Device.IN, gpio)
        if path is not None:
            self.set_path(path)

    def set_path(self, path):
        if os.path.isfile(path):
            self._path = path
        else:
            raise ValueError('File does not exist.')

    def update(self):
        if os.path.isfile(self._path):
            with open(self._path, 'r') as dev_file:
                data = dev_file.read()
            val_pos = data.find('t=')
            if val_pos >= 0:
                self._value = float(data[(val_pos + 2):])/1000.0
            else:
                raise ValueError('Could not parse sensor value. Is the sensor type correct?')
        else:
            raise IOError('File does not exist.')
        return self._value

    @staticmethod
    def list_available_sensors():
        available_sensors = []
        base_path = '/sys/bus/w1/devices/'
        sensors = glob.glob(base_path + '*-*')
        available_sensors = [s + '/w1_slave' for s in sensors]
        return available_sensors

class DiscreteSensor(Device):
    def __init__(self, gpio=4, path=None):
        Device.__init__(self, Device.IN, gpio)
    def update(self):
        self._value = GPIO.input(self._gpio)
        return self._value

class DeviceList:
    def __init__(self):
        self._devices = []

    def add_device(self, name, device):
        self._devices.append({'name':name, 'value':0.0, 'handle':device})

    def update_all(self):
        for device in self._devices:
            device['value'] = device['handle'].update()

    def get_dict(self):
        d = {}
        for i in self._devices:
            d[i['name']] = round(i['value'], 1)
        return d

    def get_value(self, idx):
        return self._devices[idx]['value']

'''
#Testing stuff
sensor1 = W1Sensor(4, W1Sensor.list_available_sensors()[0])
sensor1.update()
print(sensor1.get_value())
'''
