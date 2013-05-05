#!/usr/bin/env python
import sys
import inspect


class BackendPluginFactory(object):

    def create(self, plugin_name="mongodb", **kwargs):
        """Import the needed lib and return an object NmapBackendPlugin
           representing the backend of your desire.
           NmapBackendPlugin is an abstract class, to know what argument
           need to be given, review the code of the subclass you need
        """
        backendplugin = None
        plugin_path = "libnmap.plugins.%s" % (plugin_name)
        __import__(plugin_path)
        pluginobj = sys.modules[plugin_path]
        pluginclasses = inspect.getmembers(pluginobj, inspect.isclass)
        for classname, classobj in pluginclasses:
            if inspect.getmodule(classobj).__name__.find(plugin_path) == 0:
                backendplugin = classobj(**kwargs)
        return backendplugin
