from os import getlogin
from erstudiolib.ERSdbtypes import ERSdbtypes


class GPO():
    '''
    This class is used to generate an ERStudio Physical model for a particular target database.
    The default database type is is PostgreSQL 10 and above

    '''

    def __init__(self):
        self.default_locn = f"C:\\Users\\{getlogin()}\\ERSTUDIO\\DEFAULT\\"
        self.gpo_location = f"C:\\Users\\{getlogin()}\\ERSTUDIO\\GPO\\"
        self.Destination = ERSdbtypes().Destination
        self.dbtype = self.Destination["PostgreSQL 10.x-12.x"]
        self.indexstorage = "bobidx"
        self.tablestorage = "bob"
        self.namingtemplate = "[none]"

    def getBoilerText(self, filename):
        fo = open(filename, 'r')
        return fo.read()

    def getdbtypes(self):
        return self.Destination.keys()

    def getdbtype(self):
        return self.dbtype

    def setdbtype(self, dbtype="PostgreSQL 10.x-12.x"):
        self.dbtype = self.Destination[dbtype]

    def setindexstorage(self, storage):
        self.indexstorage = storage

    def getindexstorage(self):
        return self.indexstorage

    def settablestorage(self, storage):
        self.tablestorage = storage

    def gettablestorage(self):
        return self.tablestorage

    def setnamingtemplate(self, template="[none]"):
        self.namingtemplate = template

    def getnamingtemplate(self, template="[none]"):
        return self.namingtemplate

    def write(self, appname):
        physDestModel = appname + self.dbtype[3]
        headerBoiler = self.getBoilerText(f"{self.default_locn}template{self.dbtype[3]}.gpo")

        physHeader = headerBoiler.format(targetdatabaseid=self.dbtype[0],
                                         PhysicalModel=physDestModel,
                                         targetdb=self.dbtype[1],
                                         indexstorage=self.indexstorage,
                                         datamapping=self.dbtype[2],
                                         namingtemplate=self.namingtemplate,
                                         tablestorage=self.tablestorage)

        physgpoName = f'{self.gpo_location}{appname}_{self.dbtype[3]}.gpo'

        physFo = open(physgpoName, 'w')
        physFo.write(physHeader)
        physFo.close()
        return physgpoName
