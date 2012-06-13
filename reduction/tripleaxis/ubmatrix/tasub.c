/*----------------------------------------------------------------------
 SICS interface to the triple axis spectrometer calculation 
 module.

 copyright: see file COPYRIGHT
 
 Mark Koennecke, April-May 2005
----------------------------------------------------------------------*/
#include <assert.h>
#include "sics.h"
#include "lld.h"
#include "tasub.h"
#include "tasdrive.h"
/*------------------- motor indexes in motor data structure ---------*/
#define A1   0
#define A2   1
#define MCV  2
#define MCH  3
#define A3   4
#define A4   5
#define SGU  6
#define SGL  7
#define A5   8
#define A6   9
#define ACV 10
#define ACH 11
/*----------------- data structure management code -------------------*/
static void saveCrystal(char *objName, char *name, pmaCrystal crystal,
			FILE *fd){
  fprintf(fd,"%s %s dd %f\n",objName, name, crystal->dd);
  fprintf(fd,"%s %s hb1 %f\n",objName, name, crystal->HB1);
  fprintf(fd,"%s %s hb2 %f\n",objName, name, crystal->HB2);
  fprintf(fd,"%s %s vb1 %f\n",objName, name, crystal->VB1);
  fprintf(fd,"%s %s vb2 %f\n",objName, name, crystal->VB2);
  fprintf(fd,"%s %s ss %d\n",objName, name, crystal->ss);
}
/*------------------------------------------------------------------*/
static void saveReflections(ptasUB self, char *name, FILE *fd){
  tasReflection r;
  int status;

  status = LLDnodePtr2First(self->reflectionList);
  fprintf(fd,"%s clear\n",name);
  while(status == 1){
    LLDnodeDataTo(self->reflectionList,&r);
    fprintf(fd,"%s addref %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f\n",
	     name, r.qe.qh, r.qe.qk, r.qe.ql, r.angles.a3, r.angles.sample_two_theta, 
	    r.angles.sgu, r.angles.sgl, 
	    KtoEnergy(r.qe.ki), KtoEnergy(r.qe.kf));
    status = LLDnodePtr2Next(self->reflectionList);
  }
}
/*-------------------------------------------------------------------*/
static int tasUBSave(void *pData, char *name, FILE *fd){
  ptasUB self = (ptasUB)pData;
  tasReflection r;

  if(self == NULL){
    return 0;
  }
  fprintf(fd,"#---- tasUB module %s\n", name);
  saveCrystal(name,"mono",&self->machine.monochromator,fd);
  saveCrystal(name,"ana",&self->machine.analyzer,fd);
  fprintf(fd,"%s cell %f %f %f %f %f %f\n", name, self->cell.a,
	  self->cell.b, self->cell.c, self->cell.alpha,
	  self->cell.beta, self->cell.gamma);
  saveReflections(self,name,fd);
  if(self->tasMode == KICONST){
     fprintf(fd,"%s const  ki\n",name);
  }else if(self->tasMode == ELASTIC){
  	fprintf(fd,"%s const elastic\n",name);
  } else {
    fprintf(fd,"%s const  kf\n",name);
  }
  fprintf(fd,"%s ss %d\n", name,self->machine.ss_sample);
  fprintf(fd," %s setub %f %f %f  %f %f %f  %f %f %f\n",
	  name,
	  self->machine.UB[0][0], self->machine.UB[0][1], self->machine.UB[0][2],
	  self->machine.UB[1][0], self->machine.UB[1][1], self->machine.UB[1][2],
	  self->machine.UB[2][0], self->machine.UB[2][1], self->machine.UB[2][2]);
  fprintf(fd," %s setnormal %f %f %f\n",
	  name,
	  self->machine.planeNormal[0][0], self->machine.planeNormal[1][0], 
	  self->machine.planeNormal[2][0]);
  fprintf(fd,"%s settarget %f %f %f %f  %f %f\n",
	  name,
	  self->target.qh, self->target.qk, self->target.ql, self->target.qm, 
	  self->target.ki, self->target.kf);
  r = self->r1;
  fprintf(fd,"%s r1 %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f\n",
	     name, r.qe.qh, r.qe.qk, r.qe.ql, r.angles.a3, r.angles.sample_two_theta, 
	    r.angles.sgu, r.angles.sgl, 
	    KtoEnergy(r.qe.ki), KtoEnergy(r.qe.kf));
  r = self->r2;
  fprintf(fd,"%s r2 %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f\n",
	     name, r.qe.qh, r.qe.qk, r.qe.ql, r.angles.a3, r.angles.sample_two_theta, 
	    r.angles.sgu, r.angles.sgl, 
	    KtoEnergy(r.qe.ki), KtoEnergy(r.qe.kf));
  fprintf(fd,"%s update\n", name);
  return 1;
}
/*------------------------------------------------------------------*/
static void defaultMonochromator(pmaCrystal mono){
  mono->dd = 3.35;
  mono->ss = 1;
  mono->HB1 = 1.;
  mono->HB2 = 1.;
  mono->VB1 = 1.;
  mono->VB2 = 1.;
}
/*--------------------------------------------------------------------*/
static ptasUB MakeTasUB(){
  ptasUB pNew = NULL;

  pNew = (ptasUB)malloc(sizeof(tasUB));
  if(pNew == NULL){
    return NULL;
  }
  memset(pNew,0,sizeof(tasUB));
  
  pNew->pDes = CreateDescriptor("TAS-UB");
  pNew->machine.UB = mat_creat(3,3,UNIT_MATRIX);
  pNew->machine.planeNormal = mat_creat(3,1,ZERO_MATRIX);
  pNew->reflectionList = LLDcreate(sizeof(tasReflection));
  if(!pNew->pDes || !pNew->machine.UB || pNew->reflectionList < 0 ||
     pNew->machine.planeNormal == NULL){
    free(pNew);
    return NULL;
  }
  
  pNew->pDes->SaveStatus = tasUBSave;
  pNew->machine.ss_sample = 1;
  defaultMonochromator(&pNew->machine.monochromator);
  defaultMonochromator(&pNew->machine.analyzer);
  defaultCell(&pNew->cell);
  pNew->tasMode = KICONST;
  pNew->targetEn = .0;
  pNew->actualEn = .0;
  pNew->mustRecalculate = 1;

  return pNew;
}
/*-------------------------------------------------------------------*/
static void KillTasUB(void *pData){
  ptasUB self = (ptasUB)pData;
  
  if(self == NULL){
    return;
  }
  LLDdelete(self->reflectionList);
  if(self->pDes != NULL){
    DeleteDescriptor(self->pDes);
  }
  if(self->machine.UB != NULL){
    mat_free(self->machine.UB);
  }
  if(self->machine.planeNormal != NULL){
    mat_free(self->machine.planeNormal);
  }
  free(self);
}
/*===================== computation section =========================*/
static int readTASAngles(ptasUB self, SConnection *pCon, 
			 ptasAngles ang){
  int status;
  float val;

  /*
    Monochromator
  */
  status = MotorGetSoftPosition(self->motors[A2],pCon,&val);
  if(status == 0){
    return status;
  }
  ang->monochromator_two_theta = val;

  /*
    Analyzer
  */
  if(self->tasMode != ELASTIC){
	  status = MotorGetSoftPosition(self->motors[A6],pCon,&val);
  	if(status == 0){
    	return status;
  	}
  	ang->analyzer_two_theta = val;
  } else {
  	ang->analyzer_two_theta = ang->monochromator_two_theta;
  }

  /*
    crystal
  */
  status = MotorGetSoftPosition(self->motors[A3],pCon,&val);
  if(status == 0){
    return status;
  }
  ang->a3 = val;
  status = MotorGetSoftPosition(self->motors[A4],pCon,&val);
  if(status == 0){
    return status;
  }
  ang->sample_two_theta = val;
  status = MotorGetSoftPosition(self->motors[SGU],pCon,&val);
  if(status == 0){
    return status;
  }
  ang->sgu = val;
  status = MotorGetSoftPosition(self->motors[SGL],pCon,&val);
  if(status == 0){
    return status;
  }
  ang->sgl = val;
  return 1;
}
/*==================== interpreter interface section =================*/
static int testMotor(ptasUB pNew, SConnection *pCon, char *name, int idx){
  char pBueffel[132];

  if(pNew->motors[idx] == NULL){
    snprintf(pBueffel,131,"ERROR: required motor %s NOT found",name);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } else {
    return 1;
  }
}
/*--------------------------------------------------------------------*/ 
int TasUBFactory(SConnection *pCon,SicsInterp *pSics, void *pData,                
		 int argc, char *argv[]){
  ptasUB pNew = NULL;
  int status = 0, i;
  char pBueffel[132];
  char names[][3] = {"ei","ki",
		    "qh","qk","ql",
		    "ef","kf",
		    "en"};

  if(argc < 2) {
    SCWrite(pCon,"ERROR: need name to install tasUB",eError);
    return 0;
  }
  pNew = MakeTasUB();
  if(pNew == NULL){
    SCWrite(pCon,"ERROR: out of memory creating tasUB",eError);
    return 0;
  }

  /*
    assign motors
  */
  pNew->motors[0] = FindMotor(pSics,"a1");
  pNew->motors[1] = FindMotor(pSics,"a2");
  pNew->motors[2] = FindMotor(pSics,"mcv");
  pNew->motors[3] = FindMotor(pSics,"mch");
  pNew->motors[4] = FindMotor(pSics,"a3");
  pNew->motors[5] = FindMotor(pSics,"a4");
  pNew->motors[6] = FindMotor(pSics,"sgu");
  pNew->motors[7] = FindMotor(pSics,"sgl");
  pNew->motors[8] = FindMotor(pSics,"a5");
  pNew->motors[9] = FindMotor(pSics,"a6");
  pNew->motors[10] = FindMotor(pSics,"acv");
  pNew->motors[11] = FindMotor(pSics,"ach");

  /*
    curvature motors may be missing, anything else is a serious problem
  */
  status += testMotor(pNew, pCon,"a1",A1);
  status += testMotor(pNew, pCon,"a2",A2);
  status += testMotor(pNew, pCon,"a3",A3);
  status += testMotor(pNew, pCon,"a4",A4);
  status += testMotor(pNew, pCon,"sgu",SGU);
  status += testMotor(pNew, pCon,"sgl",SGL);
  status += testMotor(pNew, pCon,"a5",A5);
  status += testMotor(pNew, pCon,"a6",A6);
  if(status != 8){
    return 0;
  }
  
  status = AddCommand(pSics,argv[1],
		      TasUBWrapper,
		      KillTasUB,
		      pNew);
  if(status != 1){
    SCWrite(pCon,"ERROR: duplicate tasUB command not created",eError);
    return 0;
  }

  /*
    install virtual motors
  */
  for(i = 0; i < 8; i++){
    status = InstallTasMotor(pSics,pNew,i+1,names[i]);
    if(status != 1){
      snprintf(pBueffel,131,"ERROR: failed to create TAS motor %s", names[i]);
      SCWrite(pCon,pBueffel,eError);
    }
  }
  status = InstallTasQMMotor(pSics,pNew);
  if(status != 1){
    snprintf(pBueffel,131,"ERROR: failed to create TAS motor qm");
    SCWrite(pCon,pBueffel,eError);
  }

  return 1;
}
/*-----------------------------------------------------------------*/
static int setCrystalParameters(pmaCrystal crystal, SConnection *pCon,
				int argc, char *argv[]){
  int status;
  double d;
  char pBueffel[132];

  status = Tcl_GetDouble(InterpGetTcl(pServ->pSics),argv[3],&d);
  if(status != TCL_OK){
    snprintf(pBueffel,131,"ERROR: failed to convert %s to number",
	     argv[3]);
    SCWrite(pCon,pBueffel,eError);
    return 1;
  }

  if(!SCMatchRights(pCon,usMugger)){
    return 0;
  }

  strtolower(argv[2]);
  if(strcmp(argv[2],"dd") == 0){
    crystal->dd = d;
    SCSendOK(pCon);
    SCparChange(pCon);
    return 1;
  }else if(strcmp(argv[2],"ss") == 0){
    if(d > .0){
      crystal->ss = 1;
    } else {
      crystal->ss = -1;
    }
    SCSendOK(pCon);
    SCparChange(pCon);
    return 1;
  }else if(strcmp(argv[2],"hb1") == 0){
    crystal->HB1 = d;
    SCSendOK(pCon);
    SCparChange(pCon);
    return 1;
  }else if(strcmp(argv[2],"hb2") == 0){
    crystal->HB2 = d;
    SCSendOK(pCon);
    SCparChange(pCon);
    return 1;
  }else if(strcmp(argv[2],"vb1") == 0){
    crystal->VB1 = d;
    SCSendOK(pCon);
    SCparChange(pCon);
    return 1;
  }else if(strcmp(argv[2],"vb2") == 0){
    crystal->VB2 = d;
    SCSendOK(pCon);
    SCparChange(pCon);
    return 1;
  } else {
    snprintf(pBueffel,131,"ERROR: crystal parameter %s not known", 
	     argv[2]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  }
}
/*-----------------------------------------------------------------*/
static int getCrystalParameters(pmaCrystal crystal, SConnection *pCon,
				int argc, char *argv[]){
  char pBueffel[132];

  strtolower(argv[2]);
  if(strcmp(argv[2],"dd") == 0){
    snprintf(pBueffel,131,"%s.%s.dd = %f",argv[0],argv[1],crystal->dd);
    SCWrite(pCon,pBueffel,eValue);
    return 1;
  }else if(strcmp(argv[2],"hb1") == 0){
    snprintf(pBueffel,131,"%s.%s.hb1 = %f",argv[0],argv[1],crystal->HB1);
    SCWrite(pCon,pBueffel,eValue);
    return 1;
  }else if(strcmp(argv[2],"hb2") == 0){
    snprintf(pBueffel,131,"%s.%s.hb2 = %f",argv[0],argv[1],crystal->HB2);
    SCWrite(pCon,pBueffel,eValue);
    return 1;
  }else if(strcmp(argv[2],"vb1") == 0){
    snprintf(pBueffel,131,"%s.%s.vb1 = %f",argv[0],argv[1],crystal->VB1);
    SCWrite(pCon,pBueffel,eValue);
    return 1;
  }else if(strcmp(argv[2],"vb2") == 0){
    snprintf(pBueffel,131,"%s.%s.vb2 = %f",argv[0],argv[1],crystal->VB1);
    SCWrite(pCon,pBueffel,eValue);
    return 1;
  }else if(strcmp(argv[2],"ss") == 0){
    snprintf(pBueffel,131,"%s.%s.ss = %d",argv[0],argv[1],crystal->ss);
    SCWrite(pCon,pBueffel,eValue);
    return 1;
  }else {
    snprintf(pBueffel,131,"ERROR: crystal parameter %s not known", 
	     argv[2]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  }
}
/*------------------------------------------------------------------*/
static int handleCrystalCommands(pmaCrystal crystal, SConnection *pCon,
				 int argc, char *argv[]){
  char pBueffel[132];
  
  if(argc < 3){
    snprintf(pBueffel,131,"ERROR: insufficent number of arguments to %s %s",
	     argv[0],argv[1]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  }
  if(argc > 3) {
    return setCrystalParameters(crystal,pCon,argc,argv);
  } else {
    return getCrystalParameters(crystal,pCon,argc,argv);
  }
}
/*---------------------------------------------------------------------*/
static int tasReadCell(SConnection *pCon, ptasUB self, int argc, char *argv[]){
  int status;
  Tcl_Interp *pTcl = InterpGetTcl(pServ->pSics);
  char pBueffel[256];

  if(argc < 8){
    SCWrite(pCon,"ERROR: insufficient number of arguments to tasub cell",
	    eError);
    return 0;
  }

  if(!SCMatchRights(pCon,usUser)){
    return 0;
  }

  status = Tcl_GetDouble(pTcl,argv[2],&self->cell.a);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[2]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  }
  status = Tcl_GetDouble(pTcl,argv[3],&self->cell.b);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[3]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  }
  status = Tcl_GetDouble(pTcl,argv[4],&self->cell.c);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[4]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  }
  status = Tcl_GetDouble(pTcl,argv[5],&self->cell.alpha);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[5]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  }
  status = Tcl_GetDouble(pTcl,argv[6],&self->cell.beta);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[6]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  }
  status = Tcl_GetDouble(pTcl,argv[7],&self->cell.gamma);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[7]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  }
  self->ubValid = 0;
  SCWrite(pCon,"WARNING: UB is now invalid",eWarning); 
  SCparChange(pCon);
  SCSendOK(pCon);
  return 1;
}
/*---------------------------------------------------------------------*/
static void tasListCell(SConnection *pCon, char *name, lattice direct){
  char pBueffel[255];

  snprintf(pBueffel,255,"%s.cell = %f %f %f %f %f %f",
	   name,direct.a, direct.b,direct.c,
	   direct.alpha,direct.beta,direct.gamma);
  SCWrite(pCon,pBueffel,eValue);
}
/*--------------------------------------------------------------------*/
static void clearReflections(ptasUB self){
  int status;

  status = LLDnodePtr2First(self->reflectionList);
  while(status != 0){
    LLDnodeDelete(self->reflectionList);
    status = LLDnodePtr2Next(self->reflectionList);
  }
  self->ubValid = 0;
}
/*------------------------------------------------------------------*/
static void listReflections(ptasUB self, SConnection *pCon){
  tasReflection r;
  int status;
  int count = 0;
  char line[256];
  Tcl_DString list;

  Tcl_DStringInit(&list);
  snprintf(line,255,
   " NO     QH     QK     QL      A3      A4    SGU    SGL     EI     EF\n");
  Tcl_DStringAppend(&list,line,-1);
  status = LLDnodePtr2First(self->reflectionList);
  while(status == 1){
    count++;
    LLDnodeDataTo(self->reflectionList,&r);
    snprintf(line,255,"%3d %6.2f %6.2f %6.2f %7.2f %7.2f %6.2f %6.2f %6.2f %6.2f\n",
	     count, r.qe.qh, r.qe.qk, r.qe.ql, r.angles.a3, r.angles.sample_two_theta, 
	     r.angles.sgu, r.angles.sgl, KtoEnergy(r.qe.ki), KtoEnergy(r.qe.kf));
    Tcl_DStringAppend(&list,line,-1);
    status = LLDnodePtr2Next(self->reflectionList);
  }
  if(count == 0){
    SCWrite(pCon,"Reflection list is empty",eValue);
  } else {
    SCWrite(pCon,Tcl_DStringValue(&list),eValue);
  }
  Tcl_DStringFree(&list);
}
/*-------------------------------------------------------------------*/
#define ABS(x) (x < 0 ? -(x) : (x)) 
/*-------------------------------------------------------------------*/
static int addReflection(ptasUB self, SicsInterp *pSics, 
			 SConnection *pCon, 
			 int argc, char *argv[]){
  tasReflection r;
  int status, count = 11;
  char pBueffel[256];
  tasAngles angles;
  Tcl_DString list;

  if(argc < 5){
    SCWrite(pCon,"ERROR: need at least miller indices to add reflection",
	    eError);
    return 0;
  }

  if(!SCMatchRights(pCon,usUser)){
    return 0;
  }

  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[2],&r.qe.qh);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[2]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[3],&r.qe.qk);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[3]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[4],&r.qe.ql);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[4]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 

  if(self->tasMode == ELASTIC){
  	count = 10;
  }
  if(argc >= count){
    status = Tcl_GetDouble(InterpGetTcl(pSics),argv[5],&r.angles.a3);
    if(status != TCL_OK){
      snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[5]);
      SCWrite(pCon,pBueffel,eError);
      return 0;
    } 
    status = Tcl_GetDouble(InterpGetTcl(pSics),argv[6],&r.angles.sample_two_theta);
    if(status != TCL_OK){
      snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[6]);
      SCWrite(pCon,pBueffel,eError);
      return 0;
    } 
    status = Tcl_GetDouble(InterpGetTcl(pSics),argv[7],&r.angles.sgu);
    if(status != TCL_OK){
      snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[7]);
      SCWrite(pCon,pBueffel,eError);
      return 0;
    } 
    status = Tcl_GetDouble(InterpGetTcl(pSics),argv[8],&r.angles.sgl);
    if(status != TCL_OK){
      snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[8]);
      SCWrite(pCon,pBueffel,eError);
      return 0;
    } 
    status = Tcl_GetDouble(InterpGetTcl(pSics),argv[9],&r.qe.ki);
    if(status != TCL_OK){
      snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[9]);
      SCWrite(pCon,pBueffel,eError);
      return 0;
    } 
	r.qe.ki = energyToK(r.qe.ki);
    if(self->tasMode != ELASTIC){
    	status = Tcl_GetDouble(InterpGetTcl(pSics),argv[10],&r.qe.kf);
    	if(status != TCL_OK){
      	snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[10]);
      	SCWrite(pCon,pBueffel,eError);
      	return 0;
    	} 
    	r.qe.kf = energyToK(r.qe.kf);
    } else {
    	r.qe.kf = r.qe.ki;
    }
  } else {
    if(argc > 5){
      SCWrite(pCon,
	      "WARNING: not all angles given on command line, using positions instead",
	      eWarning);
    }
    status = readTASAngles(self,pCon,&r.angles);
    if(status != 1){
      return status;
    }
    r.qe.ki = maCalcK(self->machine.monochromator,r.angles.monochromator_two_theta);
    r.qe.kf = maCalcK(self->machine.analyzer,r.angles.analyzer_two_theta);
  }
  if(self->tasMode == ELASTIC){
  	r.qe.kf = r.qe.ki;
  }
  if(ABS(r.qe.ki - r.qe.kf) > .01) {
    SCWrite(pCon,"WARNING: KI != KF!",eWarning);
  }
  LLDnodeAppend(self->reflectionList,&r);
  Tcl_DStringInit(&list);
  snprintf(pBueffel,255,
   "     QH     QK     QL      A3      A4    SGU    SGL     EI     EF\n");
  Tcl_DStringAppend(&list,pBueffel,-1);
  snprintf(pBueffel,255,
	   " %6.2f %6.2f %6.2f %7.2f %7.2f %6.2f %6.2f %6.2f %6.2f\n",
	     r.qe.qh, r.qe.qk, r.qe.ql, r.angles.a3, r.angles.sample_two_theta, 
	   r.angles.sgu, r.angles.sgl, KtoEnergy(r.qe.ki), 
	   KtoEnergy(r.qe.kf));
  Tcl_DStringAppend(&list,pBueffel,-1);
  SCWrite(pCon,Tcl_DStringValue(&list),eValue);
  Tcl_DStringFree(&list);
  SCparChange(pCon);
  return 1;
}
/*------------------------------------------------------------------------------*/
static int readReflection(SConnection *pCon, SicsInterp *pSics, 
			  ptasReflection res,
			 int argc, char *argv[]){
  tasReflection r;
  int status;
  char pBueffel[256];

  if(!SCMatchRights(pCon,usUser)){
    return 0;
  }

  if(argc < 11){
    SCWrite(pCon,"ERROR: not enough parameters to read reflection",eError);
    return 0;
  }
  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[2],&r.qe.qh);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[2]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[3],&r.qe.qk);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[3]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[4],&r.qe.ql);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[4]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[5],&r.angles.a3);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[5]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[6],&r.angles.sample_two_theta);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[6]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[7],&r.angles.sgu);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[7]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[8],&r.angles.sgl);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[8]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[9],&r.qe.ki);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[9]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  r.qe.ki = energyToK(r.qe.ki);
  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[10],&r.qe.kf);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[10]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  r.qe.kf = energyToK(r.qe.kf);
  if(ABS(r.qe.ki - r.qe.kf) > .01) {
    SCWrite(pCon,"WARNING: KI != KF!",eWarning);
  }
  *res = r;
  return 1;
}
/*-----------------------------------------------------------------*/
int findReflection(int list, int idx, ptasReflection r){
  int count = 0;
  int status;

  status = LLDnodePtr2First(list);
  while(status == 1){
    if(count == idx){
      LLDnodeDataTo(list,r);
      return 1;
    }
    status = LLDnodePtr2Next(list);
    count++;
  }
  return 0;
}
/*------------------------------------------------------------------*/
static void listUB(ptasUB self , SConnection *pCon){
  Tcl_DString list;
  char pBueffel[255];
  int i;
  tasReflection r;

  Tcl_DStringInit(&list);
  if(self->machine.UB == NULL){
    Tcl_DStringAppend(&list,"NO UB",-1);
  } else { 
    Tcl_DStringAppend(&list,"UB = ", -1);
      snprintf(pBueffel,255,"%f %f %f\n", self->machine.UB[0][0],
	       self->machine.UB[0][1],self->machine.UB[0][2]);
      Tcl_DStringAppend(&list,pBueffel,-1);
    for(i = 1; i < 3; i++){
      snprintf(pBueffel,255,"     %f %f %f\n", self->machine.UB[i][0],
	       self->machine.UB[i][1],self->machine.UB[i][2]);
      Tcl_DStringAppend(&list,pBueffel,-1);
    }
  }
  snprintf(pBueffel,255,"UB generated from reflections:\n");
  Tcl_DStringAppend(&list,pBueffel,-1);
  snprintf(pBueffel,255,
   "      QH       QK       QL      A3      A4    SGU    SGL     EI     EF\n");
  Tcl_DStringAppend(&list,pBueffel,-1);
  r = self->r1;
  snprintf(pBueffel,255,
    " %8.4f %8.4f %8.4f %7.2f %7.2f %6.2f %6.2f %6.2f %6.2f\n",
	   r.qe.qh, r.qe.qk, r.qe.ql, r.angles.a3, 
	   r.angles.sample_two_theta, r.angles.sgu, r.angles.sgl, 
	   KtoEnergy(r.qe.ki), KtoEnergy(r.qe.kf));
  Tcl_DStringAppend(&list,pBueffel,-1);
  r = self->r2;
  snprintf(pBueffel,255,
    " %8.4f %8.4f %8.4f %7.2f %7.2f %6.2f %6.2f %6.2f %6.2f\n",
	   r.qe.qh, r.qe.qk, r.qe.ql, r.angles.a3, 
	   r.angles.sample_two_theta, r.angles.sgu, r.angles.sgl, 
	   KtoEnergy(r.qe.ki), KtoEnergy(r.qe.kf));
  Tcl_DStringAppend(&list,pBueffel,-1);
  snprintf(pBueffel,255,"Plane Normal: %8.4f %8.4f %8.4f\n",
	   self->machine.planeNormal[0][0], self->machine.planeNormal[1][0],
	   self->machine.planeNormal[2][0]);
  Tcl_DStringAppend(&list,pBueffel,-1);
  if(self->ubValid == 0){
    Tcl_DStringAppend(&list,"WARNING: UB matrix is invalid\n",-1);
  }
  SCWrite(pCon,Tcl_DStringValue(&list),eValue);
  Tcl_DStringFree(&list);
}
/*-----------------------------------------------------------------*/
static void printReflectionDiagnostik(ptasUB self, SConnection *pCon,
				      tasReflection r){
  tasReflection r2;
  Tcl_DString list;
  char line[256];
  tasQEPosition qe;
  tasAngles angles;

  Tcl_DStringInit(&list);
  snprintf(line,255,
   "METHOD        QH       QK       QL      A3      A4    SGU    SGL     EI     EF\n");
  Tcl_DStringAppend(&list,line,-1);
  snprintf(line,255,
    "INPUT   %8.4f %8.4f %8.4f %7.2f %7.2f %6.2f %6.2f %6.2f %6.2f\n",
	     r.qe.qh, r.qe.qk, r.qe.ql, r.angles.a3, 
	   r.angles.sample_two_theta, r.angles.sgu, r.angles.sgl, 
	   KtoEnergy(r.qe.ki), KtoEnergy(r.qe.kf));
  Tcl_DStringAppend(&list,line,-1);
  qe.ki = r.qe.ki;
  qe.kf = r.qe.kf;
  qe.qh = r.qe.qh;
  qe.qk = r.qe.qk;
  qe.ql = r.qe.ql;
  calcAllTasAngles(&self->machine,qe,&angles);
  snprintf(line,255,
      "QE->ANG %8.4f %8.4f %8.4f %7.2f %7.2f %6.2f %6.2f %6.2f %6.2f\n",
	     r.qe.qh, r.qe.qk, r.qe.ql, 
	   angles.a3, angles.sample_two_theta, 
	   angles.sgu, angles.sgl, KtoEnergy(r.qe.ki), KtoEnergy(r.qe.kf));
  Tcl_DStringAppend(&list,line,-1);
  angles.a3 = r.angles.a3;
  angles.sample_two_theta = r.angles.sample_two_theta;
  angles.sgu = r.angles.sgu;
  angles.sgl = r.angles.sgl;
  calcTasQEPosition(&self->machine,angles,&qe);
  snprintf(line,255,
      "ANG->QE %8.4f %8.4f %8.4f %7.2f %7.2f %6.2f %6.2f %6.2f %6.2f\n",
	     qe.qh, qe.qk, qe.ql, angles.a3, angles.sample_two_theta, 
	     angles.sgu, angles.sgl, KtoEnergy(qe.ki), KtoEnergy(qe.kf));
  Tcl_DStringAppend(&list,line,-1);
  SCWrite(pCon,Tcl_DStringValue(&list),eWarning);
  Tcl_DStringFree(&list);
}
/*------------------------------------------------------------------*/
static void listDiagnostik(ptasUB self, SConnection *pCon){
  tasReflection r;
  int status;

  status = LLDnodePtr2First(self->reflectionList);
  while(status == 1){
    LLDnodeDataTo(self->reflectionList,&r);
    printReflectionDiagnostik(self,pCon,r);
    status = LLDnodePtr2Next(self->reflectionList);
  }
}
/*------------------------------------------------------------------*/
static int calcUB(ptasUB self, SConnection *pCon, SicsInterp *pSics, 
		  int argc, char *argv[]){
  int idx1, idx2, status;
  tasReflection r1, r2;
  char pBueffel[256];
  MATRIX UB = NULL;

  if(argc < 4){
    SCWrite(pCon,
	"ERROR: not enough arguments for UB calculation, need index of two reflections",
	    eError);
    return 0;
  }

  if(!SCMatchRights(pCon,usUser)){
    return 0;
  }

  status = Tcl_GetInt(InterpGetTcl(pSics),argv[2],&idx1);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[2]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  idx1--;
  status = findReflection(self->reflectionList, idx1,&r1);
  if(status != 1){
    snprintf(pBueffel,255,"ERROR: cannot find reflection with index %d",idx1+1);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  }
  status = Tcl_GetInt(InterpGetTcl(pSics),argv[3],&idx2);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[3]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  idx2--;
  status = findReflection(self->reflectionList, idx2,&r2);
  if(status != 1){
    snprintf(pBueffel,255,"ERROR: cannot find reflection with index %d",idx2+1);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  }

  UB = calcTasUBFromTwoReflections(self->cell,r1,r2,&status);
  if(UB == NULL){
    switch(status){
    case UBNOMEMORY:
      SCWrite(pCon,"ERROR: out of memory calculating UB matrix",eError);
      break;
    case REC_NO_VOLUME:
      SCWrite(pCon,"ERROR: bad cell constants, no volume",eError);
      break;
    }
    return 0;
  }
  if(mat_det(UB) < .000001){
    SCWrite(pCon,"ERROR: invalid UB matrix, check reflections",eError);
    return 0;
  }
  if(self->machine.UB != NULL){
    mat_free(self->machine.UB);
  }
  if(self->machine.planeNormal != NULL){
    mat_free(self->machine.planeNormal);
  }
  self->machine.UB = UB;
  self->machine.planeNormal = calcPlaneNormal(r1,r2);
  self->r1 = r1;
  self->r2 = r2;
  self->ubValid = 1;
  listUB(self,pCon);
  listDiagnostik(self,pCon);
  SCparChange(pCon);
  return 1;
}
/*------------------------------------------------------------------*/
static int calcRefAngles(ptasUB self, SConnection *pCon, 
			 SicsInterp *pSics, 
			 int argc, char *argv[]){
  tasQEPosition q;
  tasAngles angles;
  char pBueffel[256];
  int status;

  if(self->tasMode == ELASTIC){
 	  if(argc < 6){
    	SCWrite(pCon,"ERROR: need Qh, Qk, Ql, EI for calculation",
	    	eError);
    	return 0;
 	  }
  } else {
	  if(argc < 7){
    	SCWrite(pCon,"ERROR: need Qh, Qk, Ql, EI, EF for calculation",
	    	eError);
    	return 0;
  	}
  } 
  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[2],&q.qh);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[2]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[3],&q.qk);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[3]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[4],&q.ql);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[4]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[5],&q.ki);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[5]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  if(self->tasMode != ELASTIC){
	  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[6],&q.kf);
  	if(status != TCL_OK){
    	snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[6]);
    	SCWrite(pCon,pBueffel,eError);
    	return 0;
  	}
  } else {
  	q.kf = q.ki;
  }
  q.ki = energyToK(q.ki);
  q.kf = energyToK(q.kf);

  status = calcAllTasAngles(&self->machine,q,&angles);
  switch(status){
  case ENERGYTOBIG:
    SCWrite(pCon,"ERROR: energy to big",eError);
    return 0;
    break;
  case UBNOMEMORY:
    SCWrite(pCon,"ERROR: Out of memory calculating angles",eError);
    return 0;
    break;
  case BADRMATRIX:
    SCWrite(pCon,"ERROR: bad crystallographic parameters or bad UB",eError);
    return 0;
    break;
  case TRIANGLENOTCLOSED:
    SCWrite(pCon,"ERROR: scattering triangle not closed",eError);
    return 0;
    break;
  }
  if(self->tasMode != ELASTIC){
	  snprintf(pBueffel,255," %8.2f   %8.2f %8.2f %8.2f %8.2f   %8.2f",
		   angles.monochromator_two_theta, 
	   		angles.a3, angles.sample_two_theta,
	   		angles.sgl, angles.sgu,
	   	angles.analyzer_two_theta);
  } else {
	  snprintf(pBueffel,255," %8.2f   %8.2f %8.2f %8.2f %8.2f",
		   angles.monochromator_two_theta, 
	   		angles.a3, angles.sample_two_theta,
	   		angles.sgl, angles.sgu);
  }
  SCWrite(pCon,pBueffel,eValue);
  return 1;
}
/*------------------------------------------------------------------*/
static int calcQFromAngles(ptasUB self, SConnection *pCon, 
			 SicsInterp *pSics, 
			 int argc, char *argv[]){
  tasQEPosition q;
  tasAngles angles;
  char pBueffel[256];
  int status;

  if(self->tasMode != ELASTIC){
	  if(argc < 8){
    	SCWrite(pCon,"ERROR: need a2, a3, a4, sgu, sgl, a6 for calculation",
	    	eError);
    	return 0;
  	}
  } else {
	  if(argc < 7){
    	SCWrite(pCon,"ERROR: need a2, a3, a4, sgu, sgl for calculation",
	    	eError);
    	return 0;
  	}
  } 
  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[2],
			 &angles.monochromator_two_theta);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[2]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[3],&angles.a3);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[3]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[4],&angles.sample_two_theta);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[4]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[5],&angles.sgu);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[5]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[6],&angles.sgl);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[6]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  if(self->tasMode != ELASTIC){
	  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[7],&angles.analyzer_two_theta);
  	if(status != TCL_OK){
    	snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[7]);
    	SCWrite(pCon,pBueffel,eError);
   	 return 0;
  	}
  } else {
  		angles.analyzer_two_theta = angles.monochromator_two_theta;
  } 
  status = calcTasQEPosition(&self->machine,angles,&q);
  switch(status){
  case UBNOMEMORY:
    SCWrite(pCon,"ERROR: Out of memory calculating angles",eError);
    return 0;
    break;
  }

  if(self->tasMode == ELASTIC){
  		q.kf = q.ki;
  }
  snprintf(pBueffel,255,"%8.4f %8.4f %8.4f %8.4f %8.4f",
	   q.qh, 
	   q.qk,
	   q.ql,
	   KtoEnergy(q.ki),
	   KtoEnergy(q.kf));
  SCWrite(pCon,pBueffel,eValue);
  return 1;
}
/*------------------------------------------------------------------*/
static int setUB(SConnection *pCon, SicsInterp *pSics, ptasUB self,
		 int argc, char *argv[]){
  double value;
  char pBueffel[256];
  int status;

  if(argc < 11){
    SCWrite(pCon,"ERROR: not enough arguments for setting UB",
	    eError);
    return 0;
  }

  if(!SCMatchRights(pCon,usUser)){
    return 0;
  }

  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[2],&value);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[2]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  self->machine.UB[0][0] = value; 

  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[3],&value);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[3]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  self->machine.UB[0][1] = value; 

  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[4],&value);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[4]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  self->machine.UB[0][2] = value; 

  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[5],&value);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[5]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  self->machine.UB[1][0] = value; 

  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[6],&value);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[6]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  self->machine.UB[1][1] = value; 

  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[7],&value);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[7]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  self->machine.UB[1][2] = value; 

  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[8],&value);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[8]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  self->machine.UB[2][0] = value; 

  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[9],&value);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[9]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  self->machine.UB[2][1] = value; 

  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[10],&value);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[10]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  self->machine.UB[2][2] = value; 
  self->ubValid = 1;
  SCSendOK(pCon);
  SCparChange(pCon);

  return 1;
}
/*------------------------------------------------------------------*/
static int setNormal(SConnection *pCon, SicsInterp *pSics, ptasUB self,
		 int argc, char *argv[]){
  double value;
  char pBueffel[256];
  int status;

  if(argc < 5){
    SCWrite(pCon,"ERROR: not enough arguments for setting plane normal",
	    eError);
    return 0;
  }
  
  if(!SCMatchRights(pCon,usUser)){
    return 0;
  }

  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[2],&value);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[2]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  self->machine.planeNormal[0][0] = value; 

  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[3],&value);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[3]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  self->machine.planeNormal[1][0] = value; 

  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[4],&value);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[4]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  self->machine.planeNormal[2][0] = value; 
  SCSendOK(pCon);
  SCparChange(pCon);

  return 1;
}
/*------------------------------------------------------------------*/
static int setTarget(SConnection *pCon, SicsInterp *pSics, ptasUB self,
		 int argc, char *argv[]){
  double value;
  char pBueffel[256];
  int status;

  if(argc < 8){
    SCWrite(pCon,"ERROR: not enough arguments for setting qe target",
	    eError);
    return 0;
  }
  
  if(!SCMatchRights(pCon,usUser)){
    return 0;
  }

  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[2],&self->target.qh);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[2]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 

  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[3],&self->target.qk);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[3]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 

  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[4],&self->target.ql);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[4]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 

  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[5],&self->target.qm);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[5]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[6],&self->target.ki);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[6]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  status = Tcl_GetDouble(InterpGetTcl(pSics),argv[7],&self->target.kf);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[7]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 

  SCSendOK(pCon);

  return 1;
}
/*------------------------------------------------------------------*/
static int tasUpdate(SConnection *pCon, ptasUB self){
  int status;
  tasAngles angles;
  
  status = readTASAngles(self,pCon,&angles);
  if(status != 1){
    return status;
  }
  status = calcTasQEPosition(&self->machine, angles, &self->current);
  if(status < 0){
    SCWrite(pCon,"ERROR: out of memory calculating Q-E variables",eError);
    return 0;
  }
  if(self->tasMode == ELASTIC){
  	self->current.kf = self->current.ki;
  }
  self->mustRecalculate = 0;
  SCSendOK(pCon);
  return 1;
} 
/*------------------------------------------------------------------*/
static int deleteReflection(SConnection *pCon, SicsInterp *pSics,
			    ptasUB self, int argc, char *argv[]){
  int idx, count = 0, status;
  char pBueffel[256];

  if(argc < 3){
    SCWrite(pCon,"ERROR: need number of reflection to delete",eError);
    return 0;
  }
  status = Tcl_GetInt(InterpGetTcl(pSics),argv[2],&idx);
  if(status != TCL_OK){
    snprintf(pBueffel,255,"ERROR: failed to convert %s to number",argv[2]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  } 
  idx--;
  status = LLDnodePtr2First(self->reflectionList);
  while(status == 1){
    if(count == idx){
      LLDnodeDelete(self->reflectionList);
      break;
    }
    status = LLDnodePtr2Next(self->reflectionList);
    count++;
  }
  SCSendOK(pCon);
  return 1;
}
/*-------------------------------------------------------------------*/
int TasUBWrapper(SConnection *pCon,SicsInterp *pSics, void *pData,                
		 int argc, char *argv[]){
  ptasUB self = NULL;
  char pBueffel[131];
  int status, newSS;

  self = (ptasUB)pData;
  assert(self != NULL);

  if(argc < 2){
    SCWrite(pCon,"ERROR: insufficient arguments to tasUB",eError);
    return 0;
  }

  strtolower(argv[1]);
  if(strcmp(argv[1],"mono") == 0){
    return handleCrystalCommands(&self->machine.monochromator,pCon,argc,argv);
  } else  if(strcmp(argv[1],"ana") == 0){
    return handleCrystalCommands(&self->machine.analyzer,pCon,argc,argv);
  }else if(strcmp(argv[1],"cell") == 0){
    if(argc > 2){
      return tasReadCell(pCon,self,argc,argv);
    } else {
      tasListCell(pCon,argv[0],self->cell);
      return 1;
    }
  } else  if(strcmp(argv[1],"clear") == 0){
    clearReflections(self);
    clearReflections(self);
    SCWrite(pCon,"WARNING: UB is now invalid",eWarning);
    SCSendOK(pCon);
    return 1;
  } else  if(strcmp(argv[1],"listref") == 0){
    listReflections(self,pCon);
    return 1;
  } else  if(strcmp(argv[1],"addref") == 0){
    return addReflection(self,pSics,pCon,argc,argv);
  } else  if(strcmp(argv[1],"listub") == 0){
    listUB(self,pCon);
    return 1;
  } else  if(strcmp(argv[1],"makeub") == 0){
    return calcUB(self,pCon,pSics,argc,argv);
  } else  if(strcmp(argv[1],"calcang") == 0){
    return calcRefAngles(self,pCon,pSics,argc,argv);
  } else  if(strcmp(argv[1],"calcqe") == 0){
    return calcQFromAngles(self,pCon,pSics,argc,argv);
  } else  if(strcmp(argv[1],"setub") == 0){
    return setUB(pCon,pSics,self,argc,argv);
  } else  if(strcmp(argv[1],"setnormal") == 0){
    return setNormal(pCon,pSics,self,argc,argv);
  } else  if(strcmp(argv[1],"settarget") == 0){
    return setTarget(pCon,pSics,self,argc,argv);
  } else  if(strcmp(argv[1],"update") == 0){
    return tasUpdate(pCon,self);
  } else  if(strcmp(argv[1],"del") == 0){
    return deleteReflection(pCon,pSics,self,argc,argv);
  } else  if(strcmp(argv[1],"r1") == 0){
    return readReflection(pCon,pSics,&self->r1,argc,argv);
  } else  if(strcmp(argv[1],"r2") == 0){
    return readReflection(pCon,pSics,&self->r2,argc,argv);
  } else  if(strcmp(argv[1],"const") == 0){
    if(argc > 2){
      strtolower(argv[2]);
      if(!SCMatchRights(pCon,usUser)){
	return 0;
      }
      if(strcmp(argv[2],"ki") == 0){
	self->tasMode = KICONST;
      } else if(strcmp(argv[2],"kf") == 0){
	self->tasMode = KFCONST;
      } else if(strcmp(argv[2],"elastic") == 0){
	self->tasMode = ELASTIC;
      } else {
	SCWrite(pCon,
		"ERROR: unknown triple axis mode, accepted are ki, kf, elastic",
		eError);
	return 0;
      }
      SCSendOK(pCon);
      return 1;
    } else {
      if(self->tasMode == KICONST){
	snprintf(pBueffel,131,"%s.const = ki",argv[0]);
      } else if(self->tasMode == ELASTIC){
      	snprintf(pBueffel,131,"%s.const = elastic", argv[0]);
      } else {
	snprintf(pBueffel,131,"%s.const = kf",argv[0]);
      }
      SCWrite(pCon,pBueffel,eValue);
      return 1;
    }
  } else  if(strcmp(argv[1],"ss") == 0){
    if(argc > 2){
      strtolower(argv[2]);
      if(!SCMatchRights(pCon,usUser)){
	return 0;
      }
      status = Tcl_GetInt(InterpGetTcl(pSics),argv[2],&newSS);
      if(status != TCL_OK){
	SCWrite(pCon,"ERROR: failed to convert argument to number",eError);
	return 0;
      }
      if(newSS != 1 && newSS != -1){
	SCWrite(pCon,"ERROR: invalid value for scattering sense, only 1, -1 allowed",
		eError);
	return 0;
      }
      self->machine.ss_sample = newSS;
      tasUpdate(pCon,self);
      SCSendOK(pCon);
      return 1;
    } else {
      snprintf(pBueffel,131,"%s.ss = %d",argv[0],self->machine.ss_sample);
      SCWrite(pCon,pBueffel,eValue);
      return 1;
    }
  } else {
    snprintf(pBueffel,131,"ERROR: subcommand %s to %s not defined",argv[1],
	     argv[0]);
    SCWrite(pCon,pBueffel,eError);
    return 0;
  }
  return 1;
}

