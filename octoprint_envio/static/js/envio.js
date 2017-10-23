$(function() {
    function EnvioViewModel(parameters) {
        var self = this;

        self.global_settings = parameters[1];
        self.sensor_settings = ko.observableArray();
        self.device_settings = ko.observableArray();

        self.sensors = ko.observableArray();
        self.devices = ko.observableArray();

        self.sensorTypes = [{'name':'Discrete', 'id':0},{'name':'W1', 'id':1}];
        self.devTypes = [{'name':'Discrete', 'id':0},{'name':'PWM', 'id':3}];

        self.onBeforeBinding = function(){
            self.sensor_settings(self.global_settings.settings.plugins.envio.sensors())
            self.device_settings(self.global_settings.settings.plugins.envio.devices())
            self.sensor_refresh_rate = self.global_settings.settings.plugins.envio.sensor_refresh_rate
        }
        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "envio") { return; }
            self.devices(data);
        };

        self.addSensor = function(){
            self.sensor_settings.push({'name':'New sensor','gpio':2,'path':'/sys/bus/w1/devices/', 'direction':0, 'type':0});
        };

        self.removeSensor = function(){
            self.sensor_settings.remove(this);
        };

        self.addDevice = function(){
            self.device_settings.push({'name':'New device','gpio':2,'output':440, 'time':3, 'direction':1, 'type':3});
        };

        self.removeDevice = function(){
            self.device_settings.remove(this);
        };
    }

    ADDITIONAL_VIEWMODELS.push({
        construct: EnvioViewModel,
        dependencies: ["temperatureViewModel", "settingsViewModel"],
        elements: ["#navbar_plugin_envio", "#settings_plugin_envio"]
    });
});
