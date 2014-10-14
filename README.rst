DataGridField
=============

.. contents:: **Table of contents**

Released under the GNU General Public License

A table input component for the Plone Archetypes framework. Uses JavaScript to make entering tabular data more
user friendly process - there are no round trip HTTP requests to the server when inserting or deleting rows.


Features
--------

* Any number of columns set by a developer
* Any number of rows filled by a user
* Insert and deleting rows without submitting a form
* Many different column types


Requirements
------------

* Plone 4 (for Plone 3, use the latest release in the 1.7 branch or 1.6 branch, for Plone 2.5,
  use the latest release in the 1.6 branch)
* A browser with JavaScript support. There isn't yet graceful degradation for
  browsers without JavaScript.


Installation
------------

This version of DataGridField is distributed as an
egg at the Python Package index.  Information about configuring either for a zope instance
house a Plone site can be found by reading the `Installing an Add-on Product`_
tutorial.

.. _Installing an Add-on Product: http://plone.org/documentation/kb/add-ons

Once you've succesfully done this, you can use the Add/Remove Products screen to install the DataGridField into your
site. See below for information about experimenting with the demo types.

How to use
----------

When developing an `Archetypes`__ content type you will be able to add a new kind of field: the ``DataGridField``.
Low level data stored inside this field will be a Python tuple of dicts.

__ http://developer.plone.org/content/archetypes/

The widget used for this new type of field is the ``DataGridWidget``.

Field definition
~~~~~~~~~~~~~~~~

Follow a list of all ``DataGridField`` configurations:

``columns``
    A tuple of all columns ids.
    Default is a single column named "*default*".
``fixed_rows``
    A sequence of ``FixedRow`` instances that are row values that must exists.
    If those rows are deleted, they will be re-added when saving the content.

    See examples in the code for implementation details.
``allow_insert``
    User can append new rows. Currently is only an UI feature, this is not yet checked
    at application level.
    Default is True.
``allow_delete``
    User can delete rows. This is currently UI feature, this is not yet checked at
    application level.
    Default is True.
``allow_reorder``
    User can reorder rows. This is currently UI feature, this is not yet checked at
    application level.
    Default is True.
``searchable``
    If true all the contents of the DataGridField is concatenated to searchable text
    and given to text indexer.
    Default is False.
``allow_empty_rows``
    Set to false to allow empty rows in the data.
    Default is True.
``allow_oddeven``
    Set to true to hifhligh odd/even rows in edit/view form.
    Default is False

Widget definition
~~~~~~~~~~~~~~~~~

When defining a new ``DataGridWidget`` you can manage following options:

``show_header``
   Choose to display or not table headers in view or edit.
``auto_insert``
   Automatically add new rows when the last row is being edited.
``columns``
   A dict containing columns definition.

   This option is not required, but you must provide it for advanced datagrid configuration (see below).

Columns definition
~~~~~~~~~~~~~~~~~~

When defining columns (using the ``columns`` option in the *widget* definition above) you must provide a dict
composed by:

* a key that must be found in the ``columns`` definition of *field*.
* a ``Column`` class (or subclass) instance

Every ``Column`` instance have following options:

``label`` (required)
    The pretty label for the column.
``col_description``
    Additional description for the column scope
``default``
    Default value for every new value of the column
``default_method``
    Like ``default`` above, but instead of a static value it must be an attribute for a method
    that can be called on the context (similar to the *default_method* of Archetypes fields)
``visible``
    Define if the column will be visible.
    Default is True.
``required``
    If true, for every provided row, values in this columns must be filled.
    Default is False.

Apart the simple ``Column`` implementation, this product will provide additional kind of columns classes like:

* SelectColumn
* LinesColumn
* LinkColumn
* RadioColumn
* ...

Please refer to the `source code`__ for a complete list of columns and details of additional options.

__ https://github.com/collective/Products.DataGridField/tree/master/Products/DataGridField

Usage examples
~~~~~~~~~~~~~~

Simple example with three free text columns:

.. code-block:: python

        schema = BaseSchema + Schema((

        DataGridField('DemoField',
                widget = DataGridWidget(),
                columns=('column1','column2','The third')
                ),
        ))

Complex example with different column types and user friendly labels:

.. code-block:: python

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
                            'column1' : Column("Toholampi city rox",
                                               col_description="Go Toholampi or go home.",
                                               required=True),
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

Since DataGridField 1.5, if you wish to retain old way of automatic row inserting.
Here is a bit logic behind all this - otherwise there will be an extra row added when
you edit DGF and press save.

* You must set property ``auto_insert`` = True to DataGridWidget
* You must set property ``allow_empty_rows`` = False to DataGridField


Known bugs
----------

* Sometimes on Firefox column sizes start changing after the user enters some
  data. Not sure if this is a Firefox bug, though.
* Prefilled default values work only for text and select columns
* Radio button and link column postback is not handled properly. This needs
  fixes very deep into Zope (ZPublisher). If the form validation fails,
  link column and radio button columns lost their values.
* Not all types of columns are supported by all browsers because of
  HTML incompatibilities.  See
  http://www.w3schools.com/tags/tag_input.asp for details.


Demo
----

A demo type is included. It is disabled by default. This type is neither pretty nor very functional,
but demonstrates how a data grid should be used. You can install this type into your site by
running the "DataGridField (Example DGF content types)" from the Generic Setup tool within the ZMI.


References
----------

* `Custom Search product`__ uses DataGridField for editing search form query fields.
* `London School of Marketing`__ uses DataGridField extensively

__ http://plone.org/products/custom-search/
__ http://www.londonschoolofmarketing.com site

Contributors
------------

People who have been making this true:

* Mikko Ohtamaa, `Red Innovation`__
* Danny Bloemendaal
* Radim Novotny
* Justin Ryan
* Alexander Limi
* PloneSolutions <info@plonesolutions.com>
* Martin Aspeli <optilude@gmx.net>
* Paul Everitt, Zope Europe Association <paul@zope-europe.org>
* Development was helped by Vincent Bonamy
* Maurits van Rees
* Andreas Jung
* T Kim Nguyen <nguyen@uwosh.edu>

__ http://www.redinnovation.com

Original concept and prototype:

* Geir Baekholt, Plone Solutions <info@plonesolutions.com>
* Paul Everitt, Zope Europe Association <paul@zope-europe.org>

Sponsorship
-----------

Organizations paying up for the development:

* `London School of Marketing`__
* `United Nations Environment Programme`__

__ http://www.londonschoolofmarketing.com
__ http://www.unep.org
