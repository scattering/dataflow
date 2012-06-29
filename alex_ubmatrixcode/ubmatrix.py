'''
Author: Alex Yee

Edit History
    See Research Journal
'''
import sys
import numpy as N 
#import scipy
#import scipy.optimize
from openopt import NLSP

def star(a,b,c,alpha,beta,gamma):
   "Calculate unit cell volume, reciprocal cell volume, reciprocal lattice parameters"
   alpha=N.radians(alpha)
   beta=N.radians(beta)
   gamma=N.radians(gamma)
   V=2*a*b*c*\
   N.sqrt(N.sin((alpha+beta+gamma)/2)*\
           N.sin((-alpha+beta+gamma)/2)*\
           N.sin((alpha-beta+gamma)/2)*\
           N.sin((alpha+beta-gamma)/2))
   Vstar=(2*N.pi)**3/V;
   astar=2*N.pi*b*c*N.sin(alpha)/V
   bstar=2*N.pi*a*c*N.sin(beta)/V
   cstar=2*N.pi*b*a*N.sin(gamma)/V
   alphastar=N.arccos((N.cos(beta)*N.cos(gamma)-\
                            N.cos(alpha))/ \
                           (N.sin(beta)*N.sin(gamma)))
   betastar= N.arccos((N.cos(alpha)*N.cos(gamma)-\
                            N.cos(beta))/ \
                           (N.sin(alpha)*N.sin(gamma)))
   gammastar=N.arccos((N.cos(alpha)*N.cos(beta)-\
                            N.cos(gamma))/ \
                           (N.sin(alpha)*N.sin(beta)))
   V=V
   alphastar=N.degrees(alphastar)
   betastar=N.degrees(betastar)
   gammastar=N.degrees(gammastar)
   return astar,bstar,cstar,alphastar,betastar,gammastar

def calcB(astar,bstar,cstar,alphastar,betastar,gammastar,c, alpha):
   "Calculates the B matrix using the crystal dimensions calculated in the 'star' method"
   alphastar = N.radians(alphastar)
   betastar = N.radians(betastar)
   gammastar = N.radians(gammastar)
   alpha = N.radians(alpha)
   
   Bmatrix=N.array([[astar, bstar*N.cos(gammastar), cstar*N.cos(betastar)],
                    [0, bstar*N.sin(gammastar), -cstar*N.sin(betastar)*N.cos(alpha)],
                    [0, 0, cstar]],'Float64') #check the third element
   #"cstarN.sin(betastar)*N.sin(alpha)" for third element is equivalent
   return Bmatrix

def calcU(h1, k1, l1, h2, k2, l2, omega1, chi1, phi1, omega2, chi2, phi2, Bmatrix):
   "Calculates the UB matrix using 2 sets of observations (h#, k#, l#) and their respective angle measurements in degrees (omega#, chi#, phi#)"
   #Convertiung angles given in degrees to radians
   omega1 = N.radians(omega1)
   chi1 = N.radians(chi1)
   phi1 = N.radians(phi1)
   omega2 = N.radians(omega2)
   chi2 = N.radians(chi2)
   phi2 = N.radians(phi2)
   
   hmatrix1 = N.array([h1, k1, l1])
   hmatrix2 = N.array([h2, k2, l2])
   h1c = N.dot(Bmatrix, hmatrix1) 
   h2c = N.dot(Bmatrix, hmatrix2)
   h3c = N.cross(h1c, h2c)
   
   ''' Making the orthogonal unit-vectors t#c:
   t1c is parallel to h1c
   t3c is orthogonal to both t1c and t2c, and thus is parallel to h3c
   t2c must be orthogonal to both t1c and t2c
   '''
   t1c = h1c / N.sqrt(N.power(h1c[0], 2) + N.power(h1c[1], 2) + N.power(h1c[2], 2))
   t3c = h3c / N.sqrt(N.power(h3c[0], 2) + N.power(h3c[1], 2) + N.power(h3c[2], 2))
   t2c = N.cross(t3c, t1c)
   Tc = N.array([t1c, t2c, t3c]).T
   #realU=N.array([[ -5.28548868e-01,   8.65056241e-17,  -6.63562568e-16],
   #               [ -0.00000000e+00,   4.86909792e-01,   2.90030482e-16],
   #               [  0.00000000e+00,   0.00000000e+00,  -1.26048191e-01]])
   
   #calculating u_phi 
   u1p = N.array([N.cos(omega1)*N.cos(chi1)*N.cos(phi1) - N.sin(omega1)*N.sin(phi1),
                N.cos(omega1)*N.cos(chi1)*N.sin(phi1) + N.sin(omega1)*N.cos(phi1),
                N.cos(omega1)*N.sin(chi1)],'Float64')
   u2p = N.array([N.cos(omega2)*N.cos(chi2)*N.cos(phi2) - N.sin(omega2)*N.sin(phi2),
                N.cos(omega2)*N.cos(chi2)*N.sin(phi2) + N.sin(omega2)*N.cos(phi2),
                N.cos(omega2)*N.sin(chi2)],'Float64')
   u3p = N.cross(u1p, u2p)
   
   ''' Making orthogonal unit-vectors t#p
   Tp should be exactaly superimposed on Tc
   t#p is created the same way t#c was, except using u#p instead of h#c
   '''
   t1p = u1p / N.sqrt(u1p[0]**2 + u1p[1]**2 + u1p[2]**2)
   t3p = u3p / N.sqrt(u3p[0]**2 + u3p[1]**2 + u3p[2]**2)
   t2p = N.cross(t3p, t1p)
   Tp = N.array([t1p, t2p, t3p],'Float64').T
   
   #calculating the UB matrix
   Umatrix = N.dot(Tp, Tc.T) 
   #UBmatrix = N.dot(Umatrix, Bmatrix)
   return Umatrix 
   
