import unittest
import Device

class W1SensorTestCase(unittest.TestCase):
    def setUp(self):
        self.dev = Device.W1Sensor(4, Device.W1Sensor.list_available_sensors()[0])

    def tearDown(self):
        self.dev = None

    def test_list_w1_devices(self):
        sensor_list = Device.W1Sensor.list_available_sensors()
        self.assertTrue(len(sensor_list))

    def test_update(self):
        val = self.dev.update()
        self.assertTrue(val > 0)

    def test_set_gpio(self):
        self.dev.set_gpio(5, Device.Device.IN)
        self.assertEqual(self.dev.get_gpio(), 5)

class DiscreteSensorTestCase(unittest.TestCase):
    def setUp(self):
        self.dev = Device.DiscreteSensor(17)

    def tearDown(self):
        self.dev = None

    def test_update(self):
        val = self.dev.update()
        self.assertTrue(val > 0)

    def test_set_gpio(self):
        self.dev.set_gpio(5, Device.Device.IN)
        self.assertEqual(self.dev.get_gpio(), 5)

class PWMDeviceTestCase(unittest.TestCase):
    def setUp(self):
        self.dev = Device.PWMDevice(27)

    def tearDown(self):
        self.dev = None

    def test_run(self):
        self.dev.run(440, 3)
        self.assertTrue(True)

class DeviceListTestCase(unittest.TestCase):
    def setUp(self):
        self.list = Device.DeviceList()

    def tearDown(self):
        self.list = None

    def test_add_device(self):
        self.list.add_device('dev1', Device.W1Sensor(4, Device.W1Sensor.list_available_sensors()[0]))
        self.list.add_device('dev2', Device.DiscreteSensor(6))
        self.assertEqual(len(self.list.get_list()), 2)

    def test_update_settings(self):
        self.list.add_device('dev1', Device.W1Sensor(4, Device.W1Sensor.list_available_sensors()[0]))
        self.list.add_device('dev2', Device.DiscreteSensor(17))
        self.list.add_device('dev3', Device.DiscreteSensor(6))
        settings = self.list.get_settings_list()
        settings[1]['gpio'] = 8
        self.list.update_list(settings)
        new_settings = self.list.get_settings_list()
        self.assertEqual(new_settings[1]['gpio'], 8)

    def test_update_remove_settings(self):
        self.list.add_device('dev1', Device.W1Sensor(4, Device.W1Sensor.list_available_sensors()[0]))
        self.list.add_device('dev2', Device.DiscreteSensor(17))
        self.list.add_device('dev3', Device.DiscreteSensor(6))
        settings = []
        settings.append({'name':'dev2', 'gpio': 4, 'direction':Device.Device.IN, 'path':None, 'type':Device.Device.DISCRETE})
        self.list.update_list(settings)
        self.assertEqual(len(self.list.get_list()), 1)


w1_suite = unittest.TestLoader().loadTestsFromTestCase(W1SensorTestCase)
discrete_suite = unittest.TestLoader().loadTestsFromTestCase(DiscreteSensorTestCase)
device_list_suite = unittest.TestLoader().loadTestsFromTestCase(DeviceListTestCase)
pwm_suite = unittest.TestLoader().loadTestsFromTestCase(PWMDeviceTestCase)
alltests = unittest.TestSuite([w1_suite, discrete_suite, device_list_suite,pwm_suite])
unittest.TextTestRunner(verbosity=2).run(alltests)
