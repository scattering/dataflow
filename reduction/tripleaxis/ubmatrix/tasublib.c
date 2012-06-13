/**
 * This is a library of functions and data structures for performing 
 * triple axis spectrometer angle calculations using the UB-matrix
 * formalism as described by Mark Lumsden, to appear in Acta Cryst.
 *
 * copyright: see file COPYRIGHT
 *
 * Mark Koennecke, April 2005
 */
#include <math.h>
#include <stdlib.h>
#include <assert.h>
#include "trigd.h"
#include "vector.h"
#include "tasublib.h"

#define ABS(x) (x < 0 ? -(x) : (x)) 
#define PI 3.141592653589793
#define ECONST 2.072
#define DEGREE_RAD      (PI/180.0)      /* Radians per degree */
#define VERT 0
#define HOR  1
/*============== monochromator/analyzer stuff =========================*/
double energyToK(double energy){
  double K;
  
  K = sqrt(energy/ECONST);
  return K;
}
/*---------------------------------------------------------------------*/
double KtoEnergy(double k){
  double energy;

  energy = ECONST*k*k;
  return energy;
}
/*-------------------------------------------------------------------*/
static double calcCurvature(double B1, double B2, double theta, 
			    int ori){
  assert(ori == VERT || ori == HOR);
  if(ori == VERT){
    return B1 + B2/Sind(ABS(theta));
  } else {
    return B1 + B2*Sind(ABS(theta));
  }
}
/*--------------------------------------------------------------------*/
int maCalcTwoTheta(maCrystal data, double k, double *two_theta){
  double fd, theta;

  /* fd = k/(2.*data.dd); */
  fd = PI/(data.dd*k);
  if(fd > 1.0) {
    return ENERGYTOBIG;
  }
  theta = Asind(fd)*data.ss;
  *two_theta = 2.*theta;
  return 1;
}
/*--------------------------------------------------------------------*/
double maCalcVerticalCurvature(maCrystal data, double two_theta){
  return calcCurvature(data.VB1,data.VB2, two_theta/2.,VERT);
}
/*-------------------------------------------------------------------*/
double maCalcHorizontalCurvature(maCrystal data, double two_theta){
  return calcCurvature(data.HB1,data.HB2, two_theta/2.,HOR);
}
/*--------------------------------------------------------------------*/
double maCalcK(maCrystal data, double two_theta){
  double k;
  k = ABS(data.dd * Sind(two_theta/2));
  if(ABS(k) > .001){
    k = PI / k;
  } else {
    k = .0;
  }
  return k;
}
/*==================== reciprocal space ==============================*/
static MATRIX tasReflectionToHC(tasQEPosition r, MATRIX B){
  MATRIX h = NULL, hc = NULL;

  h = makeVector();
  if(h == NULL){
    return NULL;
  }
  vectorSet(h,0,r.qh);
  vectorSet(h,1,r.qk);
  vectorSet(h,2,r.ql);

  hc = mat_mul(B,h);
  killVector(h);
  return hc;
}
/*------------------------------------------------------------------
 a quadrant dependent tangens
 ------------------------------------------------------------------*/
