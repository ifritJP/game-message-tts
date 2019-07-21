# -*- coding: utf-8; -*-
import sys
import tkinter
import prepare_ocr
import ocr
from PIL import Image
import data
import adjust
import screenshot
import tts
import threading
import re
import webbrowser
import urllib.parse
import uihelper


def show(param, history):
    root = tkinter.Tk()

    uihelper.registerEntryPopupMenu(root)

    def apply_param():
        param.game_title = titleVal.get()
        param.exclude_txt = excludePattern.get()
        param.volume = volumeVal.get()
        param.speed = speed.get()

    def on_closing():
        apply_param()
        root.destroy()

    root.title("game message tts")
    root.protocol("WM_DELETE_WINDOW", on_closing)

    lastTxt = None

    titleFrame = tkinter.LabelFrame(root, bd=2, relief="ridge", text="game title")
    titleFrame.pack(fill="both", expand=True)
    titleVal = tkinter.StringVar()
    titleBox = tkinter.Entry(titleFrame, textvariable=titleVal)
    titleBox.insert(tkinter.END, param.game_title)
    titleBox.pack(fill="both", expand=True)

    # パラメータ調整ウィンドウ表示
    def pushedParamButton(event):
        adjust.show(root, param)
        apply_param()
    paramButton = tkinter.Button(root, text='adjust parameter', width=50)
    paramButton.bind("<1>", pushedParamButton)
    paramButton.pack(fill="both", expand=True)

    # OCR で抽出したメッセージ
    textArea = tkinter.Text(root, width=50, height=5)
    textArea.insert(tkinter.END, "")
    textArea.pack(fill="both", expand=True)

    frame = tkinter.Frame(root)
    frame.pack(fill="both", expand=True)

    def play(txt):
        apply_param()

        def run():
            print(txt)
            tts.speak(txt, param.volume, param.speed)
        run()
        # thread = threading.Thread(target=run)
        # thread.start()

    # ocr 開始

    def pushedOcrButton(event):
        apply_param()
        # textArea の text を出力
        game_image = screenshot.getImageWith(param)
        ocr_image = prepare_ocr.createPreparedOCRImage(game_image, param, False)
        txt = ocr.getTxt(ocr_image).replace('\n', ' ').replace('|', 'I')
        if param.exclude_txt != "":
            txt = re.sub(param.exclude_txt, '', txt)
        textArea.delete('1.0', 'end -1c')
        textArea.insert(tkinter.END, txt)

        lastTxt = txt
        history.add(param.game_title, lastTxt)

        play(lastTxt)

    ocrButton = tkinter.Button(frame, text=u'OCR')
    ocrButton.bind("<1>", pushedOcrButton)
    ocrButton.pack(fill="both", side='left', expand=True)


    # 再生ボタン
    def pushedRepeatButton(event):
        lastTxt = textArea.get('1.0', 'end -1c')
        history.modifyLastText(lastTxt)
        play(lastTxt)

        sys.stdout.flush()
    repeatButton = tkinter.Button(frame, text=u'play')
    repeatButton.bind("<1>", pushedRepeatButton)
    repeatButton.pack(fill="both", side='left', expand=True)


    # 停止ボタン
    def pushedStopButton(event):
        tts.stop()

    repeatButton = tkinter.Button(frame, text=u'stop')
    repeatButton.bind("<1>", pushedStopButton)
    repeatButton.pack(fill="both", side='left', expand=True)

    
    # 翻訳
    def pushedTranslateButton(event):
        lastTxt = textArea.get('1.0', 'end -1c')
        url = "https://translate.google.co.jp/?sl=en&tl=ja&text=%s" % (urllib.parse.quote(lastTxt))
        webbrowser.open(url)

    translateButton = tkinter.Button(frame, text=u'translate')
    translateButton.bind("<1>", pushedTranslateButton)
    translateButton.pack(fill="both", side='left', expand=True)

    # 除外文字列パターン
    excludeFrame = tkinter.LabelFrame(root, bd=2, relief="ridge", text="excluding re-pattern")
    excludeFrame.pack(fill="both", expand=True)
    excludePattern = tkinter.StringVar()
    excludeBox = tkinter.Entry(excludeFrame, textvariable=excludePattern)
    excludeBox.insert(tkinter.END, param.exclude_txt)
    excludeBox.pack(fill="both", expand=True)

    # ボリューム
    tkinter.Label(root, text='volume').pack(side="left")
    volumeVal = tkinter.IntVar()
    volume = tkinter.Scale(root, orient='h', from_=0, to=100, variable=volumeVal)
    volume.set(param.volume)
    volume.pack(side='left')

    # スピード
    speed = tkinter.IntVar()
    speed.set(param.speed)
    speedSpin = tkinter.Spinbox(
        root, textvariable=speed, from_=-10, to=10, increment=1, width=10)
    speedSpin.pack(side='right', padx=10)

    speedLabel = tkinter.Label(root, text='speed')
    speedLabel.pack(side="right")

    root.mainloop()


if __name__ == '__main__':

    history_path = "history.json"
    history = data.History.loadFile(history_path)
    if len(sys.argv) >= 2:
        conf_path = sys.argv[1]
    else:
        conf_path = "conf/conf.json"
    param = data.Parameter.loadFile(conf_path)
    show(param, history)

    history.save(history_path)
    param.save(conf_path)
