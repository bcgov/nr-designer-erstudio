from erstudiolib.dbconnect import DBConnect
from erstudiolib.CMO import CMO
from erstudiolib.THE import the_objects


class Containers():
    '''
    This class is a wrapper around the table used to drive the migration process.
    It reads the app/schemas/Designer repo information into a Dictionary used to
    build and executed the necessary steps for a migration
    '''

    def __init__(self, run='Y', dsn='rdrprod1'):
        self.db = DBConnect(dsn)
        self.run = run

    def __del__(self):
        if self.db is not None:
            if self.db.connection is not None:
                self.db.connection.close()

    def buildCMOs(self):
        '''
        ERStudio allows for a configuration file, with the suffix 'CMO' to be used when preformaing a compare and merge.
        The Automation Inteface object for Compare and Merge allows one to specify a CMO file to run a compare and merge

        This function builds a structure , for each app, to contain point to a Physical and Logical CMO file
        for each Schema within the app

        It then calls the appropriate subroutine to build the CMO file for a schema in that app
        :return:
        A Dictionary with Information about the app, and the location of any CMO files
        '''
        CMOlist = {}
        sql = f"""SELECT APPLICATION_NAME,
            INSTANCE_NAME,
            SCHEMA_NAME,
            REPO,
            WORKAREA,
            CONTAINER,
            ERSTUDIO
            FROM BJG_CONTAINERS
            WHERE
                RUN='{self.run}'
            ORDER BY 1,3,4"""

        cur = self.db.connection.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        app = ""
        for row in rows:
            print(row)
            if app != row[0]:
                CMOlist[row[0]] = {}
                CMOlist[row[0]]['DESIGNER REPOSITORY'] = row[3]
                CMOlist[row[0]]['WORK AREA'] = row[4]
                CMOlist[row[0]]['DESIGNER NAME'] = row[5]
                CMOlist[row[0]]['DIAGRAM NAME'] = row[6]
                CMOlist[row[0]]['SCHEMAS'] = {}
                app = row[0]
            if row[2] != 'THE':
                CMOs = self.schemaCMO(row)
            else:
                the = the_objects()
                CMOs = the.appCMO(row)

            if len(CMOs) > 0:
                CMOlist[row[0]]['SCHEMAS'][row[2]] = CMOs

        return CMOlist

    def schemaCMO(self, source):
        dsn = source[1]
        if dsn == 'airprod1':
            dsn = 'airprod'

        schemadb = DBConnect(dsn)

        sql = f"select '{source[1]}',owner,object_type, object_name from all_objects where owner = '{source[2]}' and object_type in ( 'SEQUENCE','TABLE', 'VIEW', 'MATERIALIZED VIEW') and (object_name not like 'MLOG$%' and object_name not like 'RUPD$%')"
        sql2 = f"select '{source[1]}', owner, 'SYNONYM', synonym_name from all_synonyms where table_owner = '{source[2]}'"
        appcur = schemadb.connection.cursor()
        appcur.execute(sql)
        objs = appcur.fetchall()
        appcur.execute(sql2)
        syns = appcur.fetchall()
        appcur.close()
        CMOs = []
        if len(objs) > 0:
            objList = {'TABLE': {},
                       'VIEW': {},
                       'MATERIALIZED VIEW': {},
                       'SEQUENCE': {},
                       'SYNONYM': {},
                       'ENT': {}}

            for obj in objs:
                '''
                objList[object_type][object_name] = 0
                '''
                objList[obj[2]][obj[3]] = {}
                objList[obj[2]][obj[3]]['EntityName'] = ''
                objList[obj[2]][obj[3]]['Owner'] = obj[1]

            # so at this  point fill in the designer bits I guess....
            for syn in syns:
                objList[syn[2]][syn[3]] = {}
                objList[syn[2]][syn[3]]['EntityName'] = ''
                objList[syn[2]][syn[3]]['Owner'] = syn[1]

            cmo = CMO()
            CMOs = cmo.write(source[0], source[2], dsn, objList)

        schemadb.connection.close()
        return CMOs
