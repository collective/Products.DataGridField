from zope.interface import Interface


class DemoProfile(Interface):
    """Marker interface for our demo GS profile."""


# DataGrid interfaces
class IDataGridField(Interface):
    """A DataGrid can be used to manipulate two-dimensional data
    """

    def getColumns(instance):
        """Get a tuple of column names, in the order they are held in the grid.
        """

    def getRowCount(instance):
        """Get the number of rows in the grid.
        """

    def getRow(instance, rowNumber):
        """Get the given row by number. The first row is rowNumber 0. Returns
        a dict of the row.
        """
        pass

    def getColumn(instance, columnName):
        """Get the given column by name as a tuple of values.
        """
        pass

    def search(instance, key=None, **kwargs):
        """Search for rows. If key is given look for this value in the first
        column. If key is not given, at least one kwarg must be given,
        specifying column names and values. For example,
            search(surname='Jones', title='Mr')
        will return all rows with the surname and title matching Mr. Jones.
        Always returns a tuple of dicts.
        """
        pass

    def lookup(instance, key, column, lookupColumn=None):
        """Look for the given key in the column specified by lookupColumn.

        If no lookupColumn is given, look in the first column. For the
        first row found, return the value stored in the corresponding
        column as given by the 'column' parameter. Returns None if the
        key could not be found.

        (if you've used Excel, this is similar to VLOOKUP)
        """
        pass

    def getAsDisplayList(instance, keyCol=None, valueCol=None):
        """Get two columns of each row as a DisplayList - the key columns is
        keyCol, and the value column is valueCol. If these are not given,
        use the first two columns, respectively.
        """
        pass

    def getAsGrid(instance):
        """Return a tuple of tuples - the outer tuple has one element
        per row in the grid, the inner tuple has one element per column
        in that row.
        """
        pass
