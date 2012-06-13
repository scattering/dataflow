
/*----------------------------------------------------------------------
 SICS interface to the triple axis spectrometer calculation 
 module.

 copyright: see file COPYRIGHT
 
 Mark Koennecke, April-May 2005
----------------------------------------------------------------------*/
#ifndef TASUB
#define TASUB
#include <stdio.h>
#include "tasublib.h"
#include "cell.h"
#include "motor.h"

/*------------------- defines for tasMode -----------------------------------*/
        typedef struct{
                pObjectDescriptor pDes;
                tasMachine machine;
                int reflectionList;
                lattice cell;
                tasQEPosition target;
                tasQEPosition current;
                int tasMode;
                double targetEn, actualEn;
                int mustRecalculate;
                int mustDrive; 
                pMotor motors[12];
                tasReflection r1, r2;
	        int ubValid;
}tasUB, *ptasUB;


/*--------------------- the tas virtual motor data structure ---------------------*/
typedef struct {
        pObjectDescriptor pDes;
        pIDrivable pDriv;
        ptasUB math;
        int code;       
        }tasMot, *ptasMot;

/*--------------------------------------------------------------------*/

int TasUBFactory(SConnection *pCon,SicsInterp *pSics, void *pData,                
                int argc, char *argv[]);
int TasUBWrapper(SConnection *pCon,SicsInterp *pSics, void *pData,                
                int argc, char *argv[]);


int findReflection(int list, int idx, ptasReflection r);
#endif 
