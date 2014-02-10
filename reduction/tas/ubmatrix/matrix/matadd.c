/*
*-----------------------------------------------------------------------------
*	file:	matadd.c
*	desc:	matrix addition
*	by:	ko shu pui, patrick
*	date:	24 nov 91	v0.1
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
*	funct:	mat_add
*	desct:	addition of two matrice
*	given:	A, B = Compatible matrice to be added
*	retrn:	NULL if malloc() fails
*		else allocated matrix of A + B
*	comen:
*-----------------------------------------------------------------------------
*/
MATRIX mat_add( A, B )
MATRIX A, B;
{
	int	i, j;
	MATRIX	C;

	if ((C = mat_creat( MatRow(A), MatCol(A), UNDEFINED )) == NULL)
		return (NULL);

	for (i=0; i<MatRow(A); i++)
	for (j=0; j<MatCol(A); j++)
		{
		C[i][j] = A[i][j] + B[i][j];
		}
	return (C);
}

