# -*- coding:utf-8 -*-
from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from DateTime.DateTime import DateTime
from Products.DataGridField.Column import Column
from collective.js.jqueryui.utils import get_python_date_format
import time
__author__ = 'Gustavo Lepri <lepri@simplesconsultoria.com.br>'
__docformat__ = 'restructuredtext'





class DateTimeColumn(Column):
    """ Defines DataGridField column with DateTime
    """

    security = ClassSecurityInfo()

    def __init__(self, title, with_time=False):
        """ Create a DateTime column

        @param with_time True or False to show time (hour and minute)

        """
        Column.__init__(self, title)
        self.with_time = with_time

    def getWith_time(self):
        return self.with_time

    def getMacro(self):
        """ Return macro used to render this column in view/edit """
        return "datagrid_datetime_cell"

    def hours_minutes(self, date):
        """Return (hour, date) from a given DateTime instance.
        """
        if isinstance(date, DateTime):
            return date.hour(), date.minute()
        return '', ''

    def datestr(self, context, date):
        """Return formated date string from a given DateTime instance.
        """
        if date and hasattr(date, 'strftime'):
            format = get_python_date_format(context.REQUEST)
            return date.strftime(format)
        elif date:
            # Maybe a string or other bad value
            return date
        else:
            return ''

    def processCellData(self, form, value, context, field, columnId):
        """ Read cell values from raw form data
        """
        newValue = []
        fieldname = field.getName()
        for row in value:
            newRow = {}
            for key in row.keys():
                newRow[key] = row[key]
                datestr = row[columnId]
                if datestr:
                    hours = int(form.get(fieldname + '_hour', 0))
                    minutes = int(form.get(fieldname + '_minute', 0))
                    datestr = '%s %s:%s:00' % (datestr, hours, minutes)
                    date_format = get_python_date_format(context.REQUEST)
                    try:
                        tp = time.strptime(datestr, date_format + ' %H:%M:%S')
                    except ValueError:
                        tp = ''
                    newRow[columnId] = ((tp and DateTime(time.mktime(tp)))
                                        or row[columnId])
            newValue.append(newRow)
        return newValue

# Initializes class security
InitializeClass(DateTimeColumn)
