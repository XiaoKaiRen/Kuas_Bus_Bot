#!/usr/bin/python 
# -*- coding: utf-8 -*-
import Menu_tool

def select_tool(text):
    if (text == u"訂車"):
       return Menu_tool.show_bus_day()

def select_postback(text):
    st = text.split(",")

    if (st[0] == 'sstar'):
        st[0] = 'ShowBus'
        return Menu_tool.J_or_Y(','.join(st))
        
    elif (st[0] == 'ShowBus'):
        st[0] = 'chkset'
        return Menu_tool.show_day_bus(st)
        
    elif (st[0] == 'chkset'):
        st[0] = 'setBus'
        return Menu_tool.chkset(st)
        
    elif (st[0] == 'setBus'):  
        st[0] = 'EShowBus'
        return Menu_tool.setBus(st)
        
    elif (st[0] == 'EShowBus'):
        st[0] = 'Echkset'
        mid = st[5]
        st[5] = st[6]
        st[6] = mid
        st.pop()
        st.pop()
        print (','.join(st))
        return Menu_tool.show_day_bus(st)
    elif (st[0] == 'Echkset'):
        st[0] = 'EsetBus'
        return Menu_tool.chkset(st)
    elif (st[0] == 'EsetBus'):
        st[0] = 'End'
        return Menu_tool.setBus(st)
    