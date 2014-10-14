"""
    Archetypes items used in DataGridField unit testing and examples

"""
# Zope imports
from AccessControl import ClassSecurityInfo

# Plone imports
from Products.Archetypes import atapi

# Local imports
from Products.DataGridField import DGFMessageFactory as _
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
from Products.DataGridField.RadioColumn import RadioColumn
from Products.DataGridField.CheckboxColumn import CheckboxColumn
from Products.DataGridField.FixedColumn import FixedColumn
from Products.DataGridField.DataGridField import FixedRow
from Products.DataGridField.HelpColumn import HelpColumn
from Products.DataGridField.LinkColumn import LinkColumn
from Products.DataGridField.DateColumn import DateColumn
from Products.DataGridField.DatetimeColumn import DatetimeColumn
from Products.DataGridField.DatetimeLocalColumn import DatetimeLocalColumn
from Products.DataGridField.FileColumn import FileColumn
from Products.DataGridField.EmailColumn import EmailColumn
from Products.DataGridField.ColorColumn import ColorColumn
from Products.DataGridField.PasswordColumn import PasswordColumn
from Products.DataGridField.RangeColumn import RangeColumn
from Products.DataGridField.MonthColumn import MonthColumn
from Products.DataGridField.SearchColumn import SearchColumn
from Products.DataGridField.TimeColumn import TimeColumn
from Products.DataGridField.UrlColumn import UrlColumn
from Products.DataGridField.WeekColumn import WeekColumn
from Products.DataGridField.config import PKG_NAME


class DataGridDemoType(atapi.BaseContent):
    """ Very simple DataGridField demo.

    This class is used in unit testing, mainly to check old interface
    compatibility (without widget column definitions). Please see the
    more complex examples below.
    """
    security = ClassSecurityInfo()

    schema = atapi.BaseSchema + atapi.Schema((

        DataGridField('DemoField',
                searchable=True, # One unit tests checks whether text search works
                widget = DataGridWidget(),
                columns=('column1','column2','The third'),
                default=[
                {'column1':'a', 'column2':'b', 'The third':'c'},
                {'column1':'d', 'column2':'e', 'The third':'f'}
                ]
            ),
        ),
    )

    meta_type = portal_type = archetype_name = 'DataGridDemoType'

atapi.registerType(DataGridDemoType, PKG_NAME)


class DataGridDemoType2(atapi.BaseContent):
    """ Demo for different DataGridWidget columns

    This class is used in unit testing

    Check manual that:
        - Rows are inserted automatically when a value is filled in
        - Select column has sample 2 as a default value
    """
    security = ClassSecurityInfo()

    schema = atapi.BaseSchema + atapi.Schema((

        DataGridField('AutoInsertDemoField',
                searchable=True, # One unit tests checks whether text search works
                columns=("column1", "column2", "column3"),
                allow_empty_rows = False, # Must be false to make auto insert feature perform correctly
                widget = DataGridWidget(
                    auto_insert = True,
                    description="Automatically insert new rows when the last row is being filled. When you edit the last row, a new row is created automatically.",
                    description_msgid='DataGridDemoType_help_AutoInsertRows',
                    i18n_domain='datagridfield',
                    columns={
                    },
                 ),
         ),

        DataGridField('DemoField2',
                searchable=True, # One unit tests checks whether text search works
                columns=("column1", "column2", "select_sample"),
                widget = DataGridWidget(
                    description="Set default values for created rows. Choose SelectColumn value from the default dictionary",
                    description_msgid='DataGridDemoType_help_DemoField2',
                    i18n_domain='datagridfield',
                    columns={
                        'column1' : Column(_(u"Toholampi city rox"), required=True, col_description=_(u"Go Toholampi or go home.")),
                        'column2' : Column(_(u"My friendly name"), default=_(u"Some default text")),
                        'select_sample' : SelectColumn(_(u"Friendly name"), vocabulary="getSampleVocabulary", default="sample2")
                    },
                 ),
         ),

        DataGridField('DemoField3',
                columns=("column1", "column2"),
                widget = DataGridWidget(
                    description="Test radio and checkbox columns",
                    description_msgid='DataGridDemoType_help_DemoField3',
                    i18n_domain='datagridfield',
                    columns={
                        'column1' : RadioColumn("Radio column", vocabulary="getSampleVocabulary"),
                        'column2' : CheckboxColumn("Checkbox column")
                    },
                 ),
         ),

        DataGridField('DemoField4',
                columns=("text_column", "help_column"),
                widget = DataGridWidget(
                    description="Help column test",
                    description_msgid='DataGridDemoType_help_DemoField4',
                    i18n_domain='datagridfield',
                    columns={
                        'text_column' : Column("Text column"),
                        # Help is help.pt
                        'help_column' : HelpColumn("Help", _(u"See help here"), "help", "info.png")
                    },
                 ),
         ),

        DataGridField('DemoField5',
                columns=("link_column",),
                widget = DataGridWidget(
                    description="Set of links",
                    columns={
                        'link_column' : LinkColumn("Link column"),
                    },
                 ),
         ),

        DataGridField('DemoField6',
                columns=("date_column",),
                widget = DataGridWidget(
                    description="date column",
                    columns={
                        'date_column' : DateColumn("Date column"),
                    },
                 ),
         ),

        DataGridField('DemoField7',
                columns=("datetime_column",),
                widget = DataGridWidget(
                    description="datetime column",
                    columns={
                        'datetime_column' : DatetimeColumn("Datetime column"),
                    },
                 ),
         ),

        DataGridField('DemoField8',
                columns=("datetimelocal_column",),
                widget = DataGridWidget(
                    description="datetime column, local time zone",
                    columns={
                        'datetimelocal_column' : DatetimeLocalColumn("DatetimeLocal column"),
                    },
                 ),
         ),

        DataGridField('DemoField9',
                columns=("file_column",),
                widget = DataGridWidget(
                    description="file column",
                    columns={
                        'file_column' : FileColumn("File column"),
                    },
                 ),
         ),

        DataGridField('DemoField10',
                columns=("email_column",),
                widget = DataGridWidget(
                    description="email column",
                    columns={
                        'email_column' : EmailColumn("Email column"),
                    },
                 ),
         ),

        DataGridField('DemoField11',
                columns=("color_column",),
                widget = DataGridWidget(
                    description="color column",
                    columns={
                        'color_column' : ColorColumn("Color column"),
                    },
                 ),
         ),

        DataGridField('DemoField12',
                columns=("password_column",),
                widget = DataGridWidget(
                    description="password column",
                    columns={
                        'password_column' : PasswordColumn("Password column"),
                    },
                 ),
         ),

        DataGridField('DemoField13',
                columns=("range_column",),
                widget = DataGridWidget(
                    description="range column",
                    columns={
                        'range_column' : RangeColumn("Range column"),
                    },
                 ),
         ),

        DataGridField('DemoField14',
                columns=("month_column",),
                widget = DataGridWidget(
                    description="month column",
                    columns={
                        'month_column' : MonthColumn("Month column"),
                    },
                 ),
         ),

        DataGridField('DemoField15',
                columns=("search_column",),
                widget = DataGridWidget(
                    description="search column",
                    columns={
                        'search_column' : SearchColumn("Search column"),
                    },
                 ),
         ),

        DataGridField('DemoField16',
                columns=("time_column",),
                widget = DataGridWidget(
                    description="time column",
                    columns={
                        'time_column' : TimeColumn("Time column"),
                    },
                 ),
         ),

        DataGridField('DemoField17',
                columns=("url_column",),
                widget = DataGridWidget(
                    description="url column",
                    columns={
                        'url_column' : UrlColumn("Url column"),
                    },
                 ),
         ),

        DataGridField('DemoField18',
                columns=("week_column",),
                widget = DataGridWidget(
                    description="week column",
                    columns={
                        'week_column' : WeekColumn("Week column"),
                    },
                 ),
         ),


        ))

    meta_type = portal_type = archetype_name = 'DataGridDemoType2'

    def getSampleVocabulary(self):
        """Get a sample vocabulary
        """
        return atapi.DisplayList(

            (("sample", _(u"Sample value 1"),),
            ("sample2", _(u"Sample value 2"),),))

