import os
import time
import glob
import RPi.GPIO as GPIO

class Device:
    (IN,OUT,IO) = [0,1,2]
    (DISCRETE,W1,SPI, PWM) = [0,1,2,3]
    def __init__(self, direction=0, device_type=0, gpio=None):
        self.set_type(device_type)
        self.set_direction(direction)
        if gpio is not None:
            self.set_gpio(gpio,direction)

    @staticmethod
    def factory(dtype, direction=0, gpio=None, path=None):
        if direction == Device.IN:
            if dtype == Device.W1: return W1Sensor(gpio, path)
            if dtype == Device.DISCRETE: return DiscreteSensor(gpio)
        elif direction == Device.OUT:
            if dtype == Device.PWM: return PWMDevice(gpio)

    def update(self):
        raise NotImplementedError('This method has to be implemented within a subclass!')

    def run(self):
        raise NotImplementedError('This method has to be implemented within a subclass!')

    def set_gpio(self, gpio, direction):
        gpio = int(gpio)
        if gpio in range(2,28):
            GPIO.setmode(GPIO.BCM)
            if direction == self.IN:
                GPIO.setup(gpio, GPIO.IN)
            elif direction == self.OUT:
                GPIO.setup(gpio, GPIO.OUT)
            self._gpio = gpio
        else:
            raise ValueError('Not a valid GPIO number. Available GPIO pins are <2;27>.')

    def get_gpio(self):
        return self._gpio

    def set_direction(self, direction):
        if direction in range(0,3):
            self._direction = direction
        else:
            raise ValueError('Invalid direction. Supported: Device.IN, Device.OUT, Device.IO.')

    def set_type(self, dtype):
        if dtype in range(0,4):
            self._type = dtype
        else:
            raise ValueError('Invalid device type. Supported: Device.DISCRETE, Device.W1, Device.SPI.')

    def get_params(self):
        return {'gpio': self._gpio, 'type': self._type, 'direction': self._direction}

    def get_value(self):
        return self._value

class W1Sensor(Device):
    def __init__(self, gpio=4, path=None):
        Device.__init__(self, Device.IN, Device.W1, gpio)
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

    def get_params(self):
        return {'gpio': self._gpio, 'type': self._type, 'direction': self._direction, 'path': self._path}

class DiscreteSensor(Device):
    def __init__(self, gpio=4):
        Device.__init__(self, Device.IN, Device.DISCRETE, gpio)
    def update(self):
        self._value = GPIO.input(self._gpio)
        return self._value

class PWMDevice(Device):
    def __init__(self,gpio=27):
        Device.__init__(self, Device.OUT, Device.PWM, gpio)
    def run(self, freq, tm):
        if(freq==0):
            time.sleep(tm)
            return
        T = 1.0 / freq
        delay = T / 2
        nofCycles = int(tm * freq)
        for i in range(nofCycles):
            GPIO.output(self._gpio, True)
            time.sleep(delay)
            GPIO.output(self._gpio, False)
            time.sleep(delay)

class DeviceList:
    def __init__(self):
        self._devices = []
        self._handles = []

    def add_device(self, name, device):
        self._devices.append({'name':name, 'value':0.0})
        self._handles.append(device)

    def update_all(self):
        for device, handle in zip(self._devices, self._handles):
            device['value'] = handle.update()

    def get_list(self):
        return self._devices

    def get_value(self, idx):
        return self._devices[idx]['value']

    def get_value_by_name(self, name):
        for d in self._devices:
            if d['name'] == name:
                return d['value']
        return None

    def get_handle(self, idx):
        return self._handles[idx]

    def update_device_settings(self, name, gpio=None, path=None, dtype=None, direction=None):
        found = False
        for device, handle in zip(self._devices, self._handles):
            if device['name'] == name:
                handle.set_gpio(gpio, direction) if gpio is not None else 0
                handle.set_type(dtype) if dtype is not None else 0
                handle.set_direction(direction) if direction is not None else 0
                if dtype == Device.W1:
                    handle.set_path(path)
                found = True
                break

        if found == False:
            print('\nCreating new device. gpio: {}'.format(gpio))
            self.add_device(name, Device.factory(dtype, direction, gpio, path))

        return found

    def get_settings_list(self):
        l = []
        for device, handle in zip(self._devices, self._handles):
            d = handle.get_params()
            d['name'] = device['name']
            l.append(d)
        return l

    def update_list(self, devices):
        # Update existing devices or add new ones
        for new_device in devices:
            self.update_device_settings(new_device['name'], new_device.get('gpio'), new_device.get('path'), new_device['type'], new_device['direction'])

        # Remove deconfigured devices
        new_device_names = [new_device['name'] for new_device in devices]
        for device, handle in zip(self._devices[:], self._handles[:]):
            if device['name'] not in new_device_names:
                self._devices.remove(device)
                self._handles.remove(handle)

'''
#Testing stuff
sensor1 = W1Sensor(4, W1Sensor.list_available_sensors()[0])
sensor1.update()
print(sensor1.get_value())
'''
