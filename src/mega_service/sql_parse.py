
class SQLParse():
    '''
        parse sql 
    '''
    def __init__(self,sql):
        '''
        
        '''
        self.sql=sql
        
    def _standard_format(self):
        _sql=self.sql
        if self.sql.find("'"):
            _sql=_sql.replace("'","")
        if self.sql.find('"'):
            _sql=_sql.replace('"','')
        if self.sql.find('"'):
            _sql=_sql.replace('"','')
        if self.sql.find('"'):
            _sql=_sql.replace('"','')
        