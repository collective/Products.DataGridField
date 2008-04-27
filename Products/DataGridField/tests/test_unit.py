import unittest
from zope.testing import doctest
from zope.testing import doctestunit

OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


def test_suite():
    return unittest.TestSuite([
        doctestunit.DocFileSuite('validators.txt',
                                 package='Products.DataGridField.tests',
                                 optionflags=OPTIONFLAGS),
        ])
