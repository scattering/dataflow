#!/usr/bin/python

import sys
#sys.path.append(r'c:\ubmatrix')
print sys.path
import ubmatrix.matrix.PyUB 
#import PyUB

ub = PyUB.PyUB()
#
# ub is now a PyUB object. See its members using dir(ub).
#
#  ub.monochromator_dspacing         Monochromator d (default = 3.354160 (PG))
#  ub.analyzer_dspacing              Analyzer      d (default = 3.354160 (PG))
#  ub.monochromator_ss               Scattering sense of monochromator (+-1)
#  ub.sample_ss                      Scattering sense of sample        (+-1)
#  ub.analyzer_ss                    Scattering sense of monochromator (+-1)
#  ub.a                              "a" Lattice parameter (default = 2 PI)
#  ub.b                              "b" Lattice parameter (default = 2 PI)
#  ub.c                              "c" Lattice parameter (default = 2 PI)
#  ub.alpha                          "alpha" Lattice parameter (default = 90.0 degrees)
#  ub.beta                           "beta"  Lattice parameter (default = 90.0 degrees)
#  ub.gamma                          "gamma" Lattice parameter (default = 90.0 degrees)
#
# To set up the UB matrix, you must enter two reflections:
ub.setReflection(refl=1,ei=14.7,ef=14.7,qh=1,qk=0,ql=0,a3=0.0,sample_two_theta=21.639293,sgl=0.0,sgu=0.0)
ub.setReflection(refl=2,ei=14.7,ef=14.7,qh=0,qk=1,ql=0,a3=90.0,sample_two_theta=21.639293,sgl=0.0,sgu=0.0)
# Then call self.calcub() and self.calcplanenormal()
ub.calcub()
ub.calcplanenormal()
#
# You may then calculate spectrometer angles for a given ei,ef,H,K,L using self.calcangles():
#
(a2,a3,a4,sgl,sgu,a6) = ub.calcangles(ei=14.7,ef=14.7,qh=0.707,qk=0.707,ql=0)
ub.dump()   # Print current members of ub object
print "A2 = %f  A3 = %f  A4 = %f  sgl = %f  sgu = %f  A6= %f \n"%(a2,a3,a4,sgl,sgu,a6)
#
# You can also calculate ei,ef,H,K,L,q using self.calcHKL():
# 
(ei,ef,qh,qk,ql,q) = ub.calcHKL(monochromator_two_theta=a2,a3=a3,sample_two_theta=a4,sgl=sgl,sgu=sgu,analyzer_two_theta=a6)
print "Ei = %f  Ef = %f  Qh = %f  Qk = %f  Ql = %f  Q = %f"%(ei,ef,qh,qk,ql,q)
