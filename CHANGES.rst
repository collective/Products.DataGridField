Changelog
=========

1.9.0 (2013-09-19)
------------------

- Support argument ``label`` plus the standard keyword arguments in
  all Columns: ``col_description ``, ``default``, ``default_method``,
  ``visible``, ``required``.  Child classes may support more arguments
  or keywords arguments.
  [maurits]

- No longer support ``label_msgid`` in Columns.  This was unused for
  years.
  [maurits]

- Change ``Column.getLabel`` to support translation again.  You should
  pass a request as the context.
  [maurits]

- New column option ``col_description``: display help text for column purpose
  [keul]

- New column option ``required``: mark data inside column as required
  [keul]

- Added alpha channel to grid icons
  [keul]

- Added a ``visualClear`` div after the "add new row" button.
  This fix visual issues when field validation error take place.
  [keul]

- Give focus to first column of new added row [keul]


1.8.4 (2013-01-04)
------------------

- added Italian locale [cekk]


1.8.3 (2012-08-23)
------------------

- support for brower view names as 'vocabulary' parameter
  for SelectColumn class

1.8.2 (2012-08-23)
------------------

- added new CSS classes to the manipulator table cells in order 
  to be able to attach custom JS handlers
  [ajung]


1.8.1 (2012-06-28)
------------------

- Added English locale. Minor internal packaging improvements.
  [maurits]


1.8.0 (2012-05-29)
------------------

- Strip empty spaces in a list of values.
  [WouterVH]

- final 1.8.0 release
  [ajung]


1.8b2 (2011-05-08)
------------------

- French translation.
  [thomasdesvenain]

- Added titles on row manipulators images.
  [thomasdesvenain]

- Fixed setting a field value using a base string, using json decoder.
  Added tests.
  [thomasdesvenain]

- fixed check for 'empty' for LineColumns 
  [ajung]


1.8b1 (2010-08-16)
------------------

- Register locales directory in zcml.
  [buchi]

- Added German translations.
  [buchi]


1.8a2 (2010-06-02)
------------------

- Fixed Unauthorized error in queryDataGrid when the aq_parent of an
  object is private, even when we do not actually need any info from
  that parent.  (Change ported from 1.6.2.)
  [maurits]

- Added support for Spanish localization
  [macagua]

- Added support for i18n
  [macagua]

- the TD cells of a rendered DGF field now contain an additional
  CSS class 'col-$colnumber'
  [ajung]

- removed pointless Plone==4 pinning in setup.py causing more
  problems than it actually solves


1.8a1 (2009-11-07)
------------------

- Fixed possible TypeError when submitting the base_metadata form.
  [maurits]

- In the view macro use the supplied accessor instead of thinking we
  know how to get the accessor ourselves as that gives wrong results
  with LinguaPlone.
  Fixes http://plone.org/products/datagridfield/issues/14
  [maurits]

- Fixed tests for Plone 4, including a good cleanup.
  [maurits]

- Adaptation to work on Plone 4/Zope 2.12.
  For Plone 3, please use the 1.7 or 1.6 branches.
  [vincentfretin]


1.7 (unreleased)
----------------

- When there is an empty row with the template_row_marker and
  validation fails (for any field), make sure we do not end up with
  *two* empty rows.
  [maurits+vpretre]

- added LinesColumn (used as custom vocabulary source in PFGDataGrid field)
  [naro]

- added unique column classnames for thead and tbody table section to identify
  columns and modify it's properties through css (specially width for each
  column seperatly). Now we can remove the style attributes and do some
  template code cleanup.  [saily]

- allow Products.Archetypes.interfaces.IVocabulary providing objects as
  Vocabularies. This makes SelectColumn usable in archetypes.schemaextender
  w/o having to patch the extended class.
  [jensens]

- Move installation back to GenericSetup, end of Plone 2.5.x support
  [andrewb, but real thanks goes to wichert]


1.6 (2009-01-28)
----------------

- Merging of colliding datagridwidget.css and datagridwidget.css.dtml files.
  Fixes issue #30: http://plone.org/products/datagridfield/issues/30.  Which
  file was ultimately selected appears to be inconsistent.  If you're
  depending upon an overridden version of either and notice bugs with regards
  to hidden columns and/or rows appearing or the promise of adding additional
  DGF rows when using the FixedColumn, you'd be well suited to reconcile your
  customizations with the merged files from r10445 at:
  http://dev.plone.org/archetypes/changeset/10445
  [andrewb]


1.6rc1
------

- Adding Plone 2.5.x DataGridField profile "default_25x" to overcome difference in
  GS namespace for the registration of our skin directory.  Without this, one needed
  to manually add the correct FSDV within the portal_skins tool for .pt, .dtml,
  images, etc. to exist with the DataGridWidget's skins directory. [andrewb]

