#include <Python.h>
#include <structmember.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include "tasublib.h"
/*
  Members:
  ==MACHINE PARAMETERS========================================================
  monochromator_dspacing    double 
  monochromator_ss          int      Scattering sense
  sample_ss                 int      Scattering sense
  analyzer_dspacing         double
  analyzer_ss               int      Scattering sense
  ==SAMPLE PARAMETERS=========================================================
  a                         double   Default 6.2831
  b                         double   Default 6.2831
  c                         double   Default 6.2831
  alpha                     double   Default 90.0
  beta                      double   Default 90.0
  gamma                     double   Default 90.0
  ==ANGLES=======================  COMPLETE DESCRIPTION OF SINGLE STATE  =====
  monochromator_two_theta   double
  sample_rotation           double
  sample_two_theta          double
  analyzer_two_theta        double 
  sgu                       double   Sample Upper Tilt
  sgl                       double   Sample Lower Tilt
  ==QE VALUES====================  COMPLETE DESCRIPTION OF SINGLE STATE  =====
  ki                        double
  kf                        double
  q                         double   Magnitude of momemtum transfer
  qh                        double
  qk                        double
  ql                        double
  ==TRANSITIONAL QUANTITIES===================================================
  UB                        MATRIX (**double)
  plane_normal              MATRIX (**double)
  ============================================================================

  Prescription for Python wrapper:
    Initialize experiment
        Load machine parameters
	Load sample parameters (lattice)
    Calculate Orientation matrix
        Load angles,qe for first reflection
	Load angles,qe for second reflection
	Calculate UB matrix      calcTasUBFromTwoReflections()
	Calculate plane normal   calcPlaneNormal()
    Use UB matrix to find machine angles
        Specify qe
	Calculate angles needed to achieve specified qe calcAllTasAngles()

    TODO: Write getsetters for UB and PlaneNormal
*/

#define D_PG 3.35416
#define D_CU 1.278
#ifndef PI
#define PI 3.141592653589793
#endif

typedef struct {
  PyObject_HEAD
  lattice cell;
  tasMachine machine;
  tasReflection refl1;
  tasReflection refl2;
} tas;

#ifndef PyMODINIT_FUNC /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif

static void PyUB_dealloc(tas * self)
{
  self->ob_type->tp_free((PyObject *)self);
}

static void PyUB_defaults(tas * self)
{
  self->machine.monochromator.dd = D_PG;
  self->machine.analyzer.dd      = D_PG;
  self->machine.monochromator.ss =  1;
  self->machine.analyzer.ss      =  1;
  self->machine.ss_sample        =  1;
  self->cell.a = 2 * PI;
  self->cell.b = 2 * PI;
  self->cell.c = 2 * PI;
  self->cell.alpha = 90.0;
  self->cell.beta  = 90.0;
  self->cell.gamma = 90.0;
}

static PyObject* PyUB_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
  tas * self;

  self = (tas *)type->tp_alloc(type,0);
  if (self == NULL) {
    PyErr_SetString(PyExc_RuntimeError,"tas allocation error");
    return NULL;
  }
  return (PyObject *)self;
}

static int PyUB_init(tas * self, PyObject *args, PyObject *kwds)
{
  PyUB_defaults(self);
  return 0;
}

