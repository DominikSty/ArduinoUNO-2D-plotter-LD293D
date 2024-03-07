import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class DrawingAreaWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Drawing Area Example")
        self.set_default_size(552, 601)
        self.set_resizable(False)

        fixed = Gtk.Fixed()
        self.add(fixed)

        self.WIDTH, self.HEIGHT = 55, 55
        self.SCALLING = 10  # Downscale for SVG (optional)

        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_size_request(self.WIDTH*self.SCALLING, self.HEIGHT*self.SCALLING)
        self.drawing_area.connect('draw', self.on_draw)
        self.drawing_area.connect('button-press-event', self.on_button_press)
        self.drawing_area.connect('motion-notify-event', self.on_motion_notify)
        self.drawing_area.connect('button-release-event', self.on_button_release)
        
        self.drawing_area.set_events(Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.BUTTON_RELEASE_MASK)

        fixed.put(self.drawing_area, 1, 50)

        self.lines = []  # An array storing all lines
        self.current_line = None

        # Label info for instructions
        self.label01 = Gtk.Label(label="Holding the left mouse button draws a line.\nPressing the right mouse button removes the last one")
        fixed.put(self.label01, 150, 1)

        self.save_button = Gtk.Button(label="Save to SVG")
        self.save_button.connect("clicked", self.save_to_svg)
        fixed.put(self.save_button, 1, 1)

    def on_draw(self, widget, cr):
        cr.set_source_rgb(1, 1, 1)  # White background
        cr.paint()
        cr.set_source_rgb(0, 0, 0)  # Black lines
        cr.set_line_width(1*self.SCALLING)
        for line in self.lines:
            cr.move_to(int(line[0][0]), int(line[0][1]))
            cr.line_to(int(line[1][0]), int(line[1][1]))
            cr.stroke()
        if self.current_line:
            cr.move_to(int(self.current_line[0][0]), int(self.current_line[0][1]))
            cr.line_to(int(self.current_line[1][0]), int(self.current_line[1][1]))
            cr.stroke()

    def on_button_press(self, widget, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            self.current_line = [(event.x, event.y), (event.x, event.y)]

    def on_motion_notify(self, widget, event):
        if event.state & Gdk.EventMask.BUTTON_PRESS_MASK:
            if self.current_line:
                x, y = event.x, event.y
                x = max(0, min(x, self.WIDTH * self.SCALLING))
                y = max(0, min(y, self.HEIGHT * self.SCALLING))
                self.current_line[1] = (x, y)
                widget.queue_draw()

    def on_button_release(self, widget, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            if self.current_line:
                x, y = event.x, event.y
                x = max(0, min(x, self.WIDTH * self.SCALLING))
                y = max(0, min(y, self.HEIGHT * self.SCALLING))
                self.current_line[1] = (x, y)
                self.lines.append(self.current_line)
                self.current_line = None
                widget.queue_draw()

        elif event.button == Gdk.BUTTON_SECONDARY:  # Right mouse button support
            if self.lines:
                self.lines.pop()  # Delete last line
                widget.queue_draw()

    def save_to_svg(self, button):
        dialog = Gtk.FileChooserDialog(title="Please choose a file", parent=self, action=Gtk.FileChooserAction.SAVE)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK)

        dialog.set_do_overwrite_confirmation(True)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename() + '.svg'
            svg_content = '<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n'.format(self.WIDTH, self.HEIGHT)
            for line in self.lines:
                svg_content += '<path d="M {},{} L {},{}" fill="none" stroke="black" />\n'.format(int(line[0][0]/self.SCALLING), int(line[0][1]/self.SCALLING), int(line[1][0]/self.SCALLING), int(line[1][1]/self.SCALLING))
            svg_content += '</svg>'

            with open(filename, 'w') as f:
                f.write(svg_content)

            print("Linie zostały zapisane w pliku:", filename)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

win = DrawingAreaWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
