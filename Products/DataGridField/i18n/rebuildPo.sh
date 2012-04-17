#!/bin/sh

i18ndude rebuild-pot --pot plone-datagridfield.pot --create plone ..
i18ndude filter plone-datagridfield.pot plone-exclude-datagridfield.pot > plone-final-datagridfield.pot
i18ndude sync --pot plone-final-datagridfield.pot plone-datagridfield-??.po