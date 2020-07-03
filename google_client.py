import pygtk
pygtk.require('2.0')
import gtk


builder = Gtk.Builder()
builder.add_from_file("google_client.glade")