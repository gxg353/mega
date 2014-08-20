'''
Created on Aug 19, 2014

@author: xchliu
'''

class Chart(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.slowlog={'xaxis':[],'data':[]}
        self.yaxis_name=''
        self.data_list=[]
        self.type='line'
        self.title=''

    
    def generate(self,data,title=None,*kwgs,**args):
        '''
            data: a list of data  [(1,2,3),(2,2,3)]
            
        '''
        if title:
            self.title=title
            self.slowlog['title']=title
        if self.yaxis_name:
            self.slowlog['yaxis_name']=self.yaxis_name
        self.slowlog['type']=self.type
        for line in self.data_list:
            self.slowlog['data'].append({line:[]})
        for d in data:
            self.slowlog['xaxis'].append(str(d[0]))
            for i in range(len(self.data_list)):
                self.slowlog['data'][i][self.data_list[i]].append(int(d[i+1]))
        self.slowlog['xaxis']=[x for x in self.slowlog['xaxis']]
        return self.slowlog
    
    def js_pack(self):
        data='''{chart: {type: %s},
            title: {text: %s},
            xAxis: {categories: %s},
            yAxis: {title: {text:%s}},
            series: %s
        }
        ''' %(self.type,self.title,[x for x in self.slowlog['xaxis']],self.slowlog['yaxis_name'],[ x for x in self.slowlog['data']])
        print data
        return data
        