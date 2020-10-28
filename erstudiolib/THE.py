from erstudiolib.dbconnect import DBConnect
from erstudiolib.CMO import CMO


class the_objects():
    '''
    This class is a wrapper arounf DBP01's proxy_object_usage table to seperate the THE schems into
    individual ERStudio diagrams and build the CMOs needed to reverse enigneer the objects
    '''


    def __init__(self, dsn='dbp01'):
        self.db = DBConnect(dsn)

    def __del__(self):
        if self.db.connection is not None:
            self.db.connection.close()

    def appCMO(self, source):
        app = source[0]
        if app == 'ADAM (FOR)':
            app = 'ADAM'

        sql = f"""select sys_context('USERENV','CON_NAME'), APPLICATION_ACRONYM, OBJECT_TYPE, OBJECT_NAME ,''
        FROM THE.PROXY_OBJECT_USAGE 
        WHERE OBJECT_TYPE in ('VIEW','TABLE','MATERIALIZED VIEW','SYNONYM','SEQUENCE')
        and APPLICATION_ACRONYM = '{app}' 
        ORDER BY 1,2,3"""
        cur = self.db.connection.cursor()
        cur.execute(sql)
        objs = cur.fetchall()
        cur.close()
        CMOs = []
        if len(objs) > 0:
            objList = {}
            objList['TABLE'] = {}
            objList['VIEW'] = {}
            objList['MATERIALIZED VIEW'] = {}
            objList['SEQUENCE'] = {}
            objList['SYNONYM'] = {}
            objList['ENT'] = {}

            for obj in objs:
                '''
                objList[object_type][object_name] = 0
                '''
                objList[obj[2]][obj[3]] = {}
                objList[obj[2]][obj[3]]['EntityName'] = ''
                objList[obj[2]][obj[3]]['Owner'] = source[2]


            cmo = CMO()
            CMOs = cmo.write(source[0], source[2], source[1], objList)

        return CMOs

