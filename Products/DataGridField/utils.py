"""

    Small utility functions for DGF

    Copyright 2006 Red Innovation

"""

__author__ = 'Mikko Ohtamaa <mikko@redinnovation.com>'
__docformat__ = 'restructuredtext'

from AccessControl import ModuleSecurityInfo, allow_module
from Products.CMFCore.utils import getToolByName


module = "Products.DataGridField.utils"
security = ModuleSecurityInfo(module)
allow_module(module)

security.declarePublic("makeAbsoluteLink")
def makeAbsoluteLink(link, context):
    """ Convert site relative links to absolute URLs

    Absolute links are passed through as is.
    Assume all http:// prefixed links are absolute.
    """

    if link == "":
        # this prevents makeAbsoluteLink not to
        # do nasty things with empty fields
        return ""

    # see if the link is absolute
    if link.startswith("http://"):
        return link
    else:
        portal_url = getToolByName(context, "portal_url")
        if link[:1] == "/":
            return portal_url() + link
        else:
            # if first character is / don't add it twice
            return portal_url() + "/" + link

security.declarePublic("makeRelativeLink")
def makeRelativeLink(link, context):
    """ Convert absolute (copy-pasted) links to site relative links

    If user enters absolute link which points to current portal,
    convert link to relative link so it survives portal relocation.

    Assume are http:// prefixed links are absolute.
    """

    # check for absolute, avoid extra work below
    if link.startswith("http://"):
        portal_url = getToolByName(context, "portal_url")()
        if link.startswith(portal_url):
            return link[len(portal_url):]

    # if first character is / don't add it twice
    return link
