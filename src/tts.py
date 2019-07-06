# -*- coding: utf-8; -*-

import sys
import win32com.client
import pythoncom

def speak( txt, volume, speed ):
    pythoncom.CoInitialize()
    
    spvoice = win32com.client.Dispatch("SAPI.SpVoice")
    
    # 女性の英語
    # voiceInfo = spvoice.GetVoices( "Gender=Female" and "Language=409" )
    
    # 英語
    voiceInfo = spvoice.GetVoices("Language=409")
    
    # for i in range(voiceInfo.Count):
    #     item = voiceInfo.Item(i)
    #     print(item.GetAttribute("Name"))
    #     print(item.GetAttribute("Gender"))
    #     print(item.GetAttribute("Language"))
    #     sys.stdout.flush()
    
    spvoice.Voice = voiceInfo.Item(0)  # 声色
    spvoice.Volume = volume  # 0 〜 100
    spvoice.Rate = speed  # -10 〜 10
    
    spvoice.Speak( txt )

if __name__ == '__main__':
    print("'%s'" % (speak( "Hello world", 100, 0 )) )
    
