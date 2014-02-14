function ubmatrix()
dtor=pi/180;
lambda=2.5086;
a=5.72; b=a; c=9.24;
alpha=90; beta=90; gamma=90;
H=[1 0 0]'
%H=[0 0 1]'


%[alphastar betastar gammastar]=calc_recipangles(alpha,beta,gamma);
%V=calc_volume(a,b,c,alpha,beta,gamma)
a1=[a 0 0];
a2=[0 b 0];
a3=[0 0 c];
%[b1 b2 b3]=calc_recipvectors(a1,a2,a3)
B=calc_Bmatrix(a,b,c,alpha,beta,gamma,a1,a2,a3);

%G=sqrt(eye(3)/(B'*B))  %Gives metric tensor 
%det(B)


ubmatrix=[0.1748064     0.0024864     0.0003803; ...
         0.0018390    -0.0926724    -0.0917617; ...
        -0.0017826     0.1482211    -0.0573787];

%1/(det(ubmatrix))
Urafin=ubmatrix/B;

refl.hkl=[2 0 0];
refl.tth=52.0249;
refl.om=26.0124;
refl.chi=0;
refl.phi=.36;
refl(1).hkl=[2 0 0];


refl(2).hkl=[0 2 0];
refl(2).tth=52.0249;
refl(2).om=26.0124;
relf(2).chi=57.9758;
refl(2).phi=-88.4631;
refl(2).chi=57.9758;



Umine=calc_Umatrix(refl,B);
ubmatrixmine=Umine*B



%%%Calculate from angles
%lambda=1.75;
%tth1=56;%99;%108;
%om1=30;%26;%37.4;
%th1=tth1/2;
%chi1=44;%-38;
%phi1=39.3;%-126.56;
%uphia=calc_Uphi((om1-th1),chi1,phi1);
%ubinverse=eye(3)/ubmatrixmine
%h1=2*sin(th1*dtor)*ubinverse*uphia/lambda
%return
lambda=1.75
H=[3 0 1]'
H=[2 0 4]'
%H=[1 0 5]'
d=dspace_calculate(H(1),H(2),H(3),a,b,c,alpha,beta,gamma);
twotheta=calc_twotheta(lambda,d);
theta=twotheta/2;
omega=twotheta/2;
uphi=ubmatrixmine*H*lambda/2/sin(theta*dtor);
chi=-.58; phi=0.6;
p0=[chi phi];
options=optimset('Display','Iter','MaxIter',280,'LargeScale','on','TolFun',1e-6,'TolX', 1e-6);
%p=fsolve(@calcangles,p0,options,(omega-theta),uphi);
%fprintf( '    TwoTheta            %5.2f \n', twotheta);
%fprintf( '    Omega            %5.2f \n', omega);
%fprintf('     Chi            %5.2f \n', p(1));
%return

h=[1.53 1];
%h=[1 3.53]
%h=[4 0];
lq=4.0
lr=[lq lq]
%lr=[0 0];
H1=[h 0]'
H2=[h lr(1)]'
H3=[h lr(2)]'

H1=[1 2 0]'
H2=[0 0 1]'
H3=[0 0 1]'

%H1=[1 0 0]'
%H2=[0 1 0]'
%H3=[1 0 0]'

%lambda=1.75 %Thomas experiment
lambda=2.35916;

%H1=[2 0 0]'
d1=dspace_calculate(H1(1),H1(2),H1(3),a,b,c,alpha,beta,gamma);
twotheta1=calc_twotheta(lambda,d1);
theta1=twotheta1/2;
uphi1_ub=ubmatrixmine*H1*lambda/2/sin(theta1*dtor);

%H2=[0 2 0]'
d2=dspace_calculate(H2(1),H2(2),H2(3),a,b,c,alpha,beta,gamma);
twotheta2=calc_twotheta(lambda,d2);
theta2=twotheta2/2;
uphi2_ub=ubmatrixmine*H2*lambda/2/sin(theta2*dtor);

%H3=[2 2 0]'
d3=dspace_calculate(H3(1),H3(2),H3(3),a,b,c,alpha,beta,gamma);
twotheta3=calc_twotheta(lambda,d3);
theta3=twotheta3/2;
uphi3_ub=ubmatrixmine*H3*lambda/2/sin(theta3*dtor);

p0=[chi phi 0 50 25];
p=fsolve(@calcangles_scattplane,p0,options,uphi1_ub,uphi2_ub,uphi3_ub,theta1,theta2,theta3);   
%calcangles_scattplane(p,uphi1_ub,uphi2_ub);

fprintf( '    TwoTheta1            %5.2f \n', twotheta1);
fprintf( '    TwoTheta2            %5.2f \n', twotheta2);
fprintf( '    TwoTheta3            %5.2f \n', twotheta3);
%fprintf( '    Omega            %5.2f \n', omega);
fprintf('     Chi            %5.2f \n', p(1));
fprintf( '    Phi            %5.2f \n', p(2));
fprintf( '    Omega1            %5.2f \n', p(3));
fprintf( '    Omega2            %5.2f \n', p(4));
fprintf( '    Omega3            %5.2f \n', p(5));

return


function d=dspace_calculate(h,k,l,a,b,c,alph,bet,gamm)
dtor=pi/180;
alpha=alph*dtor;
beta=bet*dtor;
gamma=gamm*dtor;
denominator=1+2*cos(alpha)*cos(beta)*cos(gamma)-cos(alpha)^2-cos(beta)^2-cos(gamma)^2;
numerator=h^2*sin(alpha)^2/a^2+k^2*sin(beta)^2/b^2+l^2*sin(gamma)^2/c^2+2*h*k*(cos(alpha)*cos(beta)-cos(gamma))/a/b ...
    +2*k*l*(cos(beta)*cos(gamma)-cos(alpha))/b/c+2*l*h*(cos(gamma)*cos(alpha)-cos(beta))/a/c;
dinverse_squared=numerator/denominator;
d=1.0/sqrt(dinverse_squared);
return

function tth=calc_twotheta(lambda,d)
dtor=pi/180;
tth=(2*asin(lambda/2./d)/dtor);
return

function z=calcangles(p,om,uphi_ub);
dtor=pi/180;
%chi=p(1)*dtor;
%phi=p(2)*dtor;
%omega=om*dtor;
%A=cos(omega)*cos(chi)*cos(phi);
%B=cos(omega)*cos(chi)*sin(phi);
%z(1)=A-sin(omega)*sin(phi)-uphi(1);
%z(2)=B+sin(omega)*cos(phi)-uphi(2);
%z(3)=cos(omega)*sin(chi)-uphi(3);

chi=p(1);
phi=p(2);
omega=om;
uphi_rmatrix=calc_Uphi(om,chi,phi)
z(1)=uphi_rmatrix(1)-uphi_ub(1);
z(2)=uphi_rmatrix(2)-uphi_ub(2);
z(3)=uphi_rmatrix(3)-uphi_ub(3);
return

function z=calcangles_scattplane(p,uphi1_ub,uphi2_ub,uphi3_ub,theta1,theta2,theta3);
chi=p(1);
phi=p(2);
omega1=p(3);
omega2=p(4);
omega3=p(5);
uphi1_rmatrix=calc_Uphi(omega1-theta1,chi,phi);
uphi2_rmatrix=calc_Uphi(omega2-theta2,chi,phi);
uphi3_rmatrix=calc_Uphi(omega3-theta3,chi,phi);


z(1)=uphi1_rmatrix(1)-uphi1_ub(1);
z(2)=uphi1_rmatrix(2)-uphi1_ub(2);
z(3)=uphi1_rmatrix(3)-uphi1_ub(3);

z(4)=uphi2_rmatrix(1)-uphi2_ub(1);
z(5)=uphi2_rmatrix(2)-uphi2_ub(2);
z(6)=uphi2_rmatrix(3)-uphi2_ub(3);

z(7)=uphi3_rmatrix(1)-uphi3_ub(1);
z(8)=uphi3_rmatrix(2)-uphi3_ub(2);
z(9)=uphi3_rmatrix(3)-uphi3_ub(3);
return

function [alphastar,betastar,gammastar]=calc_recipangles(alph,bet,gamm)
dtor=pi/180;
alpha=alph*dtor;
beta=bet*dtor;
gamma=gamm*dtor;
alphastar=acos((cos(beta)*cos(gamma)-cos(alpha))/sin(beta)/sin(gamma))/dtor;
betastar=acos((cos(alpha)*cos(gamma)-cos(beta))/sin(alpha)/sin(gamma))/dtor;
gammastar=acos((cos(alpha)*cos(beta)-cos(gamma))/sin(alpha)/sin(beta))/dtor;
return

function [b1,b2,b3]=calc_recipvectors(a1,a2,a3)
b1=cross(a2,a3)/(a1*cross(a2,a3)');
b2=cross(a3,a1)/(a1*cross(a2,a3)');
b3=cross(a1,a2)/(a1*cross(a2,a3)');
return



function V=calc_volume(a,b,c,alph,bet,gamm);
dtor=pi/180;
alpha=alph*dtor;
beta=bet*dtor;
gamma=gamm*dtor;
V=a*b*c*sqrt(1-cos(alpha)^2-cos(beta)^2-cos(gamma)^2+2*cos(alpha)*cos(beta)*cos(gamma));
return


function B=calc_Bmatrix(a,b,c,alph,bet,gamm,a1,a2,a3)
dtor=pi/180;
alpha=alph*dtor;
beta=bet*dtor;
gamma=gamm*dtor;
[alphastar_deg betastar_deg gammastar_deg]=calc_recipangles(alph,bet,gamm);
alphastar=alphastar_deg*dtor;
betastar=betastar_deg*dtor;
gammastar=gammastar_deg*dtor;
[b1v b2v b3v]=calc_recipvectors(a1,a2,a3);
b1=norm(b1v); b2=norm(b2v); b3=norm(b3v);
B=[b1 b2*cos(gammastar) b3*cos(betastar);...
   0 b2*sin(gammastar) -b3*sin(betastar)*cos(alpha);...
   0 0 1/c];
return


function T=calc_Tmatrix(v1,v2)
t1=[v1(1) v1(2) v1(3)];
t3=cross(v1,[v2(1) v2(2) v2(3)]);
t2=cross(t3,t1);

t1=t1/norm(t1);
t2=t2/norm(t2);
t3=t3/norm(t3);

T=[t1;t2;t3]';
return

function uphi=calc_Uphi(om,chi,phi);
dtor=pi/180;
om=om*dtor;
chi=chi*dtor;
phi=phi*dtor;

phisense=-1;
omegasense=-1;

PhiM=[cos(phi) phisense*sin(phi) 0;...
     -phisense*sin(phi) cos(phi) 0; ...
     0 0 1];

ChiM=[cos(chi) 0 sin(chi);...
      0 1 0;...
      -sin(chi) 0 cos(chi)];

OmegaM=[cos(om)  omegasense*sin(om) 0; ...
        -omegasense*sin(om) cos(om) 0; ...
        0 0 1];

uphi=PhiM'*ChiM'*OmegaM'*[1 0 0]';
%uphi=(eye(3)/(OmegaM*ChiM*PhiM))*[1 0 0]';
return

function U=calc_Umatrix(refl,B)

%refl(1)
%refl(2)
hc1=B*refl(1).hkl';
hc2=B*refl(2).hkl';
uphi1=calc_Uphi(refl(1).om-refl(1).tth/2.0, refl(1).chi, refl(1).phi)
uphi2=calc_Uphi(refl(2).om-refl(2).tth/2.0, refl(2).chi, refl(2).phi)
Tc=calc_Tmatrix(hc1,hc2);
Tphi=calc_Tmatrix(uphi1,uphi2);
U=Tphi*Tc';
%U=Tphi/Tc;
return