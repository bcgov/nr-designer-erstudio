import win32com.client as win32
from os import path
from os import getcwd
from erstudiolib.spreadsheet import Spreadsheet

class ERStudio():
    '''
    This class is a wrapper around the ERStudio COM interface
    It also controls behaviour in terms of file placement
    - self.basedir - the root directory for objects read and written. Defaults to getcwd()
    - self.dm1dir - the diretory where DM1s are read/written if they are not found in the repository
    - self.defaultdir - where the default templates for a DM1 file and files used to generate the CMO file
    - self.basefile - the default DM! file that the content is layered onto


    '''
    def __init__(self, basedir=f"{getcwd()}\\"):
        self.basedir = basedir
        self.dm1dir = self.basedir + r"DM1\\"
        self.defaultdir = f"{self.basedir}templates\\"
        self.cmodir = f"{self.basedir}CMO\\"
        self.basefile = f"{self.defaultdir}default.DM1"
        self.xlsdir = f"{self.basedir}XLS\\"
        self.physicalmodelname = None
        self.fromrepo = False
        self.dm1prefix = ""
        self.appname = None
        self.filename = None
        self.diagramfile = None
        self.diagram = None
        self.model = None
        self.submodel = None
        self.entity = None
        self.app = win32.Dispatch("ERStudio.Application")
        self.attachment_text_type = 5
        self.attachment_boolean_type = 1
        self.xlsfile = Spreadsheet()

    def __del__(self):
        self.close()
        '''
        self.app.Quit()
        '''

    def addtoproject(self, projectname=None):
        if self.fromrepo:
            projects = self.app.RepoProjects()
            project = projects.Item(projectname)
            if project is None:
                project = projects.Add(projectname, '', None, None)
            diagramlist = project.GetDiagramList()
            x = diagramlist.Add(self.filename)
            project.SetDiagramList(diagramlist)
            project.AddDiagrams()
        return

    def open(self, app, projectname='Test'):
        '''

        :param file:
        :return:
        if file exists open it
        if file doesn't exist copy the basefile to this file name
        '''

        self.appname = app
        self.filename = f"{self.dm1prefix}{self.appname}.DM1"
        self.diagram = self.app.DiagramItem(self.filename)

        bool = self.app.RepoGetDiagram(self.filename)
        if bool == 1:
            '''
            Diagram exists in the repo --> check it out
            '''
            self.fromrepo = True
            self.diagram = self.app.DiagramItem(self.filename)
            bool2 = self.diagram.RepoCheckoutDiagram(True, "check out for Designer ETL run")
            if bool2 == 0:
                print(f"Problem checking out {app}")
            else:
                self.diagram = self.app.DiagramItem(self.filename)
                self.diagramfile = self.diagram.GetFullFilePath()
                print(self.diagramfile)

        else:
            '''
            Not in the Repo
            see if it exists in the designated location
            If not create it
            '''
            self.diagramfile = f"{self.dm1dir}{self.filename}"
            if not path.exists(self.diagramfile):
                # to get layout OPEN the default and save if to the new location
                self.app.OpenFile(self.basefile)
                self.diagram = self.app.DiagramItem('default.DM1')
                #            shutil.copyfile(self.basefile, self.diagramfile)
                # self.diagram = self.app.NewDiagram()
                self.diagram.SaveFile(self.diagramfile)
            else:
                self.diagram = self.app.OpenFile(self.diagramfile)
                if self.diagram is None:
                    self.diagram = self.app.ActiveDiagram()

            self.diagram.RepoAddDiagram()

        # self.diagram = self.app.NewDiagram()
        self.diagram.ProjectName = self.filename
        self.diagram.CopyrightOwner = 'Government of British Columbia'
        self.physicalmodelname = f"{self.appname.upper()}_Physical"
        models = self.diagram.Models()
        model = models.Item('Physical')
        if model is None:
            model = models.Item(self.physicalmodelname)
            if model is None:
                models.Add(self.physicalmodelname, 100)
        else:
            model.Name = self.physicalmodelname

        #self.addtoproject(projectname)
        self.diagram.SaveFile("")
        self.xlsfile.open(self.xlsdir+self.appname+'.xlsx')
        '''
        open an Excel spreadsheet for trapping all the pieces found in Designer but not in ERStudio
        '''
        return self.diagram

    def close(self):
        if self.diagramfile is not None:
            self.diagram.SaveFile("")
            if self.fromrepo:
                self.diagram.RepoCheckinDiagram("Check In after Designer ETL Run")
            self.app.CloseDiagram(self.app.ActiveDiagram().FileName)
            self.diagramfile = None
            '''
            close an Excel spreadsheet 
            '''
        self.xlsfile.close()

    def genPhysicalModel(self, gpo):
        models = self.diagram.Models()
        model = models.Item('Logical')
        if model is not None:
            physgen = model.PhysicalGenerationObject()
            physgen.GenPhysicalUsingFileBasedQuickLaunch(gpo)
        return

    def genDDL(self, ddo, modelname):
        models = self.diagram.Models()
        model = models.Item(modelname)
        ddlgen = None
        if model is not None:
            ddlgen = model.DDLGenerationObject()
            ddlgen.GenDDLUsingFileBasedQuickLaunch(ddo)
            ddlgen.DropObjects = True
            ddlgen.GenerateAliases = True
            ddlgen.GenerateSynonyms = True
            ddlgen.GenSynonymComment = True
            ddlgen.GenerateTableLabel = True
            ddlgen.GenerateTableComment = True
            ddlgen.GenerateColumnComment = True
            ddlgen.GenerateColumnDefault = True
            ddlgen.GenCommitStatement = True
            ddlgen.GenerateViews = True

            ddlgen.GenViewCreateStatement = True
            ddlgen.GenViewDropStatement = True
            ddlgen.GenerateAllEntities()
            if ddlgen.GenerateDDL():
                print('DDL Generated!')
                print(ddlgen.CreationScriptFilePath)
        return ddlgen.CreationScriptFilePath

    def setdescription(self, text):
        self.diagram.Description = text

    def setauthor(self, text):
        self.diagram.Author = text

    def setversion(self, version):
        self.diagram.Version = version

    def setObjComment(self, objectname, objecttype, comment, model_name=None):
        if comment is not None:
            if model_name is None:
                model_name = self.physicalmodelname

            models = self.diagram.Models()
            model = models.Item(model_name)
            if objecttype == 'TABLE':
                tables = model.Entities()
                table = tables.Item(objectname)
                if table is not None:
                    table.UserComments().Add(comment)
            elif objecttype == 'VIEW':
                views = model.Views()
                view = views.Item(objectname)
                if view is not None:
                    view.UserComments().Add(comment)
            elif objecttype == 'SNAP':
                mviews = model.OracleMaterializedViews()
                mview = mviews.Item(objectname)
                if mview is not None:
                    mview.UserComments().Add(comment)

    def setObjNote(self, objectname, objecttype, note, model_name=None):
        if note is not None:
            if model_name is None:
                model_name = self.physicalmodelname

            models = self.diagram.Models()
            model = models.Item(model_name)
            if objecttype == 'TABLE':
                tables = model.Entities()
                table = tables.Item(objectname)
                if table is not None:
                    table.Note = note
            elif objecttype == 'VIEW':
                views = model.Views()
                view = views.Item(objectname)
                if view is not None:
                    view.Note = note

    def setObjDescription(self, objectname, objecttype, description, model_name=None):
        if description is not None:
            if model_name is None:
                model_name = self.physicalmodelname

            models = self.diagram.Models()
            model = models.Item(model_name)
            if objecttype == 'TABLE':
                tables = model.Entities()
                table = tables.Item(objectname)
                if table is not None:
                    if table.Definition is None or len(table.Definition) == 0:
                        # don't replace reverse engineered description
                        table.Definition = description
            elif objecttype == 'VIEW':
                views = model.Views()
                view = views.Item(objectname)
                if view is not None:
                    if view.Definition is None or len(view.Definition) == 0:
                        # don't replace reverse engineered description
                        view.Definition = description
            elif objecttype == 'SNAP':
                mviews = model.OracleMaterializedViews()
                mview = mviews.Item(objectname)
                if mview is not None:
                    if mview.Definition is None or len(mview.Definition) == 0:
                        # don't replace reverse engineered description
                        mview.Definition = description

    def setAttrDescription(self, objectname, attrname, description, model_name=None):
        if description is not None:
            if model_name is None:
                model_name = self.physicalmodelname

            models = self.diagram.Models()
            model = models.Item(model_name)
            tables = model.Entities()
            table = tables.Item(objectname)
            if table is not None:
                cols = table.Attributes()
                attr = cols.Item(attrname)
                if attr is not None:
                    if attr.Definition is None or len(attr.Definition) == 0:
                        # don't replace reverse engineered description
                        attr.Definition = description

    def setAttrComment(self, objectname, attrname, comment, model_name=None):
        if comment is not None:
            if model_name is None:
                model_name = self.physicalmodelname

            models = self.diagram.Models()
            model = models.Item(model_name)
            tables = model.Entities()
            table = tables.Item(objectname)
            if table is not None:
                cols = table.Attributes()
                attr = cols.Item(attrname)
                if attr is not None:
                    attr.UserComments().Add(comment)

    def setAttrNote(self, objectname, attrname, note, model_name=None):
        if note is not None:
            if model_name is None:
                model_name = self.physicalmodelname

            models = self.diagram.Models()
            model = models.Item(model_name)
            tables = model.Entities()
            table = tables.Item(objectname)
            if table is not None:
                cols = table.Attributes()
                attr = cols.Item(attrname)
                if attr is not None:
                    attr.Note = note

    def appendObjectNotes(self, objectname, note, model_name=None):
        if model_name is None:
            model_name = self.physicalmodelname

        models = self.diagram.Models()
        model = models.Item(model_name)
        tables = model.Entities()
        table = tables.Item(objectname)
        if table is not None:
            table.Note += note

    def appendAttrNotes(self, tablename, columnname, note, model_name):
        if model_name is None:
            model_name = self.physicalmodelname

        models = self.diagram.Models()
        model = models.Item(model_name)
        tables = model.Entities()
        table = tables.Item(tablename)
        if table is not None:
            cols = table.Attributes()
            attr = cols.Item(columnname)
            if attr is not None:
                attr.Note += note

    def mergereport(self, cmo):
        self.diagram.SetActiveModel('Logical')
        mergemodel = self.diagram.MergeModelObject()
        report = f"{self.basedir}{self.appname}_mergereport.rtf"
        x = mergemodel.MergeReport(cmo, report, 1, 0)

    def compareandmerge(self, cmo, model_type='Physical'):
        self.diagram.SetActiveModel(self.physicalmodelname)
        mergemodel = self.diagram.MergeModelObject()
        if model_type == 'Physical':
            x = mergemodel.DoMerge(cmo, 2)
        elif model_type == 'Logical':
            x = mergemodel.DoMerge(cmo, 1)
        self.diagram.SaveFile("")

    def addModel(self, app, dbtype=100):
        models = self.diagram.Models()
        bob = models.Item(self.physicalmodelname)
        if bob:
            return self.physicalmodelname, bob

        self.model = models.Add(self.physicalmodelname, dbtype)
        return self.physicalmodelname, self.model

    def addSubModel(self, name, model_name=None, definition=None):
        if model_name is None:
            model_name = self.physicalmodelname

        models = self.diagram.Models()
        model = models.Item(model_name)

        if model is not None:
            self.diagram.SetActiveModel(model_name)

        submodels = model.SubModels()
        submodel = submodels.Item(name)
        if submodel is None:
            submodel = submodels.Item("Main Model")
            submodel.ActivateSubModel()
            submodel = submodels.Add(name)
            submodel.ActivateSubModel()

        self.submodel = submodel
        '''
        if definition is not None:
            self.submodel.Definition = definition
        '''
        return self.submodel

    def add_physobj_to_submodel(self, object_name, object_type, model_name=None):
        if model_name is None:
            model_name = self.physicalmodelname

        models = self.diagram.Models()
        model = models.Item(model_name)
