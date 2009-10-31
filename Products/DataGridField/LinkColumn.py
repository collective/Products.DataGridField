"""

    Copyright 2006 Red Innovation

"""

__author__ = 'Mikko Ohtamaa <mikko@redinnovation.com>'
__docformat__ = 'restructuredtext'

from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.DataGridField.Column import Column
from Products.DataGridField.utils import makeAbsoluteLink, makeRelativeLink


class LinkColumn(Column):
    """ Defines DataGridField column with link descriptions and targets

    Description and link is stored as one text entry, in of
    form which is used by many Wikis.

    Format:
        "description" "|" "link"

    If links begin with http:// they are absolute. Otherwise
    links are relative to the portal root.
    Managing absolute and relative links are done through utils module
    functions.
    """

    security = ClassSecurityInfo()

    def __init__(self, title, linkClass=""):
        """ Create a Links

        @param linkClass CSS class for <a> links in view mode

        """
        Column.__init__(self, title)
        self.linkClass = linkClass

    security.declarePublic('getMacro')
    def getMacro(self):
        """ Return macro used to render this column in view/edit """
        return "datagrid_link_cell"

    security.declarePublic('getLinkClass')
    def getLinkClass(self):
        return self.linkClass

    security.declarePublic('getLink')
    def getLink(self, instance, cell):
        """ Extract link address from cell data """

        if cell == None:
            return ""

        splitted = cell.split("|")
        if len(splitted) >= 2:
            return makeAbsoluteLink(splitted[1], instance)
        return ""

    security.declarePublic('getRelativeLink')
    def getRelativeLink(self, instance, cell):
        """ Extract link address from cell data """

        if cell == None:
            return ""

        splitted = cell.split("|")
        if len(splitted) >= 2:
            return makeRelativeLink(splitted[1], instance)
        return ""

    security.declarePublic("getDescription")
    def getDescription(self, cell):
        """ Extract link description from cell data """

        if cell == None:
            return ""

        splitted = cell.split("|")
        if len(splitted) >= 1:
            return splitted[0]
        return ""


    security.declarePublic('processCellData')
    def processCellData(self, form, value, context, field, columnId):
        """ Read cell values from raw form data

        Read form fields xxx_link and xx_desc and form one
        description from them.
        """

        # scan all rows and build desc|link string pair for
        # fields
        newValue = []
        for row in value:

            # we must clone row since
            # row is readonly ZPublished.HTTPRequest.record object
            newRow = {}
            for key in row.keys():
                newRow[key] = row[key]

            if newRow.has_key(columnId + "_desc"):
                desc = newRow[columnId + "_desc"]
            else:
                desc = ""

            if newRow.has_key(columnId + "_link"):
                link = newRow[columnId + "_link"]
            else:
                link = ""

            link = makeRelativeLink(link, context)

            if desc or link:
                newRow[columnId] = "%s|%s" % (desc, link)
            else:
                # don't add | character alone
                # causes extra new row to appear
                newRow[columnId] = ""

            newValue.append(newRow)

        return newValue

# Initializes class security
InitializeClass(LinkColumn)
