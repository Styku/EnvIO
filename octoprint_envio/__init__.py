# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from octoprint.util import RepeatedTimer

class EnvioPlugin(octoprint.plugin.StartupPlugin, octoprint.plugin.TemplatePlugin, octoprint.plugin.AssetPlugin, octoprint.plugin.SettingsPlugin):
    def __init__(self):
        self._sensorTimer = None
        self.sensor_refresh_rate = 5.0

    def read_sensors(self):
        path = '/sys/bus/w1/devices/28-0416c0d320ff/w1_slave'
        f = open(path, 'r')
        temp = -1
        for line in f:
            start = line.find('t=')
            if start >= 0:
                temp = float(line[(start + 2):])/1000.0
        f.close()
        self._logger.info("Refreshing temperature...")
        self._plugin_manager.send_plugin_message(self._identifier, dict(temperature=round(temp, 1)))

    def get_settings_defaults(self):
        return dict(sensor_refresh_rate=self.sensor_refresh_rate)

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

        self.sensor_refresh_rate = float(self._settings.get(["sensor_refresh_rate"]))
        self._logger.info("Setting refresh rate to {}".format(self.sensor_refresh_rate))
        if self._sensorTimer is not None:
            try:
                self._sensorTimer.cancel()
            except:
                pass
        self.start_timer()

    def on_after_startup(self):
        self.sensor_refresh_rate = float(self._settings.get(["sensor_refresh_rate"]))
        self.start_timer()

    def start_timer(self):
        self._sensorTimer = RepeatedTimer(self.sensor_refresh_rate, self.read_sensors, None, None, True)
        self._sensorTimer.start()

    def get_assets(self):
        return {
                "js": ["js/envio.js"]
        }

__plugin_implementation__ = EnvioPlugin()
