from setuptools import setup

setup(name='azurerm',
      version='0.4',
      description='Simple Azure Resource Manager library',
      url='http://github.com/gbowerman/azurerm',
      author='sendmarsh',
      author_email='guybo@outlook.com',
      license='MIT',
      packages=['azurerm'],
	  install_requires=[
          'adal',
      ],
      zip_safe=False)