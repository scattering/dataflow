/*
*-----------------------------------------------------------------------------
*	file:	matdump.c
*	desc:	matrix mathematics - object dump
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
#include "matrix.h"

/*
*-----------------------------------------------------------------------------
*	funct:	mat_dump
*	desct:	dump a matrix
*	given:	A = matrice to dumped
*	retrn:	nothing
*	comen:	matrix a dumped to standard output
*-----------------------------------------------------------------------------
*/
MATRIX mat_dump( A )
MATRIX A;
{
    return(mat_fdumpf(A, "%f ", stdout));
}

/*
*-----------------------------------------------------------------------------
*	funct:	mat_dumpf
*   desct:  dump a matrix with format string to standard output
*	given:	A = matrice to dumped
*	retrn:	nothing
*	comen:	matrix a dumped to standard output
*-----------------------------------------------------------------------------
*/
MATRIX mat_dumpf( A, s )
MATRIX A;
char *s;
{
    return (mat_fdumpf(A, s, stdout));
}

MATRIX mat_fdump( A, fp )
MATRIX A;
FILE *fp;
{
    return (mat_fdumpf(A, "%f ", fp));
}

MATRIX mat_fdumpf( A, s, fp )
MATRIX A;
char *s;
FILE *fp;
{
	int	i, j;

	for (i=0; i<MatRow(A); i++)
		{
		for (j=0; j<MatCol(A); j++)
			{
            fprintf( fp, s, A[i][j] );
			}
        fprintf( fp, "\n" );
		}

	return (A);
}
