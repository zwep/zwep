import setuptools


def requirements():
    with open('requirements.txt') as f:
        return f.read().strip().split('\n')

def readme():
    with open('README.md') as f:
        return f.read()

setuptools.setup(name='zwep',
      version='0.1.0',
      description='My own package...',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Topic :: Processing :: Misc',
      ],
      keywords='misc help functions',
      author='Seb Harrevelt',
      author_email='sebharrevelt@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=requirements(),
      include_package_data=True,
      zip_safe=False)