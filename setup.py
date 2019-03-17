from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="multiprocess",
    version="0.0.1",
    description="A better way to run shell commands in Python.",
    author='Dominic Slee',
    author_email='domslee1@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=[
        'multiprocess'
    ],
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    #url='TODO',
    #license='BSD'
)
