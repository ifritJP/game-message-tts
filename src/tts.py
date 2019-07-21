# -*- coding: utf-8; -*-

import sys
import win32com.client
import pythoncom
import time

def setup():
    spvoice = win32com.client.Dispatch("SAPI.SpVoice" )
    pythoncom.CoInitialize()

    
    # for i in range(voiceInfo.Count):
    #     item = voiceInfo.Item(i)
    #     print(item.GetAttribute("Name"))
    #     print(item.GetAttribute("Gender"))
    #     print(item.GetAttribute("Language"))
    #     sys.stdout.flush()


    # 女性の英語
    # voiceInfo = spvoice.GetVoices( "Gender=Female" and "Language=409" )

    # 英語
    voiceInfo = spvoice.GetVoices("Language=409")
    
    spvoice.Voice = voiceInfo.Item(0)  # 声色
    
    
    return spvoice

spvoice = setup()    

def speak( txt, volume, speed ):
    
    
    spvoice.Volume = volume  # 0 〜 100
    spvoice.Rate = speed  # -10 〜 10

    stop()
    spvoice.Speak( txt, 1 )

def stop():
    spvoice.Skip( "Sentence", 10000 )
    


if __name__ == '__main__':
    
    print("'%s'" % (speak( "Hello world", 100, 0 )) )
    time.sleep( 0.1 )
    print("'%s'" % (speak( "as soon as possible", 100, 0 )) )
    time.sleep( 2 )
    
