import os
import glob
import RPi.GPIO as GPIO

class Sensor:
    (DISCRETE, W1, SPI) = (0, 1, 2)
    def __init__(self, stype=0, gpio=None, path=None):
        self.set_type(stype)

        if path is not None:
            self.set_path(path)

        if gpio is not None:
            self.set_gpio(gpio)

    def set_type(self, type):
        if type in range(3):
            self._type = type
        else:
            raise ValueError('Sensor type not supported, allowed types are: Sensor.DISCRETE, Sensor.W1, Sensor.SPI.')

    def set_gpio(self, gpio):
        if gpio in range(2,28):
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(gpio, GPIO.IN)
            self._gpio = gpio

        else:
            raise ValueError('Not a valid GPIO number. Available GPIO pins are <2;27>.')

    def set_path(self, path):
        if os.path.isfile(path):
            self._path = path
        else:
            raise ValueError('File does not exist.')

    def update(self):
        if self._type == self.W1:
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
        elif self._type == self.DISCRETE:
            self._value = GPIO.input(self._gpio)
        elif self._type is None:
            raise ValueError('Sensor type has not been set, cannot update.')
        else:
            raise ValueError('Update methoid is not supported for this type of sensor')
        return self._value

    def list_available_sensors(self):
        available_sensors = []
        if self._type == self.W1:
            base_path = '/sys/bus/w1/devices/'
            sensors = glob.glob(base_path + '*-*')
            available_sensors = [s + '/w1_slave' for s in sensors]
        else:
            raise ValueError('Only W1 type supports device lookup.')
        return available_sensors

    def get_value(self):
        return self._value


def list_w1_devices():
    available_sensors = []
    base_path = '/sys/bus/w1/devices/'
    sensors = glob.glob(base_path + '*-*')
    available_sensors = [s + '/w1_slave' for s in sensors]
    return available_sensors
'''
Testing stuff
sensor1 = Sensor()
sensor1.set_type(Sensor.W1)
path = sensor1.list_available_sensors()[0]
sensor1.set_path(path)
sensor1.update()
print(sensor1.get_value())
'''
