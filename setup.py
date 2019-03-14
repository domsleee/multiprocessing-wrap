try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="MultiProcess",
    version="0.0.1",
    description="A better way to run shell commands in Python.",
    author='Dominic Slee',
    author_email='domslee1@gmail.com',
    long_description='TODO',
    py_modules=[
        'MultiProcess'
    ],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    url='TODO',
    license='BSD'
)