def calcUB (*args):
    Umatrix = calcU(*args)
    UBmatrix = N.dot(Umatrix, args[-1])
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
        
        theta = N.radians(observations[i]['theta'])
        chi = N.radians(observations[i]['chi'])
        phi = N.radians(observations[i]['phi'])
        twotheta = N.radians(observations[i]['twotheta'])
        omega = theta - twotheta/2.0
        
        u1p = N.cos(omega)*N.cos(chi)*N.cos(phi) - N.sin(omega)*N.sin(phi)
        u2p = N.cos(omega)*N.cos(chi)*N.sin(phi) + N.sin(omega)*N.cos(phi)
        u3p = N.cos(omega)*N.sin(chi)
        
        uv1p = 2.0*N.sin(twotheta/2) / wavelength * u1p
        uv2p = 2.0*N.sin(twotheta/2) / wavelength * u2p
        uv3p = 2.0*N.sin(twotheta/2) / wavelength * u3p

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
        outvec.append(N.dot(UB[0], h[i]) - Uv[3*i])
        outvec.append(N.dot(UB[1], h[i]) - Uv[3*i + 1])
        outvec.append(N.dot(UB[2], h[i]) - Uv[3*i + 2])   
        
   return outvec
   
    
  
# ******************************* END - METHODS FOR REFINING THE UB MATRIX *******************************


# **************************** START - METHOD FOR OBTAINING LATTICE PARAMETERS FROM UB ****************************
def calculateLatticeParameters(UBmatrix):

    G = N.linalg.inv(N.dot(UBmatrix.T, UBmatrix))
    
    abc = N.sqrt(N.diag(G))
    a = abc[0]
    b = abc[1]
    c = abc[2]
    
    alpha = N.degrees(N.arccos(G[1, 2]/b/c))
    beta = N.degrees(N.arccos(G[0, 2]/a/c))
    gamma = N.degrees(N.arccos(G[0, 1]/a/b))
    
    latticeParameters = {'a': a, 'b': b, 'c': c, 'alpha': alpha, 'beta': beta, 'gamma': gamma}
    return latticeParameters
# **************************** END - METHOD FOR OBTAINING LATTICE PARAMETERS FROM UB ****************************

def calcTwoTheta(h, stars, wavelength):
    "Calculates the twotheta value for a vector h with lattice parameters given. Useful for finding observed reflections."
    q = calcq (h[0], h[1], h[2], stars)
    twotheta = N.degrees(2 * N.arcsin(wavelength * q / 4 / N.pi))
    return twotheta
    

# *********************************** START - calculations for bisecting mode  *********************************** 

