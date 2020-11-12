import xlsxwriter

class Spreadsheet():
    def __init__(self, filename=None):
        self.row = 0
        self.col = 0
        self.filename = None
        self.workbook = None
        self.worksheet = None
        self.workarea = None
        self.DesignerRepo = None
        self.open(filename)


    def open(self, filename):
        self.filename = filename
        self.workbook = xlsxwriter.Workbook(self.filename, {'in_memory': True})
        self.worksheet = self.workbook.add_worksheet()
        self.col = 0
        self.worksheet.write(self.row, self.col, 'Designer Repo')
        self.col += 1
        self.worksheet.write(self.row, self.col, 'Designer Workarea')
        self.col += 1
        self.worksheet.write(self.row, self.col, 'Application')
        self.col += 1
        self.worksheet.write(self.row, self.col, 'Object Type')
        self.col += 1
        self.worksheet.write(self.row, self.col, 'Object Name')
        self.row +=1


    def close(self):
        self.workbook.close()
        return

    def setdesignerrepo(self, name):
        self.DesignerRepo = name

    def setworkarea(self, name):
        self.workarea = name

    def write(self, values):
        self.col = 0
        self.worksheet.write(self.row, self.col, self.DesignerRepo)
        self.col += 1
        self.worksheet.write(self.row, self.col, self.workarea)
        for val in values:
            self.col += 1
            self.worksheet.write(self.row, self.col, val)
        self.row += 1

