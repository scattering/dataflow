/*
*-----------------------------------------------------------------------------
*	file:	mattoepz.c
*	desc:	matrix mathematics - toeplitz matrix
*	by:	ko shu pui, patrick
*	date:	26 nov 91 v0.1
*	revi:	14 may 92 v0.2
*	ref:
*       [1] Mary L.Boas, "Mathematical Methods in the Physical Sciene,"
*	John Wiley & Sons, 2nd Ed., 1983. Chap 3.
*
*-----------------------------------------------------------------------------
*/

#include <stdio.h>

#include "matrix.h"

/*
*-----------------------------------------------------------------------------
*	funct:	mat_SymToeplz
*	desct:	create a n x n symmetric Toeplitz matrix from
*		a n x 1 correlation matrix
*	given:	R = correlation matrix (n x 1)
*	retrn:	the symmetric Toeplitz matrix
*-----------------------------------------------------------------------------
*/
MATRIX mat_SymToeplz( R )
MATRIX R;
{
	int	i, j, n;
	MATRIX	T;

	n = MatRow(R);
	T = mat_creat(n, n, UNDEFINED);

	for (i=0; i<n; i++)
	for (j=0; j<n; j++)
		{
		T[i][j] = R[abs(i-j)][0];
		}
	return (T);
}
