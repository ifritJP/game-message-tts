# -*- coding: utf-8; -*-

import json
import time
import sys

from dataclasses import field
from marshmallow_dataclass import dataclass
import marshmallow.validate
from typing import List


def loadDataclass(path, dataclass):
    return dataclass.Schema().load(json.load(open(path))).data


def saveDataclass(path, dataclass, obj):
    fileObj = open(path, "w")
    fileObj.write(dataclass.Schema().dumps(
        obj, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': ')).data)
    fileObj.close()


@dataclass
class Parameter:
    # 抽出した line からメッセージボックスを検出する時、
    # ある line と対になる line を見つける。
    # このとき、対となる line との関係を制限する。
    # MIN_HEIGHT 以上の高さ、 MIN_WIDTH 以上の幅
    MIN_HEIGHT: int = field(default=50)

    MIN_WIDTH: int = field(default=300)

    # この Y 座標より上はメッセージボックス検出から外す。 画面上部が 0。
    top_margin: int = field(default=10)
    bottom_margin: int = field(default=10)

    MAX_Y: int = field(default=0)

    # 切り出したメッセージボックスを、さらに shrink するサイズ
    OFFSET: List[int] = field(default_factory=lambda: [0, 0, 0, 0])

    # 切り出メッセージボックスの固定領域
    message_fix_region: List[int] = field(default_factory=lambda: [0, 0, 0, 0])
    valid_message_fix_region: bool = field(default=False)

    # 切り出したメッセージボックスから文字領域を二値化する際の閾値
    message_thresh: int = field(default=120)

    # ocr 後のメッセージから除外する文字列パターン
    exclude_txt: str = field(default="")

    game_title: str = field(default="")
    game_window_title: str = field(default="")
    game_window_class: str = field(default="")
    volume: int = field(default=100)
    speed: int = field(default=0)

    # コンストラクタを宣言する場合は、全てのメンバを宣言しないといけないので、
    # テスト用のデフォルトインスタンス生成関数を staticmethod で作成する
    @staticmethod
    def create_default():
        return Parameter(MIN_HEIGHT=50,
                         MIN_WIDTH=300,
                         top_margin=10,
                         bottom_margin=10,
                         OFFSET=[0, 0, 0, 0],
                         message_fix_region=[0, 0, 0, 0],
                         valid_message_fix_region=False,
                         message_thresh=0,
                         exclude_txt="",
                         game_title="game title",
                         game_window_title="game window title",
                         game_window_class="game window class",
                         volume=100,
                         speed=0)

    @staticmethod
    def loadFile(path):
        try:
            return loadDataclass(path, Parameter)
        except:
            print(sys.exc_info()[0])
            return Parameter.create_default()

    def save(self, path):
        saveDataclass(path, Parameter, self)


@dataclass
class LogItem:
    # ゲームタイトル
    title: str
    # 日付
    date: int
    # テキスト
    text: str
    # テキスト長
    len: int

    @staticmethod
    def create(title, txt):
        return LogItem(title, time.time(), txt, len(txt))


@dataclass
class History:
    history: List[LogItem]

    def add(self, title, text):
        self.history.append(LogItem.create(title, text))

    def modifyLastText(self, text):
        self.history[len(self.history) - 1].text = text

    @staticmethod
    def loadFile(path):
        try:
            return loadDataclass(path, History)
        except:
            print(sys.exc_info()[0])
            return History([])

    def save(self, path):
        saveDataclass(path, History, self)


if __name__ == '__main__':
    param = Parameter.create_default()
    print(param)
    txt, _ = Parameter.Schema().dumps(param)
    print(txt)
    param2, _ = Parameter.Schema().loads(txt)
    print(param2.volume)

    param3 = Parameter.loadFile("conf.json")
    print(param3)

    param3.save("conf2.json")

    log = History([])
    for txt in ["abc", "def"]:
        log.add("game", txt)

    print(log)

    log.save("history.json")
