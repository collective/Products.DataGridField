#!/bin/sh

i18ndude rebuild-pot --pot plone-datagridfield.pot --create plone ..
i18ndude sync --pot plone-datagridfield.pot plone-datagridfield-??.po