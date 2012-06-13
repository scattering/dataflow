/**
 * this is a little library for performing crystallographic cell transformations
 * for SICS. Some of the actual code was lifted from the Risoe program tascom.
 *
 * copyright: see file COPYRIGHT
 *
 * Mark Koennecke, March 2005
 */
#include <stdio.h>
#include <assert.h>
#include <math.h>
#include "trigd.h"
#include "cell.h"

/* define constants */
#ifndef PI
#define PI              (3.1415926536)  /* pi */
#endif
#define TWOPI           (2*PI)          /* 2*pi */
/*****************************************************************************
 * default value for a cell
 ****************************************************************************/
void defaultCell(plattice cell){
  cell->a = 1.;
  cell->b = 1.;
  cell->c = 1.;
  cell->alpha = 90.;
  cell->beta = 90.;
  cell->gamma = 90.;
}
/*******************************************************************************
* Transform direct lattice to reciprocal lattice.
*******************************************************************************/
int directToReciprocalLattice(lattice direct, plattice reciprocal)
{
  double alfa, beta, gamma;
  double cos_alfa, cos_beta, cos_gamma;
  double sin_alfa, sin_beta, sin_gamma;
  double ad, bd, cd;
  double arg, vol;

  alfa = direct.alpha;
  beta = direct.beta;
  gamma = direct.gamma;

  cos_alfa = Cosd (alfa);
  cos_beta = Cosd (beta);
  cos_gamma = Cosd (gamma);

  sin_alfa = Sind (alfa);
  sin_beta = Sind (beta);
  sin_gamma = Sind (gamma);

  reciprocal->alpha = Acosd ((cos_beta*cos_gamma - cos_alfa)/sin_beta/sin_gamma);
  reciprocal->beta =Acosd ((cos_alfa*cos_gamma - cos_beta)/sin_alfa/sin_gamma);
  reciprocal->gamma = Acosd ((cos_alfa*cos_beta - cos_gamma)/sin_alfa/sin_beta);

  ad = direct.a;
  bd = direct.b;
  cd = direct.c;

  arg = 1 + 2*cos_alfa*cos_beta*cos_gamma - cos_alfa*cos_alfa -
					    cos_beta*cos_beta -
					    cos_gamma*cos_gamma;
  if (arg < 0.0)
    {
      return REC_NO_VOLUME;
    }

  vol = ad*bd*cd*sqrt (arg);
  reciprocal->a = bd*cd*sin_alfa/vol;
  reciprocal->b = ad*cd*sin_beta/vol;
  reciprocal->c = bd*ad*sin_gamma/vol;

  return (0);
}
/*******************************************************************************
* Transform reciprocal lattice to direct lattice.
*******************************************************************************/
int reciprocalToDirectLattice(lattice reciprocal, plattice direct)
{
  double alfa, beta, gamma;
  double cos_alfa, cos_beta, cos_gamma;
  double sin_alfa, sin_beta, sin_gamma;
  double ar, br, cr;
  double arg, vol;

  alfa = reciprocal.alpha;
  beta = reciprocal.beta;
  gamma = reciprocal.gamma;

  cos_alfa = Cosd (alfa);
  cos_beta = Cosd (beta);
  cos_gamma = Cosd (gamma);

  sin_alfa = Sind (alfa);
  sin_beta = Sind (beta);
  sin_gamma = Sind (gamma);

  direct->alpha = Acosd ((cos_beta*cos_gamma - cos_alfa)/sin_beta/sin_gamma);
  direct->beta = Acosd ((cos_alfa*cos_gamma - cos_beta)/sin_alfa/sin_gamma);
  direct->gamma =  Acosd ((cos_alfa*cos_beta - cos_gamma)/sin_alfa/sin_beta);

  ar = reciprocal.a;
  br = reciprocal.b;
  cr = reciprocal.c;

  arg = 1 + 2*cos_alfa*cos_beta*cos_gamma - cos_alfa*cos_alfa -
					    cos_beta*cos_beta -
					    cos_gamma*cos_gamma;
  if (arg < 0.0)
    {
      return REC_NO_VOLUME;
    }

  vol = ar*br*cr*sqrt (arg);
  direct->a = br*cr*sin_alfa/vol;
  direct->b = ar*cr*sin_beta/vol;
  direct->c = br*ar*sin_gamma/vol;

  return (0);
}
/***************************************************************************************
 * Build a B matrix
 ***************************************************************************************/
int calculateBMatrix(lattice direct, MATRIX B) {
  lattice reciprocal;
  int status;

  assert(MatRow(B) == 3);
  assert(MatCol(B) == 3);

  status = directToReciprocalLattice(direct,&reciprocal);
  if(status < 0) {
    return status;
  }
  
  mat_fill(B,ZERO_MATRIX);
  
  /*
    top row
  */
  B[0][0] = reciprocal.a;
  B[0][1] = reciprocal.b*Cosd(reciprocal.gamma);
  B[0][2] = reciprocal.c*Cosd(reciprocal.beta);

  /*
    middle row
  */
  B[1][1] = reciprocal.b*Sind(reciprocal.gamma);
  B[1][2] = -reciprocal.c*Sind(reciprocal.beta)*Cosd(direct.alpha);
  
  /*
    bottom row
  */
  B[2][2] = 1./direct.c;
  
  return 1;
}
/*--------------------------------------------------------------------------*/
int cellFromUB(MATRIX UB, plattice direct){
  MATRIX UBTRANS, GINV, G;

  UBTRANS = mat_tran(UB);
  if(UBTRANS == NULL){
    return CELLNOMEMORY;
  }
  GINV = mat_mul(UBTRANS,UB);
  if(GINV == NULL){
    mat_free(UBTRANS);
    return CELLNOMEMORY;
  }
  G = mat_inv(GINV);
  if(G == NULL){
    mat_free(UBTRANS);
    mat_free(GINV);
    return CELLNOMEMORY;
  }
  direct->a = sqrt(G[0][0]);
  direct->b = sqrt(G[1][1]);
  direct->c = sqrt(G[2][2]);
  direct->alpha = Acosd(G[1][2]/(direct->b * direct->c));
  direct->beta = Acosd(G[2][0]/(direct->a * direct->c));
  direct->gamma = Acosd(G[0][1]/(direct->a * direct->c));
  return 1;
}

