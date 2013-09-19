"""

    Column with help for DataGridField

    Written by Juan Grigera <juan@grigera.com.ar>.

"""

from __future__ import nested_scopes
__docformat__ = 'epytext'
__author__ = "Juan Grigera <juan@grigera.com.ar>"

from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.CMFCore.permissions import View
from Products.DataGridField.Column import Column


class HelpColumn(Column):
    """ Help column support.

    Behaves like normal text cell, but has a help pop-up icon next to it.
    """

    security = ClassSecurityInfo()

    def __init__(self, label, helper_text, script, icon, **kwargs):
        """ Create a HelpColumn

        """
        Column.__init__(self, label, **kwargs)
        self.helper_text = helper_text
        self.helper_url = script
        self.icon = icon

    security.declareProtected(View, 'getVocabulary')
    def getVocabulary(self, instance):
        """ Gets this column vocabulary for specific Archetypes instance
        """
        try:
            func = getattr(instance, self.vocabulary)
        except AttributeError:
            raise AttributeError, "Class %s is missing vocabulary function %s" % (str(instance), self.vocabulary)

        return func()


    security.declarePublic('getMacro')
    def getMacro(self):
        """ Return macro used to render this column in view/edit """
        return "datagrid_help_cell"

    security.declarePublic('getHelperUrl')
    def getHelperUrl(self):
        """ Return url to open"""
        return self.helper_url

    security.declarePublic('getHelperText')
    def getHelperText(self):
        """ Return help text"""
        return self.helper_text

    security.declarePublic('getIcon')
    def getIcon(self):
        return self.icon

# Initializes class security
InitializeClass(HelpColumn)
