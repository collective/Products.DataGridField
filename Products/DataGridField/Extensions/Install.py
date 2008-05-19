"""
    DataGridField quick install script
            
    Copyright 2006 DataGridField authors
    
"""

__author__  = 'Mikko Ohtamaa <mikko@redinnovation.com>'
__docformat__ = 'restructuredtext'

# Python imports
import StringIO
from cStringIO import StringIO
import string

from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ManagePortal
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.Archetypes import listTypes

# Config
from Products.DataGridField.config import *
from Products.DataGridField import HAS_PLONE30

def install(self):
    out=StringIO()
    
    # get portal_setup tool
    setup_tool = getToolByName(self, 'portal_setup')
    
    # get the correct profile
    if HAS_PLONE30:
        setup_tool.runAllImportStepsFromProfile("profile-Products.DataGridField:default", purge_old=False)
    else:
        # BBB: We install our product by running a GS profile.  We use the old-style Install.py module 
        # so that our product works w/ the Quick Installer in Plone 2.5.x
        old_context = setup_tool.getImportContextID()
        setup_tool.setImportContext('profile-Products.DataGridField:default_25x')
        setup_tool.runAllImportSteps()
        setup_tool.setImportContext(old_context)
    
    # if INSTALL_DEMO_TYPES:
    #     installTypes(self, out, classes, PKG_NAME)
    
    out.write('Installation completed.\n')
    return out.getvalue()

def uninstall(self):
    out=StringIO()
    return out.getvalue()

