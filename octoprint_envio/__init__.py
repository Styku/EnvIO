# coding=utf-8
import Device

import octoprint.plugin
from octoprint.util import RepeatedTimer
from collections import defaultdict

class EnvioPlugin(octoprint.plugin.StartupPlugin, octoprint.plugin.TemplatePlugin, octoprint.plugin.AssetPlugin, octoprint.plugin.SettingsPlugin):
    def __init__(self):
        self._sensorTimer = None
        self._refresh_rate = 5.0
        self._sensors = None
        self._devices = None
        self._triggers = []

    def read_sensors(self):
        self._sensors.update_all()
        #if self._sensors.get_value(1) == 0: self._devices.get_handle(0).run(440, 2)

        for trigger in self._triggers:
            self._logger.info(trigger)
            if self.compare(value=self._sensors.get_value_by_name(trigger['sensor']), threshold=int(trigger['threshold']), operator=trigger['operator']):
                self._devices.get_handle_by_name(trigger['device']).run(440,2)
        data = {}
        data['sensors'] = self._settings.get(['sensors'])[:]
        data['w1'] = [''] + Device.W1Sensor.list_available_sensors()
        for i in data['sensors']:
            i['value'] = self._sensors.get_value_by_name(i['name'])

        self._plugin_manager.send_plugin_message(self._identifier, data)
        self._logger.info(data)

    def get_settings_defaults(self):
        return dict(sensor_refresh_rate=self._refresh_rate,
                    sensors=[],
                    devices=[],
                    triggers=[])

    def on_settings_save(self, data):
        self._logger.info('New settings:')
        self._logger.info(data)

        if 'devices' in data: self._devices.update_list(data['devices'])
        if 'sensors' in data: self._sensors.update_list(data['sensors'])
        if 'triggers' in data: self._triggers = data['triggers']
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

        self._refresh_rate = float(self._settings.get(['sensor_refresh_rate']))
        self._logger.info("Setting refresh rate to {}".format(self._refresh_rate))
        if self._sensorTimer is not None:
            try:
                self._sensorTimer.cancel()
            except:
                pass
        self.start_timer()

    def on_after_startup(self):
        self._refresh_rate = float(self._settings.get(['sensor_refresh_rate']))
        self._sensors = Device.DeviceList()
        self._devices = Device.DeviceList()
        self._sensors.update_list(self._settings.get(['sensors']))
        self._devices.update_list(self._settings.get(['devices']))
        self._triggers = self._settings.get(['triggers'])
        self.start_timer()

    def start_timer(self):
        self._sensorTimer = RepeatedTimer(self._refresh_rate, self.read_sensors, None, None, True)
        self._sensorTimer.start()

    def get_assets(self):
        return {
                "js": ["js/envio.js"],
                "css": ["css/envio.css"]
        }

    def compare(self, value, threshold, operator):
        return {
                0: value==threshold,
                1: value!=threshold,
                2: value<threshold,
                3: value<=threshold,
                4: value>threshold,
                5: value>=threshold
                }[operator]


__plugin_implementation__ = EnvioPlugin()
