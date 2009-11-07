from setuptools import setup, find_packages
import os

version = '1.8a1'
readme = open(os.path.join("Products", "DataGridField", "README.txt")).read()
history = open(os.path.join("Products", "DataGridField", "HISTORY.txt")).read()
long_description = readme + "\n" + history


setup(name='Products.DataGridField',
      version=version,
      description="A table input component for Plone.",
      long_description=long_description,
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Plone",
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
          # -*- Extra requirements: -*-
          'Plone>=4.0dev',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
