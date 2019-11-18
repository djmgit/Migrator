# setup.py
from setuptools import setup
import setuptools
import shutil
import os

def get_dependencies():
  with open("requirements.txt") as req:
    lines = req.readlines()
    lines = [line.strip() for line in lines]
    return lines

setup(name='migrator-1.0-djmgit',
      version='1.0',
      description='A tool for flexible reassignment of kafka topic partitions',
      long_description='A tool for flexible reassignment of kafka topic partitions',
      classifiers=[
        'Development Status :: 1.0',
        'License :: GPL',
        'Programming Language :: Python :: 3.6',
        'Topic :: Automation :: Systems :: Devops',
      ],
      keywords='kafka automation devops systems',
      url='https://github.com/djmgit/Migrator',
      author='Deepjyoti Mondal',
      author_email='djmdeveloper060796@gmail.com',
      license='GPL',
      packages=setuptools.find_packages(),
      install_requires=get_dependencies(),
      entry_points={
          'console_scripts': ['migrator=migrator.driver.driver:drive'],
      },
      include_package_data=True,
      zip_safe=False)

if __name__ == "__main__":
  print (setuptools.find_packages())
