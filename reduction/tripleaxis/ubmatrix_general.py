'''
Author: Alex Yee

Edit History
    See Research Journal
'''
import sys
import numpy as np
#import scipy
#import scipy.optimize

from openopt import SNLE
#import multiprocessing as NLSP


#TODO:
#Use metric tensor for determining figure of merit for fit
#Set up mode to use a single vector for "scattering plane mode" of triple axis
#Make sure paths are continous
#observations are h,k,l,ei,ef<--> a2, a6, a3,a4, chi, phi
#Implement powder mode for tilt stage
#use a,b,c explicitly so can constrain to orthorhombic, cubic, etc.
#Refactor to use "a", "b" as stand-in for mu, nu, chi, phi??


#Generally, we shall work in a left handed coordinate system, in which clockwise (CW) rotations are positive.
#We shall define Q=ki-kf (as opposed to Q=kf-ki as used in Busing & Levy.
#We shall have possitive energy tranfer for neutron energy loss, that is dE=Ei-Ef
#For us, theta is theta_measured (aka Lumsden's 's')--that is, the actual rotation of the shaft about the z axis
#Should we just call it a3???



def e_to_k(e):
    k=np.sqrt(e/2.072)
    return k

def e_to_wavelength(e):
    wavelength=9.045/np.sqrt(e)
    return wavelength

def a2_to_k(a2,dspacing):
    taum=2*np.pi/dspacing
    k=taum/np.sqrt(2.0-2*np.cos(a2))
    return k


def calcq(H, K, L, stars):
    "Given reciprocal-space coordinates of a vector, calculate its coordinates in the Cartesian space."
    q = modvec(H, K, L, stars);
    return q
def calc_q_inelastic(ei,ef,tth):
    """
    Following the Lumsden formulation, calculate q.
    """    
    ki=e_to_k(ei)
    kf=e_to_k(ef)
    q=np.sqrt(ki**2+kf**2-2*ki*kf*np.cos(np.radians(tth)))
    return q

def calc_tth_inelastic(ei,ef,q):
    """
    Following the Lumsden formulation, calculate tth from q.
    """    
    ki=e_to_k(ei)
    kf=e_to_k(ef)
    cos2t=-(q**2-ki**2-kf**2)/(2*ki*kf)
    #if abs(cos2t) > 1, then scattering triangle doesn't close and we should raise an exception
    tth=np.arccos(cos2t)
    return np.degrees(tth)


def calc_th_inelastic(ei,ef,tth):
    """
    Following the Lumsden formulation, calculate th.  Tth is given in radians
    """
    ki=e_to_k(ei)
    kf=e_to_k(ef)    
    th=np.arctan2((ki-kf*np.cos(tth)),kf*np.sin(tth))
    return np.degrees(th)

def calc_om_inelastic(ei,ef,tth,theta):
    """
    Following the Lumsden formulation, calculate om.
    """
    om=theta-calc_th_inelastic(ei,ef,tth)
    #theta is the instrument theta
    return om

def scalar(x1, y1, z1, x2, y2, z2, stars):
    "calculates scalar product of two vectors"
    a = stars['astar']
    b = stars['bstar']
    c = stars['cstar']
    alpha = np.radians(stars['alphastar'])
    beta = np.radians(stars['betastar'])
    gamma = np.radians(stars['gammastar'])

    s=x1*x2*a**2+y1*y2*b**2+z1*z2*c**2+(x1*y2+x2*y1)*a*b*np.cos(gamma)+(x1*z2+x2*z1)*a*c*np.cos(beta)+(z1*y2+z2*y1)*c*b*np.cos(alpha)
    return s


def modvec(x, y, z, stars):
    "Calculates modulus of a vector defined by its fraction cell coordinates"
    "or Miller indexes"
    m=np.sqrt(scalar(x, y, z, x, y, z, stars))
    return m






def gen_rot_x(vu):
    """generate a matrix which rotates a vector about the x-axis in a clockwise (CW) fashion.  We shall assume that
    nu is in radians.
    """
    
    rotx=np.array([[1.0,0,0],
                   [0,np.cos(vu),-np.sin(vu)],
                   [0,np.sin(vu),np.cos(vu)]
                   ], 'Float64'
                  )
    return rotx

def gen_rot_y(mu):
    """generate a matrix which rotates a vector about the y-axis in a clockwise (CW) fashion.  We shall assume that
    mu is in radians.
    """
    
    roty=np.array([[np.cos(mu),0,np.sin(mu)],
                   [0,1,0],
                   [-np.sin(mu),0,np.cos(mu)]
                   ], 'Float64'
                  )
    return roty



def gen_rot_z(w):
    """generate a matrix which rotates a vector about the z-axis in a clockwise (CW) fashion.  We shall assume that
    w is in radians. 
    """
    
    rotz=np.array([[np.cos(w),-np.sin(w),0.0],
                   [np.sin(w),np.cos(w),0],
                   [0,0,1.0]
                   ], 'Float64'
                  )
    return rotz




def star(a,b,c,alpha,beta,gamma):
    "Calculate unit cell volume, reciprocal cell volume, reciprocal lattice parameters"
    alpha=np.radians(alpha)
    beta=np.radians(beta)
    gamma=np.radians(gamma)
    V=2*a*b*c*\
        np.sqrt(np.sin((alpha+beta+gamma)/2)*\
               np.sin((-alpha+beta+gamma)/2)*\
               np.sin((alpha-beta+gamma)/2)*\
               np.sin((alpha+beta-gamma)/2))
    Vstar=(2*np.pi)**3/V;
    astar=2*np.pi*b*c*np.sin(alpha)/V
    bstar=2*np.pi*a*c*np.sin(beta)/V
    cstar=2*np.pi*b*a*np.sin(gamma)/V
    alphastar=np.arccos((np.cos(beta)*np.cos(gamma)-\
                        np.cos(alpha))/ \
                       (np.sin(beta)*np.sin(gamma)))
    betastar= np.arccos((np.cos(alpha)*np.cos(gamma)-\
                        np.cos(beta))/ \
                       (np.sin(alpha)*np.sin(gamma)))
    gammastar=np.arccos((np.cos(alpha)*np.cos(beta)-\
                        np.cos(gamma))/ \
                       (np.sin(alpha)*np.sin(beta)))
    V=V
    alphastar=np.degrees(alphastar)
    betastar=np.degrees(betastar)
    gammastar=np.degrees(gammastar)
    return astar,bstar,cstar,alphastar,betastar,gammastar

