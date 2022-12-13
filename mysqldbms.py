import pyodbc
import sys

class SQLDBConnector:
    def __init__(self,db="",server=""):
        self.db = db
        self.server = server
        self.conn = pyodbc.connect("DRIVER={SQL Server};SERVER=%s;DATABASE=%s;TRUSTED_CONNECTION='yes'"%
                                   (self.server,self.db),
                                   autocommit=True)

    def executeQuery(self,sql="",params=()):
        try:
            self.cursor = self.conn.cursor()
            result = self.cursor.execute(sql,params)
            return result
        except pyodbc.DatabaseError as e:
            print(e)
            sys.exit

    def callProc(self, procname="",params=()):
        try:
            self.cursor = self.conn.cursor()
            if len(params)>0:
                param_no = "?,"*len(params)
                result = self.cursor.execute("{CALL %s (%s)}" % (procname,param_no[:len(param_no)-1]),params)
            else:
                result = self.cursor.execute("{CALL %s}" % procname)
            return result
        except pyodbc.DatabaseError as e:
            print(e)
            sys.exit
