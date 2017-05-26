#!/usr/bin/python 
# -*- coding: utf-8 -*-

import os
import bus_tool
import requests
import json
import datetime,calendar
# sudo pip install flask
from flask import Flask, request, abort
# sudo pip install line-bot-sdk
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, 
    TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, 
    MessageTemplateAction, URITemplateAction, CarouselTemplate, 
    CarouselColumn, CarouselColumn, ImagemapSendMessage,
    BaseSize, URIImagemapAction, ImagemapArea,
    MessageImagemapAction, ConfirmTemplate
    
)



def show_day_bus(text):
    
    col=[]
    act=[]
    x = 0
    isd = False
    gbus = bus_tool.ikuasbus(text[1])

    for i in range(0,gbus.get_datalen(), 1):
        
        if (gbus.get_startStation(i) == text[5] and gbus.get_resEnable(i) == True):
            isd = True
            x += 1
            act.append(PostbackTemplateAction(
                        label=gbus.get_driveTime(i),
                        text=' ',
                        data=','.join(text) + ',' + gbus.get_driveTime(i) +',' + str(gbus.get_busid(i))
                    ))
            if (x == 3):
                col.append(
                CarouselColumn(
                        thumbnail_image_url='https://example.com/item2.jpg',
                        title=text[2] + '/' + text[3] + u'　' +text[4],
                        text= text[5] + u'➡️' + text[6],
                        actions=act 
                    )
                )
                x = 0
                act=[]
    if (x != 0):
        while x < 3:
            x += 1
            act.append(MessageTemplateAction(
                                label=' ',
                                text=' '
                            ))
            
        col.append(
        CarouselColumn(
                thumbnail_image_url='https://example.com/item2.jpg',
                title=text[2] + '/' + text[3] + u'　' + text[4],
                text= text[5] + u'➡️' + text[6],
                actions=act
            )
        )
        x = 0
        act=[]
            
    
        
    carousel_template_message = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(col)
)
    print carousel_template_message
    if (isd):
        return carousel_template_message
    else:
        text_message = TextSendMessage(text = '已經沒有可預約班次瞜!')
        return text_message
    
def rbksend():
    imagemap_message = ImagemapSendMessage(
    base_url='http://studorm.kuas.edu.tw/web2/images/193628_2.png',
    alt_text='this is an imagemap',
    base_size=BaseSize(height=901, width=901),
    actions=[
        URIImagemapAction(
            link_uri='https://example.com/',
            area=ImagemapArea(
                x=0, y=0, width=450, height=901
            )
        ),
        MessageImagemapAction(
            text='hello',
            area=ImagemapArea(
                x=520, y=0, width=451, height=901
            )
        )
    ]
)
    print imagemap_message
    return imagemap_message
    
    
def show_bus_day():
    chrday = ['(一)','(二)','(三)','(四)','(五)','(六)','(日)']
    now_date = datetime.datetime.now()
    thismonth = calendar.monthrange(now_date.year,now_date.month)[1]
    
    col=[]
    act=[]
    x = 0
    if (now_date.day + 15 < thismonth  ):
        for i in range(0,15, 1):
            now = datetime.datetime.now()
            date = now + datetime.timedelta(days = i)
            pinM = date.strftime("%m")
            pinD = date.strftime("%d")
            pin = date.strftime("%Y/%m/%d")
            x += 1
            act.append(PostbackTemplateAction(
                        label = pinM + "/" + pinD + "   " + chrday[date.weekday()],
                        text = ' ',
                        data = 'sstar,'+pin+','+pinM+','+pinD + ',' + chrday[date.weekday()]
                        
                    ))
            if (x == 3):
                col.append(
                CarouselColumn(
                        thumbnail_image_url='https://example.com/item2.jpg',
                        title='請選擇日期',
                        text=' ',
                        actions=act 
                    )
                )
                x = 0
                act=[]
        
    carousel_template_message = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(col)        
)    

    return carousel_template_message
    
def J_or_Y(text):
    confirm_template_message = TemplateSendMessage(
    alt_text='Confirm template',
    template=ConfirmTemplate(
        text='請選擇出發地',
        actions=[
            PostbackTemplateAction(
                label='建工',
                text=' ',
                data= text + u",建工,燕巢"
            ),
            PostbackTemplateAction(
                label='燕巢',
                text=' ',
                data= text + u",燕巢,建工"
            )
        ]
    )
)
    return confirm_template_message
    
def chkset(st):
    confirm_template_message = TemplateSendMessage(
    alt_text='Confirm template',
    template=ConfirmTemplate(
        text=u'確定要預約本班車嗎?\n' + st[2]+ '/'+ st[3] +' '+ st[4] + u'　' + st[7] + u'　\n'+st[5] + u'➡️' + st[6],
        actions=[
            PostbackTemplateAction(
                label='確定預約',
                text= ' ',
                data= ','.join(st) 
            ),
            PostbackTemplateAction(
                label='取消',
                text=' ',
                data=' '
            )
        ]
    )
)
    print (','.join(st))
    return confirm_template_message
    
def setBus(st):
    UName = '1104137125'
    UKey = '852053BDF66C8558072B6A3FFD69F4B0'
    sBus = bus_tool.ikuasset(UName,UKey)
    sBus.busset(st[8])
    print(st[0])
    if (sBus.get_success() == True and st[0] != 'End'):
        confirm_template_message = TemplateSendMessage(
    alt_text='Confirm template',
    template=ConfirmTemplate(
        text= sBus.get_message() + ',' + u'是否預約回程校車?',
        actions=[
            PostbackTemplateAction(
                label='是',
                text= ' ',
                data=  ','.join(st) 
            ),
            PostbackTemplateAction(
                label='否',
                text=' ',
                data=' '
            )
        ]
    )
)
        return confirm_template_message
    else:
        text_message = TextSendMessage(text = sBus.get_message())
        return text_message