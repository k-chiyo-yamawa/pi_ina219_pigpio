try:
    # Try using ez_setup to install setuptools if not already installed.
    from ez_setup import use_setuptools
    use_setuptools()
except ImportError:
    # Ignore import error and assume Python 3 which already has setuptools.
    pass

from setuptools import setup

DESC = ('This Python library for Raspberry Pi makes it easy to leverage the '
        'complex functionality of the Texas Instruments INA219 '
        'sensor to measure voltage, current and power.')

classifiers = ['Development Status :: 5 - Production/Stable',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 3.4',
               'Programming Language :: Python :: 3.5',
               'Programming Language :: Python :: 3.6',
               'Programming Language :: Python :: 3.7',
               'Topic :: System :: Hardware :: Hardware Drivers']

# Define required packages.
requires = ['pigpio']


def read_long_description():
    try:
        import pypandoc
        return pypandoc.convert_file('README.md', 'rst')
    except (IOError, ImportError):
        return ""


setup(name='pi-ina219-pigpio',
      version='1.4.1',
      author='Kazuma Chiyo',
      author_email='k.chiyo@yamawa.com',
      description=DESC,
      long_description=read_long_description(),
      license='MIT',
      url='https://github.com/k-chiyo-yamawa/pi_ina219_pigpio',
      classifiers=classifiers,
      keywords='ina219 raspberrypi pigpio',
      install_requires=requires,
      test_suite='tests',
      py_modules=['ina219'])