def calcB(astar,bstar,cstar,alphastar,betastar,gammastar,c, alpha):
    "Calculates the B matrix using the crystal dimensions calculated in the 'star' method"
    alphastar = np.radians(alphastar)
    betastar = np.radians(betastar)
    gammastar = np.radians(gammastar)
    alpha = np.radians(alpha)

    Bmatrix=np.array([[astar, bstar*np.cos(gammastar), cstar*np.cos(betastar)],
                     [0, bstar*np.sin(gammastar), -cstar*np.sin(betastar)*np.cos(alpha)],
                     [0, 0, cstar]],'Float64') #check the third element
    #"cstarnp.sin(betastar)*np.sin(alpha)" for third element is equivalent
    return Bmatrix



def isInPlane(h1, h2, v,tol=1e-5):
    "Checks if vector v lies in the plane formed by vectors h1 and h2 by calculating the determinant."
    determinant = (h1[0]*h2[1]*v[2] - h1[0]*v[1]*h2[2] - h1[1]*h2[0]*v[2] + h1[1]*v[0]*h2[2] + h1[2]*h2[0]*v[1] - h1[2]*v[0]*h2[1])
    if np.abs(determinant-tol) > 0: #outside of tolerance
        return False
    else:
        return True
    
def make_orthonormal(o1, o2):
    """Given two vectors, creates an orthonormal set of three vectors. 
    Maintains the direction of o1 and the coplanarity of o1 and o2"""
    o1 = o1 / np.linalg.norm(o1)
    o2 = o2 / np.linalg.norm(o2)
    o3 = np.cross(o1, o2)
    o3 = o3 / np.linalg.norm(o3)
    o2 = np.cross(o3, o1)
    return o1, o2, o3

def calc_plane(p, h, k, l, normalize=True):
    o1 = np.array([p[0], p[1], p[2]])
    o2 = np.array([p[3], p[4], p[5]])
    if normalize:
        o1, o2, o3 = make_orthonormal(o1, o2)
    else:
        o3 = np.cross(o1, o2)
    A = np.array([o1, o2, o3]).T
    a_arr = []
    b_arr = []
    c_arr = []

    for i in range(len(h)):
        hkl = np.array([h[i], k[i], l[i]])
        sol = np.linalg.solve(A, hkl)
        a = sol[0]
        b = sol[1]
        c = sol[2]
        a_arr.append(a)
        b_arr.append(b)
        c_arr.append(c)
    return a_arr, b_arr, c_arr

def calculateLatticeParameters(UBmatrix):
    """
    Calculate lattice parameters from UB matrix
    """

    G = np.linalg.inv(np.dot(UBmatrix.T, UBmatrix))

    abc = np.sqrt(np.diag(G))
    a = abc[0]*2*np.pi
    b = abc[1]*2*np.pi
    c = abc[2]*2*np.pi

    alpha = np.degrees(np.arccos(G[1, 2]/b/c))
    beta = np.degrees(np.arccos(G[0, 2]/a/c))
    gamma = np.degrees(np.arccos(G[0, 1]/a/b))

    latticeParameters = {'a': a, 'b': b, 'c': c, 'alpha': alpha, 'beta': beta, 'gamma': gamma}
    return latticeParameters


def calcTwoTheta(h, stars, ei):
    """Calculates the twotheta value for a vector h with lattice parameters given. 
    Useful for finding observed reflections.  Assumes diffraction"""
    q = calcq (h[0], h[1], h[2], stars)
    wavelength=e_to_wavelength(ei)
    twotheta = np.degrees(2 * np.arcsin(wavelength * q / 4 / np.pi))
    return twotheta



def calc_om_elastic(h1,k1,l1,ei,th1,stars):
    q1=calcq(h1,k1,l1,stars)
    tth1=calcTwoTheta([h1,k1,l1],stars,ei)
    om1=th1-tth1/2.0    
    return om1

class UBCalc(object):
    def __init__(self):
        pass

    def calc_u_phi(self,omega,chi,phi):
        """
        Calculates u_phi using the rmatrix, we will assume that the angles we are given are in degrees.
        """
        r_matrix=self.generate_rmatrix(omega,chi,phi)
        u_phi=np.dot(np.linalg.inv(r_matrix),np.array([1.,0.,0.],'Float64'))
        #u1p = np.array([np.cos(omega1)*np.cos(chi1)*np.cos(phi1) - np.sin(omega1)*np.sin(phi1),
        #                   np.cos(omega1)*np.cos(chi1)*np.sin(phi1) + np.sin(omega1)*np.cos(phi1),
        #                   np.cos(omega1)*np.sin(chi1)],'Float64')
        #u2p = np.array([np.cos(omega2)*np.cos(chi2)*np.cos(phi2) - np.sin(omega2)*np.sin(phi2),
        #               np.cos(omega2)*np.cos(chi2)*np.sin(phi2) + np.sin(omega2)*np.cos(phi2),
        #               np.cos(omega2)*np.sin(chi2)],'Float64')
        #u3p = np.cross(u1p, u2p)   
        
        #u1p = np.cos(omega)*np.cos(chi)*np.cos(phi) - np.sin(omega)*np.sin(phi)
        #u2p = np.cos(omega)*np.cos(chi)*np.sin(phi) + np.sin(omega)*np.cos(phi)
        #u3p = np.cos(omega)*np.sin(chi)    
        return u_phi     
    
    def calc_hphi(self,phi,omega1,tth,chi,ei):
        #x vector are the intial estimates
        #phi = x[1]
        #omega1 = x[2]
        #omega2 = x[3]
        theta1 = tth/2
        hphi=np.array([0,0,0],'Float64')
        q=calc_q_inelastic(ei,ei,tth)
        u1=self.calc_u_phi(omega1,chi,phi)
        hphi[0]=q * u1[0]
        hphi[1]=q * u1[1]
        hphi[2]=q * u1[2]
        return hphi    
    
    def calcUB (self,*args):
        Umatrix = self.calcU(*args)
        UBmatrix = np.dot(Umatrix, args[-1])
        return UBmatrix
    
    def calcU(self):
        pass
    
    def generate_rmatrix(self,omega,chi,phi,scattering_sense_omega=-1,scattering_sense_chi=1, scattering_sense_phi=-1):
        pass



# *********************************** START - calculations for bisecting mode  *********************************** 

class StrategyBisectingMode(object):
    def __init__(self):
        pass

    def calcIdealAngles(self,h, UBmatrix, Bmatrix, stars):
        "Calculates the remaining angles with omega given as 0"
        "Returns (twotheta, theta, omega, chi, phi)"
        '''myUBmatrix=np.array([[ -0.8495486120866541,0.8646150711829229,-1.055554030805845],
                         [-0.7090402876860106,0.7826211792587279,1.211714627203656],
                         [1.165768160358335,1.106088263216144,-0.03224481098900243]],'Float64')
       '''
        #hp = np.dot(UBmatrix, h[0:2])
        hp=np.dot(UBmatrix,h[:,0:3].T)
        ei=h[:,3]
        ef=h[:,4]
        #probably need to consider scattering sense here...
        #also, we must get the sign, sign correct
        phi = np.degrees(np.arctan2(hp[1], hp[0]))
        chi = np.degrees(np.arctan2(hp[2], np.sqrt(hp[0]**2 + hp[1]**2)))
    
        q = calcq(h[:,0], h[:,1], h[:,2], stars)
        #twotheta = np.degrees(2 * np.arcsin(wavelength * q / 4 / np.pi))
        twotheta= calc_tth_inelastic(ei,ef,q)
        theta = twotheta / 2.0  
        omega = 0
    
        #print 'chi',chi, 180-chi
        #print 'phi',phi, 180+phi
        results={'twotheta':twotheta,
                 'theta':theta,
                 'omega':omega,
                 'chi':chi,
                 'phi':phi
                 }
        return results

