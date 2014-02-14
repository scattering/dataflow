/*
*-----------------------------------------------------------------------------
*	file:	matsubx.c
*	desc:	find submatrix
*	by:	ko shu pui, patrick
*	date:	24 may 92 v0.4
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
*	funct:	mat_submat
*	desct:	return a submatrix S of A
*	given:	A = main matrix,
*		i,j = row and column of A to be deleted to obtained S
*	retrn:	S
*-----------------------------------------------------------------------------
*/
MATRIX mat_submat( A, i, j )
MATRIX A;
int i,j;
{
	int	m, m1, p, p1;
	MATRIX	S;

	S = mat_creat(MatRow(A)-1, MatCol(A)-1, UNDEFINED);

	for (m=m1=0; m<MatRow(A); m++)
		{
		if (m==i) continue;
		for (p=p1=0; p<MatCol(A); p++)
			{
			if (p==j) continue;
			S[m1][p1] = A[m][p];
			p1++;
			}
		m1++;
		}

	return (S);
}