def calcIdealAngles(h, UBmatrix, Bmatrix, wavelength, stars):
   "Calculates the remaining angles with omega given as 0"
   "Returns (twotheta, theta, omega, chi, phi)"
   '''myUBmatrix=N.array([[ -0.8495486120866541,0.8646150711829229,-1.055554030805845],
                     [-0.7090402876860106,0.7826211792587279,1.211714627203656],
                     [1.165768160358335,1.106088263216144,-0.03224481098900243]],'Float64')
   '''
   hp = N.dot(UBmatrix, h)
   phi = N.degrees(N.arctan2(hp[1], hp[0]))
   chi = N.degrees(N.arctan2(hp[2], N.sqrt(hp[0]**2 + hp[1]**2)))
      
   q = calcq (h[0], h[1], h[2], stars)
   twotheta = N.degrees(2 * N.arcsin(wavelength * q / 4 / N.pi))
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
   
   desiredhp = N.dot(UBmatrix, desiredh)
   
   #Old code (scipy.optimize.fsolve) produced inaccurate results with far-off estimates
   #solutions = scipy.optimize.fsolve(equations, x0, args=(h1p, h2p, wavelength)) 

   q = calcq (desiredh[0], desiredh[1], desiredh[2], stars)

   twotheta = 2.0 * N.arcsin(wavelength * q / 4.0 / N.pi)
    
   x0 = [0.0]
   p = NLSP(secondequations, x0, args=(desiredhp, chi, phi, wavelength, twotheta))
   r = p.solve('nlp:ralg')
   omega = r.xf[0]
   theta = twotheta/2.0 + omega   # ------ ALTERNATE SOLUTION FOR THETA ------
   
   
   #theta = r.xf[1]  # ------ SOLVER POTENTIALLY INACCURATE FOR THETA ------
    
    
   solutions = [twotheta, theta, omega]
   return N.degrees(solutions) #% 360
   #returns an array of 3 angles [twotheta, theta, omega]
   
   
   
def calcScatteringPlane (h1, h2, UBmatrix, wavelength,stars):
   "Calculates the chi and phi for the scattering plane defined by h1 and h2. Used with calcIdealAngles2."
   #Accepts two scattering plane vectors, h1 and h2, the UB matrix, and the wavelength
   h1p = N.dot(UBmatrix, h1)
   h2p = N.dot(UBmatrix, h2)
   
   x0 = [0.0, 0.0, 0.0, 0.0]
   
   q = calcq (h1[0], h1[1], h1[2], stars)
   twotheta1 = 2.0 * N.arcsin(wavelength * q / 4.0 / N.pi)
   q = calcq (h2[0], h2[1], h2[2], stars)
   twotheta2 = 2.0 * N.arcsin(wavelength * q / 4.0 / N.pi)
   
   p0 = NLSP(scatteringEquations, x0, args=(h1p, h2p, wavelength, twotheta1, twotheta2))
   r0 = p0.solve('nlp:ralg')
   chi = N.degrees(r0.xf[0]) #xf is the final array, xf[0] = chi
   phi = N.degrees(r0.xf[1]) #                       xf[1] = phi
   
   return chi, phi
   
   
   
def scatteringEquations(x, h1p, h2p, wavelength,tth1,tth2):
   #x vector are the intial estimates
   chi = x[0]
   phi = x[1]
   omega1 = x[2]
   omega2 = x[3]
   theta1 = tth1/2
   theta2 = tth2/2

   outvec=[h1p[0] - 2.0/wavelength * N.sin(theta1) * (N.cos(omega1)*N.cos(chi)*N.cos(phi) - N.sin(omega1)*N.sin(phi)),
           h1p[1] - 2.0/wavelength * N.sin(theta1) * (N.cos(omega1)*N.cos(chi)*N.sin(phi) + N.sin(omega1)*N.cos(phi)),
           h1p[2] - 2.0/wavelength * N.sin(theta1) * N.cos(omega1)*N.sin(chi),
           h2p[0] - 2.0/wavelength * N.sin(theta2) * (N.cos(omega2)*N.cos(chi)*N.cos(phi) - N.sin(omega2)*N.sin(phi)),
           h2p[1] - 2.0/wavelength * N.sin(theta2) * (N.cos(omega2)*N.cos(chi)*N.sin(phi) + N.sin(omega2)*N.cos(phi)),
           h2p[2] - 2.0/wavelength * N.sin(theta2) * N.cos(omega2)*N.sin(chi)]  
   return outvec
   
   
   
