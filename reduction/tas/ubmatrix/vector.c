/**
 * This is a little collection of vector functions for use with the UB
 * calculation routines. Therefore vectors are mapped onto the matrix
 * package. Strictly speaking all routines only work properly on 3D
 * vectors.
 *
 * copyright: see file COPYRIGHT
 *
 * Mark Koennecke, March 2005
 */
#include <stdlib.h>
#include <assert.h>
#include <math.h>
#include "vector.h"
/*----------------------------------------------------------------------*/
MATRIX makeVector(){
  return mat_creat(3,1,ZERO_MATRIX);
}
/*---------------------------------------------------------------------*/
MATRIX makeVectorInit(double val[3]){
  int i;
  MATRIX result = NULL;

  result = makeVector();
  if(result == NULL){
    return result;
  }
  for(i = 0; i < 3; i++){
    result[i][0] = val[i];
  } 
  return result;
}
/*---------------------------------------------------------------------*/
void vectorToArray(MATRIX v, double val[3]){
  int i;

  assert(MatCol(v) == 3);
  for(i = 0; i < 3; i++){
    val[i] = v[i][0];
  }
}
/*----------------------------------------------------------------------*/
void killVector(MATRIX v){
  mat_free(v);
}
/*----------------------------------------------------------------------*/
void vectorSet(MATRIX v, int idx, double value){
  assert(idx >= 0 && idx < 3);

  v[idx][0] = value;
}
/*----------------------------------------------------------------------*/
double vectorGet(MATRIX v, int idx){
  assert(idx >= 0 && idx < 3);

  return v[idx][0];
}
/*----------------------------------------------------------------------*/
double vectorLength(MATRIX v){
  assert(MatRow(v) == 3);

  return sqrt(v[0][0]*v[0][0] + v[1][0]*v[1][0] + v[2][0]*v[2][0]);
}
/*---------------------------------------------------------------------*/
void normalizeVector(MATRIX v){
  int i;
  double norm;

  norm = vectorLength(v);
  if(norm > .001) {
    for(i = 0; i < 3; i++){
      v[i][0] /= norm;
    }
  } else {
    for(i = 0; i < 3; i++){
      v[i][0] = .0;
    }
  }
}
/*----------------------------------------------------------------------*/
double vectorDotProduct(MATRIX v1, MATRIX v2){
  double sum;
  int i;

  assert(MatRow(v1) == MatRow(v2));

  sum = .0;
  for(i = 0; i < MatRow(v1); i++){
    sum += v1[i][0]*v2[i][0];
  }
  return sum;
}
/*----------------------------------------------------------------------*/
MATRIX vectorCrossProduct(MATRIX v1, MATRIX v2){
  MATRIX result;

  assert(MatRow(v1) == 3);
  assert(MatRow(v2) == 3);

  result = makeVector();
  if(result == NULL){
    return NULL;
  }
  vectorSet(result,0,vectorGet(v1,1)*vectorGet(v2,2) - vectorGet(v1,2)*vectorGet(v2,1));
  vectorSet(result,1,vectorGet(v1,2)*vectorGet(v2,0) - vectorGet(v1,0)*vectorGet(v2,2));
  vectorSet(result,2,vectorGet(v1,0)*vectorGet(v2,1) - vectorGet(v1,1)*vectorGet(v2,0));
  return result;
}
/*-------------------------------------------------------------------------*/
MATRIX matFromTwoVectors(MATRIX v1, MATRIX v2){
  MATRIX a1, a2, a3, result;
  int i;

  a1 = mat_copy(v1);
  if(a1 == NULL){
    return NULL;
  }
  normalizeVector(a1);

  a3 = vectorCrossProduct(v1,v2);
  if(a3 == NULL){
    return NULL;
  }
  normalizeVector(a3);

  a2 = vectorCrossProduct(a1,a3);
  if(a2 == NULL){
    return NULL;
  }

  result = mat_creat(3,3,ZERO_MATRIX);
  if(result == NULL){
    return NULL;
  }

  for(i = 0; i < 3; i++){
    result[i][0] = vectorGet(a1,i);
    result[i][1] = vectorGet(a2,i);
    result[i][2] = vectorGet(a3,i);
  }
  killVector(a1);
  killVector(a2);
  killVector(a3);
  return result;
}
