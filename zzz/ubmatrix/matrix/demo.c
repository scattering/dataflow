/*
*-----------------------------------------------------------------------------
*	file:	demo.c
*	desc:	demostrate how to use Patrick's matrix toolbox
*	by:	ko shu pui, patrick
*	date:	24 nov 91 v0.1
*	revi:	14 may 92 v0.2
*		24 may 92 v0.4
*	ref:
*       [1] Mary L.Boas, "Mathematical Methods in the Physical Sciene,"
*	John Wiley & Sons, 2nd Ed., 1983. Chap 3.
*
*	[2] Kendall E.Atkinson, "An Introduction to Numberical Analysis,"
*	John Wiley & Sons, 1978.
*
*	[3] Alfred V.Aho, John E.Hopcroft, Jeffrey D.Ullman, "The Design
*	and Analysis of Computer Algorithms," 1974.
*
*-----------------------------------------------------------------------------
*/
#include <stdio.h>
#include <time.h>
#include "matrix.h"

int main()
{
	MATRIX	A, B, X, M;
	FILE	*fp;
	double	result;
	time_t	t1, t2;
	int	tinv, tdet, tmul;

	A = mat_creat( 10, 10, UNDEFINED );
	B = mat_creat( 10, 1, UNDEFINED );

	if ((fp = fopen( "demo.dat", "r" )) == NULL)
		{
		fprintf( stderr, "file cannot be opened\n" );
		exit (0);
		}

	fgetmat( A, fp );
	printf( "|- Matrix A -|\n");
	mat_dumpf( A, "%+06.1f " );

	t1 = time(&t1);
	result = mat_det(A);
	t2 = time(&t2);
	tdet = t2 - t1;
	printf( "\n\nDet(A) = %f\n", result );

	printf( "|- Inv A -|\n");
	t1 = time(&t1);
	X = mat_inv( A );
	t2 = time(&t2);
	tinv = t2 - t1;

	if (X == NULL)
		printf( "A is a singular matrix\n" );
	else
	{
		mat_dumpf(X, "%+06.1f ");

		printf( "|- A x Inv A -|\n");
		t1 = time(&t1);
		M = mat_mul( X, A );
		t2 = time(&t2);
		tmul = t2 - t1;
		mat_dumpf( M, "%+06.1f " );

		mat_free(M);
		mat_free(X);
	}

	fgetmat( B, fp );
	printf( "|- Matrix B -|\n");
	mat_dumpf( B, "%+06.1f " );

	printf( "|- A x B -|\n");
	mat_free(mat_dumpf(mat_mul(A, B), "%+06.1f "));

	printf( "time for finding 10 x 10 matrix inversion is less than %d secs\n", tinv );
	printf( "time for finding 10 x 10 matrix determinant is less than %d secs\n", tdet );
	printf( "time for finding 10 x 10 matrix multiplication is less than %d secs\n", tmul );

	mat_free( A );
	mat_free( B );

	fclose(fp);

}