static PyObject * PyUB_print(tas * self)
{
  printf("monochromator_dspacing = %f\n", self->machine.monochromator.dd);
  printf("monochromator_ss       = %d\n", self->machine.monochromator.ss);
  printf("sample_ss              = %d\n", self->machine.ss_sample);
  printf("analyzer_dspacing      = %f\n", self->machine.analyzer.dd);
  printf("analyzer_ss            = %d\n", self->machine.analyzer.ss);
  printf("a                      = %f\n", self->cell.a);
  printf("b                      = %f\n", self->cell.b);
  printf("c                      = %f\n", self->cell.c);
  printf("alpha                  = %f\n", self->cell.alpha);
  printf("beta                   = %f\n", self->cell.beta);
  printf("gamma                  = %f\n", self->cell.gamma);
  printf("Reflection_1 ==============\n");
  printf("monochromator_two_theta= %f\n", self->refl1.angles.monochromator_two_theta);
  printf("a3                     = %f\n", self->refl1.angles.a3);
  printf("sample_two_theta       = %f\n", self->refl1.angles.sample_two_theta);
  printf("sgl                    = %f\n", self->refl1.angles.sgl);
  printf("sgu                    = %f\n", self->refl1.angles.sgu);
  printf("analyzer_two_theta     = %f\n", self->refl1.angles.analyzer_two_theta);
  printf("ki                     = %f\n", self->refl1.qe.ki);                    
  printf("kf                     = %f\n", self->refl1.qe.kf);                    
  printf("qh                     = %f\n", self->refl1.qe.qh);                    
  printf("qk                     = %f\n", self->refl1.qe.qk);                    
  printf("ql                     = %f\n", self->refl1.qe.ql);                    
  printf("q                      = %f\n", self->refl1.qe.qm);
  printf("Reflection_2 ==============\n");
  printf("monochromator_two_theta= %f\n", self->refl2.angles.monochromator_two_theta);
  printf("a3                     = %f\n", self->refl2.angles.a3);
  printf("sample_two_theta       = %f\n", self->refl2.angles.sample_two_theta);
  printf("sgl                    = %f\n", self->refl2.angles.sgl);
  printf("sgu                    = %f\n", self->refl2.angles.sgu);
  printf("analyzer_two_theta     = %f\n", self->refl2.angles.analyzer_two_theta);
  printf("ki                     = %f\n", self->refl2.qe.ki);                    
  printf("kf                     = %f\n", self->refl2.qe.kf);                    
  printf("qh                     = %f\n", self->refl2.qe.qh);                    
  printf("qk                     = %f\n", self->refl2.qe.qk);                    
  printf("ql                     = %f\n", self->refl2.qe.ql);                    
  printf("q                      = %f\n", self->refl2.qe.qm);
  if (self->machine.UB != (MATRIX)NULL) {
    printf("UB =====================\n");
    printf("   %9.6f  %9.6f  %9.6f\n",self->machine.UB[0][0],
	   self->machine.UB[0][1],self->machine.UB[0][2]);
    printf("   %9.6f  %9.6f  %9.6f\n",self->machine.UB[1][0],
	   self->machine.UB[1][1],self->machine.UB[1][2]);
    printf("   %9.6f  %9.6f  %9.6f\n",self->machine.UB[2][0],
	   self->machine.UB[2][1],self->machine.UB[2][2]);
  }
  if (self->machine.planeNormal != (MATRIX)NULL) {
    printf("PlaneNormal ============\n");
    printf("   %9.6f\n",self->machine.planeNormal[0][0]);
    printf("   %9.6f\n",self->machine.planeNormal[1][0]);
    printf("   %9.6f\n",self->machine.planeNormal[2][0]);
  }
  Py_RETURN_NONE;
}

static PyObject * PyUB_CalcUB(tas * self)
{
  /* Remember to manage memory for UB matrix. 
     This would be a great place for a memory leak. */
  int errorcode;
  char errstring[80];
  if (self->machine.UB != (MATRIX) NULL) 
    mat_free(self->machine.UB);
  if ((self->machine.UB = calcTasUBFromTwoReflections(self->cell,
						      self->refl1,
						      self->refl2,
						      &errorcode))
      == NULL) {
    /* Throw an exception */
    switch(errorcode) {
    case ENERGYTOBIG:
      sprintf(errstring,"Specified energy too big");
      break;
    case BADSYNC:
      sprintf(errstring, "Monochromator and analyzer out of sync");
      break;
    case UBNOMEMORY:
      sprintf(errstring, "No memory for UB matrix");
      break;
    case TRIANGLENOTCLOSED:
      sprintf(errstring, "Cannot close scattering triangle");
      break;
    case BADRMATRIX:
      sprintf(errstring, "Bad R matrix");
      break;
    case BADUBORQ:
      sprintf(errstring, "Bad UB matrix or Q");
      break;
    default:
      sprintf(errstring, "General fault");
    }
    PyErr_SetString(PyExc_ArithmeticError,errstring);
    Py_RETURN_NONE;
  }

  Py_RETURN_NONE;
}

static PyObject * PyUB_CalcPlaneNormal(tas * self)
{
  /* Remember to manage memory for plane normal.
     This would be a great place for a memory leak. */
  if (self->machine.planeNormal != (MATRIX) NULL) 
    mat_free(self->machine.planeNormal);
  if ((self->machine.planeNormal = calcPlaneNormal(self->refl1,self->refl2))
      == NULL) {
    PyErr_SetString(PyExc_ArithmeticError,
		    "General fault calculating plane normal");
    Py_RETURN_NONE;    
  }
  Py_RETURN_NONE;
}

