from setuptools import setup

setup(
    name='hello',
    packages=['hello_package'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
