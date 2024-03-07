import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

class DrawingArea(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()

        self.set_size_request(220, 220)
        self.connect("draw", self.on_draw)

    def on_draw(self, widget, cr):
        width = widget.get_allocated_width()
        height = widget.get_allocated_height()

        # Rysowanie siatki
        cr.set_source_rgb(0.8, 0.8, 0.8)
        cr.set_line_width(1)

        for x in range(0, width, 55):
            cr.move_to(x, 0)
            cr.line_to(x, height)
            cr.stroke()

        for y in range(0, height, 55):
            cr.move_to(0, y)
            cr.line_to(width, y)
            cr.stroke()

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Drawing Area Example")
        self.set_default_size(300, 300)
        self.set_border_width(10)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box)

        drawing_area = DrawingArea()
        box.pack_start(drawing_area, True, True, 0)

        save_button = Gtk.Button(label="Save Drawing")
        save_button.connect("clicked", self.on_save_clicked)
        box.pack_end(save_button, False, False, 0)

    def on_save_clicked(self, button):
        print("Save button clicked")

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
