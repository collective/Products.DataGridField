"""

    Unit testing for DataGridField product

    Copyright 2006 DataGridField authors

"""

import sys
import logging

# Output debug log
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger("DataGridField").setLevel(logging.DEBUG)

from Products.DataGridField.tests.DataGridTestCase import DataGridTestCase
from Products.Archetypes.atapi import DisplayList

from Products.DataGridField.utils import makeAbsoluteLink, makeRelativeLink


class TestInstallation(DataGridTestCase):

    def afterSetUp(self):
        types = self.portal.portal_types.objectIds()
        self.failUnless('DataGridDemoType' in types)

    def testPortalTypes(self):
        types = self.portal.portal_types.objectIds()
        self.failUnless('DataGridDemoType' in types)

    def testPortalSkins(self):
        skins = self.portal.portal_skins.objectIds()
        self.failUnless('DataGridWidget' in skins)

    def testAddingDemo(self):
        self.folder.invokeFactory('DataGridDemoType', 'foo')
        self.failUnless('foo' in self.folder.objectIds())

    def testSettingField(self):
        self.folder.invokeFactory('DataGridDemoType', 'foo')
        vals = [{'column1':'joe'}]
        self.folder.foo.setDemoField(vals)
        self.assertEqual(len(self.folder.foo.getDemoField()), 1)

        row1 = self.folder.foo.getDemoField()[0]
        self.failUnless('column1' in row1.keys(), "Row was " + str(row1))
        pair1 = row1['column1']
        self.assertEqual(pair1, vals[0]['column1'])

    def testSettingFieldWithOrder(self):
        self.folder.invokeFactory('DataGridDemoType', 'foo')
        vals = [{'column1':'joe', 'orderindex_': 1},
                {'column1':'jack', 'orderindex_': 0}]
        self.folder.foo.setDemoField(vals)
        self.assertEqual(len(self.folder.foo.getDemoField()), 2)
        self.assertEqual(self.folder.foo.getDemoField()[0]['column1'],
                         vals[1]['column1'])
        self.assertEqual(self.folder.foo.getDemoField()[1]['column1'],
                         vals[0]['column1'])

    def testSettingEmptyRows(self):
        """ It should be possible to set empty rows """
        self.folder.invokeFactory('DataGridDemoType', 'foo')

        vals = ({'The third': '', 'column1': 'xxx', 'column2': '', }, )
        self.folder.foo.setDemoField(vals)
        self.assertEqual(self.folder.foo.getDemoField(), vals)

        vals = ({'The third': '', 'column1': '', 'column2': '', },)
        self.folder.foo.setDemoField(vals)
        self.assertEqual(self.folder.foo.getDemoField(), vals)

    def testRenderingDoesNotFail(self):
        """See if a page containing DGF will output HTML without
        exceptions in view mode.
        """
        self.folder.invokeFactory('DataGridDemoType', 'foo')
        self.failUnless(self.folder.foo())


