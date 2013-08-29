"""
    DataGridField field class

    Copyright 2006 DataGridField authors, see documentation for details

"""
from __future__ import nested_scopes
import json

__docformat__ = 'epytext'
__author__  = 'Mikko Ohtamaa <mikko@redinnovation.com>'

import StringIO
import logging
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import DisplayList
from Products.Archetypes.Field import ObjectField
from Products.Archetypes.Field import encode
from Products.Archetypes.Field import registerField
from Products.DataGridField import DataGridWidget
from Products.DataGridField.interfaces import IDataGridField
from zope.interface import implements

# Our logger object
logger = logging.getLogger('DataGridField')
logger.debug("DataGridField loading")

class DataGridField(ObjectField):
    """ Table field with undefined number of rows

    DataGridField provides an user fillable table with fixed
    columns and undefined number of rows.

    Data is maintained internally:
        - DataGridField.value is a list
        - Each list item represents a row
        - Each row is a dictionary using column names as a key
    """
    implements(IDataGridField)

    _properties = ObjectField._properties.copy()
    _properties.update({
        'type' : 'datagrid',
        'mode' : 'rw',
        # inital data of the field in form sequence of dicts
        'default' : ({},),

        'widget' : DataGridWidget,

        # Column id list (sequence of strings)
        'columns' : ('default',),

        # sequence of FixedRow instances.
        # See FixedRow class documentation
        'fixed_rows' : [],

        # User can append new rows. Currently UI feature. This is not yet checked
        # at application level in set().
        'allow_insert' : True,

        # User can delete rows. This is currently UI feature (red delete button).
        # This is not yet checked at application level in set().
        'allow_delete' : True,

        # User can reorder rows. This is currently UI feature (ordering buttons).
        # This is not yet checked at application level in set().
        'allow_reorder' : True,

         # If true all the contents of the DataGridField is concatenated
         # to searchable text and given to text indexer
        'searchable' : False,

        # Set to false to allow empty rows in the data.
        # Needed for auto insert feature
        'allow_empty_rows' : True,

        # Set to true to hifhligh odd/even rows in edit/view form
        'allow_oddeven' : False,
        
        # Validators that check for required columns
        'validators': ('isColumnFilled',),
        })

    security = ClassSecurityInfo()


    def __init__(self, name=None, **kwargs):
        """ Create DataGridField instance
        """

        # call super constructor
        ObjectField.__init__(self, name, **kwargs)

    def getColumnIds(self):
        """ Return list of column ids """
        return self.columns

    security.declarePrivate('set')
    def set(self, instance, value, **kwargs):
        """
        The passed in object should be a records object, or a sequence of dictionaries
        """

        # Help to localize problems in Zope trace back
        __traceback_info__ = value, type(value)

        # we sanitize the values
        cleaned = []
        doSort = False

        logging.debug("Setting DGF value to " + str(value))

        if value == ({},):
            # With some Plone versions, it looks like that AT init
            # causes DGF to get one empty dictionary as the base value
            # and later, it will be appended as a cleaned row below if
            # we don't filter out it here.
            value = []

        if isinstance(value, basestring):
            # replace () by []
            value = value.strip()
            if value.startswith('('):
                value = "[%s]" % value[1:-1]

            # if simple quotes are used as separators, replace them by '"'
            if value.replace(' ', '')[2] == "'":
                value = value.replace("'",'"')

            value = json.loads(value)
        else:

            # Passed in value is a HTML form data
            # from DataGridWidget. Value is Python array,
            # each item being a dictionary with column_name : value mappins
            # + orderinder which is used in JS reordering

            for row in value:
                order = row.get('orderindex_', None)

                empty = True

                if order != "template_row_marker":
                    # don't process hidden template row as
                    # input data
                    val = {}
                    for col in self.getColumnIds():
                        row_value = row.get(col,'')
                        # LinesColumn provides list, not string.
                        if isinstance(row_value, basestring):
                            val[col] = row_value.strip()
                        else:
                            val[col] = [value.strip() for value in row_value]

                        if val[col]:
                            empty = False

                    if order is not None:
                        try:
                            order = int(order)
                            doSort = True
                        except ValueError:
                            pass

                    # create sortable tuples
                    if (not self.allow_empty_rows) and empty:
                        logger.debug("Filtered out an empty row")
                    else:
                        logger.debug("Appending cleaned row:" + str(val))
                        cleaned.append((order, val.copy()))

            if doSort:
                cleaned.sort()

            # remove order keys when sorting is complete
            value = tuple([x for (throwaway, x) in cleaned])

        # fill in data
        ObjectField.set(self, instance, value, **kwargs)

    security.declarePrivate('get')
    def get(self, instance, **kwargs):
        """ Return DataGridField value

        Value is a list object of rows.

        If parameter mimetype == 'text/plain' is passed,
        a string containing all cell values concatenated together is returned.
        This is for site indexing services (DataGridField.searchable = true).
        """

        if(kwargs.has_key('mimetype') and kwargs['mimetype'] == 'text/plain'):
            # Data is returned for text indexing
            # Concatenate all cell values
            buffer = StringIO.StringIO()

            value = ObjectField.get(self, instance, **kwargs) or ()
            value = self.resetFixedRows(instance, value)

            for row in value:
                for col in self.getColumnIds():
                    buffer.write(row.get(col,''))
                    # separate the last word of a cell
                    # and the first of the next cell
                    buffer.write(' ')

            return encode(buffer.getvalue(), instance, **kwargs)

        else:
            # Return list containing all encoded rows
            value = ObjectField.get(self, instance, **kwargs) or ()
            value = self.resetFixedRows(instance, value)

            data = [encode(v, instance, **kwargs) for v in value]

            return tuple(data)

    security.declarePrivate('getRaw')
    def getRaw(self, instance, **kwargs):
        return self.get(instance, **kwargs)

    security.declarePublic('get_size')
    def get_size(self, instance):
        """Get size of the stored data used for get_size in BaseObject
        """
        size=0
        for line in self.get(instance):
            size+=len(str(line))
        return size

    # Grid API as defined in interfaces.py

    security.declarePublic('getColumns')
    def getColumns(self, instance):
        return self.columns

    security.declarePublic('getRowCount')
    def getRowCount(self, instance):
        return len(self.get(instance))

    def getRow(self, instance, rowNumber):
        """Get the given row by number. The first row is rowNumber 0. Returns
        a dict of the row.
        """
        data = self.get(instance)
        if rowNumber > len(data):
            raise IndexError, "Tried to access row %d when there are %d available" % (rowNumber, len(data))
        return data[rowNumber]

    def getColumn(self, instance, columnName):
        """Get data in the given column by name as a tuple of values.
        """
        data = self.get(instance)
        col = []
        for row in data:
            col.append(row[columnName])
        return tuple(col)

    def search(self, instance, key=None, **kwargs):
        """Search for rows. If key is given look for this value in the first
        column. If key is not given, at least one kwarg must be given,
        specifying column names and values. For example,
            search(surname='Jones', title='Mr')
        will return all rows with the surname and title matching Mr. Jones.
        Always returns a tuple of dicts.
        """
        data = self.get(instance)
        if key is not None:
            kwargs[self.getColumnIds()[0]] = key
        matches = []
        for r in data:
            match = True
            for k, v in kwargs.items():
                if r[k] != v:
                    match = False
            if match:
                matches.append(r)
        return tuple(matches)


    def lookup(self, instance, key, column, lookupColumn=None):
        """Look for the given key in the column specified by lookupColumn.
        If no lookupColumn is given, look in the first column. For the first row
        found, return the value stored in the corresponding column as given by
        the 'column' parameter. Returns None if the key could not be found.

        (if you've used Excel, this is similar to VLOOKUP)
        """
        data = self.get(instance)
        if lookupColumn is None:
            lookupColumn = self.columns[0]
        for r in data:
            if r[lookupColumn] == key:
                return r[column]
        return None


    def getAsDisplayList(self, instance, keyCol=None, valueCol=None):
        """Get two columns of each row as a DisplayList - the key columns is
        keyCol, and the value column is valueCol. If these are not given,
        use the first two columns, respectively.
        """
        data = self.get(instance)

        if keyCol is None:
            keyCol = self.getColumnIds()[0]
        if valueCol is None:
            valueCol = self.getColumnIds()[1]

        lst = DisplayList()
        for r in data:
            lst.add(r[keyCol], r[valueCol])

        return lst

    def getAsGrid(self, instance):
        """Return a tuple of tuples - the outer tuple has one element
        per row in the grid, the inner tuple has one element per column
        in that row.
        """
        data = self.get(instance)
        rows = []
        for r in data:
            rows.append(tuple([r[c] for c in self.getColumnIds()]))
        return tuple(rows)

    def resetFixedRows(self, instance, data):
        """ See that fixed rows exists.

        Go through data (list of rows/dict) and add fixed rows if they are missing.

        1. Go through all fixed rows
        2. See if the key column of the fixed row has value in user data
        3. If the row is missing, (re)append it

        @param data user set data
        @return modified data w/fixed rows present
        """

        # is fixed row property used
        if hasattr(self, "fixed_rows") and self.fixed_rows != None:

            if isinstance(self.fixed_rows, basestring):
                # fixed rows is a name of a member function

                try:
                    func = getattr(instance, self.fixed_rows)
                except AttributeError:
                    raise AttributeError, "Class %s is missing fixed row data function %s" % (str(instance), self.fixed_rows)

                fixedRowsData = func()

            else:
                # fixed rows is a direct value

                fixedRowsData = self.fixed_rows

            newRows = list(data[:])

            for fixedRow in fixedRowsData:
                # go through data set and see if the fixed key value exists
                keyValue = fixedRow.initialData[fixedRow.keyColumn]

                exist = False

                for row in data:
                    if row.has_key(fixedRow.keyColumn):
                        if row[fixedRow.keyColumn] == keyValue:
                            # row exists and has user set value
                            exist = True
                            break

                if not exist:
                    # initialize fixed data
                    newRows.append(fixedRow.initialData)

            return tuple(newRows)
        else:
            # fixed rows behavior is disabled
            return data


class FixedRow:
    """ Row which is always present at DataGridField data.

    This is a useful use case for situations where user must be
    forced to fill in some rows containing pre-set data. An example could
    be the filling of programming language knowledge in CV. Languages are preset
    and user fills in his/her experience. User can also add some weird languages outside
    pre-set languages.

    Instead of going with normal field.default behavior, fixed rows allow some flexibility
    when changing the fixed data set after item initialization. For example,
    the set of programming languages can be updated and user refills missing values
    to his/her CV.
    """

    def __init__(self, keyColumn, initialData):
        """
        @param initialData Dictionary for the row when user has deleted the fiexd row/item is initialized
        @param keyColumn Column which existence of value determines the need for a fixed row
        """
        self.keyColumn = keyColumn
        self.initialData = initialData

registerField(DataGridField,
              title='DataGridField',
              description=('Used for storing tabular string data'))
