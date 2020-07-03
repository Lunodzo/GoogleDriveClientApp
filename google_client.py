#Demo to integrate with the GTK

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# We import the Gtk module. The require_version() method ensures the namespace 
# gets loaded with the given version. The gi.repository is the Python module 
# for PyGObject. PyGObject (Python GObject introspection) contains Python bindings 
# and support for gobject, glib, gtk and other Gnome libraries.

#To succesful run your program, install pyGobject package using any package installer.
#Have you tried jhbuild
class MyWindow(Gtk.Window):

    def __init__(self):
        super(MyWindow, self).__init__()

        self.init_ui()

    def init_ui(self):    

        self.set_icon_from_file("icon.png") # sets the application icon from the image file name.
        self.set_title("Icon")
        self.set_default_size(280, 180)

        label = Gtk.Label()
        self.add(label)
        
        self.connect("destroy", Gtk.main_quit)

builder = Gtk.Builder()
builder.add_from_file("google_client.glade")
builder.add_objects_from_file("google_client.glade", ("upload", "download"))


#Connecting signals

window = builder.get_object("global_window")
window.show_all()
window.connect("destroy", Gtk.main_quit)
Gtk.main()
