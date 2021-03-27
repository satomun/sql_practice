#SQL練習アプリ

import pandas as pd
import streamlit as st
import sqlite3
conn=sqlite3.connect("practice.db")
c=conn.cursor()

def table_init1():
    c.execute('drop table 社員')
    c.execute('CREATE TABLE  IF NOT EXISTS 社員(社員コード text,氏名 text,性別  text,生年月日 date,部署 text, 入社年月日 date,上司コード text, PRIMARY KEY(社員コード))')
    sql1  = 'insert into 社員(社員コード,氏名,性別,生年月日,部署,入社年月日,上司コード) values (?,?,?,?,?,?,?)'
    data1 = [
    ('001','佐藤','女','19840410','総務','20060401',""), 
    ('002','山口', '女', '19850620','営業','20070401',""), 
    ('003','江頭', '男', '19900810','情報システム','20070401',""), 
    ('004','古村', '女', '19830521','経理','20100401','001'), 
    ('005','矢野', '男', '20000131','情報システム','20200401','003'),
    ('006','青木', '女', '19971203','営業','20200401','002')]
    c.executemany(sql1, data1)
    conn.commit()

def table_init2():
    c.execute('drop table 資格')
    c.execute('CREATE TABLE  IF NOT EXISTS 資格(社員コード text,保有資格 text,取得日 date,PRIMARY KEY(社員コード,保有資格))')
    sql2 = 'insert into 資格(社員コード,保有資格,取得日) values (?,?,?)'
    data2 = [
    ('001','簿記３級', '20140610'), 
    ('001','簿記２級', '20150610'), 
    ('002','簿記３級', '20150610'), 
    ('004','簿記３級', '20201110'), 
    ('005','簿記３級', '20181110'), 
    ('005','基本情報技術者', '20190420')]
    c.executemany(sql2, data2)
    conn.commit()

def exsql(sql):
    if "SELECT" in sql.upper():
        c.execute(sql)
        data=c.fetchall()
        return data
    else:
        c.execute(sql)
        conn.commit()
        return pd.DataFrame()

def view_all(table):
    c.execute('select * from "{}" '.format(table))
    data=c.fetchall()
    data=pd.DataFrame(data)
    return data

col1,col2=st.beta_columns(2)

with col1:
    button_init = st.button("テーブルを初期値にする")
    sql=st.text_area("SQLを入力",max_chars=1000,height=200)
    button_exec = st.button("SQLを実行する")

    if button_exec:
        return_data=exsql(sql)
        st.table(return_data)

with col2:

    if button_init:
        table_init1()
        table_init2()

    shainn = view_all("社員")
    colname1 = {0:"社員コード",1:"氏名",2:"性別",3:"生年月日",4:"部署",5:"入社年月日",6:"上司コード"}
    shainn = shainn.rename(columns=colname1)
    st.table(shainn)

    shikaku = view_all("資格")
    colname2 = {0:"社員コード",1:"保有資格",2:"取得日"}
    shikaku = shikaku.rename(columns=colname2)
    st.table(shikaku)