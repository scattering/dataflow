/*
*-----------------------------------------------------------------------------
*	file:	matcreat.c
*	desc:	matrix mathematics - object creation
*	by:	ko shu pui, patrick
*	date:	24 nov 91 v0.1
*	revi:	14 may 92 v0.2
*		21 may 92 v0.3
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

#ifdef	__TURBOC__
#include <alloc.h>
#else
#include <stdlib.h>
#endif

#include "matrix.h"

MATRIX	_mat_creat( row, col )
int row, col;
{
	MATBODY	*mat;
	int 	i;

	if ((mat = (MATBODY *)malloc( sizeof(MATHEAD) + sizeof(double *) * row)) == NULL)
		return (mat_error( MAT_MALLOC ));

	for (i=0; i<row; i++)
	{
	if ((*((double **)(&mat->matrix) + i) = (double *)malloc(sizeof(double) * col)) == NULL)
		return (mat_error( MAT_MALLOC ));
	}

	mat->head.row = row;
	mat->head.col = col;

	return (&(mat->matrix));
}

/*
*-----------------------------------------------------------------------------
*	funct:	mat_creat
*	desct:	create a matrix
*	given:  row, col = dimension, type = which kind of matrix
*	retrn:	allocated matrix (use mat_free() to free memory)
*-----------------------------------------------------------------------------
*/
MATRIX	mat_creat( row, col, type )
int row, col, type;
{
	MATRIX	A;

	if ((A =_mat_creat( row, col )) != NULL)
		{
		return (mat_fill(A, type));
		}
	else
		return (NULL);
}

/*
*-----------------------------------------------------------------------------
*	funct:	mat_fill
*	desct:	form a special matrix
*	given:  A = matrix, type = which kind of matrix
*	retrn:	A
*-----------------------------------------------------------------------------
*/
MATRIX mat_fill( A, type )
MATRIX A;
int type;
{
	int	i, j;

	switch (type)
		{
		case UNDEFINED:
			break;
		case ZERO_MATRIX:
		case UNIT_MATRIX:
			for (i=0; i<MatRow(A); i++)
			for (j=0; j<MatCol(A); j++)
				{
				if (type == UNIT_MATRIX)
					{
					if (i==j)
						{
						A[i][j] = 1.0;
						continue;
						}
					}
				A[i][j] = 0.0;
				}
			break;
		}
	return (A);
}


/*
*-----------------------------------------------------------------------------
*	funct:	mat_free
*	desct:	free an allocated matrix
*	given:  A = matrix
*	retrn:	nothing <actually 0 = NULL A passed, 1 = normal exit>
*-----------------------------------------------------------------------------
*/
int mat_free( A )
MATRIX A;
{
	int i;

	if (A == NULL)
		return (0);
	for (i=0; i<MatRow(A); i++)
		{
		free( A[i] );
		}
	free( Mathead(A) );
	return (1);
}

/*
*-----------------------------------------------------------------------------
*	funct:	mat_copy
*	desct:	duplicate a matrix
*	given:	A = matrice to duplicated
*	retrn:	C = A
*	comen:
*-----------------------------------------------------------------------------
*/
MATRIX mat_copy( A )
MATRIX A;
{
	int	i, j;
	MATRIX	C;

	if ((C = mat_creat( MatRow(A), MatCol(A), UNDEFINED )) == NULL)
		return (NULL);

	for (i=0; i<MatRow(A); i++)
	for (j=0; j<MatCol(A); j++)
		{
		C[i][j] = A[i][j];
		}
	return (C);
}


MATRIX mat_colcopy1( A, B, cola, colb )
MATRIX A, B;
int cola, colb;
{
	int	i, n;

	n = MatRow(A);
	for (i=0; i<n; i++)
		{
		A[i][cola] = B[i][colb];
		}
	return (A);
}

int fgetmat( A, fp )
MATRIX A;
FILE *fp;
{
	int 	i, j, k=0;

	for (i=0; i<MatRow(A); i++)
	for (j=0; j<MatCol(A); j++)
		{
/*
*	to avoid a bug in TC
*/
#ifdef	__TURBOC__
		{
		double	temp;
		k += fscanf( fp, "%lf", &temp );
		A[i][j] = temp;
		}
#else
		k += fscanf( fp, "%lf", &A[i][j] );
#endif

		}

	return (k);
}
