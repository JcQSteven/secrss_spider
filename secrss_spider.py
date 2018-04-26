#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/17 5:18 PM
# @Author  : Steven
# @Contact : 523348709@qq.com
# @Site    :
# @File    : 360bbs.py
# @Software: PyCharm
import requests
import sqlite3
from bs4 import BeautifulSoup

class Sqlite_db():
    def __init__(self):
        self.conn=sqlite3.connect('../secrss.sqlite')
        self.cur=self.conn.cursor()
        #mysql列名
        #self.mysql_bar='url,title,time_line,tag,author,head,body'
        self.mysql_col_num=8
        mysql_col = []
        for i in range(0,self.mysql_col_num):
            mysql_col.append('?')
        self.mysql_col=','.join(mysql_col)


    def add(self,table,*data):
        sql = 'insert into %s values(NUll,%s)' % (table,self.mysql_col)
        #print sql
        self.cur.execute(sql, data)
        self.conn.commit()

    def test(self,*data):
        pass
        #print self.conn.


    def get_all(self,table):
        sql='select * from %s'%table
        self.cur.execute(sql)
        value=self.cur.fetchall()
        print value

    def get_last_one(self,table,col_name):
        sql='select %s from %s order by ID DESC limit 1'%(col_name,table)
        self.cur.execute(sql)
        result=self.cur.fetchone()
        return result[0]

if __name__ == '__main__':

    sqlite=Sqlite_db()
    sec_id = int(sqlite.get_last_one('secrss','sec_id')+1)
    false_id=0
    while 1:
        print sec_id
        url = 'https://www.secrss.com/articles/%d'%sec_id
        s = requests.session()
        r = s.get(url)
        if r.status_code!=404:
            false_id=0
            html=r.content
            bsoj=BeautifulSoup(html,'html.parser')

            title=bsoj.find('h1').text.strip()
            time_line=bsoj.find('span',class_='time').text
            try:
                tag=bsoj.find('span',class_='tag').text.strip()
            except AttributeError:
                tag='NULL'
            author=bsoj.find('span',class_='author').text.strip()
            head=bsoj.find('div',class_='summary').text.rstrip().lstrip()
            body=bsoj.find('div',class_='article-body').text.rstrip().lstrip()
            body=body.replace(u'安全内参',u'网络安全通')
            body=body.replace(' ','\n')
            sqlite.add('secrss', sec_id,url, title, time_line, tag, author, head, body)
            sec_id=sec_id+1

        else:
            if false_id<4:
                false_id=false_id+1
                sec_id = sec_id + 1
                print 'try'+str(false_id)
                continue
            else:
                print'finished'
                break



