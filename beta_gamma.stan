//Estimate the parameters of a beta distribution
data {
  int N;                        //sample size
  real<lower=0,upper=1> y[N];   //y consists of N real values between zero and one
  real<lower=0>          a1;
  real<lower=0>          b1;
  real<lower=0>          a2;
  real<lower=0>          b2; 
}
parameters {
  real<lower=0> alpha;          //shape constrained to be nonnegative
  real<lower=0> beta;           //scale constrained to be nonnegative
}
model {
  alpha ~ gamma(a1,b1);         //gamma prior for shape
  beta  ~ gamma(a2,b2);         //gamma prior for scale
  
  y     ~ beta(alpha,beta);     //beta likelihood given parameters alpha,beta
}