# *********************************** END - calculations for bisecting mode  *********************************** 
    

# ********************************* START - calculations for scattering plane mode  ********************************* 

class StrategyScatteringPlane(object):
    def __init__(self):
        pass
    def calcIdealAngles(self,desiredh, chi, phi, UBmatrix, stars,ubcalc):
        "Calculates the twotheta, theta, and omega values for a desired h vector. Uses chi and phi from calcScatteringPlane."
        #Accepts the desired h vector, chi, phi, the UB matrix, the wavelength, and the stars dictionary
    
        desiredhp = np.dot(UBmatrix, desiredh[0:3])
    
        #Old code (scipy.optimize.fsolve) produced inaccurate results with far-off estimates
        #solutions = scipy.optimize.fsolve(equations, x0, args=(h1p, h2p, wavelength)) 
    
        q = calcq (desiredh[0], desiredh[1], desiredh[2], stars)
    
        #twotheta = 2.0 * np.arcsin(wavelength * q / 4.0 / np.pi)
    
        ei=desiredh[3]
        ef=desiredh[4]
        #q=calc_q_inelastic(ei,ef,desiredh[0],desiredh[1],desiredh[2])
        twotheta=calc_tth_inelastic(ei,ef,q)
    
        x0 = [0.0]
        p = SNLE(self.secondequations, x0, args=(desiredhp, chi, phi, ei, twotheta,ubcalc))
        r = p.solve('nlp:ralg')
        omega = r.xf[0]
        #theta = twotheta/2.0 + omega   # ------ ALTERNATE SOLUTION FOR THETA ------
    
        #theta=calc_th_inelastic(ei,ef,np.radians(twotheta))
        
        theta=twotheta/2.0+omega
    
        #theta = r.xf[1]  # ------ SOLVER POTENTIALLY INACCURATE FOR THETA ------
    
    
        solutions = [twotheta, theta, omega]
        return solutions #% 360
        #returns an array of 3 angles [twotheta, theta, omega]



    def secondequations(self,x, hp, chi, phi, ei,tth,ubcalc):
        #theta = x[0]
        #omega = x[1]
        omega=x[0]
        theta=tth/2
        q=calc_q_inelastic(ei,ei,tth)
        u1=ubcalc.calc_u_phi(omega,chi,phi)
        outvec=[hp[0] - (q/(2*np.pi)) * u1[0],
                hp[1] - (q/(2*np.pi)) * u1[1],
                hp[2] - (q/(2*np.pi)) * u1[2]]
        return outvec    



