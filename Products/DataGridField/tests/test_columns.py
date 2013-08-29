"""

    Unit test cases for DataGridField column definition manipulation

    Copyright 2006 Mikko Ohtamaa

"""

from Products.DataGridField.tests.DataGridTestCase import DataGridTestCase


class TestColumns(DataGridTestCase):
    """ Unit test cases for DataGridField column definition manipulation """

    def afterSetUp(self):
        self.folder.invokeFactory('DataGridDemoType', 'demo')
        self.demo = self.folder.demo

        self.folder.invokeFactory('DataGridDemoType2', 'demo2')
        self.demo2 = self.folder.demo2

        self.folder.invokeFactory('InvalidDataGridDemoType', 'invalid_demo')
        self.invalid_demo = self.folder.invalid_demo

    def testFill(self):
        """ Test that it is possible to enter data """
        self.demo.setDemoField([
                {'column1':'a', 'column2':'b', 'The third':'c'},
                {'column1':'d', 'column2':'e', 'The third':'f'}])
        self.field = self.demo.getField('DemoField')

    def testGetVocabulary(self):
        """ Test if vocabulary is received correctly for a select column
        """

        field = self.demo2.getField("DemoField2")
        col = field.widget.getColumnDefinition(field, "select_sample")
        vocab = col.getVocabulary(self.demo2)

        self.assertEqual(vocab.keys()[0], 'sample')
        self.assertEqual(vocab.keys()[1], 'sample2')

        self.assertEqual(vocab.values()[0], 'Sample value 1')
        self.assertEqual(vocab.values()[1], 'Sample value 2')

    def testInvalidWidgetColumnDefinition(self):
        """Try to get column definitions when there is field<->widget
        mismatch.
        """

        try:
            self.invalid_demo.getColumnLabels(self.invalid_demo, self)
            passed = False
        except AttributeError:
            # widget is missing column select_sample, should raise an error
            passed = True
            pass

        self.failUnless(passed, "Missing widget column ids were not catched")

    def testGetColumnDefinition(self):
        """ Just get column definitions"""

        field = self.demo2.getField("DemoField2")
        col = field.widget.getColumnDefinition(field, "select_sample")

        # backward compatibility: no explict column defnition given
        # so it should have been constructed automatically
        field = self.demo2.getField("DemoField2")
        col = field.widget.getColumnDefinition(field, "column1")

    def testGetColumnNames(self):
        """ Get user friendly column names """
        field = self.demo2.getField("DemoField2")
        names = field.widget.getColumnLabels(field, self.demo2)
        self.assertEqual(
            names,
            ["Toholampi city rox", "My friendly name", "Friendly name"])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestColumns))
    return suite