#        ents = []
#        self.submodel.EntityNames(ents)
        if model.Logical:
            object_name = object_name.title()

        if object_type == 'VW':
            if model.Views() is not None:
                views = model.Views()
                if views.Item(object_name) is not None:
                    viewds = self.submodel.ViewDisplays()
                    if viewds.Item(object_name) is None:
                        viewds.Add(object_name)

        elif object_type == 'TBL':
            if model.Entities() is not None:
                ents = model.Entities()
                ent = ents.Item(object_name.title())
                if ent is not None:
                    entds = self.submodel.EntityDisplays()
                    if entds.Item(object_name) is None:
                        entds.Add(object_name)
                    '''
                    reld = self.submodel.RelationshipDisplays()
                    rels = ent.ChildRelationships()
                    if rels is not None:
                        for i in range(rels.Count):
                            rel = rels.Item(i)
                            reld.Add(rel.ID)

                    rels = ent.ParentRelationships()
                    if rels is not None:
                        for i in range(rels.Count):
                            rel = rels.Item(i)
                            reld.Add(rel.ID)
                    '''

        elif object_type == 'ENT':
            if model.Entities() is not None:
                ents = model.Entities()
                ent = ents.Item(object_name.title())
                if ent is not None:
                    entds = self.submodel.EntityDisplays()
                    if entds.Item(object_name) is None:
                        entds.Add(object_name)
                    '''    
                    reld = self.submodel.RelationshipDisplays()
                    rels = ent.ChildRelationships()
                    if rels is not None:
                        for i in range(rels.Count):
                            rel = rels.Item(i)
                            reld.Add(rel.ID)

                    rels = ent.ParentRelationships()
                    if rels is not None:
                        for i in range(rels.Count):
                            rel = rels.Item(i)
                            reld.Add(rel.ID)
                    '''

        elif object_type == 'SNP':
            if model.OracleMaterializedViews() is not None:
                mviews = model.OracleMaterializedViews()
                if mviews.Item(object_name) is not None:
                    mviewds = self.submodel.MaterializedViewDisplays()
                    if mviewds.Item(object_name) is None:
                        mviewds.Add(object_name)
        #self.diagram.SaveFile("")

    def addEntNametoPhys(self, tabname, entname, model_name='Logical'):
        models = self.diagram.Models()
        model = models.Item(model_name)
        ents = model.Entities()
        ent = ents.Item(tabname)
        if ent is not None:
            if entname is not None:
                ent.EntityName = entname
        else:
            self.xlsfile.write((self.appname, 'Entity', tabname))

    def addEntity(self, name, definition):
        bob = self.model.Entities.Item(name)
        if bob:
            return bob

        self.entity = self.model.Entities.Add(0, 0)
        if definition is not None:
            self.entity.Definition = definition
        self.entity.EntityName = name

    def add_fk_phrase(self, fk, phrase, inverse, model_name='Logical'):
        if model_name is None:
            model_name = self.physicalmodelname

        models = self.diagram.Models()
        model = models.Item(model_name)
        rels = model.Relationships()
        rel = rels.Item(fk)
        if rel is not None:
            rel.VerbPhrase = phrase
            rel.InversePhrase = inverse
        else:
            self.xlsfile.write((self.appname, 'Foreign Key', fk))


    def add_attr_name(self, tablename, columnname, attributename, domain=None, model_name='Logical'):
        if model_name is None:
            model_name = self.physicalmodelname

        models = self.diagram.Models()
        model = models.Item(model_name)
        tables = model.Entities()
        table = tables.Item(tablename)
        if table is not None:
            cols = table.Attributes()
            attr = cols.Item(columnname)
            if attr is not None:
                attr.AttributeName = attributename
                if domain is not None:
                    dd = self.diagram.Dictionary
                    dom = dd.Domains().Item(domain)
                    if dom is not None:
                        attr.DomainId = dom.ID
            else:
                self.xlsfile.write((self.appname, 'Atribute', tablename+'.'+columnname))

        # self.diagram.SaveFile("")
    def fixaudtitcols(self, name, model_name='Logical'):
        if model_name is None:
            model_name = self.physicalmodelname

        models = self.diagram.Models()
        model = models.Item(model_name)
        tables = model.Entities()
        table = tables.Item(name)
        if table is not None:
            cols = table.Attributes()
            attr = cols.Item("WHO_UPDATED")
            if attr is not None:
                attr.AttributeName = "Who Updated"
            attr = cols.Item("WHO_CREATED")
            if attr is not None:
                attr.AttributeName = "Who Created"
            attr = cols.Item("WHEN_UPDATED")
            if attr is not None:
                attr.AttributeName = "When Updated"
            attr = cols.Item("WHEN_CREATED")
            if attr is not None:
                attr.AttributeName = "When Created"



    def add_domain(self, name, attributename, columnname, datatype, datalength, datascale, default, nullable, note, definition, comment, parentdomain):
        dd = self.diagram.Dictionary
        domain = dd.Domains().Add(name, columnname.replace(' ','_'))
        domain.AttributeName = attributename
        domain.Datatype = datatype
        domain.DataLength = datalength
        domain.DataScale = datascale
        domain.Definition = definition
        domain.ParentDomain = parentdomain
        domain.Note = note
        domain.DeclaredDefault = default
        if domain.UserComments() is not None:
            domain.UserComments().Add(comment)
        # domain.Nullable = nullable

    def addtagtype(self, description, tagtype='Tag'):
        attachtypes = self.diagram.Dictionary.AttachmentTypes()
        attachtype = attachtypes.Item(tagtype)
        if not attachtype:
            attachtype = attachtypes.Add(tagtype, description)

        return attachtype

    def addtag(self, tag, type, description, value, tagtype='Tag'):
        attachtype = self.addtagtype('Tags used to indicate metadata about the model', tagtype)
        if attachtype is not None:
            attachments = attachtype.Attachments()
            attachment = attachments.Item(tag)
            if attachment is None:
                attachment = attachments.Add(tag, description, value, type)
                if attachment is not None:
                    bound = self.diagram.BoundAttachments().Add(attachment.ID)
            else:
                attachment.ValueDefault = value
        return
'''
Designer 
- query should mirror tables


ERSTudio
- Dictionary Name: {App}_DD
- Name : 			i$sdd_dom.NAME
- AttributeName: 		i$sdd_dom.NAME
- ColumnName: 			i$sdd_dom.NAME
- DataType:			i$sdd_dom.DATATYPE
- DataLength			i$sdd_dom.MAXIMUM_ATTRIBUTE_LENGTH
- DataScale			i$sdd_dom.COLUMN_PRECISION
- DeclaredDefault		i$sdd_dom.DEFAULT_VALUE
- Nullable			i$sdd_dom.NULL_VALUE
- Note
- Definition			i$sdd_dom.Description
- ParentDomain			i$sdd_dom.supertyperef

'''