# -*- coding: utf-8; -*-

import sys
import tkinter
from tkinter import ttk
import glob
import gui
import data
import os.path
import time
import urllib.parse


def show(conf_dir):
    root = tkinter.Tk()

    def createCombbox(parent, title, valList, onSelected):
        frame = tkinter.LabelFrame(parent, bd=2, relief="ridge", text=title)
        frame.pack(fill="both", expand=True)
        val = tkinter.StringVar()
        combo = ttk.Combobox(frame, textvariable=val, state='readonly')
        combo.config(values=valList)
        combo.set(valList[0])
        if onSelected:
            combo.bind("<<ComboboxSelected>>", onSelected)
        combo.pack(fill="both", expand=True)
        return val

    pathList = []
    for path in glob.glob("conf/*"):
        basename = os.path.basename(path)
        pathList.append(urllib.parse.unquote(basename))

    new_config_txt = "<new config>"
    pathList.append(new_config_txt)

    confPathVar = createCombbox(root, "config", pathList, None)

    def pushedButton(event):
        conf_path = confPathVar.get()

        root.destroy()

        history_path = "history.json"
        history = data.History.loadFile(history_path)

        if conf_path == new_config_txt:
            new_config = True
            param = data.Parameter()
            param.game_title = "%d" % (time.time())
        else:
            new_config = False
            conf_path = os.path.join(conf_dir, urllib.parse.quote(conf_path))
            param = data.Parameter.loadFile(conf_path)

        gui.show(param, history)

        history.save(history_path)

        if new_config:
            title = urllib.parse.quote(param.game_title)
            conf_path = os.path.join(conf_dir, "%s.json" % (title))

            param.save(conf_path)

    okButton = tkinter.Button(root, text=u'OK', width=50)
    okButton.bind("<1>", pushedButton)
    okButton.pack(fill="both", expand=True)

    root.mainloop()


if __name__ == '__main__':
    show("conf")
