//Estimate the parameters of a beta distribution
data {
  int N;                        //sample size
  real<lower=0,upper=1> y[N];   //y consists of N real values between zero and one
}
parameters {
  real<lower=0> alpha;          //shape constrained to be nonnegative
  real<lower=0> beta;           //scale constrained to be nonnegative
}
model {
  alpha ~ normal(0,50);         //half-normal prior for shape
  beta  ~ normal(0,50);         //half-normal prior for scale
  
  y     ~ beta(alpha,beta);     //beta likelihood given parameters alpha,beta
}
