DataGridField
=============

Released under the GNU General Public License

A table input component for Plone. Uses Javascript to make entering tabular data more user friendly process -
there are no round trip HTTP requests to the server when inserting or deleting rows.


Features
--------

	o Any number of columns set by a developer

	o Any number of rows filled by a user

	o Insert and deleting rows without submitting a form

	o Many different column types


Requirements
------------

	o Plone 4 (for Plone 3, use the latest release in the 1.7 branch or 1.6 branch, for Plone 2.5, use the latest release in the 1.6 branch)

	o A browser with Javascript support. There isn't yet graceful degradation for
	  browsers without Javascript.


Installation
------------

This version of DataGridField is distributed as an
egg at the Python Package index.  Information about configuring either for a zope instance
house a Plone site can be found by reading the `Installing an Add-on Product`_
tutorial and the "Installing a third party product" section of the `Managing Project with zc.buildout`_ tutorial.

.. _Installing an Add-on Product: http://plone.org/documentation/tutorial/third-party-products
.. _Managing Project with zc.buildout: http://plone.org/documentation/tutorial/buildout/installing-a-third-party-product

Once you've succesfully done this, you can use the Add/Remove Products screen to install the DataGridField into your
site. See below for information about experimenting with the demo types.


Quality
-------

	o Tested with Firefox 2.0, IE 6, IE 7


Usage examples
--------------

Simple example with three free text columns::

        schema = BaseSchema + Schema((

        DataGridField('DemoField',
                widget = DataGridWidget(),
                columns=('column1','column2','The third')
                ),
        ))

Complex example with different column types and user friendly labels::

	# Plone imports
	from Products.Archetypes.public import DisplayList
	from Products.Archetypes.public import *

	# Local imports
	from Products.DataGridField import DataGridField, DataGridWidget
	from Products.DataGridField.Column import Column
	from Products.DataGridField.SelectColumn import SelectColumn

	class DataGridDemoType(BaseContent):
	    """A simple archetype

	    """

	    schema = BaseSchema + Schema((
	        DataGridField('DemoField',
	                searchable = True,
	                columns=("column1", "column2", "select_sample"),
	                widget = DataGridWidget(
	                    columns={
	                        'column1' : Column("Toholampi city rox"),
	                        'column2' : Column("My friendly name"),
	                        'select_sample' : SelectColumn("Friendly name", vocabulary="getSampleVocabulary")
	                    },
	                 ),
	         ),

	        ))

	    def getSampleVocabulary(self):
	        """
	        """
	        """ Get list of possible taggable features from ATVocabularyManager """
	        return DisplayList(

	            (("sample", "Sample value 1",),
	            ("sample2", "Sample value 2",),))

For more examples, see unit test code.


Notes
-----

	o Since DataGridField 1.5, if you wish to retain old way of automatic row inserting.
	  Here is a bit logic behind all this - otherwise there will be an extra row
	  added when you edit DGF and press save.

		o You must set property auto_insert = True to DataGridWidget

		o You must set property allow_empty_rows = False to DataGridField


Known bugs
----------

	o Sometimes on Firefox column sizes start changing after the user enters some
	  data. Not sure if this is a Firefox bug, though.

	o Prefilled default values work only for text and select columns

	o Radio button and link column postback is not handled properly. This needs
	  fixes very deep into Zope (ZPublisher). If the form validation fails,
	  link column and radio button columns lost their values.


Demo
----

A demo type is included. It is disabled by default. This type is neither pretty nor very functional,
but demonstrates how a data grid should be used. You can install this type into your site by
running the "DataGridField (Example DGF content types)" from the Generic Setup tool within the ZMI.


References
----------

"Custom Search product":http://plone.org/products/custom-search/ uses DataGridField for editing search form query fields.

"London School of Marketing":http://www.londonschoolofmarketing.com site
uses DataGridField extensively


Contributors
------------

People who have been making this true:

	o Mikko Ohtamaa, "Red Innovation":http://www.redinnovation.com

	o Danny Bloemendaal

	o Radim Novotny

	o Justin Ryan

	o Alexander Limi

	o PloneSolutions <info@plonesolutions.com>

	o Martin Aspeli <optilude@gmx.net>

	o Paul Everitt, Zope Europe Association <paul@zope-europe.org>

	o Development was helped by Vincent Bonamy

	o Maurits van Rees

	o Andreas Jung


Original concept and prototype:

	o Geir Baekholt, Plone Solutions <info@plonesolutions.com>

	o Paul Everitt, Zope Europe Association <paul@zope-europe.org>


Sponsorship
-----------

Organizations paying up for the development

	o "London School of Marketing":http://www.londonschoolofmarketing.com

	o "United Nations Environment Programme":http://www.unep.org
