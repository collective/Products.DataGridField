from Testing import ZopeTestCase

ZopeTestCase.installProduct('DataGridField')

from Products.PloneTestCase import PloneTestCase

PROFILES = ['Products.DataGridField:default',
            'Products.DataGridField:example']

PloneTestCase.setupPloneSite(extension_profiles=PROFILES)

class DataGridTestCase(PloneTestCase.PloneTestCase):

    class Session(dict):

        def set(self, key, value):
            self[key] = value

    def _setup(self):
        PloneTestCase.PloneTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()

class DataGridFuncTestCase(PloneTestCase.FunctionalTestCase):
    class Session(dict):

        def set(self, key, value):
            self[key] = value

    def _setup(self):
        PloneTestCase.PloneTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()    