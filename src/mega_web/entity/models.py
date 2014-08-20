'''
Created on May 9, 2014

@author: xchliu
'''
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mega_web.settings")
from entity import *
from report import * 
def raw_as_qs(Table,raw_query, params=()):
        """Execute a raw query and return a QuerySet.  The first column in the
        result set must be the id field for the model.
        :type raw_query: str | unicode
        :type params: tuple[T] | dict[str | unicode, T]
        :rtype: django.db.models.query.QuerySet
        """
        cursor = connection.cursor()
        try:
            cursor.execute(raw_query, params)
            return Table.objects.filter(id__in=(x[0] for x in cursor))
        finally:
            cursor.close()