/*
 * PyUB_CalcAngles - Calculate spectrometer angles using UB matrix 
 *                   and Q,E coordinates
 *      Input:       Ei, Ef, Qh, Qk, Ql
 *      Returns:     monochromator_two_theta (A2), sample_rotation (A3),
 *                   sample_two_theta (A4), sample_lower_tilt (sgl),
 *                   sample_upper_tilt (sgu), analyzer_two_theta (A6)
 */
static PyObject * PyUB_CalcAngles(tas * self, PyObject *args, PyObject *kwds)
{
  tasAngles angles;
  tasQEPosition qe;
  tasMachine * machine;
  double ei, ef;
  int retn;
  static char *kwlist[] = {"ei","ef","qh","qk","ql", NULL};
  memset(&qe,0,sizeof(qe));
  if (!PyArg_ParseTupleAndKeywords(args,kwds,"ddddd", kwlist,
				   &ei,&ef,&(qe.qh),
				   &(qe.qk),&(qe.ql)))
    return NULL;
  qe.ki = energyToK(ei);
  qe.kf = energyToK(ef);

  machine = &(self->machine);

  if (machine->UB == (MATRIX)NULL) {
    PyErr_SetString(PyExc_RuntimeError,"Empty UB matrix!");
    return NULL;
  }

  retn = calcAllTasAngles(&(self->machine), qe, &angles);
  if (retn) return Py_BuildValue("dddddd",
				 angles.monochromator_two_theta,
				 angles.a3,
				 angles.sample_two_theta,
				 angles.sgl,
				 angles.sgu,
				 angles.analyzer_two_theta);
				 
  Py_RETURN_NONE;
}

/*
 * PyUB_CalcHKL - Calculate reciprocal space coords given spectrometer angles
 *      Input:       monochromator_two_theta (A2), sample_rotation (A3),
 *                   sample_two_theta (A4), sample_lower_tilt (sgl),
 *                   sample_upper_tilt (sgu), analyzer_two_theta (A6)
 *      Returns:     Ki, Kf, Qh, Qk, Ql, Qm (magnitude)
 */

static PyObject * PyUB_CalcHKL(tas * self, PyObject *args, PyObject *kwds)
{
  tasAngles angles;
  tasQEPosition qe;
  tasMachine * machine;
  double ei, ef;
  int retn;
  static char *kwlist[] = {"monochromator_two_theta",
			   "a3",
			   "sample_two_theta",
			   "sgl",
			   "sgu",
			   "analyzer_two_theta",
			   NULL};
  if (!PyArg_ParseTupleAndKeywords(args,kwds,"dddddd", kwlist,
				   &(angles.monochromator_two_theta),
				   &(angles.a3),
				   &(angles.sample_two_theta),
				   &(angles.sgl),
				   &(angles.sgu),
				   &(angles.analyzer_two_theta)))
    return NULL;

  machine = &(self->machine);
  if (machine->UB == (MATRIX)NULL) {
    PyErr_SetString(PyExc_RuntimeError,"Empty UB matrix!");
    return NULL;
  }

  retn = calcTasQEPosition(&(self->machine), angles, &qe);

  ei = KtoEnergy(qe.ki);
  ef = KtoEnergy(qe.kf);

  if (retn) return Py_BuildValue("dddddd",ei,ef,qe.qh,qe.qk,qe.ql,qe.qm);
  Py_RETURN_NONE;
}