class TestGridAPI(DataGridTestCase):

    def afterSetUp(self):

        self.folder.invokeFactory('DataGridDemoType', 'demo')
        self.demo = self.folder.demo
        self.demo.setDemoField([
                {'column1': 'a', 'column2': 'b', 'The third': 'c'},
                {'column1': 'd', 'column2': 'e', 'The third': 'f'}])
        self.field = self.demo.getField('DemoField')

    def testGetColumns(self):
        columns = self.field.getColumns(self.demo)
        self.assertEqual(columns[0], 'column1')
        self.assertEqual(columns[1], 'column2')
        self.assertEqual(columns[2], 'The third')

    def testGetRowCount(self):
        self.assertEqual(self.field.getRowCount(self.demo), 2)

    def testGetRow(self):
        self.assertEqual(
            self.field.getRow(self.demo, 1),
            {'column1': 'd', 'column2': 'e', 'The third': 'f'})

    def testGetColumn(self):
        self.assertEqual(
            tuple(self.field.getColumn(self.demo, 'column2')),
            ('b', 'e',))

    def testSearchKey(self):
        self.assertEqual(
            self.field.search(self.demo, key='d'),
            ({'column1': 'd', 'column2': 'e', 'The third': 'f'}, ))

    def testSearchColumn(self):
        self.assertEqual(
            self.field.search(self.demo, column2='e'),
            ({'column1': 'd', 'column2': 'e', 'The third': 'f'}, ))

    def testSearchWithNoResults(self):
        self.assertEqual(self.field.search(self.demo, 'foo'), ())

    def testLookup(self):
        self.assertEqual(self.field.lookup(self.demo, 'd', 'column2'), 'e')

    def testLookupWithKeyColumn(self):
        self.assertEqual(
            self.field.lookup(self.demo, 'b', 'column1', 'column2'), 'a')

    def testLookupNotFound(self):
        self.assertEqual(self.field.lookup(self.demo, 'x', 'The third'), None)

    def testGetAsDisplayList(self):
        lst = DisplayList()
        lst.add('a', 'b')
        lst.add('d', 'e')
        self.assertEqual(self.field.getAsDisplayList(self.demo), lst)

    def testGetAsDisplayListWithCustomColumns(self):
        lst = DisplayList()
        lst.add('c', 'a')
        lst.add('f', 'd')
        self.assertEqual(
            self.field.getAsDisplayList(self.demo, 'The third', 'column1'),
            lst)

    def testGetAsGrid(self):
        self.assertEqual(tuple(self.field.getAsGrid(self.demo)),
                         (('a', 'b', 'c',),
                          ('d', 'e', 'f')))

    def testQueryDataGrid(self):
        self.assertEqual(
            self.demo.queryDataGrid('DemoField', 'lookup', ['d', 'column2']),
            'e')

    def testSearch(self):
        catalog_tool = self.portal.portal_catalog
        self.folder.invokeFactory('DataGridDemoType2', 'searchme')
        self.folder.searchme.setDemoField2([
                {'column1': 'randomSearchableWord', 'column2': 'b',
                 'select_sample': 'sample'},
                {'column1': 'd', 'column2': 'e', 'select_sample': 'sample'}])
        self.folder.searchme.reindexObject()
        self.failUnless(
            'randomSearchableWord' in self.folder.searchme.SearchableText())
        brains = catalog_tool(SearchableText='randomSearchableWord')
        self.failUnless(len(brains) > 0)


