from os import getlogin
from os import getcwd

class CMO():
    '''
    This clas is used to generate ERStudio Compare and Merge configuration files
    for an app and schema
    '''
    def __init__(self):
        self.default_locn = f"{getcwd()}\\templates\\"
        self.cmo_location = f"{getcwd()}\\CMO\\"
        self.dm1_location = f"{getcwd()}\\DM1\\"

    def getBoilerText(self, filename):
        fo = open(filename, 'r')
        return fo.read()

    def write(self, appname, schema, db, objects):
        physDestModel = appname + "_Physical"
        subModel = "Main Model"
        logSourceModel = "Logical"
        physDBScriptfile = f"C:\\Users\\{getlogin()}\\AppData\\Roaming\\Idera\\ERStudio\\SQLCode\\{physDestModel}.sql"
#        logDBScriptfile = f"C:\\Users\\bjgilles\\AppData\\Roaming\\Idera\\ERStudio\\SQLCode\\Logical.bas"
        username = getlogin()

        headerBoiler = self.getBoilerText(f"{self.default_locn}physical_model_header.cmo")
        logheaderBoiler = self.getBoilerText(f"{self.default_locn}logical_model_header.cmo")

        appFile = f'{self.dm1_location}test_{appname}.dm1'
        physHeader = headerBoiler.format(appfile="", modDBScriptfile=physDBScriptfile, sourceModel=physDestModel,
                                         sourceSubModel=subModel, targetModel="", targetSubModel="",
                                         Username=username, db=db, schema=schema)
        logHeader = logheaderBoiler.format(appfile="", modDBScriptfile=physDBScriptfile, sourceModel=physDestModel,
                                           sourceSubModel=subModel, targetModel=logSourceModel, targetSubModel=subModel,
                                           Username=username, db=db)
        footerBoiler = self.getBoilerText(f"{self.default_locn}Footer.txt")

        physcmoName = f'{self.cmo_location}{appname}_physical_{db}_{schema}.cmo'
        logcmoName = f'{self.cmo_location}{appname}_logical_{db}_{schema}.cmo'

        physFo = open(physcmoName, 'w')
        physFo.write(physHeader)

        logFo = open(logcmoName, 'w')
        logFo.write(logHeader)

        if len(objects['ENT']) > 0:
            logFo.write('<m_SourceEntityList>\n')
            for obj in objects['ENT']:
                logFo.write(f'<Object ObjectName="{obj}" OwnerName="{schema}"/>\n')
            logFo.write('</m_SourceEntityList>\n')

        if len(objects['TABLE']) > 0:
            logFo.write('<m_SourceEntityList>\n')
            physFo.write('<m_TargetEntityList>\n')
            for obj in objects['TABLE']:
                physFo.write(f'<Object ObjectName="{obj}" OwnerName="{schema}"/>\n')
                logFo.write(f'<Object ObjectName="{obj}" OwnerName="{schema}"/>\n')

            logFo.write('</m_SourceEntityList>\n')
            physFo.write('</m_TargetEntityList>\n')

        if len(objects['VIEW']) > 0:
            physFo.write('<m_TargetViewList>\n')
            for obj in objects['VIEW']:
                physFo.write(f'<Object ObjectName="{obj}" OwnerName="{schema}"/>\n')
            physFo.write('</m_TargetViewList>\n')

        if len(objects['MATERIALIZED VIEW']) > 0:
            physFo.write('<m_TargetMaterializedViewList>\n')
            for obj in objects['MATERIALIZED VIEW']:
                physFo.write(f'<Object ObjectName="{obj}" OwnerName="{schema}"/>\n')
            physFo.write('</m_TargetMaterializedViewList>\n')

        if len(objects['SEQUENCE']) > 0:
            physFo.write('<m_TargetSequenceList>\n')
            for obj in objects['SEQUENCE']:
                physFo.write(f'<Object ObjectName="{obj}" OwnerName="{schema}"/>\n')
            physFo.write('</m_TargetSequenceList>\n')

        if len(objects['SYNONYM']) > 0:
            physFo.write('<m_TargetSynonymList>\n')
            for obj in objects['SYNONYM'].keys():
                owner = objects['SYNONYM'][obj]['Owner']
                physFo.write(f'<Object ObjectName="{obj}" OwnerName="{owner}"/>\n')
            physFo.write('</m_TargetSynonymList>\n')

        physFo.write(footerBoiler)
        physFo.close()
        logFo.write(footerBoiler)
        logFo.close()
        return (physcmoName, logcmoName)
