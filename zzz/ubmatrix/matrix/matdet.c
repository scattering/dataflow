/*
*-----------------------------------------------------------------------------
*	file:	matdet.c
*	desc:	determinant calculations
*	by:	ko shu pui, patrick
*	date:	21 may 92 v0.3
*	revi:
*	ref:
*       [1] Mary L.Boas, "Mathematical Methods in the Physical Sciene,"
*	John Wiley & Sons, 2nd Ed., 1983. Chap 3.
*
*-----------------------------------------------------------------------------
*/
#include <stdio.h>
#include "matrix.h"

static double signa[2] = {1.0, -1.0};

/*
*-----------------------------------------------------------------------------
*	funct:	mat_minor
*	desct:	find minor
*	given:	A = a square matrix,
*		i=row, j=col
*	retrn:	the minor of Aij
*-----------------------------------------------------------------------------
*/
double mat_minor( A, i, j )
MATRIX A;
int i, j;
{
	MATRIX	S;
	double	result;

	S = mat_submat(A, i, j);
	result = mat_det( S );
	mat_free(S);

	return (result);

}

/*
*-----------------------------------------------------------------------------
*	funct:	mat_cofact
*	desct:	find cofactor
*	given:	A = a square matrix,
*		i=row, j=col
*	retrn:	the cofactor of Aij
*-----------------------------------------------------------------------------
*/
double mat_cofact( A, i, j )
MATRIX A;
int i, j;
{
	double	result;

	result = signa[(i+j)%2] * A[i][j] * mat_minor(A, i, j);

	return (result);
}

/*
*-----------------------------------------------------------------------------
*	funct:	mat_det
*	desct:	find determinant
*	given:	A = matrix
*	retrn:	the determinant of A
*	comen:
*-----------------------------------------------------------------------------
*/
double mat_det( a )
MATRIX a;
{
	MATRIX	A, P;
	int	i, j, n;
	double	result;

	n = MatRow(a);
	A = mat_copy(a);
	P = mat_creat(n, 1, UNDEFINED);

	/*
	* take a LUP-decomposition
	*/
	i = mat_lu(A, P);
	switch (i)
		{
		/*
		* case for singular matrix
		*/
		case -1:
		result = 0.0;
		break;

		/*
		* normal case: |A| = |L||U||P|
		* |L| = 1,
		* |U| = multiplication of the diagonal
		* |P| = +-1
		*/
		default:
		result = 1.0;
		for (j=0; j<MatRow(A); j++)
			{
            result *= A[(int)P[j][0]][j];
			}
		result *= signa[i%2];
		break;
		}

	mat_free(A);
	mat_free(P);
	return (result);
}
