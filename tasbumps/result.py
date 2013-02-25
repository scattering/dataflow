from pylab import *

Pl = [0.008988, 0.00885, 0.00921]
Pn = [0.008897, 0.00878, 0.00905] 
Pq = [0.008732, 0.00865, 0.00889]
Gl = [0.008898, 0.00873, 0.00908]
Gn = [0.008950, 0.00884, 0.00910]
Gq = [0.008503, 0.00840, 0.00863]

Pm = [0.008939, 0.00880, 0.00904]
Pp = [0.008642, 0.00841, 0.00881]
Pu = [0.009055, 0.00888, 0.00934]
Gm = [0.008875, 0.00876, 0.00898]
Gp = [0.008553, 0.00835, 0.00875]
Gu = [0.009206, 0.00893, 0.00939]

V = [-20, 0, 20]

M = array((Pq,Pl,Pn))
cP1,P1,dP1 = M[:,0], (M[:,1]+M[:,2])/2, (M[:,2]-M[:,1])/2
M = array((Gq,Gl,Gn))
cG1,G1,dG1 = M[:,0], (M[:,1]+M[:,2])/2, (M[:,2]-M[:,1])/2

M = array((Pp,Pm,Pu))
cP2,P2,dP2 = M[:,0], (M[:,1]+M[:,2])/2, (M[:,2]-M[:,1])/2
M = array((Gp,Gm,Gu))
cG2,G2,dG2 = M[:,0], (M[:,1]+M[:,2])/2, (M[:,2]-M[:,1])/2

hold(True)
subplot(121)
plot(V,cP1,'bo-',label='S1')
plot(V,cP2,'gD-',label='S2')
errorbar(V,P1,dP1,fmt='b,')
errorbar(V,P2,dP2,fmt='g,')
legend()
title("Poisson statistics")
xlim(-25,25)
ylim(0.0082,0.0094)

subplot(122)
plot(V,cG1,'bo-',label='S1')
plot(V,cG2,'gD-',label='S2')
errorbar(V,G1,dG1,fmt='b,')
errorbar(V,G2,dG2,fmt='g,')
legend()
title("Gaussian statistics")
xlim(-25,25)
ylim(0.0082,0.0094)

show()
