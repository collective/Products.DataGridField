from Testing import ZopeTestCase
from Products.DataGridField import HAS_PLONE31

ZopeTestCase.installProduct('DataGridField')

from Products.PloneTestCase import PloneTestCase

if HAS_PLONE31:
    # passing multiple extension profiles works for Plone 3.1.x
    PloneTestCase.setupPloneSite(extension_profiles=['Products.DataGridField:default','Products.DataGridField:example',])
else:
    PloneTestCase.setupPloneSite(products=["DataGridField",], extension_profiles=['Products.DataGridField:example',])

class DataGridTestCase(PloneTestCase.PloneTestCase):

    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def _setup(self):
        PloneTestCase.PloneTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()