static PyObject * PyUB_SetReflection(tas * self, PyObject * args, PyObject *kwds)
{
  static char * kwlist[] = {"refl","ei","ef","qh","qk","ql",
			    "a3","sample_two_theta","sgl","sgu",NULL};
  tasReflection refl;
  double ei, ef,ki,kf,q2;
  int whichrefl;
  double raddeg = PI / 180.0;
  ei = ef = ki = kf;
  if (!PyArg_ParseTupleAndKeywords(args,kwds,"iddddddddd",kwlist,
				   &whichrefl,&ei,&ef,
				   &(refl.qe.qh),&(refl.qe.qk),&(refl.qe.ql),
				   &(refl.angles.a3),&(refl.angles.sample_two_theta),
				   &(refl.angles.sgl),&(refl.angles.sgu)))
    return NULL;

  if ((whichrefl < 1) || (whichrefl > 2)) {
    PyErr_SetString(PyExc_ValueError,"Specify reflection 1 or 2");
    Py_RETURN_NONE;
  }

  if ((ei == 0) || (ef == 0)) {
    PyErr_SetString(PyExc_ValueError,"Incident and final energies must be nonzero!");
    Py_RETURN_NONE;
  }

  ki = energyToK(ei);
  kf = energyToK(ef);
  q2 = ki * ki + kf * kf - 2 * ki * kf * cos(raddeg * refl.angles.sample_two_theta);
  /* Check that q2 > 0 */
  if (q2 < 0) {
    PyErr_SetString(PyExc_ValueError,"Cannot close scattering triangle");
    Py_RETURN_NONE;
  }
  refl.qe.ki = ki;
  refl.qe.kf = kf;
  refl.qe.qm = sqrt(q2);
  refl.angles.monochromator_two_theta = 2 * asin(PI / (ki * self->machine.monochromator.dd)) / raddeg;
  refl.angles.analyzer_two_theta = 2 * asin(PI / (kf * self->machine.analyzer.dd)) / raddeg;

  if (whichrefl == 1) {
    memcpy(&(self->refl1),&refl,sizeof(tasReflection));
  } else if (whichrefl == 2) {
    memcpy(&(self->refl2),&refl,sizeof(tasReflection));
  }

  Py_RETURN_NONE;
}

static PyMemberDef PyUB_members[] = {
  {"monochromator_dspacing", T_FLOAT,  offsetof(tas,machine.monochromator.dd), 0, "Monochromator d-spacing"},
  {"monochromator_ss",       T_INT,    offsetof(tas,machine.monochromator.ss), 0, "Monochromator scattering sense"},
  {"sample_ss",              T_INT,    offsetof(tas,machine.ss_sample),        0, "Sample scattering sense"},
  {"analyzer_dspacing",      T_DOUBLE, offsetof(tas,machine.analyzer.dd),      0, "Analyzer d-spacing"},
  {"analyzer_ss",            T_INT,    offsetof(tas,machine.analyzer.ss),      0, "Analyzer scattering sense"},
  {"a",                      T_DOUBLE, offsetof(tas,cell.a),                   0, "Lattice parameter a"},
  {"b",                      T_DOUBLE, offsetof(tas,cell.b),                   0, "Lattice parameter b"},
  {"c",                      T_DOUBLE, offsetof(tas,cell.c),                   0, "Lattice parameter c"},
  {"alpha",                  T_DOUBLE, offsetof(tas,cell.alpha),               0, "Lattice parameter alpha"},
  {"beta",                   T_DOUBLE, offsetof(tas,cell.beta),                0, "Lattice parameter beta"},
  {"gamma",                  T_DOUBLE, offsetof(tas,cell.gamma),               0, "Lattice parameter gamma"},
  {"refl1_mono_two_theta",   T_DOUBLE, offsetof(tas,refl1.angles.monochromator_two_theta),0,"Monochromator two theta"},
  {"refl1_a3",               T_DOUBLE, offsetof(tas,refl1.angles.a3),                0,"Sample rotation"},
  {"refl1_sample_two_theta", T_DOUBLE, offsetof(tas,refl1.angles.sample_two_theta),  0,"Sample two theta"},
  {"refl1_sgl",              T_DOUBLE, offsetof(tas,refl1.angles.sgl),               0,"Goniometer lower tilt"},
  {"refl1_sgu",              T_DOUBLE, offsetof(tas,refl1.angles.sgu),               0,"Goniometer upper tilt"},
  {"refl1_anal_two_theta",   T_DOUBLE, offsetof(tas,refl1.angles.analyzer_two_theta),0,"Analyzer two theta"},
  {"refl1_ki",               T_DOUBLE, offsetof(tas,refl1.qe.ki),                    0,"Incident wavevector"},
  {"refl1_kf",               T_DOUBLE, offsetof(tas,refl1.qe.kf),                    0,"Outgoing wavevector"},
  {"refl1_qh",               T_DOUBLE, offsetof(tas,refl1.qe.qh),                    0,"Reciprocal space coordinate H"},
  {"refl1_qk",               T_DOUBLE, offsetof(tas,refl1.qe.qk),                    0,"Reciprocal space coordinate K"},
  {"refl1_ql",               T_DOUBLE, offsetof(tas,refl1.qe.ql),                    0,"Reciprocal space coordinate L"},
  {"refl1_q",                T_DOUBLE, offsetof(tas,refl1.qe.qm),                    0,"Momentum transfer"},  
  {"refl2_mono_two_theta",   T_DOUBLE, offsetof(tas,refl2.angles.monochromator_two_theta),0,"Monochromator two theta"},
  {"refl2_a3",               T_DOUBLE, offsetof(tas,refl2.angles.a3),                0,"Sample rotation"},
  {"refl2_sample_two_theta", T_DOUBLE, offsetof(tas,refl2.angles.sample_two_theta),  0,"Sample two theta"},
  {"refl2_sgl",              T_DOUBLE, offsetof(tas,refl2.angles.sgl),               0,"Goniometer lower tilt"},
  {"refl2_sgu",              T_DOUBLE, offsetof(tas,refl2.angles.sgu),               0,"Goniometer upper tilt"},
  {"refl2_anal_two_theta",   T_DOUBLE, offsetof(tas,refl2.angles.analyzer_two_theta),0,"Analyzer two theta"},
  {"refl2_ki",               T_DOUBLE, offsetof(tas,refl2.qe.ki),                    0,"Incident wavevector"},
  {"refl2_kf",               T_DOUBLE, offsetof(tas,refl2.qe.kf),                    0,"Outgoing wavevector"},
  {"refl2_qh",               T_DOUBLE, offsetof(tas,refl2.qe.qh),                    0,"Reciprocal space coordinate H"},
  {"refl2_qk",               T_DOUBLE, offsetof(tas,refl2.qe.qk),                    0,"Reciprocal space coordinate K"},
  {"refl2_ql",               T_DOUBLE, offsetof(tas,refl2.qe.ql),                    0,"Reciprocal space coordinate L"},
  {"refl2_q",                T_DOUBLE, offsetof(tas,refl2.qe.qm),                    0,"Momentum transfer"},  

  {NULL} /* Sentinal */
};

