/**
 * This is a library of functions and data structures for performing 
 * triple axis spectrometer angle calculations using the UB-matrix
 * formalism as described by Mark Lumsden.
 *
 * copyright: see file COPYRIGHT
 *
 * Mark Koennecke, April 2005
 */
#ifndef TASUBLIB
#define TASUBLIB
#include "cell.h"
#include "matrix/matrix.h"
/*================= error codes =====================================*/
#define ENERGYTOBIG -700
#define BADSYNC     -701  /* mono/analyzer out of sync: 2*theta != two_theta*/
#define UBNOMEMORY  -702
#define TRIANGLENOTCLOSED  -703
#define BADRMATRIX         -704
#define BADUBORQ           -705
/*========================== defines for tasMode ====================*/
#define KICONST 1
#define KFCONST 2
#define ELASTIC 3 
/*
 * in elastic mode A5, A5 will be disregarded and ki = kf at all times
 */
/*=========================== TAS Variables =========================*/
#define EI 1
#define KI 2
#define QH 3
#define QK 4
#define QL 5
#define EF 6
#define KF 7
#define EN 8
#define QM 9
/*=========================== data structures =======================*/
/**
 * data structure describing a monochromator or analyzer crystal 
 */
typedef struct {
  double dd; /* lattice spacing */
  int ss;    /* scattering sense */
  double HB1, HB2; /* horizontal curvature parameters */
  double VB1, VB2; /* vertical curvature parameters   */
} maCrystal, *pmaCrystal;
/**
 * the machine parameters of a triple axis spectrometer
 */
typedef struct {
  maCrystal monochromator, analyzer;
  MATRIX UB;
  MATRIX planeNormal; 
  int ss_sample; /* scattering sense sample */
}tasMachine, *ptasMachine;
/**
 * a position in Q - Energy space
 */ 
typedef struct {
  double ki, kf;
  double qh,qk,ql;
  double qm;
}tasQEPosition, *ptasQEPosition;
/**
 * A triple axis angle position
 */
typedef struct {
  double monochromator_two_theta;
  double a3;
  double sample_two_theta;
  double sgl;
  double sgu;
  double analyzer_two_theta;
}tasAngles, *ptasAngles;
/**
 * a full triple axis reflection
 */
typedef struct {
  tasQEPosition qe;
  tasAngles angles;
}tasReflection, *ptasReflection;
/*================= Monochromator/Analyzer stuff =====================*/
/**
 * convert an energy in meV to Ki, Kf type values
 * @param input energy
 * @return Ki, or Kf
 */
double energyToK(double energy);
/**
 * convert from Ki, Kf to energy in meV
 * @param input K value
 * @return output energy in meV
 */
double KtoEnergy(double k); 
/*----------------------------------------------------------------------*/
/**
 * calculate two_theta for k
 * @param data The crystals parameter
 * @param k The input K value to calculate
 * @param two_theta The resulting two_theta
 * @return 1 on success, a negative error code on failure
 */
int maCalcTwoTheta(maCrystal data, double k, double *two_theta);
/**
 * calculate the value for the vertical curvature
 * @param data The input crystal parameters
 * @param two_theta The tow theta value for which to calculate the curvature.
 * @return A new value for the curvature.
 */
double maCalcVerticalCurvature(maCrystal data, double two_theta);
/**
 * calculate the value for the horizontal curvature
 * @param data The input crystal parameters
 * @param two_theta The tow theta value for which to calculate the curvature.
 * @return A new value for the curvature.
 */
double maCalcHorizontalCurvature(maCrystal data, double two_theta);
/**
 * calculate the value of the K vector from the angle
 * @param data The crystals constants
 * @param two_theta The two theta read from the motor
 * @return The k value calculated from two_theta and the parameters.
 */