class UBCalcEulerian(UBCalc):
    def __init__(self):
        pass
    

    def generate_rmatrix(self,omega,chi,phi,scattering_sense_omega=-1,scattering_sense_chi=1, scattering_sense_phi=-1):
        """
        generate the r-matrix given omega, chi, and phi in degrees. -1 denotes left handed
        """
        Chi=gen_rot_y(np.radians(chi)*scattering_sense_chi)
        Phi=gen_rot_z(np.radians(phi)*scattering_sense_phi)
        Omega=gen_rot_z(np.radians(omega)*scattering_sense_omega)
        rmatrix=np.dot(np.dot(Omega,Chi),Phi)
        
        return rmatrix
    
    def calcU(self,h1, k1, l1, h2, k2, l2, omega1, chi1, phi1, omega2, chi2, phi2, Bmatrix):
        "Calculates the UB matrix using 2 sets of observations (h#, k#, l#) and their respective angle measurements in degrees (omega#, chi#, phi#)"
        #Convertiung angles given in degrees to radians
        #omega1 = np.radians(omega1)
        #chi1 = np.radians(chi1)
        #phi1 = np.radians(phi1)
        #omega2 = np.radians(omega2)
        #chi2 = np.radians(chi2)
        #phi2 = np.radians(phi2)
    
        hmatrix1 = np.array([h1, k1, l1])
        hmatrix2 = np.array([h2, k2, l2])
        h1c = np.dot(Bmatrix, hmatrix1) 
        h2c = np.dot(Bmatrix, hmatrix2)
        h3c = np.cross(h1c, h2c)
    
        ''' Making the orthogonal unit-vectors t#c:
       t1c is parallel to h1c
       t3c is orthogonal to both t1c and t2c, and thus is parallel to h3c
       t2c must be orthogonal to both t1c and t2c
       '''
        t1c = h1c / np.sqrt(np.power(h1c[0], 2) + np.power(h1c[1], 2) + np.power(h1c[2], 2))
        t3c = h3c / np.sqrt(np.power(h3c[0], 2) + np.power(h3c[1], 2) + np.power(h3c[2], 2))
        t2c = np.cross(t3c, t1c)
        Tc = np.array([t1c, t2c, t3c]).T
        #realU=np.array([[ -5.28548868e-01,   8.65056241e-17,  -6.63562568e-16],
        #               [ -0.00000000e+00,   4.86909792e-01,   2.90030482e-16],
        #               [  0.00000000e+00,   0.00000000e+00,  -1.26048191e-01]])
    
        #calculating u_phi 
        
        
        #u1p = np.array([np.cos(omega1)*np.cos(chi1)*np.cos(phi1) - np.sin(omega1)*np.sin(phi1),
        #              np.cos(omega1)*np.cos(chi1)*np.sin(phi1) + np.sin(omega1)*np.cos(phi1),
        #               np.cos(omega1)*np.sin(chi1)],'Float64')
        #u2p = np.array([np.cos(omega2)*np.cos(chi2)*np.cos(phi2) - np.sin(omega2)*np.sin(phi2),
        #               np.cos(omega2)*np.cos(chi2)*np.sin(phi2) + np.sin(omega2)*np.cos(phi2),
        #               np.cos(omega2)*np.sin(chi2)],'Float64')
        u1p=self.calc_u_phi(omega1,chi1,phi1)
        u2p=self.calc_u_phi(omega2,chi2,phi2)
        u3p = np.cross(u1p, u2p)
    
        ''' Making orthogonal unit-vectors t#p
       Tp should be exactaly superimposed on Tc
       t#p is created the same way t#c was, except using u#p instead of h#c
       '''
        t1p = u1p / np.sqrt(u1p[0]**2 + u1p[1]**2 + u1p[2]**2)
        t3p = u3p / np.sqrt(u3p[0]**2 + u3p[1]**2 + u3p[2]**2)
        t2p = np.cross(t3p, t1p)
        Tp = np.array([t1p, t2p, t3p],'Float64').T
    
        #calculating the UB matrix
        Umatrix = np.dot(Tp, Tc.T) 
        #UBmatrix = np.dot(Umatrix, Bmatrix)
        return Umatrix     
    
    # ******************************* STAR - METHODS FOR REFINING THE UB MATRIX ******************************* 
    def calcRefineUB(self,observations,stars_dict):
        #observations are an array of dictionaries for each observed reflection
        #These can be taken at different energies, but should be elastic
        hvectors = []
        Uv = []
        omt=[]
        for i in range(0, len(observations)):
            h = np.array([observations[i]['h'], observations[i]['k'], observations[i]['l']],'Float64')
            hvectors.append(h)
    
            '''
            sys.stderr.write('i %3.4f \n'%(observations[i]['h'],))
            sys.stderr.write('i %3.4f \n'%(observations[i]['k'],))
            sys.stderr.write('i %3.4f \n'%(observations[i]['l'],))
            sys.stderr.write('i %3.4f \n'%(observations[i]['twotheta'],))
            sys.stderr.write('i %3.4f \n'%(observations[i]['theta'],))
            sys.stderr.write('i %3.4f \n'%(observations[i]['chi'],))
            sys.stderr.write('i %3.4f \n'%(observations[i]['phi'],))
            '''
    
            theta =(observations[i]['theta'])  #For us, theta is theta measured (or Lumsden's 's')
            chi = (observations[i]['chi'])
            phi = (observations[i]['phi'])
            twotheta = (observations[i]['twotheta'])
            ei=observations[i]['ei']
            ef=observations[i]['ei']  #reflections are elastic!!!!
            #omega = theta - twotheta/2.0  #diffraction...
            omega=calc_om_elastic(h[0],h[1],h[2],ei,theta,stars_dict)
            #omega=calc_om_inelastic(ei,ef,twotheta)
            u1_phi=self.calc_u_phi(omega,chi,phi)
            u1p,u2p,u3p=u1_phi
            omt.append(omega)
            #u1p = np.cos(omega)*np.cos(chi)*np.cos(phi) - np.sin(omega)*np.sin(phi)
            #u2p = np.cos(omega)*np.cos(chi)*np.sin(phi) + np.sin(omega)*np.cos(phi)
            #u3p = np.cos(omega)*np.sin(chi)
                    
            #reflections are elastic
            q=calc_q_inelastic(ei,ei,twotheta)
            #uv1p=q*u1p
            #uv2p=q*u2p
            #uv3p=q*u3p
            
            #uv1p = 2.0*np.sin(twotheta/2) / wavelength * u1p
            #uv2p = 2.0*np.sin(twotheta/2) / wavelength * u2p
            #uv3p = 2.0*np.sin(twotheta/2) / wavelength * u3p
            
            uv1p=(q/(2*np.pi))*u1p
            uv2p=(q/(2*np.pi))*u2p
            uv3p=(q/(2*np.pi))*u3p
            #h1p[0] - (q1/(2*np.pi)) * u1[0]
            Uv.append(uv1p)
            Uv.append(uv2p)
            Uv.append(uv3p)
    
        x0 = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        p = SNLE(self.UBRefinementEquations, x0, args=(hvectors, Uv))#,contol=1e-15, ftol=1e-15,maxFunEvals=1e8,maxIter=1e5)
        r = p.solve('nlp:ralg')
    
        a = r.xf[0]
        b = r.xf[1]
        c = r.xf[2]
        d = r.xf[3]
        e = r.xf[4]
        f = r.xf[5]
        g = r.xf[6]
        h = r.xf[7]
        j = r.xf[8]
    
        UB = 2*np.pi*np.array([[a, b, c], [d, e, f], [g, h, j]],'Float64')
    
        return UB    

    def UBRefinementEquations(self,x, h, Uv):
        #x vector are the intial estimates
        #UB matrix will be:
        '''      (a d e)
                 (d b f)
                 (e f c)
        '''
        #h is an array of h vectors (arrays): [[h,k,l], [h,k,l],...]
        #Uv is an array of all of the u_phi vectors' elements sequentially: [up11, up12, up13, up21,...upn1, upn2, upn3] 
        a = x[0]
        b = x[1]
        c = x[2]
        d = x[3]
        e = x[4]
        f = x[5]
        g = x[6]
        j = x[7]
        k = x[8]
    
        UB = np.array([[a, b, c], [d, e, f], [g, j, k]], 'Float64')
    
        outvec = []
    
        for i in range(0, len(h)):
            #sys.stderr.write('i %d\n'%(i,))
            #sys.stdout.write('i %d\n'%(i,))
            outvec.append(np.dot(UB, h[i])[0] - Uv[3*i])
            outvec.append(np.dot(UB, h[i])[1] - Uv[3*i + 1])
            outvec.append(np.dot(UB, h[i])[2] - Uv[3*i + 2])   
    
        return outvec
    
    
    # ******************************* END - METHODS FOR REFINING THE UB MATRIX *******************************    
    def calcScatteringPlane(self,h1, h2, UBmatrix, ei,stars):
        "Returns the chi and phi for the scattering plane defined by h1 and h2. Used with calcIdealAngles2."
        #Accepts two scattering plane vectors, h1 and h2, the UB matrix, and the wavelength
        #Should we allow the scattering plane to be defined by two vectors at different energies?
        #For now, I say NoN
        
        h1p = np.dot(UBmatrix, h1)
        h2p = np.dot(UBmatrix, h2)
    
        x0 = [0.0, 0.0, 0.0, 0.0]
        wavelength=e_to_wavelength(ei)
        q1 = calcq (h1[0], h1[1], h1[2], stars)
        twotheta1 = np.degrees(2.0 * np.arcsin(wavelength * q1 / 4.0 / np.pi))
        q2 = calcq (h2[0], h2[1], h2[2], stars)
        twotheta2 = np.degrees(2.0 * np.arcsin(wavelength * q2 / 4.0 / np.pi))
        
        
        if 1:
            #original openopt
            #outp=self.scatteringEquations([45,90,-90,0],h1p, h2p, q1, q2,wavelength,twotheta1/2,twotheta2/2)
            p0 = SNLE(self.scatteringEquations, x0, args=(h1p, h2p, q1, q2),contol=1e-15, ftol=1e-15,maxFunEvals=1e8,maxIter=1e5)
            r0 = p0.solve('nlp:ralg')
            #outp=self.scatteringEquations(r0.xf,h1p, h2p, q1, q2,wavelength,twotheta1/2,twotheta2/2)
            
        
            chi = r0.xf[0] #xf is the final array, xf[0] = chi
            phi = r0.xf[1] #                       xf[1] = phi
        if 0:
            import bumps
            from bumps.fitters import FIT_OPTIONS, FitDriver, DreamFit, StepMonitor, ConsoleMonitor
            import bumps.modelfn, bumps.fitproblem
            fn=lambda chi,phi,omega1,omega2: np.linalg.norm(self.scatteringEquations([chi,phi,omega1,omega2], h1p, h2p,q1,q2))
            print fn(chi=45, phi=72.4, omega1=-90, omega2=0)
            M=bumps.modelfn.ModelFunction(fn,chi=0.0,phi=0.0,omega1=0.0,omega2=0.0)
            M._parameters['chi'].range(30,60.)
            M._parameters['phi'].range(0,90.)
            M._parameters['omega1'].range(-90,90.)
            M._parameters['omega2'].range(-90,90.)
            problem=bumps.fitproblem.FitProblem(M)
            fitdriver = FitDriver(DreamFit, problem=problem, burn=1000)
            best, fbest = fitdriver.fit()
            print best,fbest
            print 'done'
        
        print 'chi, phi', chi, phi
        return chi, phi   
    
    def scatteringEquations(self,x, h1p, h2p,q1,q2):
        #x vector are the intial estimates
        chi = x[0]
        phi = x[1]
        omega1 = x[2]
        omega2 = x[3]
        #theta1 = tth1/2
        #theta2 = tth2/2
        #q=2.0/wavelength * np.sin(theta1)
        #q1=calc_q_inelastic(ei1,ef1,tth1)
        #q2=calc_q_inelastic(ei2,ef2,tth2)
        u1=self.calc_u_phi(omega1,chi,phi)
        u2=self.calc_u_phi(omega2,chi,phi)
        
        outvec=[h1p[0] - (q1/(2*np.pi)) * u1[0],
                h1p[1] - (q1/(2*np.pi)) * u1[1],
                h1p[2] - (q1/(2*np.pi)) * u1[2],
                h2p[0] - (q2/(2*np.pi)) * u2[0],
                h2p[1] - (q2/(2*np.pi)) * u2[1],
                h2p[2] - (q2/(2*np.pi)) * u2[2]]  
        #chi,phi,omega1,omega2, theta1,theta2=np.radians([chi,phi,omega1,omega2, theta1,theta2])
        #outvec=[h1p[0] - 2.0/wavelength * np.sin(theta1) * (np.cos(omega1)*np.cos(chi)*np.cos(phi) - np.sin(omega1)*np.sin(phi)),
        #        h1p[1] - 2.0/wavelength * np.sin(theta1) * (np.cos(omega1)*np.cos(chi)*np.sin(phi) + np.sin(omega1)*np.cos(phi)),
        #        h1p[2] - 2.0/wavelength * np.sin(theta1) * np.cos(omega1)*np.sin(chi),
        #        h2p[0] - 2.0/wavelength * np.sin(theta2) * (np.cos(omega2)*np.cos(chi)*np.cos(phi) - np.sin(omega2)*np.sin(phi)),
        #        h2p[1] - 2.0/wavelength * np.sin(theta2) * (np.cos(omega2)*np.cos(chi)*np.sin(phi) + np.sin(omega2)*np.cos(phi)),
        #        h2p[2] - 2.0/wavelength * np.sin(theta2) * np.cos(omega2)*np.sin(chi)]          
        return outvec    


