'''
Author: Alex Yee

Edit History
    See Research Journal
'''
import sys
import numpy as np
#import scipy
#import scipy.optimize

from openopt import NLSP
#import multiprocessing as NLSP


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

def calcU(h1, k1, l1, h2, k2, l2, omega1, chi1, phi1, omega2, chi2, phi2, Bmatrix):
    "Calculates the UB matrix using 2 sets of observations (h#, k#, l#) and their respective angle measurements in degrees (omega#, chi#, phi#)"
    #Convertiung angles given in degrees to radians
    omega1 = np.radians(omega1)
    chi1 = np.radians(chi1)
    phi1 = np.radians(phi1)
    omega2 = np.radians(omega2)
    chi2 = np.radians(chi2)
    phi2 = np.radians(phi2)

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
    u1p = np.array([np.cos(omega1)*np.cos(chi1)*np.cos(phi1) - np.sin(omega1)*np.sin(phi1),
                   np.cos(omega1)*np.cos(chi1)*np.sin(phi1) + np.sin(omega1)*np.cos(phi1),
                   np.cos(omega1)*np.sin(chi1)],'Float64')
    u2p = np.array([np.cos(omega2)*np.cos(chi2)*np.cos(phi2) - np.sin(omega2)*np.sin(phi2),
                   np.cos(omega2)*np.cos(chi2)*np.sin(phi2) + np.sin(omega2)*np.cos(phi2),
                   np.cos(omega2)*np.sin(chi2)],'Float64')
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

def calcUB (*args):
    Umatrix = calcU(*args)
    UBmatrix = np.dot(Umatrix, args[-1])
    return UBmatrix


# ******************************* STAR - METHODS FOR REFINING THE UB MATRIX ******************************* 
def calcRefineUB(observations, wavelength):
    #observations are an array of dictionaries for each observed reflection

    hvectors = []
    Uv = []

    for i in range(0, len(observations)):
        h = [observations[i]['h'], observations[i]['k'], observations[i]['l']]
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

        theta = np.radians(observations[i]['theta'])
        chi = np.radians(observations[i]['chi'])
        phi = np.radians(observations[i]['phi'])
        twotheta = np.radians(observations[i]['twotheta'])
        omega = theta - twotheta/2.0

        u1p = np.cos(omega)*np.cos(chi)*np.cos(phi) - np.sin(omega)*np.sin(phi)
        u2p = np.cos(omega)*np.cos(chi)*np.sin(phi) + np.sin(omega)*np.cos(phi)
        u3p = np.cos(omega)*np.sin(chi)

        uv1p = 2.0*np.sin(twotheta/2) / wavelength * u1p
        uv2p = 2.0*np.sin(twotheta/2) / wavelength * u2p
        uv3p = 2.0*np.sin(twotheta/2) / wavelength * u3p

        Uv.append(uv1p)
        Uv.append(uv2p)
        Uv.append(uv3p)

    x0 = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    p = NLSP(UBRefinementEquations, x0, args=(hvectors, Uv))
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

    UB = [[a, b, c], [d, e, f], [g, h, j]]

    return UB


def UBRefinementEquations(x, h, Uv):
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

    UB = [[a, b, c], [d, e, f], [g, j, k]]

    outvec = []

    for i in range(0, len(h)):
        #sys.stderr.write('i %d\n'%(i,))
        #sys.stdout.write('i %d\n'%(i,))
        outvec.append(np.dot(UB[0], h[i]) - Uv[3*i])
        outvec.append(np.dot(UB[1], h[i]) - Uv[3*i + 1])
        outvec.append(np.dot(UB[2], h[i]) - Uv[3*i + 2])   

    return outvec



# ******************************* END - METHODS FOR REFINING THE UB MATRIX *******************************


# **************************** START - METHOD FOR OBTAINING LATTICE PARAMETERS FROM UB ****************************
def calculateLatticeParameters(UBmatrix):

    G = np.linalg.inv(np.dot(UBmatrix.T, UBmatrix))

    abc = np.sqrt(np.diag(G))
    a = abc[0]
    b = abc[1]
    c = abc[2]

    alpha = np.degrees(np.arccos(G[1, 2]/b/c))
    beta = np.degrees(np.arccos(G[0, 2]/a/c))
    gamma = np.degrees(np.arccos(G[0, 1]/a/b))

    latticeParameters = {'a': a, 'b': b, 'c': c, 'alpha': alpha, 'beta': beta, 'gamma': gamma}
    return latticeParameters
# **************************** END - METHOD FOR OBTAINING LATTICE PARAMETERS FROM UB ****************************

def calcTwoTheta(h, stars, wavelength):
    "Calculates the twotheta value for a vector h with lattice parameters given. Useful for finding observed reflections."
    q = calcq (h[0], h[1], h[2], stars)
    twotheta = np.degrees(2 * np.arcsin(wavelength * q / 4 / np.pi))
    return twotheta


# *********************************** START - calculations for bisecting mode  *********************************** 

