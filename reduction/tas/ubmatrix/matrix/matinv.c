/*
*-----------------------------------------------------------------------------
*	file:	matinv.c
*	desc:	matrix inversion
*	by:	ko shu pui, patrick
*	date:	24 nov 91 v0.1
*	revi:	14 may 92 v0.2
*	ref:
*       [1] Mary L.Boas, "Mathematical Methods in the Physical Sciene,"
*	John Wiley & Sons, 2nd Ed., 1983. Chap 3.
*
*	[2] Kendall E.Atkinson, "An Introduction to Numberical Analysis,"
*	John Wiley & Sons, 1978.
*
*-----------------------------------------------------------------------------
*/
#include <stdio.h>
#include <math.h>

#ifdef	__TURBOC__
#include <alloc.h>
#else
#include <malloc.h>
#endif

#include "matrix.h"


/*
*-----------------------------------------------------------------------------
*	funct:	mat_inv
*	desct:	find inverse of a matrix
*	given:	a = square matrix a
*	retrn:	square matrix Inverse(A)
*		NULL = fails, singular matrix, or malloc() fails
*-----------------------------------------------------------------------------
*/
MATRIX mat_inv( a )
MATRIX a;
{
	MATRIX	A, B, C, P;
	int	i, j, n;
	double	temp;

	n = MatCol(a);
	A = mat_copy(a);
	B = mat_creat( n, 1, UNDEFINED );
	C = mat_creat( n, n, UNDEFINED );
	P = mat_creat( n, 1, UNDEFINED );

	/*
	*	- LU-decomposition -
	*	also check for singular matrix
	*/
	if (mat_lu(A, P) == -1)
		{
		mat_free(A);
		mat_free(B);
		mat_free(C);
		mat_free(P);

		return (NULL);
		}

	for (i=0; i<n; i++)
		{
		mat_fill(B, ZERO_MATRIX);
		B[i][0] = 1.0;
		mat_backsubs1( A, B, C, P, i );
		}

	mat_free(A);
	mat_free(B);
	mat_free(P);
	return (C);
}
