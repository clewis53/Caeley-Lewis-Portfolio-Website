from setuptools import setup, find_packages

setup(
    name='flaskr',
    description='Simple microblog example using Flask',
    packages=find_packages(),
    entry_points='''
                 [flask.commands]
                 initdb=flaskr.flaskr:initdb_command
                 ''',
)
setup(
    name='Caeley-Lewis-Portfolio-Website',
    version='1.0',
    packages=['apps', 'dependencies'],
    url='',
    license='',
    author='caeley',
    author_email='caeleylewis53@gmail.com',
    description='Caeley Lewis\'s Portfolio WEbsite'
)
