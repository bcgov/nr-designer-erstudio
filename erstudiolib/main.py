from erstudiolib.addtoERStudio import AddtoERStudio
from erstudiolib.IrsApplications import IrsApplications
from erstudiolib.Containers import Containers
from erstudiolib.SVNParse import getAppVersionfromSVN
import sys
import getopt


def ersmain():
    '''
    This routine executes a run of the Designer to ERStudio content migration.
    It reads one parameter, passed at the command like, which specifies the value of the 'RUN' column on the
    CONTAINERS table be to used for this run.

    :return:
    '''
    run = 'Y'
    input_args = sys.argv[1:]
    try:
        opts, args = getopt.getopt(input_args, "hpdt:fm:vownsrc:ieRS:1", ["type="])
        if len(args) > 0:
            run = args[0]
    except getopt.GetoptError as err:
        print()
        sys.exit(1)
    '''
    Instantiate an instance of Containers, which is a wrapper around the CONTAINERS tasble used to drive
    the content migration. It also builds the ERStudio CMO files for reverse engineering the database schemas
    '''
    containers = Containers(run)
    '''
    Build the CMO files for this run and return a dictionary with a list of those and other info for each app, 
    indexed by the app short name 
    '''
    CMOList = containers.buildCMOs()
    '''
    In an instance of IrsApplication, a wrapper for access to IRS data
    '''
    irs = IrsApplications()
    '''
    Instantiate an instance of AddtoERtudio, which is a wrapper around the activities for adding information
    from various sources to ERStudio
    '''
    ers = AddtoERStudio()
    for app in CMOList.keys():
        '''
        For each app that needs to be migrated...
        '''
        CMOs = CMOList[app]
        if len(CMOs['SCHEMAS']) > 0:
            if CMOs['WORK AREA'] is not None:
                ers.setrepo(CMOs['DESIGNER REPOSITORY'])
                ers.openERS(app, CMOs['DIAGRAM NAME'], CMOs['WORK AREA'], CMOs['DESIGNER NAME'])

                for schema in CMOs['SCHEMAS']:
                    '''
                    for each schema in the app reverse engineer the physical model
                    add Designer descriptions for the physical objects
                    build a logical model from those physical objects
                    '''
                    print('app:', app, 'schema:', schema)
                    print(CMOs['SCHEMAS'][schema][0])
                    pm = ers.addphysmodel(CMOs['SCHEMAS'][schema][0])

                '''
                add Designer descriptions for the physical objects from the App's 
                Designer Container
                '''
                ers.addphysdescriptions()

                for schema in CMOs['SCHEMAS']:
                    '''
                    for each schema in the app 
                    build a logical model from those physical objects
                    '''
                    lm = ers.addlogmodel(CMOs['SCHEMAS'][schema][1])

                '''
                Start layering in info from other sources of truth (largely designer)
                '''
                ers.addentnames()
                ers.add_domains()
                ers.addattrnames()
                ers.add_rel_phrases()
                desc = irs.getdescription(app)
                if desc is not None:
                    ers.adddescription(irs.getdescription(app)[0])
                else:
                    ers.adddescription(None)
                fullname = irs.getfullname(app)
                if fullname is not None:
                    ers.addfullname(irs.getfullname(app)[0])

                ers.addIRSlink(app)
                ers.addauthor()
                svnver = getAppVersionfromSVN(app)
                ers.addversion(svnver.getversion())
                ers.addphyssubmodels()
                ers.addlogsubmodels()
                ers.addconvertedtag()
    ers.close()
    del ers
