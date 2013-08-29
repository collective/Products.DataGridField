"""Validator for DataGridFields.

For the DataGridFields, making them required is not enough as there is
always a hidden entry.  So we check if there is least one normal entry
and one hidden entry, so more than 1 entry in total.
"""

from Products.validation import validation
from Products.validation.interfaces.IValidator import IValidator
from Products.validation.i18n import recursiveTranslate
from zope.interface import implements

from Products.DataGridField import DGFMessageFactory as _
from Products.DataGridField.DataGridWidget import DataGridWidget

class DataGridValidator:
    """Validate as True when having at least one DataGrid item.
    """

    implements(IValidator)

    def __init__(self, name, title='', description=''):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):
        try:
            length = len(value) - 1
        except TypeError:
            return ("Validation failed(%s): cannot calculate length "
                    "of %s.""" % (self.name, value))
        except AttributeError:
            return ("Validation failed(%s): cannot calculate length "
                    "of %s.""" % (self.name, value))
        if length < 1:
            return ("Validation failed(%s): Need at least one entry."
                    % self.name)
        return True

class ColumnRequiredDataGridValidator:
    """Validate as True when data inside a column is required 
    """

    implements(IValidator)

    def __init__(self, name, title='', description=''):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):
        field = kwargs['field']
        if not isinstance(field.widget, DataGridWidget):
            # can't apply
            return True
        required_cols = []
        for cid, cdef in field.widget.columns.items():
            if cdef.required:
                required_cols.append(cid)
        if not required_cols:
            return True
        missing_columns = []
        for row in value:
            if not row.get('orderindex_', '').isdigit():
                # skipping the "template_row_marker" when on edit
                continue
            for cname, cvalue in row.items():
                if cname in required_cols and not cvalue and cname not in missing_columns:
                    missing_columns.append(cname)
        if missing_columns:
            missing_column_labels = []
            for cname in missing_columns:
                # Try to get a translated label.
                try:
                    cdef = field.widget.columns.get(cname)
                    label = cdef.getLabel(context=kwargs.get('REQUEST'))
                except:
                    # fall back to the column id.
                    label = cname
                missing_column_labels.append(label)
            return recursiveTranslate(_('missing_columns',
                                        default = u"The following columns are required but not all rows "
                                                  u"have been filled: ${columns}",
                                        mapping = {'columns': ', '.join(missing_column_labels)})
                                      , **kwargs)
        return True


isDataGridFilled = DataGridValidator(
    'isDataGridFilled', title='DataGrid has entries',
    description='The DataGridField must have at least one entry.')
validation.register(isDataGridFilled)

isColumnFilled = ColumnRequiredDataGridValidator(
    'isColumnFilled', title='Required columns have entries',
    description='All required columns must have data in every rows.')
validation.register(isColumnFilled)
