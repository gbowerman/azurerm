'''Setup file for azurerm Azure REST wrapper library'''
from setuptools import setup

try:
    import pypandoc
    LONG_DESCRIPTION = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    LONG_DESCRIPTION = open('README.md').read()


setup(name='azurerm',
      version='0.8.22',
      description='Azure Resource Manager REST wrappers',
      long_description=LONG_DESCRIPTION,
      url='http://github.com/gbowerman/azurerm',
      author='sendmarsh',
      author_email='guybo@outlook.com',
      license='MIT',
      packages=['azurerm'],
      install_requires=[
          'adal',
          'requests',
      ],
      zip_safe=False)
