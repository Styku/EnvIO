# coding=utf-8
import Device

import octoprint.plugin
from octoprint.util import RepeatedTimer


class EnvioPlugin(octoprint.plugin.StartupPlugin, octoprint.plugin.TemplatePlugin, octoprint.plugin.AssetPlugin, octoprint.plugin.SettingsPlugin):
    def __init__(self):
        self._sensorTimer = None
        self._refresh_rate = 5.0
        self._sensors = []

    def read_sensors(self):
        self._sensors.update_all()
        self._plugin_manager.send_plugin_message(self._identifier, self._sensors.get_list())
        #self._logger.info('Refreshing temperature: {}'.format(self._sensors.get_value(0)))

    def get_settings_defaults(self):
        return dict(sensor_refresh_rate=self._refresh_rate,
                    sensors=[])

    def on_settings_save(self, data):
        self._logger.info(data)
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        for device in self._settings.get(["sensors"]):
            self._sensors.add_device(device['name'], Device.W1Sensor(path=device['path']))

        self._refresh_rate = float(self._settings.get(["sensor_refresh_rate"]))
        self._logger.info("Setting refresh rate to {}".format(self._refresh_rate))
        if self._sensorTimer is not None:
            try:
                self._sensorTimer.cancel()
            except:
                pass
        self.start_timer()

    def on_after_startup(self):
        self._refresh_rate = float(self._settings.get(["sensor_refresh_rate"]))
        self._sensors = Device.DeviceList()
       # self._sensors.add_device('temperature', Device.W1Sensor(path=Device.W1Sensor.list_available_sensors()[0]))
        self.start_timer()

    def start_timer(self):
        self._sensorTimer = RepeatedTimer(self._refresh_rate, self.read_sensors, None, None, True)
        self._sensorTimer.start()

    def get_assets(self):
        return {
                "js": ["js/envio.js"]
        }

__plugin_implementation__ = EnvioPlugin()
