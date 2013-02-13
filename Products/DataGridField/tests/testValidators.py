from urllib2 import HTTPError
from unittest import TestSuite, makeSuite
from Products.DataGridField.tests.DataGridTestCase import DataGridFuncTestCase
from Products.DataGridField.examples.DataGridDemoType import DataGridDemoDateTime
from Products.Archetypes.tests.atsitetestcase import ATSiteTestCase


class TestValidation(ATSiteTestCase):

    def test_registration_filled(self):
        from Products.validation import validation
        v = validation.validatorFor('isDataGridFilled')
        self.failUnlessEqual(v((0, 1)), 1)
        self.failUnlessEqual(v([0, 1]), 1)
        self.failIfEqual(v([1]), 1)
        self.failIfEqual(v(0), 1)

    def test_registration_date(self):
        from Products.validation import validation
        v = validation.validatorFor('isValidDate')
        self.failUnlessEqual(v((0, 1)), 1)


class TestDateValidator(DataGridFuncTestCase):
    """ Unit test cases for DataGridField column definition manipulation """

    def afterSetUp(self):
        from Testing.testbrowser import Browser
        from Testing.ZopeTestCase import user_password
        self.patch_demo_type()
        browser = Browser()
        browser.addHeader('Authorization',
                          'Basic %s:%s' % ('portal_owner', user_password))
        self.browser = browser

    def patch_demo_type(self):
        ''' Patch DataGridDemoDateTime to use isValidDate '''
        field = DataGridDemoDateTime.schema['DemoField']
        validators = field.validators
        validators.appendRequired('isValidDate')
        field.validators = validators

    def test_valid_date(self):
        browser = self.browser
        browser.open('http://nohost/plone')
        browser.getLink('Add new').click()
        browser.getControl('DataGridDemoDateTime').click()
        browser.getControl('Add').click()
        browser.getControl(name='DemoField.column1:records').value = '1'
        browser.getControl(name='DemoField.column2:records').value = '1'
        browser.getControl(name='DemoField.datetime:records').value = '11/11/2011'
        browser.getControl('Save').click()
        self.failIf('is not a valid date.' in browser.contents)

    def test_invalid_date(self):
        browser = self.browser
        browser.open('http://nohost/plone')
        browser.getLink('Add new').click()
        browser.getControl('DataGridDemoDateTime').click()
        browser.getControl('Add').click()
        browser.getControl(name='DemoField.column1:records').value = '1'
        browser.getControl(name='DemoField.column2:records').value = '1'
        browser.getControl(name='DemoField.datetime:records').value = '40/11/2011'
        browser.getControl('Save').click()
        self.failUnless('is not a valid date.' in browser.contents)


def test_suite():
    suite = TestSuite()

    suite.addTest(makeSuite(TestValidation))
    suite.addTest(makeSuite(TestDateValidator))
    
    return suite
