class ERSdbtypes():
    '''
    This class lists the possible database types that are supported for SQL generation; and the Physical Model
    they will have within the ERStudio diagram

    '''

    def __init__(self):
        self.Destination = {"Oracle 12c": [100, "Oracle 12c", "Oracle 12c (system)", "_Physical"],
                            "PostgreSQL 10.x-12.x": [113, "PostgreSQL 10.x-12.x", "PostgreSQL 10.x-12.x (system)", "_PostgreSQL"]}
