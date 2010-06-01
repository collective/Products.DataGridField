## Python Script "queryDataGrid"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=fieldName, method, args
##title=Query a data grid
##

from Products.CMFPlone.utils import safe_hasattr

# Find the field on this item or any parent
# Apply the given method (passed in as a string) with the given arguments
# (as a list) and return the results.


obj = context
while obj is not None:
    if safe_hasattr(obj, 'Schema') and obj.Schema().has_key(fieldName):
        break
    else:
        obj = obj.aq_parent

query = getattr(obj.getWrappedField(fieldName), method)
return query(obj, *args)
