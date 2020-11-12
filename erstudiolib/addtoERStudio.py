from erstudiolib.ERStudio import ERStudio
from erstudiolib.Designer import Designer


class AddtoERStudio():
    def __init__(self):
        self.ERS = ERStudio()
        self.repo = None
        self.designer = None
        self.physmodel = None
        self.appname = None
        self.physmodelname = None
        self.designername = None
        self.workarea = None
        self.wa = None

    def setapp(self, app):
        self.appname = app
        self.physmodelname = f"{self.appname.upper()}_Physical"

    def setrepo(self, repo):
        if repo != self.repo:
            if self.repo is not None:
                self.designer.close()
            if repo is not None:
                self.designer = Designer(repo)
            self.repo = repo
            self.ERS.xlsfile.setdesignerrepo(repo)

    def openERS(self, app=None, diagram=None, workarea=None, designername=None):
        if app != self.appname:
            if self.appname is not None:
                self.ERS.close()

            self.designername = designername
            self.workarea = workarea

            self.setapp(app)
            self.ERS.open(diagram)
            if self.workarea is not None:
                self.ERS.xlsfile.setworkarea(self.workarea)
            self.physmodelname, self.physmodel = self.ERS.addModel(self.appname)
        return self.ERS

    def close(self):
        self.ERS.close()

    def adddescription(self, description):
        if description is not None and description[0] is not None:
            self.ERS.setdescription(description[0])
        else:
            desc = self.designer.get_descriptions_for_app(self.designername, self.workarea)
            if len(desc) > 0:
                self.ERS.setdescription(desc[0][2])

    def addfullname(self, fullname):
        if fullname is not None and fullname[0] is not None:
            self.ERS.addtag('Application Name', self.ERS.attachment_text_type, 'The Full Name of the Application from IRS', fullname[0])
        else:
            title = self.designer.get_descriptions_for_app(self.designername, self.workarea)
            if len(title) > 0:
                self.ERS.addtag('Application Name', self.ERS.attachment_text_type,  'The Full Name of the Application from Designer', fullname[0][6])

    def addversion(self, version):
        if version is not None:
            self.ERS.setversion(version)

    def addauthor(self):
        if self.designername:
            author = self.designer.get_descriptions_for_app(self.designername, self.workarea)
            if len(author) > 0:
                self.ERS.setauthor(author[0][1])
        return

    def addconvertedtag(self):
        self.ERS.addtag('Converted from Designer', self.ERS.attachment_boolean_type, 'Whether the model was converted from Designer', 'True')

    def addIRSlink(self, shortname):
        self.ERS.addtag('IRS Link', self.ERS.attachment_text_type, 'The Full Name of the Application from IRS', f"https://a100.gov.bc.ca/int/irs/viewApplication.do?name={shortname}")

    def mergereport(self, cmo):
        self.ERS.mergereport(cmo)

    def addlogmodel(self, cmo):
        print("Adding the Logical Model")
        self.ERS.compareandmerge(cmo, 'Logical')

    def addphysmodel(self, cmo):
        '''

        :return:

        Generate cmo files for logical and physical
        call ERSTudio method for each cmo file

        Result SHOULD be
            Physical Model from DB
            Logical model from Physical Model but with Physical Names
        '''
        print("Adding the Physical Model")
        self.ERS.compareandmerge(cmo, 'Physical')

    def addphysdescriptions(self):
        print("Adding Physical Object Descriptions")
        if self.ERS is None:
            self.openERS()

        if self.designername:
            tables = self.designer.get_phys_tab_descriptions_for_app(self.designername, self.workarea)
            for table in tables:
                self.ERS.setObjComment(table[0], table[1], table[4])
                self.ERS.setObjNote(table[0], table[1], table[3])
                self.ERS.setObjDescription(table[0], table[1], table[2])
                if table[1] == 'TABLE':
                    cols = self.designer.get_phys_tab_descriptions_for_app(self.designername, self.workarea, table[0], table[1])
                    for col in cols:
                        self.ERS.setAttrDescription(table[0], col[2], col[3])
                        self.ERS.setAttrNote(table[0], col[2], col[4])
                        self.ERS.setAttrComment(table[0], col[2], col[5])
        return

    def addphyssubmodels(self):
        print("Adding Physical Submodels")
        if self.ERS is None:
            self.openERS()

        if self.designername:
            models = self.designer.get_physmodels_for_app(self.designername, self.workarea)
            for model in models:
                self.ERS.addSubModel(model[0],self.physmodelname)
                objects = self.designer.get_physmodel_objects_for_app(self.designername, self.workarea, model[0])
                for obj in objects:
                    self.ERS.add_physobj_to_submodel(obj[0], obj[1],self.physmodelname)

        self.ERS.diagram.SaveFile()

    def addlogsubmodels(self):
        print("Adding Logical Submodels")
        if self.ERS is None:
            self.openERS()

        if self.designername:
            models = self.designer.get_logmodels_for_app(self.designername, self.workarea)
            for model in models:
                self.ERS.addSubModel(model[0], model_name='Logical')
                objects = self.designer.get_logmodel_objects_for_app(self.designername, self.workarea, model[0])
                for obj in objects:
                    self.ERS.add_physobj_to_submodel(obj[0], obj[1], 'Logical')

        self.ERS.diagram.SaveFile()

    def addentnames(self):
        print("Adding Entity Names")
        if self.ERS is None:
            self.ERS = self.openERS()

        if self.designername:
            objects = self.designer.get_physmodel_entnames_for_app(self.designername, self.workarea)
            for obj in objects:
                self.ERS.addEntNametoPhys(obj[0], self.erstitle(obj[1]))

    def erstitle(self, name):
        if name.startswith(self.appname+' '):
            newname = self.appname + ' ' + name[len(self.appname)+1:].title()
        elif name.startswith(self.appname+'_'):
            newname = self.appname + '_' + name[len(self.appname)+1:].title()
        else:
            newname = name.title()
        return newname

    def addattrnames(self):
        print("Adding Attribute Names")
        if self.ERS is None:
            self.ERS = self.openERS()

        if self.designername:
            '''
            get a list of table/
            '''
            objects = self.designer.get_lognames_for_app(self.designername, self.workarea)
            ent = ""
            if objects is not None:
                if len(objects) > 0:
                    '''
                    Get the name of the first entity
                    '''
                    ent = objects[0][2]


            for obj in objects:
                '''
                this seems to be the logical (no pun etc) place to check
                if WHO_UPDATED etc is in the attribute list and if so update it
                '''
                '''
                obj[0] = tabname,
                obj[1] = colname,
                obj[2] = entname, 
                obj[3] = attname, 
                obj[4] = domain
            
                order by entname, attname
                '''

                if obj[2] != ent:
                    ''''''
                    self.ERS.fixaudtitcols(self.erstitle(obj[2]))
                    ent = self.erstitle(obj[2])

                domain = None
                if obj[4] is not None:
                    try:
                        domain = self.designer.get_domain(self.designername, self.workarea, obj[2], obj[3])[3]
                    except:
                        print ("error on ", obj[0], obj[1], obj[2], obj[3], obj[4])

                self.ERS.add_attr_name(self.erstitle(obj[2]), obj[1], self.erstitle(obj[3]), domain)
            '''
            need a bit of code to fix the last entity in the list
            '''

    def add_rel_phrases(self):
        print("Adding Relationship Phrases")
        if self.ERS is None:
            self.ERS = self.openERS()

        if self.designername:
            phrases = self.designer.get_fk_phrases(self.designername, self.workarea)
            for phrase in phrases:
                self.ERS.add_fk_phrase(phrase[0], phrase[1], phrase[2])

    def add_domains(self):
        print("Adding Domains")
        if self.ERS is None:
            self.ERS = self.openERS()

        if self.designername:
            domains = self.designer.get_domains_for_app(self.designername, self.workarea)
            for domain in domains:
                if len(domain) > 0:
                    datatype = domain[9]
                    if datatype == 'VARCHAR2':
                        datatype = 'VARCHAR'
                    elif datatype == 'NUMBER':
                        datatype = 'NUMERIC'
                    elif datatype == 'BINARY_DOUBLE':
                        datatype = 'DOUBLE PRECISION'
                    elif datatype == 'BINARY_FLOAT':
                        datatype = 'FLOAT'
                    elif datatype == 'FLOAT':
                        datatype = 'REAL/SMALLFLOAT'
                    elif datatype == 'LONG':
                        datatype = 'LONG VARCHAR'
                    elif datatype == 'LONG RAW':
                        datatype = 'IMAGE/LONGBINARY'
                    elif datatype == 'CLOB':
                        datatype = 'TEXT'
                    elif datatype == 'BLOB':
                        datatype = 'PICTURE'
                    elif datatype == 'NCLOB':
                        datatype = 'NTEXT/LONG NVARCHAR'
                    elif datatype == 'RAW':
                        datatype = 'BINARY'
                    elif datatype == 'ROWID':
                        datatype = 'ROWID/VARCHAR(18)'
                    elif datatype == 'MSLABEL':
                        datatype = 'MSLABEL/VARCHAR(18)'
                    elif datatype == 'SDO_GEOMETRY' or datatype.upper() == 'MDSYS.SDO_GEOMETRY':
                        datatype = 'GEOMETRY'
                    elif datatype == 'TIMESTAMP':
                        datatype = 'DATETIME'
                    elif datatype == 'ROWID':
                        datatype = 'ROWID/VARCHAR(18)'
                    elif datatype == 'INTERVAL YEAR (2) TO MONTH' or datatype == 'INTERVAL':
                        datatype = 'INTERVAL'
                    elif datatype.upper() == 'XMLTYPE' or datatype.upper() == 'SYS.XMLTYPE':
                        datatype = 'XML'
                    elif datatype.upper() == 'URITYPE' or datatype.upper() == 'SYS.URITYPE':
                        datatype = 'CHAR(10)'
                    elif datatype.upper() == 'HTTPURITYPE' or datatype.upper() == 'SYS.HTTPURITYPE':
                        datatype = 'CHAR(10)'

                    self.ERS.add_domain(name=domain[3],
                                        attributename=domain[4],
                                        columnname=domain[5],
                                        datatype=datatype,
                                        datalength=domain[10],
                                        datascale=domain[11],
                                        default=domain[12],
                                        nullable=domain[13],
                                        note=domain[7],
                                        definition=domain[6],
                                        comment=domain[8],
                                        parentdomain=domain[2])
