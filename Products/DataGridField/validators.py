"""Validator for DataGridFields.

For the DataGridFields, making them required is not enough as there is
always a hidden entry.  So we check if there is least one normal entry
and one hidden entry, so more than 1 entry in total.
"""

import time
from DateTime.DateTime import DateTime
from datetime import datetime

from Products.validation import validation
from Products.validation.interfaces.IValidator import IValidator

from Products.DataGridField.DateTimeColumn import DateTimeColumn

from zope.interface import implements

from collective.js.jqueryui.utils import get_python_date_format

class DateValidator:
    """ Validate as True if the value is a valid date.
    """

    implements(IValidator)

    def __init__(self, name, title='', description=''):
        self.name = name
        self.title = title or name
        self.description = description

    def date_columns(self,field):
        '''Given a field we return a list of 
           DateTimeColumns 
        '''
        columns = []
        if not (field and hasattr(field,'columns')):
            return columns
        for column_id, column in field.widget.columns.items():
            if isinstance(column, DateTimeColumn):
                columns.append(column_id)
        return columns

    def __call__(self, value, *args, **kwargs):
        value.pop()
        request = kwargs.get('REQUEST',None)
        field = kwargs.get('field', None)
        date_columns = self.date_columns(field)
        date_format = request and get_python_date_format(request) or '%Y/%m/%d'
        for line in value:
            for column in date_columns:
                date = line[column]
                if hasattr(date, 'strftime'):
                    #Already a date
                    continue
                datestr = '%s 0:0:00' % (date)
                try:
                    tp = time.strptime(datestr, date_format + ' %H:%M:%S')
                    DateTime(time.mktime(tp))
                except ValueError:
                    return ("%s is not a valid date." % date)
        return True

isValidDate = DateValidator(
    'isValidDate', title='Valide DateTime entry',
    description='The DateTime value must have be a valid date.')
validation.register(isValidDate)

class DataGridValidator:
    """Validate as True when having at least one DataGrid item.
    """

    implements(IValidator)

    def __init__(self, name, title='', description=''):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):
        try:
            length = len(value) - 1
        except TypeError:
            return ("Validation failed(%s): cannot calculate length "
                    "of %s.""" % (self.name, value))
        except AttributeError:
            return ("Validation failed(%s): cannot calculate length "
                    "of %s.""" % (self.name, value))
        if length < 1:
            return ("Validation failed(%s): Need at least one entry."
                    % self.name)
        return True


isDataGridFilled = DataGridValidator(
    'isDataGridFilled', title='DataGrid has entries',
    description='The DataGridField must have at least one entry.')
validation.register(isDataGridFilled)
