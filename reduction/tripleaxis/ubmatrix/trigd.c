/**
 * This is a library of trigonmetric functions acting upon proper
 * angles and not radians. Lifted from the Risoe tascom code
 *
 * March 2005
 */
#include <math.h>
#include "trigd.h"

/* define constants */
#ifndef PI
#define PI              (3.1415926536)  /* pi */
#endif
#define DEGREE_RAD      (PI/180.0)      /* Radians per degree */
/*******************************************************************************/
double Sign(double d)
{
  if(d < .0){
    return -1;
  } else {
    return 1;
  }
}
/*******************************************************************************
* Sinus of angle in degrees.
*******************************************************************************/
extern double Sind (double x)
{
  return (sin (x*DEGREE_RAD));
}
/*******************************************************************************
* Tangens of angle in degrees.
*******************************************************************************/
extern double Tand(double x)
{
  return (tan(x*DEGREE_RAD));
}
/*******************************************************************************
* cotangens of angle in degrees
*****************************************************************************/
extern double Cotd(double x){
	if(tan(x*DEGREE_RAD) > .00001){
		return (1./tan(x*DEGREE_RAD));
	} else {
		return 0;
	}
} 
/*******************************************************************************
* Cosinus of angle in degrees.
*******************************************************************************/
extern double Cosd (double x)
{
  return (cos (x*DEGREE_RAD));
}
/*******************************************************************************
* Atan of angle in degrees.
*******************************************************************************/
extern double Atand (double x)
{
  double data;

  data = (atan(x)/DEGREE_RAD);
  return (data);
}
/*******************************************************************************
* Atan of angle in degrees.
*******************************************************************************/
extern double Atan2d (double x, double y)
{
  double data;

  data = (atan2(x,y)/DEGREE_RAD);
  return (data);
}
/*******************************************************************************
* Atan2 of angle in degrees.
*******************************************************************************/
extern double Atand2 (double x)
{
  double data;

  data = (atan(x)/DEGREE_RAD);
  return (data);
}
/*******************************************************************************
* Acos of angle in degrees.
*******************************************************************************/
extern double Acosd (double x)
{
  double data;

  data = acos(x)/DEGREE_RAD;
  return (data);
}
/*******************************************************************************
* Asin of angle in degrees.
*******************************************************************************/
extern double Asind (double x)
{
  double data;

  data = x*x;
  if (data == 1.0)
    return (180.00 - Sign (x)*90.00);
  else if (data > 1)
  {
    return (0);
  }
  else
    return (Atand (x/sqrt (1 - data)));

}
