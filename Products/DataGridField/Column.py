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


class Column(object):
    """ Stardard text edit column """

    security = ClassSecurityInfo()

    def __init__(self, label, default=None, default_method=None, label_msgid=None):
        """ Create a column

            @param label User visible name
            @param default Default value for new rows
            @param default_value Default function to generate the default value for new rows
        """
        self.label = label
        self.default = default
        self.default_method = default_method

        if label_msgid is None:
            label_msgid = label
            self.label_msgid = label_msgid

    security.declarePublic('getLabel')
    def getLabel(self, context, widget):
        """ User friendly name for the columnt

        @param context Context where translation happens
        @param widget The parent widget of this column
        """


        # TODO: translation support disabled

        #if HAS_PLONE25:
            # No translation support yet
        #    return zope.i18n.translate(
        #        _(self.label_msgid,
        #          self.label),
        #          context=context)
        #else:
        #    context.translate(
        #            msgid   = self.label_msgid,
        #            domain  = widget.i18n_domain,
        #            default = self.label)
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
