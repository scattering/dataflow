/*
*-----------------------------------------------------------------------------
*	file:	materr.c
*	desc:	matrix error handler
*	by:	ko shu pui, patrick
*	date:	24 nov 91 v0.1
*	revi:
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

/* caused problems with build in WINDOWS WR
#ifdef	__TURBOC__
#include <alloc.h>
#else
#include <malloc.h>
#endif
*/

#include "matrix.h"

MATRIX mat_error( errno )
int errno;
{
	switch( errno )
		{
		case MAT_MALLOC:
			fprintf(stderr, "mat: malloc error\n" );
			break;
		case MAT_FNOTOPEN:
			fprintf(stderr, "mat: fileopen error\n" );
			break;
		case MAT_FNOTGETMAT:
			fprintf(stderr, "fgetmat: matrix read error\n");
			break;
		}

	return (NULL);
}