class UBCalcTilt(UBCalc):
    def __init__(self):
        pass
    def generate_rmatrix(self,omega,mu,nu,scattering_sense_omega=1,scattering_sense_mu=1, scattering_sense_nu=1):
        """
        generate the r-matrix given omega, chi, and phi in radians.
        """
        M=gen_rot_y(np.radians(mu)*scattering_sense_mu)
        N=gen_rot_x(np.radians(nu)*scattering_sense_nu)
        Omega=gen_rot_z(np.radians(omega)*scattering_sense_omega)
        rmatrix=np.dot(np.dot(Omega,M),N)
        
        return rmatrix
    def calc_u_phi(self,omega,mu,nu):
            """
            Calculates u_phi using the rmatrix, we will assume that the angles we are given are in degrees.
            """
            r_matrix=self.generate_rmatrix(omega,mu,nu)
            u_phi=np.dot(np.linalg.inv(r_matrix),np.array([1.,0.,0.],'Float64'))
            #u1p = np.array([np.cos(omega1)*np.cos(chi1)*np.cos(phi1) - np.sin(omega1)*np.sin(phi1),
            #                   np.cos(omega1)*np.cos(chi1)*np.sin(phi1) + np.sin(omega1)*np.cos(phi1),
            #                   np.cos(omega1)*np.sin(chi1)],'Float64')
            #u2p = np.array([np.cos(omega2)*np.cos(chi2)*np.cos(phi2) - np.sin(omega2)*np.sin(phi2),
            #               np.cos(omega2)*np.cos(chi2)*np.sin(phi2) + np.sin(omega2)*np.cos(phi2),
            #               np.cos(omega2)*np.sin(chi2)],'Float64')
            #u3p = np.cross(u1p, u2p)   
            
            #u1p = np.cos(omega)*np.cos(chi)*np.cos(phi) - np.sin(omega)*np.sin(phi)
            #u2p = np.cos(omega)*np.cos(chi)*np.sin(phi) + np.sin(omega)*np.cos(phi)
            #u3p = np.cos(omega)*np.sin(chi)    
            return -u_phi   
        
    def calc_R_plane(self,mu_plane, nu_plane,UB,Q_vec):
        """Calculates R for a scattering plane with specified mu,nu
        
        """
        # This is N^(-1)M^(-1) * [0,0,1]'
        u_nu_perp=np.array([-np.sin(np.degrees(mu_plane)),
                            np.cos(np.degrees(mu_plane))*np.sin(np.degrees(nu_plane)),
                            np.cos(np.degrees(mu_plane))*np.cos(np.degrees(nu_plane))]
                           ,'Float64')
        Q_nu=np.dot(UB,Q_vec)
        u1_nu=Q_nu/np.linalg.norm(Q_nu)  #unit vector along q
        u2_nu=np.cross(u_nu_perp,u1_nu)
        
        #There is a 
        
        t1_nu=u1_nu
        t2_nu=u2_nu
        t3_nu=np.cross(t1_nu, t2_nu)
        T_nu=np.array([t1_nu, t2_nu,t3_nu],'Float64').T
        #the t_i form the columns of the T matrix
        R=np.linalg.inv(T_nu)
        return R
    
    def calc_angles(self,mu_plane,nu_plane,UB,Q_vec,ei,ef):
        """
        Calculate the angles for the spectrometer.  mu_plane and nu_plane give the mu and nu for
        the desired plane.  To keep the tilts flat, choose mu=nu=0.  The more general case is useful if
        we try to keep the spectrometer close to the specified plane if for example, the first two orientation vectors
        were slightly out of the plane.
        """
        
        R=self.calc_R_plane(mu_plane, nu_plane,UB,Q_vec)
        #Here, we will follow the approach of Mark Koennecke's tasub, rather than Mark Lumsden
        #becasue using arctan2, we can determine the sign
        #TODO:  check that the following are not inverted:
        #sgu-->upper tilt-->nu_plane  
        #sgl-->lower tilt-->mu_plane
        
        sgu=np.degrees(np.arctan2(R[2][1],R[2][2]))
        
        # R[2][1]= cos(sgl)sin(sgu)
        # R[2][2]= cos(sgu)cos(sgl)
        
        om=np.degrees(np.arctan2(R[1][0],R[0][0]))
        #R[1][0]= sin(om)cos(sgl)
        #R[0][0]= cos(om)cos(sgl)
        
        sgl=np.degrees(np.arcsin(-R[2][0]))
        
        QC=np.dot(UB,Q_vec)
        q=np.linalg.norm(QC)#*2.0*np.pi
        
        tth=calc_tth_inelastic(ei,ef,q) #should multiply by scattering sense
        theta=calc_th_inelastic(ei,ef,np.radians(tth))
        a3=om+theta
        
        #next, check to make sure that a3 in [-180,180]
        
        a3=a3-180 #shift the whole range
        if a3 < -180:
            a3=a3+360
        angles={}
        angles['a3']=a3
        angles['om']=om
        angles['tth']=tth
        angles['mu']=sgl
        angles['nu']=sgu
        return angles
        
        
    def calcU(self,h1, k1, l1, h2, k2, l2, omega1, mu1, nu1, omega2, mu2, nu2, Bmatrix):
            "Calculates the UB matrix using 2 sets of observations (h#, k#, l#) and their respective angle measurements in degrees (omega#, chi#, phi#)"
            #Convertiung angles given in degrees to radians
            #omega1 = np.radians(omega1)
            #chi1 = np.radians(chi1)
            #phi1 = np.radians(phi1)
            #omega2 = np.radians(omega2)
            #chi2 = np.radians(chi2)
            #phi2 = np.radians(phi2)
        
            hmatrix1 = np.array([h1, k1, l1])
            hmatrix2 = np.array([h2, k2, l2])
            h1c = np.dot(Bmatrix, hmatrix1) 
            h2c = np.dot(Bmatrix, hmatrix2)
            h3c = np.cross(h1c, h2c)
        
            ''' Making the orthogonal unit-vectors t#c:
           t1c is parallel to h1c
           t3c is orthogonal to both t1c and t2c, and thus is parallel to h3c
           t2c must be orthogonal to both t1c and t2c
           '''
            t1c = h1c / np.sqrt(np.power(h1c[0], 2) + np.power(h1c[1], 2) + np.power(h1c[2], 2))
            t3c = h3c / np.sqrt(np.power(h3c[0], 2) + np.power(h3c[1], 2) + np.power(h3c[2], 2))
            t2c = np.cross(t3c, t1c)
            Tc = np.array([t1c, t2c, t3c]).T
            #realU=np.array([[ -5.28548868e-01,   8.65056241e-17,  -6.63562568e-16],
            #               [ -0.00000000e+00,   4.86909792e-01,   2.90030482e-16],
            #               [  0.00000000e+00,   0.00000000e+00,  -1.26048191e-01]])
        
            #calculating u_phi 
            
            
            #u1p = np.array([np.cos(omega1)*np.cos(chi1)*np.cos(phi1) - np.sin(omega1)*np.sin(phi1),
            #              np.cos(omega1)*np.cos(chi1)*np.sin(phi1) + np.sin(omega1)*np.cos(phi1),
            #               np.cos(omega1)*np.sin(chi1)],'Float64')
            #u2p = np.array([np.cos(omega2)*np.cos(chi2)*np.cos(phi2) - np.sin(omega2)*np.sin(phi2),
            #               np.cos(omega2)*np.cos(chi2)*np.sin(phi2) + np.sin(omega2)*np.cos(phi2),
            #               np.cos(omega2)*np.sin(chi2)],'Float64')
            u1p=self.calc_u_phi(omega1,mu1,nu1)
            u2p=self.calc_u_phi(omega2,mu2,nu2)
            u3p = np.cross(u1p, u2p)
        
            ''' Making orthogonal unit-vectors t#p
           Tp should be exactaly superimposed on Tc
           t#p is created the same way t#c was, except using u#p instead of h#c
           '''
            t1p = u1p / np.sqrt(u1p[0]**2 + u1p[1]**2 + u1p[2]**2)
            t3p = u3p / np.sqrt(u3p[0]**2 + u3p[1]**2 + u3p[2]**2)
            t2p = np.cross(t3p, t1p)
            Tp = np.array([t1p, t2p, t3p],'Float64').T
        
            #calculating the UB matrix
            Umatrix = np.dot(Tp, Tc.T) 
            #UBmatrix = np.dot(Umatrix, Bmatrix)
            return Umatrix    


