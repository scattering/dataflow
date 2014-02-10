/*
*-----------------------------------------------------------------------------
*	file:	matsolve.c
*	desc:	solve linear equations
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
#include <stdlib.h>
#endif

#include "matrix.h"

/*
*-----------------------------------------------------------------------------
*	funct:	mat_lu
*	desct:	in-place LU decomposition with partial pivoting
*	given:	!! A = square matrix (n x n) !ATTENTION! see commen
*		P = permutation vector (n x 1)
*	retrn:	number of permutation performed
*		-1 means suspected singular matrix
*	comen:	A will be overwritten to be a LU-composite matrix
*
*	note:	the LU decomposed may NOT be equal to the LU of
*		the orignal matrix a. But equal to the LU of the
*		rows interchanged matrix.
*-----------------------------------------------------------------------------
*/
int mat_lu( A, P )
MATRIX A;
MATRIX P;
{
	int	i, j, k, n;
	int	maxi, tmp;
	double	c, c1;
	int	p;

	n = MatCol(A);

	for (p=0,i=0; i<n; i++)
		{
		P[i][0] = i;
		}

	for (k=0; k<n; k++)
	{
	/*
	* --- partial pivoting ---
	*/
	for (i=k, maxi=k, c=0.0; i<n; i++)
		{
        c1 = fabs( A[(int)P[i][0]][k] );
		if (c1 > c)
			{
			c = c1;
			maxi = i;
			}
		}

	/*
	*	row exchange, update permutation vector
	*/
	if (k != maxi)
		{
		p++;
		tmp = P[k][0];
		P[k][0] = P[maxi][0];
		P[maxi][0] = tmp;
		}

	/*
	*	suspected singular matrix
	*/
    if ( A[(int)P[k][0]][k] == 0.0 )
		return (-1);

	for (i=k+1; i<n; i++)
		{
		/*
		* --- calculate m(i,j) ---
		*/
        A[(int)P[i][0]][k] = A[(int)P[i][0]][k] / A[(int)P[k][0]][k];

		/*
		* --- elimination ---
		*/
		for (j=k+1; j<n; j++)
			{
            A[(int)P[i][0]][j] -= A[(int)P[i][0]][k] * A[(int)P[k][0]][j];
			}
		}
	}

	return (p);
}

/*
*-----------------------------------------------------------------------------
*	funct:	mat_backsubs1
*	desct:	back substitution
*	given:	A = square matrix A (LU composite)
*		!! B = column matrix B (attention!, see comen)
*		!! X = place to put the result of X
*		P = Permutation vector (after calling mat_lu)
*		xcol = column of x to put the result
*	retrn:	column matrix X (of AX = B)
*	comen:	B will be overwritten
*-----------------------------------------------------------------------------
*/
MATRIX mat_backsubs1( A, B, X, P, xcol )
MATRIX A, B, X, P;
int xcol;
{
	int	i, j, k, n;
	double	sum;

	n = MatCol(A);

	for (k=0; k<n; k++)
		{
		for (i=k+1; i<n; i++)
            B[(int)P[i][0]][0] -= A[(int)P[i][0]][k] * B[(int)P[k][0]][0];
		}

    X[n-1][xcol] = B[(int)P[n-1][0]][0] / A[(int)P[n-1][0]][n-1];
	for (k=n-2; k>=0; k--)
		{
		sum = 0.0;
		for (j=k+1; j<n; j++)
			{
            sum += A[(int)P[k][0]][j] * X[j][xcol];
			}
        X[k][xcol] = (B[(int)P[k][0]][0] - sum) / A[(int)P[k][0]][k];
		}

	return (X);
}

/*
*-----------------------------------------------------------------------------
*	funct:	mat_lsolve
*	desct:	solve linear equations
*	given:	a = square matrix A
*		b = column matrix B
*	retrn:	column matrix X (of AX = B)
*-----------------------------------------------------------------------------
*/
MATRIX mat_lsolve( a, b )
MATRIX a, b;
{
	MATRIX	A, B, X, P;
	int	n;

	n = MatCol(a);
	A = mat_copy(a);
	B = mat_copy(b);
	X = mat_creat(n, 1, ZERO_MATRIX);
	P = mat_creat(n, 1, UNDEFINED);

	mat_lu( A, P );
	mat_backsubs1( A, B, X, P, 0 );

	mat_free(A);
	mat_free(B);
	mat_free(P);
	return (X);
}
