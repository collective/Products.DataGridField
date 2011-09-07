"""

    Autocomplete column definition for DataGridField

    Copyright 2011 CommunesPlone.org


"""

from __future__ import nested_scopes
__author__ = "CommunesPlone.org <support@communesplone.be>"
__docformat__ = 'epytext'


from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.DataGridField.Column import Column


class AutocompleteColumn(Column):
    """ Defines an autocomplete column in DataGridField """

    security = ClassSecurityInfo()

    def __init__(self, title, json_view_params={}, json_view_name="jsonsearchview"):
        """ Create an AutocompleteColumn
        @param json_view_params parameters. The default jsonsearchview will use
               these parameters to query the portal_catalog
        @param json_view_name view name.  If the default view name returning the result
               by querying the portal_catalog does not the job, create your own view
        """
        Column.__init__(self, title)
        self.json_view_params = json_view_params
        self.json_view_name = json_view_name

    security.declarePublic('getMacro')
    def getMacro(self):
        """ Return macro used to render this column in view/edit """
        return "datagrid_autocomplete_cell"

    security.declarePublic('javascript')
    def javascript(self):
        return """
<script type="text/javascript">jQuery(function(){
     // Autocomplete
     jq(".DemoField2_autocomplete").autocomplete({
        source: "@@""" + self.json_view_name + "?json_view_params=" + str(self.json_view_params) + """"     });
     });
</script>
"""

# Initializes class security
InitializeClass(AutocompleteColumn)