atapi.registerType(DataGridDemoType2, PKG_NAME)


class InvalidDataGridDemoType(atapi.BaseContent):
    """ DataGridField declaration with errors

    Errors should be detected run-time, with helpful error messages.

    This class is missing column definition select_sample in DataGridWidget
    """
    security = ClassSecurityInfo()

    schema = atapi.BaseSchema + atapi.Schema((
        DataGridField('DemoField',
                searchable = True,
                columns=("column1", "column2", "select_sample"),
                widget = DataGridWidget(
                    columns={
                        'column1' : Column(_(u"Toholampi city rox")),
                        'column2' : Column(_(u"My friendly name")),
                    },
          ),),

        ))

    meta_type = portal_type = archetype_name = 'InvalidDataGridDemoType'

atapi.registerType(InvalidDataGridDemoType, PKG_NAME)


class FixedRowsDemoType(atapi.BaseContent):
    """ Demostrate fixed rows usage

    This class is used in unit testing
    """
    security = ClassSecurityInfo()

    schema = atapi.BaseSchema + atapi.Schema((

        DataGridField('DemoField',
                widget = DataGridWidget(),
                columns=('column1','column2','The third'),
                fixed_rows = [
                    FixedRow(keyColumn="column1", initialData = { "column1" : "must-exist-1", "column2" : "bbb" }),
                    FixedRow(keyColumn="column2", initialData = { "column1" : "ddd", "column2" : "must-exist-2" }),
                ]
            ),

        DataGridField('RestrictedField',
                widget = DataGridWidget(),
                columns=('column1','column2','The third'),
                allow_insert=False,
                allow_delete=False,
                allow_reorder=False,
            ),

        DataGridField('predefinedSkills',
            searchable=True,
            columns=('skill', 'level'),
            fixed_rows = "getPredefinedSkillsData",
            allow_delete = False,
            allow_insert = False,
            allow_reorder = False,
            widget = DataGridWidget(
                label="Skills",
                label_msgid='DataGridDemoType_label_Skills',
                description="Language/technology/tool/method for which employer has special interest",
                description_msgid='DataGridDemoType_help_Skills',
                i18n_domain='datagridfield',
                columns= {
                    "skill" : FixedColumn(_(u"Skill")),
                    "level" : RadioColumn(_(u"Level"), vocabulary="getSkillLevels")
                }
            ),
            ),
        ))

    meta_type = portal_type = archetype_name = 'FixedRowsDemoType'

    def getSkillLevels(self):
        return atapi.DisplayList(
            (("bad", _(u"Bad"),),
             ("good", _(u"Good"),),
             ))

    def getPredefinedSkillsData(self):
        """ Generate fixed row key information """
        skills = [ "Python", "Perl", "XML", "Java", "Plone" ]
        rows = []
        for skill in skills:
            rows.append(FixedRow(keyColumn="skill", initialData={"skill" : skill, "level" : "bad"}))

        return rows


atapi.registerType(FixedRowsDemoType, PKG_NAME)




