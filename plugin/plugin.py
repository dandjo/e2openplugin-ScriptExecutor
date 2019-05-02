from Screens.Screen import Screen
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Plugins.Plugin import PluginDescriptor
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from os import listdir
from os.path import isdir, isfile, join

scriptDirs = [
    "/usr/scripts",
    "/media/hdd/scripts",
    "/media/usb/scripts"
]
scriptDir = scriptDirs[0]

class ScriptExecutor(Screen):
    skin = """
        <screen name="ScriptExecutor" position="center,center" size="700,556" title="Script Executor">
            <widget name="scriptMenuList" position="5,5" size="690,546" scrollbarMode="showOnDemand" />                                                                  
        </screen>"""

    def __init__(self, session, args=None):
        self.session = session
        files = list()
        for f in listdir(p):
            if not isfile(join(p, f)):
                continue
            files.append((f, join(p, f)))
        files.sort()
        Screen.__init__(self, session)
        self["scriptMenuList"] = MenuList(files)
        self["actionMap"] = ActionMap(["SetupActions"], {
            "ok": self.go,
            "cancel": self.cancel
        }, -1)

    def go(self):
        script = self["scriptMenuList"].l.getCurrentSelection()[1]
        if script is None:
            self.close(None)
        else:
            self.session.open(Console, _(scriptDir), [script])

    def cancel(self):
        self.close(None)

def main(session, **kwargs):
    validDirs = [d for d in scriptDirs if isdir(d)]
    try:
        scriptDir = validDirs[0]
        session.open(ScriptExecutor)
    except IndexError:
        session.open(MessageBox, _("No suitable directory found! "\
            "Be sure to provide one of these paths on your "\
            "filesystem: ['%s']" % "', '".join(scriptDirs)), MessageBox.TYPE_ERROR)
        return None

def Plugins(**kwargs):
    return [PluginDescriptor(
                name="Script Executor",
                description=_("Executes scripts in /usr/scripts/*"),
                where=PluginDescriptor.WHERE_PLUGINMENU,
                fnc=main
            ), PluginDescriptor(
                name="Script Executor",
                description=_("Executes scripts in /usr/scripts/*"),
                where=PluginDescriptor.WHERE_EXTENSIONSMENU,
                fnc=main
            )]
