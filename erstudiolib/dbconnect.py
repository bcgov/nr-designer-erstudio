import cx_Oracle
from erstudiolib.parameters import Parameters


class DBConnect():
    '''
    A simple class to consoidate the code for starting a connection to an oracle database
    '''
    def __init__(self, dsn='rdrprod1', encoding='UTF-8'):
        self.parameters = Parameters()
        self.connection = None
        self.client_lib = f"C:\\Users\\{self.parameters.username}\\Downloads\\instantclient-basic-nt-19.8.0.0.0dbru\\instantclient_19_8"
        self.dsn = dsn
        self.encoding = encoding

        try:
            cx_Oracle.init_oracle_client(lib_dir=self.client_lib)
        except Exception as err:
            '''
            '''
            if err.__str__() == 'Oracle Client library has already been initialized':
                pass
            else:
                print("Whoops!")
                print(err)

        try:
            self.connection = cx_Oracle.connect(self.parameters.username, self.parameters.orapass, dsn, encoding=self.encoding)
        except cx_Oracle.Error as error:
            print(error)

    def close(self):
        if self.connection is not None:
            self.connection.close()

    def fetchall(self, sql):
        rows = None
        if self.connection is not None:
            cur = self.connection.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
        return rows
