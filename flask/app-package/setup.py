from setuptools import setup

# To demonstrate the usage of application package
#
# pip install -e .
# flask run

setup(
    name='hello',
    packages=['hello'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