static double rtan(double y, double x){
  double val;

  if( (x == 0.) && (y == 0.) ) {
    return .0;
  }       
  if( x == 0.) {
      if(y < 0.){
         return -PI/2.;
      } else {
	return PI/2.;
     }
  }
  if(ABS(y) < ABS(x)) {
    val = atan(ABS(y/x));
    if(x < 0.) {
      val =  PI - val;
    }
    if(y < 0.){
        val = -val;
    } 
    return val;
  } else {
      val  = PI/2. - atan(ABS(x/y));
      if(x < 0.) {
      val = PI - val;
      }
      if( y < 0.) {
      val = - val;
      }
  }
  return val;
}
/*---------------------------------------------------------------*/
static double calcTheta(double ki, double kf, double two_theta){
  /**
   *               |ki| - |kf|cos(two_theta)
   * tan(theta) = --------------------------
   *                |kf|sin(two_theta)
   */
  return rtan(ABS(ki) - ABS(kf)*Cosd(two_theta),
	      ABS(kf)*Sind(two_theta))/DEGREE_RAD;
}
/*--------------------------------------------------------------------*/
static MATRIX uFromAngles(double om, double sgu, double sgl){
  MATRIX u;

  u = makeVector();
  if(u == NULL){
    return NULL;
  }
  vectorSet(u,0,-Cosd(sgl)*Cosd(om));
  vectorSet(u,1,Cosd(sgu)*Sind(om) - Sind(sgu)*Sind(sgl)*Cosd(om));
  vectorSet(u,2,-Sind(sgu)*Sind(om) - Cosd(sgu)*Sind(sgl)*Cosd(om));
  
  return u;	    
}
/*---------------------------------------------------------------*/
static MATRIX calcTasUVectorFromAngles(tasReflection r){
  double theta, om;

  theta = calcTheta(r.qe.ki,r.qe.kf,r.angles.sample_two_theta);
  om = r.angles.a3 - theta;
  return uFromAngles(om,r.angles.sgu, r.angles.sgl);
}
/*-------------------------------------------------------------------*/
MATRIX calcPlaneNormal(tasReflection r1, tasReflection r2){
  MATRIX u1 = NULL, u2 = NULL, planeNormal = NULL;
  int i;

  u1 = calcTasUVectorFromAngles(r1);
  u2 = calcTasUVectorFromAngles(r2);
  if(u1 != NULL && u2 != NULL){
    planeNormal = vectorCrossProduct(u1,u2);
    /*
      The plane normal has to point to the stars and not to the earth
      core in order for the algorithm to work.
    */
    if(planeNormal[2][0] < .0){
      for(i = 0; i < 3; i++){
	planeNormal[i][0] = -1.*planeNormal[i][0];
      }
    }
    return planeNormal;
  } else {
    return NULL;
  }
}
/*--------------------------------------------------------------------*/
MATRIX calcTasUBFromTwoReflections(lattice cell, tasReflection r1,
				   tasReflection r2, int *errorCode){
  MATRIX B, HT, UT, U, UB, HTT  ;
  MATRIX u1, u2, h1, h2, planeNormal;
  double ud[3];
  int status;

  *errorCode = 1;

  /*
    calculate the B matrix and the HT matrix
  */
  B = mat_creat(3,3,ZERO_MATRIX);
  status = calculateBMatrix(cell,B);
  if(status < 0){
    *errorCode = status;
    return NULL;
  }
  h1 = tasReflectionToHC(r1.qe,B);
  h2 = tasReflectionToHC(r2.qe,B);
  if(h1 == NULL || h2 == NULL){
    *errorCode = UBNOMEMORY;
    mat_free(B);
    return NULL;
  }
  HT = matFromTwoVectors(h1,h2);
  if(HT == NULL){
    *errorCode = UBNOMEMORY;
    mat_free(B);
    mat_free(h1);
    mat_free(h2);
    return NULL;
  }

  /*
    calculate U vectors and UT matrix
  */
  u1 = calcTasUVectorFromAngles(r1);
  u2 = calcTasUVectorFromAngles(r2);
  if(u1 == NULL || u2 == NULL){
    *errorCode = UBNOMEMORY;
    mat_free(B);
    mat_free(h1);
    mat_free(h2);
    return NULL;
  }
  UT = matFromTwoVectors(u1,u2);
  if(UT == NULL){
    *errorCode = UBNOMEMORY;
    mat_free(B);
    mat_free(h1);
    mat_free(h2);
    mat_free(u1);
    mat_free(u2);
    mat_free(HT);
    return NULL;
  }

  /*
    UT = U * HT
  */
  HTT = mat_tran(HT);
  if(HTT == NULL){
    *errorCode = UBNOMEMORY;
    mat_free(B);
    mat_free(h1);
    mat_free(h2);
    mat_free(u1);
    mat_free(u2);
    mat_free(HT);
    return NULL;
  }
  U = mat_mul(UT,HTT);
  if(U == NULL){
    *errorCode = UBNOMEMORY; 
    mat_free(B);
    mat_free(h1);
    mat_free(h2);
    mat_free(u1);
    mat_free(u2);
    mat_free(HT);
    mat_free(HTT);
    return NULL;
  }
  UB = mat_mul(U,B);
  if(UB == NULL){
    mat_free(B);
    mat_free(h1);
    mat_free(h2);
    mat_free(u1);
    mat_free(u2);
    mat_free(HT);
    mat_free(HTT);
    mat_free(U);
    *errorCode = UBNOMEMORY;
  }

  /*
    clean up
  */
  killVector(h1);
  killVector(h2);
  mat_free(HT);
  mat_free(HTT);

  killVector(u1);
  killVector(u2);
  mat_free(UT);  

  mat_free(U);
  mat_free(B);

  return UB;
}
/*-----------------------------------------------------------------------------*/
static MATRIX buildTVMatrix(MATRIX U1V, MATRIX U2V){
  MATRIX T, T3V;
  int i;

  normalizeVector(U2V);
  T3V = vectorCrossProduct(U1V,U2V);
  normalizeVector(T3V);
  if(T3V == NULL){
    return NULL;
  }
  T = mat_creat(3,3,ZERO_MATRIX);
  if(T == NULL){
    killVector(T3V);
    return NULL;
  }
  for(i = 0; i < 3; i++){
    T[i][0] = U1V[i][0];
    T[i][1] = U2V[i][0];
    T[i][2] = T3V[i][0];
  }
  killVector(T3V);
  return T;
}
/*-----------------------------------------------------------------------------*/
static MATRIX tasReflectionToQC(tasQEPosition r, MATRIX UB){
  MATRIX Q, QC;

  Q = makeVector();
  if(Q == NULL){
    return NULL;
  }
  vectorSet(Q,0,r.qh);
  vectorSet(Q,1,r.qk);
  vectorSet(Q,2,r.ql);
  QC = mat_mul(UB,Q);
  killVector(Q);
  return QC;
}
/*----------------------------------------------------------------------------*/
static MATRIX buildRMatrix(MATRIX UB, MATRIX planeNormal,
				     tasQEPosition qe, int *errorCode){
  MATRIX U1V, U2V, TV, TVINV, M;
  
  
  *errorCode = 1;
  U1V = tasReflectionToQC(qe,UB);
  if(U1V == NULL){
    *errorCode = UBNOMEMORY;
    return NULL;
  }
  normalizeVector(U1V);

  U2V = vectorCrossProduct(planeNormal,U1V);
  if(U2V == NULL){
    killVector(U1V);
    *errorCode = UBNOMEMORY;
    return NULL;
  }
  if(vectorLength(U2V) < .0001){
    *errorCode = BADUBORQ;
    killVector(U1V);
    killVector(U2V);
    return NULL;
  }

  TV = buildTVMatrix(U1V,U2V);
  if(TV == NULL){
    killVector(U1V);
    killVector(U2V);
    *errorCode = UBNOMEMORY;
    return NULL;
  }

  TVINV = mat_inv(TV);
  if(TVINV == NULL){
    *errorCode = BADUBORQ;
  }

  killVector(U1V);
  killVector(U2V);
  mat_free(TV);
  return TVINV;
}
/*-------------------------------------------------------------------------------*/
int calcTasQAngles(MATRIX UB, MATRIX planeNormal, int ss,  tasQEPosition qe, 
		   ptasAngles angles){
  MATRIX R, QC;
  double om, q, theta, cos2t;
  int errorCode = 1;

  R = buildRMatrix(UB, planeNormal, qe, &errorCode);
  if(R == NULL){
    return errorCode;
  }
  

  angles->sgl = Asind(-R[2][0]);
  if(ABS(angles->sgl -90.) < .5){
  	mat_free(R);
    return BADUBORQ;
  }
  /*
    Now, this is slightly different then in the publication by M. Lumsden.
    The reason is that the atan2 helps to determine the sign of om
    whereas the sin, cos formula given by M. Lumsden yield ambiguous signs 
    especially for om.
    sgu = atan(R[2][1],R[2][2]) where:
      R[2][1] = cos(sgl)sin(sgu)
      R[2][2] = cos(sgu)cos(sgl)
    om = atan(R[1][0],R[0][0]) where:
      R[1][0] = sin(om)cos(sgl)
      R[0][0] = cos(om)cos(sgl)
    The definitions of th R components are taken from M. Lumsden
    R-matrix definition.
  */

  om = Atan2d(R[1][0],R[0][0]);
  angles->sgu = Atan2d(R[2][1],R[2][2]);

  QC = tasReflectionToQC(qe,UB);
  if(QC == NULL){
  	mat_free(R);
    return UBNOMEMORY;
  }

  q = vectorLength(QC);
  q = 2.*PI*vectorLength(QC); 
  cos2t = (qe.ki*qe.ki + qe.kf*qe.kf - q*q)/(2. * ABS(qe.ki) * ABS(qe.kf));
  if(ABS(cos2t) > 1.){
  	mat_free(R);
  	killVector(QC);
    return TRIANGLENOTCLOSED;
  }
  angles->sample_two_theta = ss*Acosd(cos2t);
  
  theta = calcTheta(qe.ki, qe.kf,angles->sample_two_theta);
  
  angles->a3 = om + theta;
  /*
    put a3 into -180, 180 properly. We cal always turn by 180 because the
    scattering geometry is symmetric in this respect. It is like looking at
    the scattering plane from the other side
  */
  angles->a3 -= 180.;
  if(angles->a3 < -180.){
    angles->a3 += 360.;
  }

  killVector(QC);
  mat_free(R);

  return 1;
}
/*------------------------------------------------------------------------*/
int calcTasQH(MATRIX UB, tasAngles angles, ptasQEPosition qe){
  MATRIX UBINV = NULL, QV = NULL, Q = NULL;
  double q;
  tasReflection r;
  int i;

  UBINV = mat_inv(UB);
  r.angles = angles;
  r.qe = *qe;
  QV = calcTasUVectorFromAngles(r);
  if(UBINV == NULL || QV == NULL){
    return UBNOMEMORY;
  }
  /*
    normalize the QV vector to be the length of the Q vector
    Thereby take into account the physicists magic fudge
    2PI factor
  */
  q = sqrt(qe->ki*qe->ki + qe->kf*qe->kf - 
	   2.*qe->ki*qe->kf*Cosd(angles.sample_two_theta));
  qe->qm = q;
  q /= 2. * PI;

  for(i = 0; i < 3; i++){
    QV[i][0] *= q;
  }

  Q = mat_mul(UBINV,QV);
  if(Q == NULL){
    mat_free(UBINV);
    killVector(QV);
    return UBNOMEMORY;
  }
  qe->qh = Q[0][0];
  qe->qk = Q[1][0];
  qe->ql = Q[2][0];

  killVector(QV);
  killVector(Q);
  mat_free(UBINV);

  return 1;
}
/*---------------------------------------------------------------------*/
int calcAllTasAngles(ptasMachine machine, tasQEPosition qe,
		      ptasAngles angles){
  int status;
  tasReflection r;

  status = maCalcTwoTheta(machine->monochromator,qe.ki, 
			  &angles->monochromator_two_theta);
  if(status != 1){
    return status;
  }

  status = maCalcTwoTheta(machine->analyzer,qe.kf,&
			  angles->analyzer_two_theta);
  if(status != 1){
    return status;
  }

  status = calcTasQAngles(machine->UB, machine->planeNormal,
			  machine->ss_sample, qe,angles);
  if(status != 1){
    return status;
  }

  return 1;
}
/*----------------------------------------------------------------------*/
int calcTasQEPosition(ptasMachine machine, tasAngles angles,
		      ptasQEPosition qe){
  int status;

  qe->ki = maCalcK(machine->monochromator,angles.monochromator_two_theta);
  qe->kf = maCalcK(machine->analyzer,angles.analyzer_two_theta);

  status = calcTasQH(machine->UB,angles,qe);
  if(status != 1){
    return status;
  }
  return 1;
}
/*================== POWDER Implementation ===========================*/
int calcTasPowderAngles(ptasMachine machine, tasQEPosition qe,
			ptasAngles angles){
  double cos2t;
  int status;
  tasReflection r;

  status = maCalcTwoTheta(machine->monochromator,qe.ki, 
			  &angles->monochromator_two_theta);
  if(status != 1){
    return status;
  }

  cos2t = (qe.ki*qe.ki + qe.kf*qe.kf - qe.qm*qe.qm)/(2. * ABS(qe.ki) * ABS(qe.kf));
  if(cos2t > 1.){
    return TRIANGLENOTCLOSED;
  }
  angles->sample_two_theta = machine->ss_sample*Acosd(cos2t);
  

  status = maCalcTwoTheta(machine->analyzer,qe.kf,&
			  angles->analyzer_two_theta);
  if(status != 1){
    return status;
  }

  return 1;
}
/*---------------------------------------------------------------------*/
int calcTasPowderPosition(ptasMachine machine, tasAngles angles, 
			  ptasQEPosition qe){
  
  int status;

  qe->ki = maCalcK(machine->monochromator,angles.monochromator_two_theta);
  qe->kf = maCalcK(machine->analyzer,angles.analyzer_two_theta);

  qe->qm = sqrt(qe->ki*qe->ki + qe->kf*qe->kf - 
		2.*qe->ki*qe->kf*Cosd(angles.sample_two_theta));
  return 1;
}
/*====================== Logic implementation =========================*/
void setTasPar(ptasQEPosition qe, int tasMode, int tasVar, double value){
  double et;

  assert(tasMode == KICONST || tasMode == KFCONST || tasMode == ELASTIC);

  switch(tasVar){
  case KF:
  	if(tasMode == ELASTIC){
  		qe->kf = qe->ki;
  	} else {
	    qe->kf = value;
  	}
    break;
  case EF:
  	if(tasMode == ELASTIC){
  		qe->kf = qe->ki;
  	}else {
	    qe->kf = energyToK(value);
  	}
    break;
  case KI:
    qe->ki = value;
    if(tasMode == ELASTIC){
    	qe->kf = value;
    }
    break;
  case EI:
    qe->ki = energyToK(value);
    if(tasMode == ELASTIC){
    	qe->kf = qe->ki;
    }
    break;
  case QH:
    qe->qh = value;
    break;
  case QK:
    qe->qk = value;
    break;
  case QL:
    qe->ql = value;
    break;
  case EN:
    if(tasMode == KICONST){
      et = KtoEnergy(qe->ki) - value;
      qe->kf = energyToK(et);
    } else if(tasMode == KFCONST){
      et = KtoEnergy(qe->kf) + value;
      qe->ki = energyToK(et);
    }else if(tasMode == ELASTIC){
    	qe->kf = qe->ki;
    } else {
      assert(0);
    }
    break;
  case QM:
    qe->qm = value;
    break;
  default:
    assert(0);
    break;
  } 
}
/*-------------------------------------------------------------------------*/
double getTasPar(tasQEPosition qe, int tasVar){
  switch(tasVar){
  case EI:
    return KtoEnergy(qe.ki);
    break;
  case KI:
    return qe.ki;
    break;
  case EF:
    return KtoEnergy(qe.kf);
    break;
  case KF:
    return qe.kf;
    break;
  case QH:
    return qe.qh;
    break;
  case QK:
    return qe.qk;
    break;
  case QL:
    return qe.ql;
    break;
  case EN:
    return KtoEnergy(qe.ki) - KtoEnergy(qe.kf);
    break;
  case QM:
    return qe.qm;
    break;
  default:
    assert(0);
  }
}