def secondequations(x, hp, chi, phi, wavelength,tth):
   #theta = x[0]
   #omega = x[1]
   omega=x[0]
   theta=tth/2
   outvec=[hp[0] - 2.0/wavelength * N.sin(theta) * (N.cos(omega)*N.cos(chi)*N.cos(phi) - N.sin(omega)*N.sin(phi)),
           hp[1] - 2.0/wavelength * N.sin(theta) * (N.cos(omega)*N.cos(chi)*N.sin(phi) + N.sin(omega)*N.cos(phi)),
           hp[2] - 2.0/wavelength * N.sin(theta) * N.cos(omega)*N.sin(chi)]
   return outvec

# *********************************** END - calculations for scattering plane mode  *********************************** 

    
# *********************************** START - calculations for phi fixed mode  *********************************** 
def calcIdealAngles3 (h, UBmatrix, wavelength, phi, stars):
   "Calculates the chi and theta for a desired vector h in the fixed phi mode."
   #Accepts ta desired vector h, the UB matrix, the wavelength, and the fixed phi
   hp = N.dot(UBmatrix, h)
   q = calcq (h[0], h[1], h[2], stars)
   twotheta = 2 * N.arcsin(wavelength * q / 4 / N.pi)
   
   x0 = [0.0, 0.0]
   p0 = NLSP(phiEquations, x0, args=(hp, wavelength, phi,twotheta))
   r0 = p0.solve('nlp:ralg')
   
   #r0.xf is the final array   
   twotheta=N.degrees(twotheta)
   chi = N.degrees(r0.xf[0])    # xf[0] = chi
   omega = N.degrees(r0.xf[1])  # xf[1] = omega
   theta = twotheta/2.0 + omega

   
   return twotheta, theta, omega, chi
   
   
def phiEquations(x, h1p, wavelength, phi,tth):
   #x vector are the intial estimates
   chi = x[0]
   omega1 = x[1]
   theta1=tth/2
   outvec=[h1p[0] - 2.0/wavelength * N.sin(theta1) * (N.cos(omega1)*N.cos(chi)*N.cos(phi) - N.sin(omega1)*N.sin(phi)),
           h1p[1] - 2.0/wavelength * N.sin(theta1) * (N.cos(omega1)*N.cos(chi)*N.sin(phi) + N.sin(omega1)*N.cos(phi)),
           h1p[2] - 2.0/wavelength * N.sin(theta1) * N.cos(omega1)*N.sin(chi)]
          
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
   alpha = N.radians(stars['alphastar'])
   beta = N.radians(stars['betastar'])
   gamma = N.radians(stars['gammastar'])

   s=x1*x2*a**2+y1*y2*b**2+z1*z2*c**2+(x1*y2+x2*y1)*a*b*N.cos(gamma)+(x1*z2+x2*z1)*a*c*N.cos(beta)+(z1*y2+z2*y1)*c*b*N.cos(alpha)
   return s


def modvec(x, y, z, stars):
   "Calculates modulus of a vector defined by its fraction cell coordinates"
   "or Miller indexes"
   m=N.sqrt(scalar(x, y, z, x, y, z, stars))
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

#   astar, bstar, cstar, alphastar, betastar, gammastar = star(a, b, c, alpha, beta, gamma)
#   stars = astar, bstar, cstar, alphastar, betastar, gammastar
#   Bmatrix = calcB(astar, bstar, cstar, alphastar, betastar, gammastar, c, alpha)
   stars = star(a, b, c, alpha, beta, gamma)
   Bmatrix = calcB(*(list(stars)+[c, alpha]))
   U = calcU(h1, k1, l1, h2, k2, l2, omega1, chi1, phi1, omega2, chi2, phi2, Bmatrix)
   UB=calcUB(h1, k1, l1, h2, k2, l2, omega1, chi1, phi1, omega2, chi2, phi2, Bmatrix)
   stars_dict = dict(zip(('astar','bstar','cstar','alphastar','betastar','gammastar'),
                         stars))
   onehkl = lambda i: calcIdealAngles(N.array(i,'Float64'), UB,Bmatrix, 2.35916, stars_dict)
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


if __name__=="__main__":
   pi=N.pi
   a=2*pi; b=2*pi; c=2*pi
   alpha=90; beta=90; gamma=90
   recip=star(a,b,c,alpha,beta,gamma)
   print recip
   UBtestrun()
   print('done!')

