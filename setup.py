from setuptools import setup

version = '0.1dev'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'Django',
    'django-extensions',
    'django-jsonfield >= 0.8.10',
    'django-nose',
    'geojson',
    'lizard-geodin',
    'lizard-map > 4.1',
    'lizard-maptree',
    'lizard-ui >= 4.0',
    'lizard-wms',
    'sorl-thumbnail',
    ]

setup(name='lizard-levee',
      version=version,
      description="Lizard app for showing Geodin-based levee information",
      # Note: levee is 'dijken' in Dutch.
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Programming Language :: Python',
                   'Framework :: Django',
                   ],
      keywords=[],
      author='Reinout van Rees',
      author_email='reinout.vanrees@nelen-schuurmans.nl',
      url='https://github.com/lizardsystem/lizard-levee',
      license='GPL',
      packages=['lizard_levee'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points={
        'lizard_map.adapter_class': [
            'lizard_levee_risk_adapter = lizard_levee.layers:LeveeRisk',
            ],
        'console_scripts': [
            ]},
      )
