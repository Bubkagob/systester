from setuptools import setup, find_packages

setup(name="systester",
      version="0.1",
      description="Systest toolbox",
      author="Ivan Alexandrov",
      packages=find_packages(),
      platforms="any",
      install_requires=[
          "lxml",
          "requests",
          "pymodbus"
      ],
      include_package_data=True,
      zip_safe=False)
