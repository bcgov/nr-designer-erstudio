from erstudiolib.dbconnect import DBConnect

class Designer():
    '''
    A set of methods to conect to a Designer repository and return information from the repository
    '''
    def __init__(self, dsn='rdrprod1'):
        self.db = DBConnect(dsn)

    def __del__(self):
        self.close()

    def close(self):
        self.db.close()

    def get_physmodels_for_app(self, app, wa):
        sql = f"select distinct diagram_name from bjg_app_model_obj where object_type <> 'ENT' and upper(application_name) = '{app.upper()}' and upper(wa_name) = '{wa.upper()}'"
        cur = self.db.connection.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_logmodels_for_app(self, app, wa):
        sql = f"select distinct diagram_name from bjg_app_model_obj where object_type = 'ENT' and upper(application_name) = '{app.upper()}' and upper(wa_name) = '{wa.upper()}'"
        cur = self.db.connection.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_physmodel_objects_for_app(self, app, wa, model):
        sql = f"select distinct object_name, object_type from bjg_app_model_obj where upper(application_name) = '{app.upper()}' and upper(wa_name) = '{wa.upper()}' and upper(diagram_name) = '{model.upper()}' and object_type <> 'ENT'"
        cur = self.db.connection.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_logmodel_objects_for_app(self, app, wa, model):
        sql = f"select distinct object_name, object_type from bjg_app_model_obj where upper(application_name) = '{app.upper()}' and upper(wa_name) = '{wa.upper()}' and upper(diagram_name) = '{model.upper()}' and object_type = 'ENT'"
        cur = self.db.connection.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_fk_phrases(self, app, wa):
        sql = f"select distinct fkname, phrase, inverse_phrase from bjg_fk where upper(appname) = '{app.upper()}' and upper(waname) = '{wa.upper()}' order by 1"
        cur = self.db.connection.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_descriptions_for_app(self, app, wa):
        sql = f"select distinct appname, author, appdescription, appnote, appcomment, title from BJG_WA_APP where upper(appname) = '{app.upper()}' and upper(waname) = '{wa.upper()}'"
        cur = self.db.connection.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_phys_tab_descriptions_for_app(self, app, wa, tabname=None, tabtype=None):
        if tabname is None:
            sql = f"select distinct tabname, table_type, tabdescription, tabnote, tabcomment from BJG_WA_APP_TAB_COL where upper(appname) = '{app.upper()}' and upper(waname) = '{wa.upper()}' order by 1, 2"
        else:
            if tabtype is None:
                sql = f"select distinct tabname, table_type, colname, coldescription, colnote, colcomment from BJG_WA_APP_TAB_COL where upper(appname) = '{app.upper()}' and upper(waname) = '{wa.upper()}' and upper(tabname) = '{tabname.upper()}' order by 1, 2, 3"
            else:
                sql = f"select distinct tabname, table_type, colname, coldescription, colnote, colcomment from BJG_WA_APP_TAB_COL where upper(appname) = '{app.upper()}' and upper(waname) = '{wa.upper()}' and upper(tabname) = '{tabname.upper()}' and upper(table_type) = '{tabtype.upper()}' order by 1, 2, 3"
        cur = self.db.connection.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_physmodel_entnames_for_app(self, app, wa):
        sql = f"select distinct tabname, entname from BJG_WA_APP_TAB_COL where upper(appname) = '{app.upper()}' and upper(waname) = '{wa.upper()}' order by 1"
        cur = self.db.connection.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_lognames_for_app(self, app, wa):
        sql = f"select distinct tabname, colname, entname, attrname, name from BJG_WA_APP_COL_DOM where  upper(appname) = '{app.upper()}' and upper(waname) = '{wa.upper()}' order by 3,4"
        cur = self.db.connection.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_domains_for_app(self, app, wa):
        sql1 = f"select waname,appname,parentdomain,name,attributename,columnname,description,note,comments,datatype,datalength,datascale,declareddefault,nullable from bjg_wa_app_col_dom where parentdomain is NULL and upper(appname) = '{app.upper()}' and upper(waname) = '{wa.upper()}'"
        sql2 = f"select waname,appname,parentdomain,name,attributename,columnname,description,note,comments,datatype,datalength,datascale,declareddefault,nullable from bjg_wa_app_col_dom where parentdomain is NOT NULL and upper(appname) = '{app.upper()}' and upper(waname) = '{wa.upper()}'"
        cur = self.db.connection.cursor()
        cur.execute(sql1)
        rows = cur.fetchall()
        cur.execute(sql2)
        rows.extend(cur.fetchall())
        cur.close()
        return rows

    def get_domain(self, app, wa, ent, attr):
        sql1 = f"select waname,appname,parentdomain,name,attributename,columnname,description,note,comments,datatype,datalength,datascale,declareddefault,nullable from bjg_wa_app_col_dom where waname = '{wa}' and appname = '{app}' and entname = '{ent}' and attrname = '{attr}' order by waname,appname, name"
        cur = self.db.connection.cursor()
        cur.execute(sql1)
        row = cur.fetchone()
        cur.close()
        return row
'''

'''
