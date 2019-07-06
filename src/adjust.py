# -*- coding: utf-8; -*-

import sys
import tkinter
import prepare_ocr
import ocr
from PIL import Image
import data
import decideRegion

#import pyautogui
import screenshot


def show(root, param):
    # textArea の text を出力
    sub = tkinter.Toplevel(root)

    def apply_param():
        param.message_thresh = thresh.get()
        param.game_window_title = titleBox.get()
        param.game_window_class = classBox.get()
        param.valid_message_fix_region = validRegion.get() == "1"

    def on_closing():
        apply_param()
        sub.destroy()

    sub.protocol("WM_DELETE_WINDOW", on_closing)

    frame1 = tkinter.Frame(sub)
    frame1.pack(fill="both", expand=True)

    # 処理対象のウィンドウタイトル
    titleFrame = tkinter.LabelFrame(frame1, bd=2, relief="ridge", text="window title")
    titleFrame.pack(fill="both", side="left", expand=True)
    titleBox = tkinter.Entry(titleFrame)
    titleBox.insert(tkinter.END, param.game_window_title)
    titleBox.pack(fill="both", expand=True)

    # 処理対象のウィンドウクラス
    classFrame = tkinter.LabelFrame(frame1, bd=2, relief="ridge", text="window class")
    classFrame.pack(fill="both", side="left", expand=True)
    classBox = tkinter.Entry(classFrame)
    classBox.insert(tkinter.END, param.game_window_class)
    classBox.pack(fill="both", expand=True)

    # 領域決定
    frame2 = tkinter.Frame(sub)
    frame2.pack(fill="both", expand=True)
    validRegion = tkinter.StringVar()
    validRegion.set(param.valid_message_fix_region and "1" or "0")
    validRegionCheck = tkinter.Checkbutton(
        frame2, text='メッセージボックスの領域を指定する', variable=validRegion)
    validRegionCheck.pack()

    def updateRegion(region):
        param.message_fix_region = region

        regionBox.configure(state='normal')
        regionBox.delete(0, tkinter.END)
        regionBox.insert(tkinter.END, "(%d,%d,%d,%d)"
                         % (param.message_fix_region[0], param.message_fix_region[1],
                            param.message_fix_region[2], param.message_fix_region[3]))
        regionBox.configure(state='readonly')

    def pushedRegionButton(event):
        apply_param()
        rect = screenshot.getRectOf(param.game_window_title, param.game_window_class)
        decideRegion.decideRegion(
            sub, rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1], updateRegion)

    regionButton = tkinter.Button(frame2, text=u'set region')
    regionButton.bind("<1>", pushedRegionButton)
    regionButton.pack(fill="both", expand=True)

    regionBox = tkinter.Entry(frame2)
    regionBox.insert(tkinter.END, "(%d,%d,%d,%d)"
                     % (param.message_fix_region[0], param.message_fix_region[1],
                        param.message_fix_region[2], param.message_fix_region[3]))
    regionBox.configure(state='readonly')
    regionBox.pack()

    # メッセージ抽出の閾値
    frame3 = tkinter.Frame(sub)
    frame3.pack(fill="both", expand=True)
    tkinter.Label(frame3, text='threshold').pack(side='left')
    thresh = tkinter.Scale(frame3, orient='h', from_=0, to=255)
    thresh.set(param.message_thresh)
    thresh.pack(side='left')

    # ocr 開始

    def pushedOcrButton(event):
        apply_param()

        if validRegion.get() == "1":
            # region = [param.message_fix_region[0],
            #           param.message_fix_region[1],
            #           param.message_fix_region[2] - param.message_fix_region[0],
            #           param.message_fix_region[3] - param.message_fix_region[1]]
            #game_image = pyautogui.screenshot(region=region)
            game_image = screenshot.getImageOf(param.game_window_title,
                                               param.game_window_class,
                                               param.message_fix_region)
        else:
            # game_image = Image.open('test2.png')
            game_image = screenshot.getImageOf(param.game_window_title,
                                               param.game_window_class, None )
        ocr_image = prepare_ocr.createPreparedOCRImage(game_image, param, True)
        txt = ocr.getTxt(ocr_image).replace('\n', ' ')
        textArea.delete('1.0', 'end -1c')
        textArea.insert(tkinter.END, txt)

    ocrButton = tkinter.Button(sub, text=u'Test', width=50)
    ocrButton.bind("<1>", pushedOcrButton)
    ocrButton.pack(fill="both", expand=True)

    # OCR で抽出したメッセージ
    textArea = tkinter.Text(sub, width=50, height=10)
    textArea.insert(tkinter.END, "")
    textArea.pack(fill="both", expand=True)

    sub.mainloop()


if __name__ == '__main__':
    show(tkinter.Tk(), data.Parameter.create_default())