static PyMethodDef PyUB_methods[] = {
  {"dump", (PyCFunction)PyUB_print, METH_NOARGS, "print contents of tas structure"},
  {"calcub", (PyCFunction)PyUB_CalcUB, METH_KEYWORDS,"Calculate UB matrix from two reflections"},
  {"calcplanenormal", (PyCFunction)PyUB_CalcPlaneNormal, METH_KEYWORDS,"Calculate plane normal from two reflections"},
  {"calcangles", (PyCFunction)PyUB_CalcAngles, METH_KEYWORDS, "Calculate TAS angles from UB matrix and QE position"},
  {"calcHKL", (PyCFunction)PyUB_CalcHKL, METH_KEYWORDS, "Calculate HKL coordinates from UB matrix and TAS angles"},
  {"setReflection", (PyCFunction)PyUB_SetReflection, METH_KEYWORDS, "Load data for an orienting reflection"},
  {NULL} /* Sentinal */
};

static PyTypeObject PyUBType = {
  PyObject_HEAD_INIT(NULL)
  tp_name:      "PyUB",
  tp_basicsize: sizeof(tas),
  tp_dealloc:   (destructor) PyUB_dealloc,
  tp_flags:     Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
  tp_doc:       "$Id: PyUB.c,v 1.3 2006/04/11 13:14:04 nickm Exp $",
  tp_methods:   PyUB_methods,
  tp_members:   PyUB_members,
  tp_init:      (initproc) PyUB_init,
  tp_new:       PyUB_new,
};

static PyMethodDef module_methods[] = {
  {NULL} /* Sentinel */
};

PyMODINIT_FUNC initPyUB(void)
{
  PyObject * m;

  if (PyType_Ready(&PyUBType) < 0)
    return;

  m = Py_InitModule3("PyUB", 
		     module_methods,
		     "Example module that creates an extension type");

  if (m == NULL)
    return;

  Py_INCREF(&PyUBType);
  
  PyModule_AddObject(m, "PyUB", (PyObject *)&PyUBType);

}
