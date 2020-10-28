from erstudiolib.GPO import GPO
from erstudiolib.DDO import DDO
from erstudiolib.addtoERStudio import addtoERStudio
from erstudiolib.parameters import Parameters
from github import Github

import os

'''
And example of how to 
- generate a physical model
- generate SQL from the physical model
- commit the SQL to github

This requires a psk from github, which in this example is located in the Parameters class

'''
def filetotext(filepath):
    fo = open(filepath, 'rt')
    fdata = fo.read()
    fo.close()
    return fdata

x = addtoERStudio()
x.openERS('IRS')
gpo = GPO()
gpofile = gpo.write('IRS')
x.ERS.genPhysicalModel(gpofile)
ddo = DDO()
physmodel, ddofile = ddo.write('IRS')
filepath = x.ERS.genDDL(ddofile, physmodel)

if os.path.isfile():
    data = filetotext(filepath)
else:
    files = os.listdir(filepath)
    for file in files:
        data = filetotext(file)

parms = Parameters()
ACCESS_TOKEN = parms.githubtoken
g = Github(ACCESS_TOKEN)
erstudiorepo = g.get_user().get_repos()[0]
result = None

if os.path.isdir(filepath):
    files = os.listdir(filepath)
    for fname in files:
        fdata = filetotext(f"{filepath}//{fname}")
        result = erstudiorepo.create_file(fname, "test for Michelle", fdata)

else:
    fname = ntpath.basename(filepath)
    fdata = filetotext(filepath)
    result = erstudiorepo.create_file(fname, "test for Michelle", fdata)

print(result)