/**
 * This is a little collection of vector functions for use with the UB
 * calculation routines. Therefore vectors are mapped onto the matrix
 * package. Strictly speaking all routine only work properly on 3D
 * vectors.
 *
 * copyright: see file COPYRIGHT
 *
 * Mark Koennecke, March 2005
 */
#ifndef SICSVECTOR
#define SICSVECTOR
#include <stdio.h>
#include "matrix/matrix.h"

/**
 * make a 3D vector
 * @return a 3D vector expressed as a MATRIX. The caller is resonsible
 * for removing any memory associated with this vector.
 */
MATRIX makeVector();
/**
 * make a vector and initialize with values given in val
 * @param val Array of values for the new vector
 * @return a new vector with the values in val
 */
MATRIX makeVectorInit(double val[3]);
/**
 * copy the value in v to the array val
 * @param v The vector to copy
 * @param val The array to which to copy the values
 */
void vectorToArray(MATRIX v, double val[3]);
/**
 * delete the vector v
 * @param v The vector to delete.
 */
void killVector(MATRIX v);
/**
 * set a component of a vector
 * @param v The vector to which to apply the new value
 * @param idx The index of the vector component to set
 * @param val The new value for the component.
 */
void vectorSet(MATRIX v, int idx, double value);
/**
 * get the value of a vector component
 * @param v The vector to query
 * @param idx The index of the component
 * @return The value of the vectors component.
 */
double vectorGet(MATRIX v, int idx);
/**
 * calculate the length of the vector v
 * @param v The vector to calculate the length for
 * @return The length of the vector
 */
double vectorLength(MATRIX v);
/**
 * normalize the vector by making it unit length
 * @param v The vector to normalize.
 */
void normalizeVector(MATRIX v);
/**
 * calculate the dot or scalar product of two vectors
 * @param v1 First vector
 * @param v2 Second vector
 * @return The dot product v1*v2
 */
double vectorDotProduct(MATRIX v1, MATRIX v2);
/**
 * calculate the cross product of vectors v1 and v2. This is only
 * correct when both vectors are expressed in terms of a 
 * cartesian coordinate system.
 * @param v1 The first vector
 * @param v2 The second vector
 * @return The cross product of the vectors v1, v2
 */
MATRIX vectorCrossProduct(MATRIX v1, MATRIX v2);
/**
 * this is a special function used in UB matrix calculations. 
 * It first calculates a coordinate system from the two vectors
 * where:
 * a1  = v1/|v1|
 * a2 = v1*v2/|v1*v2|
 * a3 = a1*a2
 * and then constructs a matrix with the ai as columns. 
 * @param v1 The first vector
 * @param v2 The second vector
 * @return A matrix as descibed above.
 */
MATRIX matFromTwoVectors(MATRIX v1, MATRIX v2);
#endif
