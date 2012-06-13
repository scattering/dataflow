/*
*-----------------------------------------------------------------------------
*	file:	matmul.c
*	desc:	matrix multiplication
*	by:	ko shu pui, patrick
*	date:	24 nov 91 v0.1
*	revi:
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
*	funct:	mat_mul
*	desct:	multiplication of two matrice
*	given:	A, B = compatible matrice to be multiplied
*	retrn:	NULL if malloc() fails
*		else allocated matrix of A * B
*	comen:
*-----------------------------------------------------------------------------
*/
MATRIX mat_mul( A, B )
MATRIX A, B;
{
	int	i, j, k;
	MATRIX	C;

	if ((C = mat_creat( MatRow(A), MatCol(B), UNDEFINED )) == NULL)
		return (NULL);

	for (i=0; i<MatRow(A); i++)
	for (j=0; j<MatCol(B); j++)
	for (k=0, C[i][j]=0.0; k<MatCol(A); k++)
		{
		C[i][j] += A[i][k] * B[k][j];
		}
	return (C);
}

double mat_diagmul( A )
MATRIX A;
{
	int i;
	double result = 1.0;

	for (i=0; i<MatRow(A); i++)
		{
		result *= A[i][i];
		}
	return (result);
}