class StrategyFlatPlane(object):
    def __init__(self):
        pass
    def calcIdealAngles(self,desiredh, chi, phi, UBmatrix, stars,ubcalc):
        "Calculates the twotheta, theta, and omega values for a desired h vector. Uses chi and phi from calcScatteringPlane."
        #Accepts the desired h vector, chi, phi, the UB matrix, the wavelength, and the stars dictionary
    
        desiredhp = np.dot(UBmatrix, desiredh[0:3])
    
        #Old code (scipy.optimize.fsolve) produced inaccurate results with far-off estimates
        #solutions = scipy.optimize.fsolve(equations, x0, args=(h1p, h2p, wavelength)) 
    
        q = calcq (desiredh[0], desiredh[1], desiredh[2], stars)
    
        #twotheta = 2.0 * np.arcsin(wavelength * q / 4.0 / np.pi)
    
        ei=desiredh[3]
        ef=desiredh[4]
        #q=calc_q_inelastic(ei,ef,desiredh[0],desiredh[1],desiredh[2])
        twotheta=calc_tth_inelastic(ei,ef,q)
    
        x0 = [0.0]
        p = SNLE(self.secondequations, x0, args=(desiredhp, chi, phi, ei, twotheta,ubcalc))
       




# *********************************** START - calculations for phi fixed mode  *********************************** 
def calcIdealAngles3 (h, UBmatrix, wavelength, phi, stars):
    "Calculates the chi and theta for a desired vector h in the fixed phi mode."
    #Accepts ta desired vector h, the UB matrix, the wavelength, and the fixed phi
    hp = np.dot(UBmatrix, h)
    q = calcq (h[0], h[1], h[2], stars)
    twotheta = 2 * np.arcsin(wavelength * q / 4 / np.pi)

    x0 = [0.0, 0.0]
    p0 = NLSP(phiEquations, x0, args=(hp, wavelength, phi,twotheta))
    r0 = p0.solve('nlp:ralg')

    #r0.xf is the final array   
    twotheta=np.degrees(twotheta)
    chi = np.degrees(r0.xf[0])    # xf[0] = chi
    omega = np.degrees(r0.xf[1])  # xf[1] = omega
    theta = twotheta/2.0 + omega


    return twotheta, theta, omega, chi