double maCalcK(maCrystal data, double two_theta);
/*======================= reciprocal space =============================*/
/**
 * calculate a UB from two reflections and the cell.
 * @param cell The lattice constant of the crystal
 * @param r1 The first reflection
 * @param r2 The second reflection
 * @param erroroCode An error code which gives more details
 *  when an error occurs.
 * @return a UB matix on sucess, or NULL on failure. Then errorCode
 * can be inspected what caused the problem.
 */ 
MATRIX calcTasUBFromTwoReflections(lattice cell, tasReflection r1,
				   tasReflection r2, int *errorCode);
/**
 * calcluate the normal to the plane describe by the two reflections r1, r2
 * @param r1 first reflection
 * @param r2 second reflection
 * @return a plane normal on success, NULL else
 */
MATRIX calcPlaneNormal(tasReflection r1, tasReflection r2);
/**
 * calculate the angles for r. R's h, k, l, ki, kf must be set, the angles
 * will be updated.
 * @param UB The UB matrix to use
 * @param planeNormal The normal to the scattering plane to use 
 * @param ss The scattering sense at the sample
 * @param qe The desired Q Energy position
 * @param angles The resulting angles.
 * @return 1 on success, a negative error code when errors are encountered
 */   
int calcTasQAngles(MATRIX UB, MATRIX planeNormal, 
		   int ss, tasQEPosition qe,
		   ptasAngles angles);
/**
 * calculate QH, QK, QL from the angles given
 * @param UB The UB matrix to use
 * @param angles The angles as read from the motors
 * @param qe The resulting Q Energy positions
 * @return 1 on success, a negative error code on failures.
 */
int calcTasQH(MATRIX UB, tasAngles angles, ptasQEPosition qe);
/*======================== pulling it together.. =======================*/
/**
 * calculate all the tas target angles for a position in Q-Energy space. 
 * @param machine The machine description
 * @param qe Input QE position
 * @param angles output angles.
 * @return 1 on success, a negative error code in case of problems
 */
int calcAllTasAngles(ptasMachine machine, tasQEPosition qe,
		      ptasAngles angles);
/**
 * calculate the current position of the spectrometer in Q-E space from
 * angles. 
 * @param machine The machine parameters
 * @param angles The input angles
 * @param qe The output Q-E position
 * @return 1 on success, a negative error code on errors.
 */
int calcTasQEPosition(ptasMachine machine, tasAngles angles,
		      ptasQEPosition qe);
/*======================== POWDER MODE =================================
  Powder mode is driving only QM, A3, SGGU, SGL will not be touched,
  only energy and sample two theta will be driven.
========================================================================*/
/**
 * calculate the angles for a specified energy and qm position (in qe).
 * @param machine The machine constants of the spectrometer
 * @param qe The energy, qm position desired.
 * @param angles The angles for this qe position. Please ignore a3, sgu, sgl
 * @return 1 on success, a negative error code else
 */
int calcTasPowderAngles(ptasMachine machine, tasQEPosition qe,
			ptasAngles angles);
/**
 * calculate the current energy qm position from angles. 
 * @param machine The spectrometer parameters.
 * @param angles The angles as read from the motors
 * @param qe The resulting qe position
 * @return 1 on success, a negative error code on errors
 */
int calcTasPowderPosition(ptasMachine machine, tasAngles angles, 
			  ptasQEPosition qe);
/*======================= TAS Logic =====================================*/
/**
 * set triple axis parameters, thereby taking the tasMode into account
 * @param qe The Q Energy variable set to update
 * @param tasMode The triple axis mode to apply
 * @param tasVar The TAS variable to handle. This MUST be one of the 
 * defines at the top of this file.
 * @param value The value to set for tasPar
 */ 
void setTasPar(ptasQEPosition qe, int tasMode, int tasVar, double value);
/**
 * calculates the value of a TAS parameter from qe.
 * @param qe The Q Energy psoition to extract data from
 * @parm tasVar The TAS variable to extract. This MUST be one of the
 * defines given at the top of this file.
 * @return The value of the TAS variable.
 */
double getTasPar(tasQEPosition qe, int tasVar);

#endif
