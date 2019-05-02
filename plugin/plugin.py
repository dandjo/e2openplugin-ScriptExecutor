from Screens.Screen import Screen
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Plugins.Plugin import PluginDescriptor
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from os import listdir
from os.path import isdir, isfile, join

dirs = [
    "/usr/scripts",
    "/media/hdd/scripts",
    "/media/usb/scripts"
]

class ScriptExecutor(Screen):
    skin = """
        <screen name="ScriptExecutor" position="center,center" size="700,556" title="Script Executor">
            <widget name="scriptMenuList" position="5,5" size="690,546" scrollbarMode="showOnDemand" />                                                                  
        </screen>"""

    def __init__(self, session, args=None):
        self.session = session
        self.dir = [d for d in dirs if isdir(d)][0]
        files = list()
        for f in listdir(self.dir):
            if not isfile(join(self.dir, f)):
                continue
            files.append((f, join(self.dir, f)))
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
            self.session.open(Console, _(self.dir), [script])

    def cancel(self):
        self.close(None)

def main(session, **kwargs):
    try:
        session.open(ScriptExecutor)
    except IndexError:
        session.open(MessageBox, _("No suitable directory found! "\
            "Be sure to provide one of these paths on your filesystem: "\
            "['%s']" % "', '".join(dirs)), MessageBox.TYPE_ERROR)
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
