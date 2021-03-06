#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from Tkinter import Button, Frame, Label, Text
try:
    import ImageTk
except ImportError:
    ImageTk = False


class Tkpipe(Frame):

    def __init__(self, title="Standard output", label="Propram progress"):
        Frame.__init__(self)
        self.master.title(title)
        self.grid(stick="nsew")
        self.label = label
        self.ready = False
        self.closed = False
        self.images = []


    def open(self):
        if not self.ready:
            self.ready = True
            self.createWidgets()


    def createWidgets(self):
        top = self.winfo_toplevel()

        top.rowconfigure(0, weight=1, minsize=96)
        top.columnconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, minsize=24)
        self.lbl_pretext = Label(self, text="Update progress:")
        self.lbl_pretext.grid(row=0, sticky="w")

        self.rowconfigure(1, minsize=48, weight=1)
        self.txt_messages = Text(self)
        self.txt_messages.grid(row=1, sticky="nsew")
        self.txt_messages.config(selectbackground="#d2d3bd")
        self.txt_messages.tag_config("green", foreground="darkgreen")
        self.txt_messages.tag_config("blue", foreground="darkblue")
        self.txt_messages.tag_config("red", foreground="darkred")

        self.rowconfigure(2, minsize=24)
        self.btn_quit = Button(self, text="Quit", command=self.quit)
        self.btn_quit.grid(row=2, sticky="ew")

        self.write("Process started\n-----\n", "blue")
        self.update()


    def write(self, line, tag=None):
        self.open()
        line = line.replace("\r\n", "\n")
        self.txt_messages.insert("end", line, tag)
        self.txt_messages.see("end")
        self.txt_messages.update()


    def writelines(self, iterable, tag=None):
        for line in iterable:
            self.write(line, tag)


    def flush(self):
        self.update()


    def close(self):
        if not self.closed:
            self.write("-----\nProcess ended", "blue")
            self.closed = True
            self.mainloop()


    def default(self, tagname):
        return ColoredPipe(self, tagname)


    def __del__(self, *args):
        self.close()


    def writeimage(self, image):
        if ImageTk:
            self.open()
            self.images.append(ImageTk.PhotoImage(image))
            self.txt_messages.image_create("end", {"image" : self.images[-1]})
            self.update()
        else:
            self.write("<Must install PIL to display images>\n", "blue")


class ColoredPipe:

    def __init__(self, pipe, tag):
        self.pipe = pipe
        self.default_tag = tag


    def default(self, tagname):
        return ColoredPipe(self.pipe, tagname)


    def write(self, string, tag=None):
        self.pipe.write(string, tag or self.default_tag)


    def writelines(self, iterable, tag=None):
        for line in iterable:
            self.write(line, tag or self.default_tag)

    def flush(self):
        self.pipe.flush()

    def close(self):
        self.pipe.close()

    def __del__(self, *args):
        self.pipe.__del__(*args)

    def writeimage(self, image):
        self.pipe.writeimage(image)
