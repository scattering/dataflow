from distutils.core import setup, Extension

module1 = Extension('PyUB',
                    sources = ['PyUB.c',
                               'tasublib.c',
                               'cell.c',
                               'trigd.c',
                               'vector.c'],
                    libraries = ['matrix'],
                    library_dirs = ['c:\ubmatrix\matrix']
                    )

setup(name = 'PyUB',
      version = '0.1',
      maintainer = 'Nick Maliszewskyj',
      maintainer_email = "nickm@nist.gov",
      description = 'Extension for performing triple axis angle calculations',
      ext_modules = [module1])
