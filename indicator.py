import os
from threading import Thread
import time
import atexit
try:
    from gi.repository import AppIndicator3 as AppIndicator
except:
    from gi.repository import AppIndicator

from gi.repository import Gtk
from timecollector import TimeCollector

class LogViewer(Gtk.Label):
    """widget displays logs"""
    def __init__(self):
        self.text = ''
        super(LogViewer, self).__init__(self.text)

    def log(self, string):
        self.text += string
        self.set_text(self.text)


class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__(title="Open Timer")

        self.timecollector = TimeCollector()
        atexit.register(self.timecollector.closeDataFile)

        self.collect_thread = Thread(target=self.collect_loop)
        self.collect_thread.daemon = True

        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)

        checkbutton = Gtk.CheckButton("Click me!")
        stack.add_titled(checkbutton, "check", "Check Button")

        self.log_view = LogViewer()
        stack.add_titled(self.log_view, "log", "log")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        vbox.pack_start(stack_switcher, True, True, 0)
        vbox.pack_start(stack, True, True, 0)

        self.collect_thread.start()

    def collect_loop(self):
        step = 2
        while True:
            data = self.timecollector.collect()
            if self.log_view.get_property("visible"):
                self.log_view.log(data)
            #if self.currentTask:
            #    self.currentTask.update(data, step)
            time.sleep(step)


class TimerSaverAppIndicator(object):
    icon = os.path.join(os.path.dirname(__file__), 'logo.png')

    def __init__(self):
        self.ind = AppIndicator.Indicator.new("Open Timer",
                                              self.icon,
                                              AppIndicator.IndicatorCategory.APPLICATION_STATUS)

        self.ind.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        self.ind.set_attention_icon(self.icon)

        self.win = MainWindow()
        self.win.connect("delete-event", lambda _, __: self.win.hide())

        # create a menu
        menu = Gtk.Menu()

        # create one item
        menu_items = Gtk.MenuItem("Resume")
        menu.append(menu_items)
        menu_items.connect("activate", lambda _: self.win.show_all())
        menu_items.show()

        # create one item
        menu_items = Gtk.MenuItem("Quit")
        menu.append(menu_items)
        menu_items.connect("activate", Gtk.main_quit)
        menu_items.show()

        self.ind.set_menu(menu)


if __name__ == '__main__':
    ind = TimerSaverAppIndicator()
    Gtk.main()