def calcIdealAngles(h, UBmatrix, Bmatrix, wavelength, stars):
    "Calculates the remaining angles with omega given as 0"
    "Returns (twotheta, theta, omega, chi, phi)"
    '''myUBmatrix=np.array([[ -0.8495486120866541,0.8646150711829229,-1.055554030805845],
                     [-0.7090402876860106,0.7826211792587279,1.211714627203656],
                     [1.165768160358335,1.106088263216144,-0.03224481098900243]],'Float64')
   '''
    hp = np.dot(UBmatrix, h)
    phi = np.degrees(np.arctan2(hp[1], hp[0]))
    chi = np.degrees(np.arctan2(hp[2], np.sqrt(hp[0]**2 + hp[1]**2)))

    q = calcq (h[0], h[1], h[2], stars)
    twotheta = np.degrees(2 * np.arcsin(wavelength * q / 4 / np.pi))
    theta = twotheta / 2
    omega = 0

    #print 'chi',chi, 180-chi
    #print 'phi',phi, 180+phi
    return twotheta, theta, omega, chi, phi

# *********************************** END - calculations for bisecting mode  *********************************** 



# ********************************* START - calculations for scattering plane mode  ********************************* 

def calcIdealAngles2 (desiredh, chi, phi, UBmatrix, wavelength, stars):
    "Calculates the twotheta, theta, and omega values for a desired h vector. Uses chi and phi from calcScatteringPlane."
    #Accepts the desired h vector, chi, phi, the UB matrix, the wavelength, and the stars dictionary

    desiredhp = np.dot(UBmatrix, desiredh)

    #Old code (scipy.optimize.fsolve) produced inaccurate results with far-off estimates
    #solutions = scipy.optimize.fsolve(equations, x0, args=(h1p, h2p, wavelength)) 

    q = calcq (desiredh[0], desiredh[1], desiredh[2], stars)

    twotheta = 2.0 * np.arcsin(wavelength * q / 4.0 / np.pi)

    x0 = [0.0]
    p = NLSP(secondequations, x0, args=(desiredhp, chi, phi, wavelength, twotheta))
    r = p.solve('nlp:ralg')
    omega = r.xf[0]
    theta = twotheta/2.0 + omega   # ------ ALTERNATE SOLUTION FOR THETA ------


    #theta = r.xf[1]  # ------ SOLVER POTENTIALLY INACCURATE FOR THETA ------


    solutions = [twotheta, theta, omega]
    return np.degrees(solutions) #% 360
    #returns an array of 3 angles [twotheta, theta, omega]



def calcScatteringPlane (h1, h2, UBmatrix, wavelength,stars):
    "Calculates the chi and phi for the scattering plane defined by h1 and h2. Used with calcIdealAngles2."
    #Accepts two scattering plane vectors, h1 and h2, the UB matrix, and the wavelength
    h1p = np.dot(UBmatrix, h1)
    h2p = np.dot(UBmatrix, h2)

    x0 = [0.0, 0.0, 0.0, 0.0]
    
    q = calcq (h1[0], h1[1], h1[2], stars)
    twotheta1 = 2.0 * np.arcsin(wavelength * q / 4.0 / np.pi)
    q = calcq (h2[0], h2[1], h2[2], stars)
    twotheta2 = 2.0 * np.arcsin(wavelength * q / 4.0 / np.pi)
    outp=scatteringEquations(np.radians([45,90,-90,0]),h1p, h2p,wavelength,twotheta1,twotheta2)
    p0 = NLSP(scatteringEquations, x0, args=(h1p, h2p, wavelength, twotheta1, twotheta2))
    #outp=scatteringEquations(np.radians([45,90,-90,0]),h1p, h2p,wavelength,twotheta1,twotheta2)
    r0 = p0.solve('nlp:ralg')
    chi = np.degrees(r0.xf[0]) #xf is the final array, xf[0] = chi
    phi = np.degrees(r0.xf[1]) #                       xf[1] = phi

    return chi, phi



def scatteringEquations(x, h1p, h2p, wavelength,tth1,tth2):
    #x vector are the intial estimates
    chi = x[0]
    phi = x[1]
    omega1 = x[2]
    omega2 = x[3]
    theta1 = tth1/2
    theta2 = tth2/2

    outvec=[h1p[0] - 2.0/wavelength * np.sin(theta1) * (np.cos(omega1)*np.cos(chi)*np.cos(phi) - np.sin(omega1)*np.sin(phi)),
            h1p[1] - 2.0/wavelength * np.sin(theta1) * (np.cos(omega1)*np.cos(chi)*np.sin(phi) + np.sin(omega1)*np.cos(phi)),
            h1p[2] - 2.0/wavelength * np.sin(theta1) * np.cos(omega1)*np.sin(chi),
            h2p[0] - 2.0/wavelength * np.sin(theta2) * (np.cos(omega2)*np.cos(chi)*np.cos(phi) - np.sin(omega2)*np.sin(phi)),
            h2p[1] - 2.0/wavelength * np.sin(theta2) * (np.cos(omega2)*np.cos(chi)*np.sin(phi) + np.sin(omega2)*np.cos(phi)),
            h2p[2] - 2.0/wavelength * np.sin(theta2) * np.cos(omega2)*np.sin(chi)]  
    return outvec


