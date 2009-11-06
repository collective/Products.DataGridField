"""
    Data grid UI component

    Copyright 2006-2007 DataGridField authors

"""

__author__  = 'Mikko Ohtamaa <mikko@redinnovation.com>'
__docformat__ = 'epytext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerWidget
from Products.DataGridField.Column import Column

class DataGridWidget(TypesWidget):
    """ Render a table with user addable rows

        Properties:
          - columns:
            - Dictionary of "column id" : Column instance mappings:
                - See *Column class documentation for initialization
                  parameters
          - helper_js:
              - Javascript used with the widget
          - helper_css:
              - CSS file used with the widget
          - auto_insert
              - Automatically add new rows when the last row is being edited.
                This doesn't work if the

    """

    _properties = TypesWidget._properties.copy()

    _properties.update({
        'macro' : "datagridwidget",
        'helper_css': ('datagridwidget.css',),
        'helper_js': ('datagridwidget.js',),
        'show_header' : True,
        'auto_insert': False,
        'columns' : {}, # Sequence of Column instances
        })


    security = ClassSecurityInfo()

    security.declarePublic('getColumnLabels')
    def getColumnLabels(self, field, context):
        """ Get user friendly names of all columns """

        columnDefinitions = getattr(self, 'columns', {})

        if len(columnDefinitions) == 0:
            # old way of getting column names
            columnNames = getattr(self, 'column_names', [])
            if columnNames:
                return columnNames
            else:
                return field.getColumnIds()


        names = []

        for id in field.getColumnIds():
            # Warn AT developer about his/her mistake
            if not id in columnDefinitions:
                raise AttributeError, "DataGridWidget missing column definition for " + id + " in field " + field.getName()

            col = self.columns[id]
            names.append(col.getLabel(self, context))

        return names

    security.declarePublic('getColumnDefinition')
    def getColumnDefinition(self, field, id):
        """ Return Column instance for column id """

        if id in getattr(self, 'columns', {}).keys():
            return self.columns[id]

        # Backwards compatability/shortcut
        if id in field.columns:
            label = id
            columnNames = getattr(self, 'column_names', None)
            if columnNames and len(columnNames) == len(field.columns):
                idx = list(field.columns).index(id)
                label = columnNames[idx]

            return Column(label)

        raise KeyError, "Tried to look up missing column definition for: " + str(id)

    security.declarePublic('getColumnDefs')
    def getColumnDefs(self, field, instance):
        """ Get all column definitions for a DataGridField.

            @param field Field definition
            @param instance Context object who has the field

            @return formatted column definitions as dict of { id, label, visible }
        """
        result = []

        columns = getattr(self, 'columns', {})

        for id in field.columns:
            c = self.getColumnDefinition(field, id)
            if c is None:
                raise KeyError, "Tried to look up missing column definition for: " + str(id)
            item = {'id':id, 'label':'', 'visible':True}
            visible = getattr(c, 'visible', True)
            item['visible'] = visible
            item['label'] = c.getLabel(instance, self)
            result.append(item)

        return result

    def getUserFriendlySelectionItem(self, context, item, vocab):
        """Look up the given item in the vocab and return the value, translated
        if necessary. Return an empty string if item is empty or None.
        """
        if item == None or item == '':
            return ""
        return vocab.getValue(item)


    security.declarePublic('isAutoInsertEnabled')
    def isAutoInsertEnabled(self):
        return self.auto_insert

    security.declarePublic('isDeleteEnabled')
    def isDeleteEnabled(self, context, field):
        """ Can user delete rows from DGW

        Called by template
        """
        return field.allow_delete

    security.declarePublic('isInsertEnabled')
    def isInsertEnabled(self, context, field):
        """ Can user insert new rows to DGW

        Called by template
        """
        return field.allow_insert

    security.declarePublic('isReorderingEnabled')
    def isReorderEnabled(self, context, field):
        """ Can user reorder rows in DGW

        Called by template
        """
        return field.allow_reorder

    security.declarePublic('hasAddButton')
    def hasAddButton(self, context, field):
        """ Show explict Add row button in DGW """
        return self.show_add_button

    security.declarePublic('hasHeader')
    def hasHeader(self, context, field):
        """ Render columns names in view mode"""
        return self.show_header

    security.declarePublic('process_form')
    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False):
        """ Manipulate form input data

        Data coming from widget code goes through process_form
        before stored to field.

        For example, radio button cells need to be propeply changed from
        checked values to one chosen id for saving.
        """

        value = TypesWidget.process_form(self, instance,
            field, form, empty_marker, emptyReturnsMarker)

        if value == None or value == empty_marker or len(value) == 0:
            return value

        newData = value[0]

        # Column code hook to form data and manipulate
        # it propeply where TypesWidget.process_form doesn't
        # have required functionality
        for columnId in getattr(self, 'columns', {}).keys():
            columnDefinition = self.getColumnDefinition(field, columnId)
            newData = columnDefinition.processCellData(form, newData, instance, field, columnId)

        # Clean up the last empty row (automatically inseted)
        # if auto_insert is enabled
        if self.isAutoInsertEnabled() and len(newData) > 1:
            lastRow = newData[len(newData) - 1]
            hasContent = False
            for val in lastRow.values():
                if val != None and val != "":
                    hasContent = True

            if not hasContent:
                newData = newData[:-1]


        return (newData, value[1])


    def savePostbackData(self, REQUEST, context, field, formData):
        """ Gets the value of a cell

        We cannot solely rely DataGridField.get which
        does ObjectField.get(), since form postback data
        can contain custom fields which are not directly mapped
        like Zope expects (e.g. fields with more than one <input>)

        XXX Need refactoring/clean up
        """


        # Column code hook to form data and manipulate
        # it propeply where TypesWidget.process_form doesn't
        # have required functionality
        for columnId in getattr(self, 'columns', {}).keys():
            columnDefinition = self.getColumnDefinition(field, columnId)
            formData = columnDefinition.processCellData(REQUEST, formData, context, field, columnId)


__all__ = ('DataGridWidget')

registerWidget(DataGridWidget,
               title='Data Grid',
               description=('A spreadsheet like table'),
               used_for=('Products.DataGridField.DataGridField',)
               )

