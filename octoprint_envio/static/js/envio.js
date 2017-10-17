$(function() {
    function EnvioViewModel(parameters) {
        var self = this;

        self.global_settings = parameters[1];
        self.temperature = ko.observable();

        self.onBeforeBinding = function(){
            self.settings = self.global_settings.settings.plugins.envio;
        }
        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "envio") { return; }
            self.temperature(data.temperature);
        };
    }

    ADDITIONAL_VIEWMODELS.push({
        construct: EnvioViewModel,
        dependencies: ["temperatureViewModel", "settingsViewModel"],
        elements: ["#navbar_plugin_envio", "#settings_plugin_envio"]
    });
});
