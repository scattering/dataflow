import os
from distutils.core import setup, Extension

ub_sources = ['PyUB.c', 'tasublib.c', 'cell.c', 'trigd.c', 'vector.c']
matrix_sources = [
    os.path.join('matrix',p)
    for p in ('matadd.c', 'matcreat.c', 'matdet.c','matdump.c','matdurbn.c',
              'materr.c', 'matinv.c', 'matmul.c', 'matsolve.c', 'matsub.c',
              'matsubx.c', 'mattoepz.c', 'mattran.c')
    ]
module1 = Extension('PyUB',
                    sources=ub_sources+matrix_sources,
                    )

setup(name = 'PyUB',
      version = '0.1a',
      maintainer = 'Nick Maliszewskyj',
      maintainer_email = "nickm@nist.gov",
      description = 'Extension for performing triple axis angle calculations',
      ext_modules = [module1])