def calc_hphi(phi,omega1,tth,chi,wavelength):
    #x vector are the intial estimates
    #phi = x[1]
    #omega1 = x[2]
    #omega2 = x[3]
    theta1 = tth/2
    hphi=np.array([0,0,0],'Float64')
    hphi[0]=2.0/wavelength * np.sin(theta1) * (np.cos(omega1)*np.cos(chi)*np.cos(phi) - np.sin(omega1)*np.sin(phi))
    hphi[1]=2.0/wavelength * np.sin(theta1) * (np.cos(omega1)*np.cos(chi)*np.sin(phi) + np.sin(omega1)*np.cos(phi))
    hphi[2]=2.0/wavelength * np.sin(theta1) * np.cos(omega1)*np.sin(chi)
    return hphi



def secondequations(x, hp, chi, phi, wavelength,tth):
    #theta = x[0]
    #omega = x[1]
    omega=x[0]
    theta=tth/2
    outvec=[hp[0] - 2.0/wavelength * np.sin(theta) * (np.cos(omega)*np.cos(chi)*np.cos(phi) - np.sin(omega)*np.sin(phi)),
            hp[1] - 2.0/wavelength * np.sin(theta) * (np.cos(omega)*np.cos(chi)*np.sin(phi) + np.sin(omega)*np.cos(phi)),
            hp[2] - 2.0/wavelength * np.sin(theta) * np.cos(omega)*np.sin(chi)]
    return outvec

# *********************************** END - calculations for scattering plane mode  *********************************** 


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


def phiEquations(x, h1p, wavelength, phi,tth):
    #x vector are the intial estimates
    chi = x[0]
    omega1 = x[1]
    theta1=tth/2
    outvec=[h1p[0] - 2.0/wavelength * np.sin(theta1) * (np.cos(omega1)*np.cos(chi)*np.cos(phi) - np.sin(omega1)*np.sin(phi)),
            h1p[1] - 2.0/wavelength * np.sin(theta1) * (np.cos(omega1)*np.cos(chi)*np.sin(phi) + np.sin(omega1)*np.cos(phi)),
            h1p[2] - 2.0/wavelength * np.sin(theta1) * np.cos(omega1)*np.sin(chi)]

    return outvec

# *********************************** END - calculations for phi fixed mode  *********************************** 

def isInPlane(h1, h2, v):
    "Checks if vector v lies in the plane formed by vectors h1 and h2 by calculating the determinate."
    determinate = (h1[0]*h2[1]*v[2] - h1[0]*v[1]*h2[2] - h1[1]*h2[0]*v[2] + h1[1]*v[0]*h2[2] + h1[2]*h2[0]*v[1] - h1[2]*v[0]*h2[1])
    if determinate == 0:
        return True
    else:
        return False


# ******************************* START - METHODS FOR CALCULATING Q ******************************* 
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



def calcq(H, K, L, stars):
    "Given reciprocal-space coordinates of a vector, calculate its coordinates in the Cartesian space."
    q = modvec(H, K, L, stars);
    return q

# ******************************* END - METHODS FOR CALCULATING Q ******************************* 


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


    a, b, c, alpha, beta, gamma=3.9091,3.9091,3.9091,90.0,90.,90.
    h1, k1, l1, th1, chi1, phi1, ei1, ef1=1.,0.,0.,    0.,0.,0., 14.7, 14.7
    h2, k2, l2, th2, chi2, phi2, ei2, ef2=0.,1.,0.,    0.,0.,90.,14.7, 14.7
    


#   astar, bstar, cstar, alphastar, betastar, gammastar = star(a, b, c, alpha, beta, gamma)
#   stars = astar, bstar, cstar, alphastar, betastar, gammastar
#   Bmatrix = calcB(astar, bstar, cstar, alphastar, betastar, gammastar, c, alpha)
    stars = star(a, b, c, alpha, beta, gamma)
    Bmatrix = calcB(*(list(stars)+[c, alpha]))
    U = calcU(h1, k1, l1, h2, k2, l2, omega1, chi1, phi1, omega2, chi2, phi2, Bmatrix)
    UB=calcUB(h1, k1, l1, h2, k2, l2, omega1, chi1, phi1, omega2, chi2, phi2, Bmatrix)
    

    
    
    
    stars_dict = dict(zip(('astar','bstar','cstar','alphastar','betastar','gammastar'),
                          stars))
    
    
    h1=np.array([1,0,0],'Float64')
    h2=np.array([0,1,1],'Float64')
    wavelength=2.35916
    
    chi,phi=calcScatteringPlane (h1, h2, UB, wavelength,stars_dict)
    print 'chi','phi',chi, phi
    
    
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
# **************************************** END OF UB MATRIX TESTING CODE ****************************************  


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

if __name__=="__main__":
    
    if 1:
        pi=np.pi
        a=2*pi; b=2*pi; c=2*pi
        alpha=90; beta=90; gamma=90
        recip=star(a,b,c,alpha,beta,gamma)
        print recip
        UBtestrun()
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
