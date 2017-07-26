from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()


setup(name='azurerm',
      version='0.8.10',
      description='Azure Resource Manager REST wrappers',
      long_description=long_description,
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
