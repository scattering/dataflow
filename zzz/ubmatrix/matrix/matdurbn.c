/*
*-----------------------------------------------------------------------------
*	file:	matdurbn.c
*	desc:	Levinson-Durbin algorithm
*	by:	ko shu pui, patrick
*	date:
*	revi:	21 may 92 v0.3
*	ref:
*
*       [1] "Fundementals of Speech Signal Processing," Shuzo Saito,
*       Kazuo Nakata, Academic Press, New York, 1985.
*
*-----------------------------------------------------------------------------
*/

#include <stdio.h>

#include "matrix.h"

/*
*-----------------------------------------------------------------------------
*	funct:	mat_durbin
*	desct:	Levinson-Durbin algorithm
*
*		This function solve the linear eqns Ax = B:
*
*		|  v0   v1   v2  .. vn-1 | |  a1   |    |  v1   |
*		|  v1   v0   v1  .. vn-2 | |  a2   |    |  v2   |
*		|  v2   v1   v0  .. vn-3 | |  a3   |  = |  ..   |
*		|  ...                   | |  ..   |    |  ..   |
*		|  vn-1 vn-2 ..  .. v0   | |  an   |    |  vn   |
*
*		where A is a symmetric Toeplitz matrix and B
*		in the above format (related to A)
*
*	given:	R = autocorrelated matrix (v0, v1, ... vn) (dim (n+1) x 1)
*	retrn:	x (of Ax = B)
*-----------------------------------------------------------------------------
*/
MATRIX mat_durbin( R )
MATRIX R;
{
	int	i, i1, j, ji, p;
	MATRIX	W, E, K, A, X;

	p = MatRow(R) - 1;
	W = mat_creat( p+2, 1, UNDEFINED );
	E = mat_creat( p+2, 1, UNDEFINED );
	K = mat_creat( p+2, 1, UNDEFINED );
	A = mat_creat( p+2, p+2, UNDEFINED );

	W[0][0] = R[1][0];
	E[0][0] = R[0][0];

	for (i=1; i<=p; i++)
		{
		K[i][0] = W[i-1][0] / E[i-1][0];
		E[i][0] = E[i-1][0] * (1.0 - K[i][0] * K[i][0]);

		A[i][i] = -K[i][0];

		i1 = i-1;
		if (i1 >= 1)
			{
			for (j=1; j<=i1; j++)
				{
				ji = i - j;
				A[j][i] = A[j][i1] - K[i][0] * A[ji][i1];
				}
			}

		if (i != p)
			{
			W[i][0] = R[i+1][0];
			for (j=1; j<=i; j++)
				W[i][0] += A[j][i] * R[i-j+1][0];
			}
		}

	X = mat_creat( p, 1, UNDEFINED );
	for (i=0; i<p; i++)
		{
		X[i][0] = -A[i+1][p];
		}

	mat_free( A );
	mat_free( W );
	mat_free( K );
	mat_free( E );
	return (X);
}

/*
*-----------------------------------------------------------------------------
*	funct:	mat_lsolve_durbin
*	desct:	Solve simultaneous linear eqns using
*		Levinson-Durbin algorithm
*
*		This function solve the linear eqns Ax = B:
*
*		|  v0   v1   v2  .. vn-1 | |  a1   |    |  v1   |
*		|  v1   v0   v1  .. vn-2 | |  a2   |    |  v2   |
*		|  v2   v1   v0  .. vn-3 | |  a3   |  = |  ..   |
*		|  ...                   | |  ..   |    |  ..   |
*		|  vn-1 vn-2 ..  .. v0   | |  an   |    |  vn   |
*
*	domain:	where A is a symmetric Toeplitz matrix and B
*		in the above format (related to A)
*
*	given:	A, B
*	retrn:	x (of Ax = B)
*
*-----------------------------------------------------------------------------
*/
MATRIX mat_lsolve_durbin( A, B )
MATRIX A, B;
{
	MATRIX	R, X;
	int	i, n;

	n = MatRow(A);
	R = mat_creat(n+1, 1, UNDEFINED);
	for (i=0; i<n; i++)
		{
		R[i][0] = A[i][0];
		}
	R[n][0] = B[n-1][0];

	X = mat_durbin( R );
	mat_free( R );
	return (X);
}
