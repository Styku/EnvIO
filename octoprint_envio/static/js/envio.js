$(function() {
    function EnvioViewModel(parameters) {
        var self = this;

        self.global_settings = parameters[1];
        self.sensor_settings = ko.observableArray();
        self.devices = ko.observableArray();
        self.devTypesId = [0, 1];
        self.devTypesLabels = ['Discrete', 'W1'];
        self.devTypes = [{'name':'Discrete', 'id':0},{'name':'W1', 'id':1}];
        self.onBeforeBinding = function(){
            self.sensor_settings(self.global_settings.settings.plugins.envio.sensors())
        }
        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "envio") { return; }
            self.devices(data);
        };

        self.addDevice = function(){
            self.sensor_settings.push({'name':'New sensor','gpio':2,'path':'/sys/bus/w1/devices/', 'direction':0, 'type':0});
            alert(ko.toJSON(self.sensor_settings));
        };

        self.removeDevice = function(){
            self.sensor_settings.remove(this);
        };
    }

    ADDITIONAL_VIEWMODELS.push({
        construct: EnvioViewModel,
        dependencies: ["temperatureViewModel", "settingsViewModel"],
        elements: ["#navbar_plugin_envio", "#settings_plugin_envio"]
    });
});
