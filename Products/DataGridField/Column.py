"""

    Basic columns for DataGridField.

    Copyright 2006-2007 DataGridField authors


"""

from __future__ import nested_scopes

__author__ = "Mikko Ohtamaa < mikko@redinnovation.com>"
__docformat__ = 'epytext'

# Zope imports
from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from zope.i18n import translate


class Column(object):
    """ Stardard text edit column """

    security = ClassSecurityInfo()

    def __init__(self, label, col_description=None, default=None,
                 default_method=None, visible=True, required=False):
        """ Create a column

            @param label User visible name
            @param col_description General description for the column (when label is  not enough)
            @param default Default value for new rows
            @param default_method Default function to generate the default value for new rows
            @param visible Hide column from displaying by setting this to False
            @param required Set to True when values in this column are required
        """
        self.label = label
        self.col_description = col_description
        self.default = default
        self.default_method = default_method
        self.visible = visible
        self.required = required

    security.declarePublic('getLabel')
    def getLabel(self, context, widget=None):
        """ User friendly name for the column.

        This includes translation.

        @param context Context where translation happens (should be a request)

        @param widget The parent widget of this column. This is
        ignored now, as we do not support specifying an i18n_domain in
        the widget.  The labels should be specified with a message factory.
        """
        try:
            return translate(self.label, context=context)
        except:
            # Fall back to the untranslated label instead of crashing
            # simply because translation fails.
            return self.label

    security.declarePublic('getDefault')
    def getDefault(self, context):
        """ Default value for new rows """
        if self.default_method:
            try:
                func = getattr(context, self.default_method)
            except AttributeError:
                raise AttributeError, "Class %s has no default_method %s" % (str(context), self.default_method)

            return func()


        return self.default

    security.declarePublic('getMacro')
    def getMacro(self):
        """ Return macro used to render this column in view/edit """
        return "datagrid_text_cell"

    security.declarePublic('processCellData')
    def processCellData(self, form, value, context, field, columnId):
        """ Read cell values from raw form data

        Column processing in forms may need special preparations for data if
        widgets use other than <input value> for storing their
        values in fields.

        @param form Submitted form, contains HTML fields
        @param context Archetypes item instance for the submitted form
        @param field Assigned field for this widget
        @param columnId Column what we are operating

        @return new values which are constructed by processing data
        """
        return value

# Initializes class security
InitializeClass(Column)