- Adding back Extensions and Install.py with install() function for consistent
  Add/Remove Products experience back to Plone 2.5.x, which did not handle
  GenericSetup profile-based installation.  The install code delegates to Generic
  Setup for maximal code reuse. The justification is that to completely remove
  a Add/Remove Product support in Plone 2.5.x between a beta 2 and beta 3 release
  is overly extreme.  This will workaround will be rectified in a future release. [andrewb]

  Note: This was added manually without history because the the eggified version
  of DataGridField was moved, rather than copied, thus no history at:
  http://dev.plone.org/archetypes/log/Products.DataGridField?action=follow_copy&rev=&stop_rev=&mode=follow_copy

- Updated installation instructions, info about example types, and added note about ceasing
  Plone 2.5.x support [andrewb]

- Removed check of "@@plone_lock_info" within example types' GS declarations,
  so actions render in pre-Plone locking era [andrewb]

- Made all tests pass in Plone 2.5.x, 3.0.x, and 3.1.x [andrewb]

- Made explicit names for the different GS profiles that one might choose
  to install within portal_setup [andrewb]


1.6 beta 3
----------

- Eggified in Products.AddRemoveWidget
  [SteveM]

- Register skin layer correctly.
  [maurits]

- Move installation to GenericSetup.
  [wichert]

- Removed lots and lots of unneeded import. Pyflakes found that Plone 2.1
  support has been broken for a while, so stop claiming it's still supported.
  [wichert]

- Added validator isDataGridFilled (copied from Poi, where it can
  later be removed).  Use this as validator on a DataGridField if you
  want it to have at least one entry: currently a bogus/hidden entry
  always remains even when you remove all real entries, so making a
  DataGridField required has no real effect.
  See http://plone.org/products/poi/issues/139 and 160.
  [maurits]


1.6 beta 2
----------

- Disabled INSTALL_DEMO_TYPES from config.py.
  [andrewburkhalter]


1.5
---

- Pop-up help column by Juan Grigera

- Added CheckboxColumn by Radim Novotny

- Plone 3.0 compatible (fixed CMFCorePermissions import)

- Fixed http://plone.org/products/datagridfield/issues/16 (applied the patch)

- DataGridField has new property allow_oddeven. Setting this to True will highlight
  odd end even rows in the view/edit tables. Default: False

- FixedColumn has optional parameter "visible" (default True). Setting this to False
  will hide (using css) column from both - view and edit forms.


1.5rc3
------

- Added CheckboxColumn. Implementation based on RadioColumn, so there are same bugs.
  CheckboxColumn lose values if any field on the form raises validation error.
  Be aware of that, better does not use CheckboxColumn in forms with required fields
  or fields with validators.
  [Contributor: naro, radim novotny]


1.5rc2
------

- Fixed row adding in IE. This was one of the most horrible debugging session
  I have had. There was some obscure IE bug which prevented making a DOM
  node orignally hidden to visible. I created "hacky" workaround for this.
  Tested in IE 6.0 and FF 1.5.

- Wolfram Fenske's I18N patch is disabled, since it doesn't work in Plone 2.5.
  The code is almost there. If someone wants to make it complete, it shouldn't
  take too much time.


1.5rc1
------

- Added workaround for bad DGF initializing which caused empty rows when DGF was created
  programmatically


1.0 to 1.5
----------

- Plone 2.5 compatibility guaranteed

- DGF row manipulators rewritten. Automatically adding new rows feature is
  now optional, thus making it possible for columns to have prefilled
  default values without creating a mess. Disabling auto insert is necessary
  for columns like SelectWidget which don't have empty default values.

- Refactored page template code to be more easily extendable. Now CSS file
  is used for styling DataGridWidgets.

- New column type: Link column

- (Wolfram Fenske) I18N patch

  Archetypes widgets have an attribute i18n_domain, which is used to
  determine which message catalog to use for translation. In
  DataGridField, this attribute is ignored.

  I have attached a small patch (in fact, smaller than this bug report)
  which fixes these problems. I didn't want to introduce a lot of new
  code, so I did the translation of the labels in the Column class, not
  in the page template, which might also have been a good way to do it.
  Since the functions "getLabel()" and "getColumnLabels()" are only
  called by the page template anyway, I believe this is not an issue.
  But if you'd rather translate the labels in the page template, please
  let me know and I'll write a different patch.

- (Juan Grigera) Marshaller patch

  I enjoyed your DataGriedField/Widget product for Plone, and would like
  to contributea small patch/bugfix. In the field mutator (set) the
  passed value is not always a record, but sometimes a string.
  In fact the RFC822Marshaller passes a string.
