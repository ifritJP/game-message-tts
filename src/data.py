# -*- coding: utf-8; -*-

import json
import time
import sys

# from dataclasses import field
# from marshmallow_dataclass import dataclass
# import marshmallow.validate
# from typing import List

from dataclasses import dataclass, field
from typing import List, Optional

import marshmallow
import marshmallow_dataclass


def getSchema( dataclass ):
    return marshmallow_dataclass.class_schema( dataclass )()

def loadDataclass(path, schema):
    txt = open(path).read()
    return schema.loads( txt )


def saveDataclass(path, schema, obj):
    fileObj = open(path, "w")
    # fileObj.write(dataclass.Schema().dumps(
    #     obj, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': ')).data)
    fileObj.write(schema.dumps(
        obj, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': ')))
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
        return Parameter()

    @staticmethod
    def loadFile(path):
        try:
            param = loadDataclass(path, getSchema(  Parameter ) )
            return param
        except:
            #print(sys.exc_info()[0])
            print(sys.exc_info())
            return Parameter.create_default()

    def save(self, path):
        saveDataclass(path, getSchema( Parameter ), self)


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
            return loadDataclass(path, getSchema(  History ) )
        except:
            print(sys.exc_info()[0])
            return History([])

    def save(self, path):
        saveDataclass(path, getSchema( History ), self)


if __name__ == '__main__':
    param = Parameter.create_default()
    print(param)
    schema = getSchema( Parameter )
    txt = schema.dumps(param)
    print("txt: %s" %(txt))
    param2 = schema.loads(txt)
    print( "volume: %s" %(param2.volume))

    param3 = loadDataclass("conf.json", schema )
    print( param3 )

    open( "conf2.json", "w" ).write( schema.dumps( param3 ) )

    log = History([])
    for txt in ["abc", "def"]:
        log.add("game", txt)

    print(log)

    saveDataclass( "history.json", getSchema( History ), log )
