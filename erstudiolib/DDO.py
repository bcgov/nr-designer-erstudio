from os import getlogin
from erstudiolib.ERSdbtypes import ERSdbtypes


class DDO():
    '''
    This class is used to generate SQL from an ERStudio Physical model for a particular target database.
    The default database type is is PostgreSQL 10 and above

    '''
    def __init__(self):
        self.default_locn = f"C:\\Users\\{getlogin()}\\ERSTUDIO\\DEFAULT\\"
        self.ddo_location = f"C:\\Users\\{getlogin()}\\ERSTUDIO\\DDO\\"
        self.sql_location = f"C:\\Users\\{getlogin()}\\ERSTUDIO\\SQLCode\\"
        self.Destination = ERSdbtypes().Destination
        self.dbtype = self.Destination["PostgreSQL 10.x-12.x"]

    def getBoilerText(self, filename):
        fo = open(filename, 'r')
        return fo.read()

    def getdbtypes(self):
        return self.Destination.keys()

    def setdbtype(self, dbtype="PostgreSQL 10.x-12.x"):
        self.dbtype = self.Destination[dbtype]

    def write(self, appname):
        physDestModel = appname + self.dbtype[3]
        headerBoiler = self.getBoilerText(f"{self.default_locn}template{self.dbtype[3]}.ddo")
        multiscriptfiledir = f"{self.sql_location}//{physDestModel}"
        physHeader = headerBoiler.format(MultiScriptFileDir=multiscriptfiledir,
                                         SQLCodeDirectory=self.sql_location,
                                         SQLCodeWorkingDirectory=self.sql_location,
                                         SingleSourceScriptFilePath=f"{self.sql_location}//{physDestModel}.sql")

        physddoName = f'{self.ddo_location}{appname}{self.dbtype[3]}.ddo'

        physFo = open(physddoName, 'w')
        physFo.write(physHeader)
        physFo.close()
        return physDestModel, physddoName
