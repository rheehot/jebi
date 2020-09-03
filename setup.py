import sys
from setuptools import setup


if sys.version_info < (2, 7):
    raise NotImplementedError("Sorry, you need at least Python 2.7 or Python 3.4+ to use jebi.")

import jebi
setup(name='jebi',
      version=jebi.__version__,
      description='Fast and simple WSGI-framework for small web-applications.',
      long_description_content_type="text/markdown",
      py_modules=['jebi'],
      scripts=['jebi.py'],
      license='MIT',
      platforms='any',
      )

