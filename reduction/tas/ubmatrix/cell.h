/**
 * this is a little library for performing crystallographic cell transformations
 * for SICS. Some of the actual code was lifted from the Risoe program tascom.
 *
 * copyright: see file COPYRIGHT
 *
 * Mark Koennecke, March 2005
 */
#ifndef SICSCELL
#define SICSCELL
#include "matrix/matrix.h"

/**
 * error codes
 */
#define REC_NO_VOLUME -100
#define CELLNOMEMORY  -101
/**
 * lattice parameters: either reciprocal or direct
 */
  typedef struct {
    double a,b,c;
    double alpha, beta, gamma;
  }lattice, *plattice;
/**
 * defaultCell assigns defualt values to cell parameters
 * @param cell The lattice to assign default too
 */
void defaultCell(plattice cell);
/**
 * conversion from a direct lattice to the recipcrocal one.
 * @param direct The input direct cell parameters.
 * @param reciprocal The output reciprocal cell constants
 * @return 0 on success, > 0 else
 */ 
  int directToReciprocalLattice(lattice direct, plattice reciprocal);
/**
 * conversion from a reciprocal  lattice to the directone.
 * @param reciprocal  The input reciprocal  cell parameters.
 * @param direct The output direct  cell constants
 * @return 0 on success, > 0 else
 */ 
  int reciprocalToDirectLattice(lattice reciprocal, plattice direct);
/**
   * calculate a crystallographic B matrix from the cell constants
   * @param direct The direct cell lattice to calculate B from
   * @param B will be filled with the B matrix. MUST be 3x3
   * @return 1 on success, an negative error code else
   */
int calculateBMatrix(lattice direct, MATRIX B);
/**
 * calculate the cell constants from a UB matrix
 * @param UB The input UB matrix.
 * @param direct A pointer to a structure holding the new cell constants
 * @return 1 on success, an error c ode < 0 on failure
 */
int cellFromUB(MATRIX UB, plattice direct);
#endif
