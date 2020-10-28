from erstudiolib.dbconnect import DBConnect


class IrsApplications():

    def __init__(self, dsn='rdrprod1'):
        self.db = DBConnect(dsn)

    def __del__(self):
        if self.db.connection is not None:
            self.db.connection.close()

    def getdescription(self, app):
        sql = f"SELECT TEXT FROM BJG_IRS_APPLICATIONS WHERE APPLICATION_NAME = upper('{app}')"
        cur = self.db.connection.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        cur.close()
        return row

    def getfullname(self, app):
        sql = f"SELECT FULL_NAME FROM BJG_IRS_APPLICATIONS WHERE APPLICATION_NAME = upper('{app}')"
        cur = self.db.connection.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        cur.close()
        return row
