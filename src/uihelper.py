import tkinter


def registerEntryPopupMenu(frame):

    def showPopup(event):
        menu = tkinter.Menu(frame, tearoff=False)
        menu.add_command(label='Cut', underline=5,
                         command=lambda: event.widget.event_generate("<<Cut>>"))
        menu.post(event.x_root, event.y_root)

    frame.bind_class("Entry", "<Button-3><ButtonRelease-3>", showPopup)
    frame.bind_class("Text", "<Button-3><ButtonRelease-3>", showPopup)
