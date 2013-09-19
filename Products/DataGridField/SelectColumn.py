"""

    Dropdown column definition for DataGridField

    Copyright 2006 Mikko Ohtamaa


"""

from __future__ import nested_scopes
__author__ = "Mikko Ohtamaa <mikko@redinnovation.com>"
__docformat__ = 'epytext'


from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.Archetypes.interfaces import IVocabulary
from Products.DataGridField.Column import Column


class SelectColumn(Column):
    """ Defines column with dropdown menu cells in DataGridField """

    security = ClassSecurityInfo()

    def __init__(self, label, vocabulary, col_description=None, default=None,
                 default_method=None, visible=True, required=False):
        """ Create a SelectColumn

        @param vocabulary Vocabulary method name. This method is called
               from Archetypes instance to get values for dropdown list.
        @param visible Hide column from displaying by setting this to False
        """
        Column.__init__(self, label, col_description=col_description,
                        default=default, default_method=default_method,
                        required=required)
        self.vocabulary = vocabulary
        self.visible = visible

    security.declarePublic('getVocabulary')
    def getVocabulary(self, instance):
        """ Gets this column vocabulary for specific Archetypes instance
        """
        if IVocabulary.providedBy(self.vocabulary):
            return self.vocabulary.getDisplayList(instance)
        try:
            func = getattr(instance, self.vocabulary)
        except AttributeError:
            func = instance.restrictedTraverse(self.vocabulary, None)
            if func is None:
                raise AttributeError, "Class %s is missing vocabulary function %s" % (str(instance), self.vocabulary)

        return func()


    security.declarePublic('getMacro')
    def getMacro(self):
        """ Return macro used to render this column in view/edit """
        return "datagrid_select_cell"


# Initializes class security
InitializeClass(SelectColumn)