class TestSpecialRowsBehavior(DataGridTestCase):
    """ Test fixed rows property, deletion locking, etc. """

    def afterSetUp(self):
        self.folder.invokeFactory('FixedRowsDemoType', 'demo')
        self.demo = self.folder.demo

        self.field = self.demo.getField('DemoField')
        self.failUnless(self.field != None)

        self.restrictedField = self.demo.getField('predefinedSkills')
        self.failUnless(self.restrictedField != None,
                        "No restricted field in demo type")

    def checkForCellValue(self, data, columnId, value):
        for row in data:
            if columnId in row.keys():
                if row[columnId] == value:
                    return True
        self.fail("Missing value %s for column %s" % (value, columnId))

    def testFixedRows(self):
        """Test that fixed rows are there always and non-key values
        can be changed.
        """

        # initial data get should be empty + fixed rows present
        data = self.field.get(self.demo)

        self.checkForCellValue(data, "column1", "must-exist-1")
        self.checkForCellValue(data, "column2", "must-exist-2")

    def testAddNonFixedRows(self):
        """ set more row and see that fixed rows are still present """
        self.demo.setDemoField([
                {'column1': 'a', 'column2': 'b', 'The third': 'c'},
                {'column1': 'd', 'column2': 'e', 'The third': 'f'}])

        data = self.field.get(self.demo)
        self.checkForCellValue(data, "column1", "must-exist-1")
        self.checkForCellValue(data, "column2", "must-exist-2")
        self.checkForCellValue(data, "column1", "a")
        self.checkForCellValue(data, "column2", "e")

    def testSetFixedRowValue(self):
        """ set non-key value of fixed row"""
        self.demo.setDemoField([
                {'column1': 'must-exist-1', 'column2': 'testvalue'}])
        data = self.field.get(self.demo)
        self.checkForCellValue(data, "column1", "must-exist-1")
        self.checkForCellValue(data, "column2", "must-exist-2")
        self.checkForCellValue(data, "column2", "testvalue")

        # test setting data outside fixed row definition
        self.demo.setDemoField([{'column1': 'naah', 'column2': 'nooh'}])
        data = self.field.get(self.demo)
        self.checkForCellValue(data, "column1", "naah")
        self.checkForCellValue(data, "column2", "nooh")

    def testDeleteRestrictedField(self):
        self.assertEqual(self.restrictedField.widget.isDeleteEnabled(
                self.demo, self.restrictedField), False)

    def testInsertRestrictedField(self):
        self.assertEqual(self.restrictedField.widget.isInsertEnabled(
                self.demo, self.restrictedField), False)

    def testReorderRestrictedField(self):
        self.assertEqual(self.restrictedField.widget.isReorderEnabled(
                self.demo, self.restrictedField), False)

    def testSetStringValue(self):
        self.demo.setDemoField('({"column1":"must-exist-1","column2":"testvalue"})')
        data = self.field.get(self.demo)
        self.checkForCellValue(data, "column1", "must-exist-1")
        self.checkForCellValue(data, "column2", "testvalue")

        self.demo.setDemoField("[{'column1': 'must-exist-1', 'column2': 'testvalue'}]")
        data = self.field.get(self.demo)
        self.checkForCellValue(data, "column1", "must-exist-1")
        self.checkForCellValue(data, "column2", "testvalue")

        self.demo.setDemoField('[{"column1": "must-exist-1", "column2": "testvalue"}]')
        data = self.field.get(self.demo)
        self.checkForCellValue(data, "column1", "must-exist-1")
        self.checkForCellValue(data, "column2", "testvalue")

        self.demo.setDemoField('({"column1": "must-exist-1", "column2": "testvalue"})')
        data = self.field.get(self.demo)
        self.checkForCellValue(data, "column1", "must-exist-1")
        self.checkForCellValue(data, "column2", "testvalue")

        # test with many lines

        self.demo.setDemoField('({"column1":"must-exist-1","column2":"testvalue"}, {"column1":"must-exist-2","column2":"testvalue2"})')
        value = self.demo.getDemoField()
        self.assertEqual(value[0]['column1'], "must-exist-1")
        self.assertEqual(value[0]['column2'], "testvalue")
        self.assertEqual(value[1]['column1'], "must-exist-2")
        self.assertEqual(value[1]['column2'], "testvalue2")

class TestLinkUtils(DataGridTestCase):
    """ Test LinkColumn link transforms """

    def afterSetUp(self):
        self.folder.invokeFactory("DataGridDemoType", id="sample")

    def testMakeAbsoluteURL(self):
        """ Test converting site relative links to full URLs
        """

        context = self.folder.sample

        self.assertEqual(makeAbsoluteLink("test", context),
                         "http://nohost/plone/test")
        self.assertEqual(makeAbsoluteLink("/test", context),
                         "http://nohost/plone/test")
        self.assertEqual(makeAbsoluteLink("http://test", context),
                         "http://test")

    def testMakeRelativeURL(self):
        """ Test converting full URLs to site relative links
        """

        context = self.folder.sample

        self.assertEqual(makeRelativeLink("http://nohost/plone/test", context),
                         "/test")
        self.assertEqual(makeRelativeLink("/test", context), "/test")
        self.assertEqual(makeRelativeLink("test", context), "test")
        self.assertEqual(makeRelativeLink("http://test", context),
                         "http://test")


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstallation))
    suite.addTest(makeSuite(TestGridAPI))
    suite.addTest(makeSuite(TestSpecialRowsBehavior))
    suite.addTest(makeSuite(TestLinkUtils))
    return suite
