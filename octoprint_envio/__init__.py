# coding=utf-8
import Device

import octoprint.plugin
from octoprint.util import RepeatedTimer


class EnvioPlugin(octoprint.plugin.StartupPlugin, octoprint.plugin.TemplatePlugin, octoprint.plugin.AssetPlugin, octoprint.plugin.SettingsPlugin):
    def __init__(self):
        self._sensorTimer = None
        self._refresh_rate = 5.0
        self._sensors = None
        self._devices = None

    def read_sensors(self):
        self._sensors.update_all()
        if self._sensors.get_value(1) == 0: self._devices.get_handle(0).run(440, 2)
        self._plugin_manager.send_plugin_message(self._identifier, self._sensors.get_list())
        self._logger.info('Refreshing sensors')

    def get_settings_defaults(self):
        return dict(sensor_refresh_rate=self._refresh_rate,
                    sensors=[],
                    devices=[])

    def on_settings_save(self, data):
        self._logger.info('Old data:')
        self._logger.info(self._settings.get(['sensors']))
        self._logger.info('New settings:')
        if 'sensors' in data: data.self._logger.info(data['sensors'])
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

        if 'sensors' in data: self._sensors.update_list(data['sensors'])

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
        self.start_timer()

    def start_timer(self):
        self._sensorTimer = RepeatedTimer(self._refresh_rate, self.read_sensors, None, None, True)
        self._sensorTimer.start()

    def get_assets(self):
        return {
                "js": ["js/envio.js"]
        }

__plugin_implementation__ = EnvioPlugin()
