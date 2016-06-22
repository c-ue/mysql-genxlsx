from pymysql import *
class core:
    def __init__(self,user=None,passwd=None):
        self.error=None
        if user is None or passwd is None:
            self.error = 'Field is Empty.'
            return
        try:
            self.c=connect(host='192.168.101.254',
                           user=user,
                           password=passwd,
                           db='is',
                           charset='utf8mb4',
                           cursorclass=cursors.DictCursor
                           )
        except:
            self.error = "Mysql account Error"

    def GetAllTeamName(self):
        with self.c.cursor() as cc:
            sql = 'SELECT teamid,teamname FROM teaminfo;'
            row = cc.execute(sql)
            if row == 0:
                self.error = 'Data schema error!.'
                return False
            return cc.fetchall()

    def GetTotalScoreByTid(self,tid=None):
        if tid is None:
            self.error = 'No Team ID.'
            return False
        with self.c.cursor() as cc:
            sql = 'SELECT totalscore FROM teaminfo WHERE teamid=%s'
            row = cc.execute(sql,(tid,))
            if row != 1:
                self.error = 'Data Schema broken.'
                return False
            return cc.fetchall()