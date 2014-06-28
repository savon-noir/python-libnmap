#!/usr/bin/env python
import sys
import inspect


class BackendPluginFactory(object):
    """
        This is a backend plugin factory a backend instance MUST be
        created via the static method create()
        ie : mybackend = BackendPluginFactory.create()
    """
    @classmethod
    def create(cls, plugin_name="mongodb", **kwargs):
        """Import the needed lib and return an object NmapBackendPlugin
           representing the backend of your desire.
           NmapBackendPlugin is an abstract class, to know what argument
           need to be given, review the code of the subclass you need
           :param plugin_name: str : name of the py file without .py
           :return: NmapBackend (abstract class on top of all plugin)
        """
        backendplugin = None
        plugin_path = "libnmap.plugins.{0}".format(plugin_name)
        __import__(plugin_path)
        pluginobj = sys.modules[plugin_path]
        pluginclasses = inspect.getmembers(pluginobj, inspect.isclass)
        for classname, classobj in pluginclasses:
            if inspect.getmodule(classobj).__name__.find(plugin_path) == 0:
                try:
                    backendplugin = classobj(**kwargs)
                except Exception as error:
                    raise Exception("Cannot create Backend: {0}".format(error))
        return backendplugin