def phiEquations(x, h1p, ei, phi,tth):
    #x vector are the intial estimates
    chi = x[0]
    omega1 = x[1]
    theta1=tth/2
    q=calc_q_inelastic(ei,ei,tth1)
    u1=calc_u_phi_eulerian(omega1,chi,phi)
    outvec=[h1p[0] - q * u1[0],
            h1p[1] - q * u1[1],
            h1p[2] - q * u1[2]]

    return outvec

# *********************************** END - calculations for phi fixed mode  *********************************** 







# **************************************** UB MATRIX TESTING CODE ****************************************

def UBtestrun():
    "Test method to calculate UB matrix given input"
    #a, b, c, alpha, beta, gamma, h1, k1, l1, omega1, chi1, phi1, h2, k2, l2, omega2, chi2, phi2 = input('enter data: ')
    #Test data:
    #3.9091,3.9091,3.9091,90,90,90,1,1,0,0,89.62,.001,0,0,1,0,-1.286,131.063
    #maybe: 3.9091,3.9091,3.9091,90,90,90,1,1,0,-1.855,89.62,.001,0,0,1,-.0005,-1.286,131.063
    #Should yield:
    a, b, c, alpha, beta, gamma, h1, k1, l1, omega1, chi1, phi1, h2, k2, l2, omega2, chi2, phi2=3.9091,3.9091,3.9091,90,90,90,1,1,0,0,89.62,.001,0,0,1,0,-1.286,131.063
    #a, b, c, alpha, beta, gamma, h1, k1, l1, omega1, chi1, phi1, h2, k2, l2, omega2, chi2, phi2=3.9091,3.9091,3.9091,90,90,90,1,1,0,0,0,0,\
    # 1,-1,0,0,0,90
    '''
   UB["0"] = -0.8495486120866541
   UB["1"] = 0.8646150711829229
   UB["2"] = -1.055554030805845
   UB["3"] = -0.7090402876860106
   UB["4"] = 0.7826211792587279
   UB["5"] = 1.211714627203656
   UB["6"] = 1.165768160358335
   UB["7"] = 1.106088263216144
   UB["8"] = -0.03224481098900243
   '''

#   astar, bstar, cstar, alphastar, betastar, gammastar = star(a, b, c, alpha, beta, gamma)
#   stars = astar, bstar, cstar, alphastar, betastar, gammastar
#   Bmatrix = calcB(astar, bstar, cstar, alphastar, betastar, gammastar, c, alpha)
    stars = star(a, b, c, alpha, beta, gamma)
    Bmatrix = calcB(*(list(stars)+[c, alpha]))
    U = calcU(h1, k1, l1, h2, k2, l2, omega1, chi1, phi1, omega2, chi2, phi2, Bmatrix)
    UB=calcUB(h1, k1, l1, h2, k2, l2, omega1, chi1, phi1, omega2, chi2, phi2, Bmatrix)
    stars_dict = dict(zip(('astar','bstar','cstar','alphastar','betastar','gammastar'),
                          stars))
    onehkl = lambda i: calcIdealAngles(np.array(i,'Float64'), UB,Bmatrix, 2.35916, stars_dict)
    allhkl = lambda hkl: [onehkl(i) for i in hkl]
    #h, UBmatrix, Bmatrix, wavelength, stars
    hv1=[1,0,0]
    hv2=[0,1,0]
    #result = calcIdealAngles2(hv1, hv2, UB, 2.35916)
    print UB
    return allhkl
    #print result
    #print 'chi',(180-result[0])%360
    #print 'phi',(result[1]+180)%360
    
    
    
def UBtest2():
    "Test method to calculate UB matrix given input"
    #a, b, c, alpha, beta, gamma, h1, k1, l1, omega1, chi1, phi1, h2, k2, l2, omega2, chi2, phi2 = input('enter data: ')
    #Test data:
    #3.9091,3.9091,3.9091,90,90,90,1,1,0,0,89.62,.001,0,0,1,0,-1.286,131.063
    #maybe: 3.9091,3.9091,3.9091,90,90,90,1,1,0,-1.855,89.62,.001,0,0,1,-.0005,-1.286,131.063
    #Should yield:
    a, b, c, alpha, beta, gamma=3.9091,3.9091,3.9091,90.0,90.,90.
    h1, k1, l1, th1, chi1, phi1, ei1, ef1=1.,0.,0.,    0.,0.,0., 14.7, 14.7
    h2, k2, l2, th2, chi2, phi2, ei2, ef2=0.,1.,0.,    0.,0.,90.,14.7, 14.7
    #a, b, c, alpha, beta, gamma, h1, k1, l1, omega1, chi1, phi1, h2, k2, l2, omega2, chi2, phi2=3.9091,3.9091,3.9091,90,90,90,1,1,0,0,0,0,\
    # 1,-1,0,0,0,90
    '''
   UB["0"] = -0.8495486120866541
   UB["1"] = 0.8646150711829229
   UB["2"] = -1.055554030805845
   UB["3"] = -0.7090402876860106
   UB["4"] = 0.7826211792587279
   UB["5"] = 1.211714627203656
   UB["6"] = 1.165768160358335
   UB["7"] = 1.106088263216144
   UB["8"] = -0.03224481098900243
   '''

