from django.db import models
import pymssql
# Create your models here.

def sqlstart():
    global cursor
    conn = pymssql.connect(
        server='127.0.0.1'
        , user='Alan'
        , password='123456'
        , database='foo'
        , port='1433'
    )
    cursor = conn.cursor(as_dict=True)
    # sql="SELECT * FROM data_table"
    # cursor.execute(sql)
    # topics =cursor.fetchall()
    # cursor.close()
    # conn.close()

# def sqlstart():
#     global topics
#     conn = pymssql.connect(
#         server='127.0.0.1'
#         , user='Alan'
#         , password='123456'
#         , database='foo'
#         , port='1433'
#     )
#     cursor = conn.cursor(as_dict=True)
#     sql="SELECT * FROM data_table"
#     cursor.execute(sql)
#     topics =cursor.fetchall()
#     cursor.close()
#     conn.close()

def search(key,val,page):
    if key==None or val==None:

        sql ='SELECT * FROM data_table ORDER BY usec OFFSET %s ROWS FETCH NEXT 50 ROWS ONLY'%((int(page)-1)*50)
    else:
        sql = "SELECT * FROM data_table WHERE %s = '%s' ORDER BY usec OFFSET %s ROWS FETCH NEXT 50 ROWS ONLY"%(key,val,(int(page)-1)*50)
    cursor.execute(sql)
    topics =cursor.fetchall()
    return topics
def val_count(key,val):
    if key == None or val == None:
        count = "SELECT  COUNT(*) as 總共有幾筆資料 FROM data_table"
    else:
        count = "SELECT  COUNT(*) as 總共有幾筆資料 FROM data_table WHERE %s = '%s'"%(key,val)
    cursor.execute(count)
    topics =cursor.fetchall()
    topics=topics[0]['總共有幾筆資料']
    return topics