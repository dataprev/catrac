from setuptools import find_packages, setup

# name can be any name.  This name will be used to create .egg file.
# name that is used in packages is the one that is used in the trac.ini file.
# use package name as entry_points
setup(
    name='catrac', version='0.1',
    packages=find_packages(exclude=['*.tests*']),
    entry_points = """
        [trac.plugins]
        catrac = catrac
    """,
    package_data={'catrac': ['templates/*.html', 
                                 'htdocs/css/*.css', 
                                 'htdocs/images/*']},
)
