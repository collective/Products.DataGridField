import json
import logging
from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('Products.DataGridField: jsonsearchview')

class JSONSearchView(BrowserView):
    """
      This view manage the search result to return to the autocomplete widget
    """
    def getData(self, term):
        """
          Returns data corresponding to the term received and respecting the widgets search attributes
        """
        context = aq_inner(self.context)
        json_view_params = context.REQUEST.get('json_view_params', None)
        try:
            #transform the passed args into a real dict
            json_view_params = eval(json_view_params)
        except:
            logger.error("The parameters passed to the jsonsearchview could not be evaluated to a dict : '%s'" % json_view_params)
            return ''
        json_view_termfield = context.REQUEST.get('json_view_termfield', None)
        if not json_view_termfield:
            logger.warn("No 'json_view_termfield' received, we will use 'SearchableText'")
            json_view_termfield = "SearchableText"
        #activate wildcard search
        term = '*%s*' % term
        portal_catalog = getToolByName(context, 'portal_catalog')
        json_view_params[json_view_termfield] = term
        res = portal_catalog(json_view_params)
        res = [brain.Title for brain in res]
        return json.dumps(res)
