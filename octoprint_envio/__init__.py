# coding=utf-8
import Device

import octoprint.plugin
from octoprint.util import RepeatedTimer


class EnvioPlugin(octoprint.plugin.StartupPlugin, octoprint.plugin.TemplatePlugin, octoprint.plugin.AssetPlugin, octoprint.plugin.SettingsPlugin):
    def __init__(self):
        self._sensorTimer = None
        self.sensor_data = {'global_refresh_rate': 5.0, 'sensor': []}
    def read_sensors(self):
        data = {}
        for s in self.sensor_data['sensor']:
            s['value'] = s['handle'].update()
            data[s['name']] = round(s['value'], 1)

        self._plugin_manager.send_plugin_message(self._identifier, data)
        self._logger.info('Refreshing temperature: {}'.format(self.sensor_data['sensor'][0]['handle'].get_value()))

    def get_settings_defaults(self):
        return dict(sensor_refresh_rate=self.sensor_data['global_refresh_rate'])

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

        self.sensor_data['global_refresh_rate'] = float(self._settings.get(["sensor_refresh_rate"]))
        self._logger.info("Setting refresh rate to {}".format(self.sensor_data['global_refresh_rate']))
        if self._sensorTimer is not None:
            try:
                self._sensorTimer.cancel()
            except:
                pass
        self.start_timer()

    def on_after_startup(self):
        self.sensor_data['global_refresh_rate'] = float(self._settings.get(["sensor_refresh_rate"]))
        self.sensor_data['sensor'].append({'name':'temperature', 'value':0, 'handle':Device.Sensor(stype=Device.Sensor.W1, path=Device.list_w1_devices()[0])
})
        self.start_timer()

    def start_timer(self):
        self._sensorTimer = RepeatedTimer(self.sensor_data['global_refresh_rate'], self.read_sensors, None, None, True)
        self._sensorTimer.start()

    def get_assets(self):
        return {
                "js": ["js/envio.js"]
        }

__plugin_implementation__ = EnvioPlugin()
