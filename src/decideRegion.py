import tkinter
import sys


def decideRegion(parent, x, y, width, height, onClose):

    sub = tkinter.Toplevel(parent)
    sub.overrideredirect(True)

    region = [-1, -1, -1, -1]

    sub.geometry("+%d+%d" % (x, y))
    sub.wait_visibility(sub)
    sub.wm_attributes('-alpha', 0.4)

    canvas = tkinter.Canvas(sub, width=width, height=height, cursor='cross')

    def onPress(event):
        region[0] = event.x
        region[1] = event.y

    def onRelease(event):
        region[2] = event.x
        region[3] = event.y
        if onClose:
            onClose(region)
        sub.destroy()

    def onMove(event):
        if region[0] == -1:
            return
        canvas.delete("rect")
        canvas.create_rectangle(
            region[0], region[1], event.x, event.y, fill='red', tag='rect')

    canvas.bind('<Motion>', onMove)
    canvas.bind('<ButtonPress-1>', onPress)
    canvas.bind('<ButtonRelease-1>', onRelease)

    canvas.pack(fill="both", expand=True)

#    sub.mainloop()


if __name__ == '__main__':
    root = tkinter.Tk()

    def onClose(parm):
        sys.exit()

    decideRegion(root, 100, 200, 400, 500, onClose)
    root.mainloop()
