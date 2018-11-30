from setuptools import setup

setup(
    name='casebook',
    version='0.1',
    license='MIT',
    install_requires=['mysql-connector', 'Flask'],
    description='Casebook: a simple Facebook-like exercise for a database class final project.',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Topic :: Education',
        'License :: OSI Approved :: MIT License'
    ]
)