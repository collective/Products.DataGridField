from setuptools import setup, find_packages

version = '1.9.6'
readme = open("README.rst").read()
history = open("CHANGES.rst").read()
long_description = readme + "\n" + history


setup(name='Products.DataGridField',
      version=version,
      description="A table input component for Plone.",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Framework :: Plone",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Framework :: Zope2",
          "Development Status :: 5 - Production/Stable",
          ],
      keywords='Plone DataGridField Archetypes',
      author='Jarn',
      author_email='info@jarn.com',
      maintainer='Mikko Ohtamaa',
      maintainer_email='info@redinnovation.com',
      url='http://plone.org/products/datagridfield',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      extras_require=dict(
          test=[
              # Yes, we need both CMFTestCase and PloneTestCase:
              'Products.CMFTestCase',
              'Products.PloneTestCase',
              ]
      ),
      )