#   astar, bstar, cstar, alphastar, betastar, gammastar = star(a, b, c, alpha, beta, gamma)
#   stars = astar, bstar, cstar, alphastar, betastar, gammastar
#   Bmatrix = calcB(astar, bstar, cstar, alphastar, betastar, gammastar, c, alpha)
    stars = star(a, b, c, alpha, beta, gamma)
    Bmatrix = calcB(*(list(stars)+[c, alpha]))
    
    stars_dict = dict(zip(('astar','bstar','cstar','alphastar','betastar','gammastar'),
                          stars))
    ubcalc=UBCalcEulerian()
    om1=calc_om_elastic(h1,k1,l1,ei1,th1,stars_dict)
    om2=calc_om_elastic(h2,k2,l2,ei2,th2,stars_dict)
    
    U = ubcalc.calcU(h1, k1, l1, h2, k2, l2, om1, chi1, phi1, om2, chi2, phi2, Bmatrix)
    UB=ubcalc.calcUB(h1, k1, l1, h2, k2, l2, om1, chi1, phi1, om2, chi2, phi2, Bmatrix)    
    #onehkl = lambda i: calcIdealAngles(np.array(i,'Float64'), UB,Bmatrix, 2.35916, stars_dict)
    #allhkl = lambda hkl: [onehkl(i) for i in hkl]
    #h, UBmatrix, Bmatrix, wavelength, stars
    
    #result = calcIdealAngles2(hv1, hv2, UB, 2.35916)
    print UB
    sb=StrategyBisectingMode()
    hin=np.array([[1,1,0,14.7,14.7]],'Float64')
    results=sb.calcIdealAngles(hin,UB,Bmatrix,stars_dict)
    print results
    
    #scattering plane
    hv1=np.array([1,0,0],'Float64')
    hv2=np.array([0,1,1],'Float64') 
    ei=14.7
    
    chi,phi=ubcalc.calcScatteringPlane(hv1, hv2, UB, ei,stars_dict)
    print chi, phi
    ssp=StrategyScatteringPlane()
    results=ssp.calcIdealAngles(np.array([1,1,1,14.7,14.7],'Float64'), chi, phi, UB, stars_dict,ubcalc)
    print results
    observations=[]
    observed=[[1.,0.,0.,    35.125,0.,0.,0., 14.7, 14.7],
         [0.,1.,0.,    35.125,0.,0.,90.,14.7, 14.7],
         [1.,1.,1,     63.0204,-3.754,45.0,72.43711, 14.7, 14.7]
         ]

    
    for obs in observed:
        observation={}
        observation['h']=obs[0]
        observation['k']=obs[1]
        observation['l']=obs[2]
        observation['twotheta']=obs[3]
        observation['theta']=obs[4]
        observation['chi']=obs[5]
        observation['phi']=obs[6]
        observation['ei']=obs[7]
        observation['ef']=obs[8]
        observations.append(observation)
    
    #h1, k1, l1, th1, chi1, phi1, ei1, ef1=1.,0.,0.,    0.,0.,0., 14.7, 14.7
    #h2, k2, l2, th2, chi2, phi2, ei2, ef2=0.,1.,0.,    0.,0.,90.,14.7, 14.7        
    #h3, k3, l3, th2, chi2, phi2, ei2, ef2=1.,1.0,    -3.754,45.0,72.43711, 14.7, 14.7

    UBref=ubcalc.calcRefineUB(observations,stars_dict)
    print UB
    print UBref
    
    lattice_params=calculateLatticeParameters(UB)
    print lattice_params
    
    
    
    
    return results
    #print result
    #print 'chi',(180-result[0])%360
    #print 'phi',(result[1]+180)%360    
    
    
    
    
    
def UBtest3():
    "Test method to calculate UB matrix for tilt stage"
    #a, b, c, alpha, beta, gamma, h1, k1, l1, omega1, chi1, phi1, h2, k2, l2, omega2, chi2, phi2 = input('enter data: ')
    #Test data:
    #3.9091,3.9091,3.9091,90,90,90,1,1,0,0,89.62,.001,0,0,1,0,-1.286,131.063
    #maybe: 3.9091,3.9091,3.9091,90,90,90,1,1,0,-1.855,89.62,.001,0,0,1,-.0005,-1.286,131.063
    #Should yield:
    a, b, c, alpha, beta, gamma=3.9091,3.9091,3.9091,90.0,90.,90.
    h1, k1, l1, th1, mu1, nu1, ei1, ef1=1.,0.,0.,    0.,0.,0., 14.7, 14.7
    h2, k2, l2, th2, mu2, nu2, ei2, ef2=0.,1.,0.,    90.,0.,0.,14.7, 14.7

    stars = star(a, b, c, alpha, beta, gamma)
    Bmatrix = calcB(*(list(stars)+[c, alpha]))
    
    stars_dict = dict(zip(('astar','bstar','cstar','alphastar','betastar','gammastar'),
                          stars))
    ubcalc=UBCalcTilt()
    om1=calc_om_elastic(h1,k1,l1,ei1,th1,stars_dict)
    om2=calc_om_elastic(h2,k2,l2,ei2,th2,stars_dict)
    
    U = ubcalc.calcU(h1, k1, l1, h2, k2, l2, om1, mu1, nu1, om2, mu2, nu2, Bmatrix)
    UB=ubcalc.calcUB(h1, k1, l1, h2, k2, l2, om1, mu1, nu1, om2, mu2, nu2, Bmatrix)    
    #onehkl = lambda i: calcIdealAngles(np.array(i,'Float64'), UB,Bmatrix, 2.35916, stars_dict)
    #allhkl = lambda hkl: [onehkl(i) for i in hkl]
    #h, UBmatrix, Bmatrix, wavelength, stars
    
    #result = calcIdealAngles2(hv1, hv2, UB, 2.35916)
    print UB    
    Q_vec=np.array([1.,1.,0],'Float64')
    mu_plane=0
    nu_plane=0
    angles=ubcalc.calc_angles(mu_plane,nu_plane,UB,Q_vec,14.7,14.7)
    print 'angles', angles
    return angles
    
    
# **************************************** END OF UB MATRIX TESTING CODE ****************************************  




if __name__=="__main__":
    
    if 1:
        pi=np.pi
        a=2*pi; b=2*pi; c=2*pi
        alpha=90; beta=90; gamma=90
        recip=star(a,b,c,alpha,beta,gamma)
        print recip
        if 0:
            UBtest2()
        if 1:
            UBtest3()
        print('done!')
        
        
    if 0:
        pi=np.pi
        a=3.9091; b=3.9091; c=3.9091
        alpha=90; beta=90; gamma=90
        UBMatrix=np.array([[1.0025837,-1.255604,.0420678],
                          [1.2563042,1.0021650,-.029173],
                          [-.003439,.0510781,1.6065072]])
        UBMatrix=np.array([1.00258371638,-1.25560446131,0.0420678730826,1.25630427793,1.00216507632,-0.0291735947875,-0.00343954412323,0.0510781177682,1.60650725893],'Float64')
        UBMatrix=UBMatrix.reshape(3,3)
        wavelength=2.37051
        tth=np.radians(30.4466)
        phi=np.radians(-12.3291)
        omega=np.radians(129.993)
        chi=np.radians(-67.5906)
        hphi=calc_hphi(phi,omega,tth,chi,wavelength)
        UBinv=np.linalg.inv(UBMatrix)
        hcalc=2*pi*np.dot(UBinv,hphi)
        print hcalc
        
        p=[1,1,1,1,-1,0]
        h=[1]
        k=[1]
        l=[1]
        res=calc_plane(p,h,k,l,normalize=False)
        print res
