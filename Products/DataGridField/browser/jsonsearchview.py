import json
import logging
from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('Products.DataGridField: jsonsearchview')

class JSONSearchView(BrowserView):
    """
    """
    def getData(self, term):
        """
        """
        context = aq_inner(self.context)
        json_view_params = context.REQUEST.get('json_view_params', None)
        try:
            #transform the passed args into a real dict
            json_view_params = eval(json_view_params)
        except:
            logger.error("The parameters passed to the jsonsearchview could not be evaluated to a dict : '%s'" % json_view_params)
            return ''
        #activate wildcard search
        term = '*%s*' % term
        portal_catalog = getToolByName(context, 'portal_catalog')
        res = portal_catalog(json_view_params, SearchableText=term)
        res = [brain.Title for brain in res]
        return json.dumps(res)
