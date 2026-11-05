import numpy as np

# Problem 3.a
def R_to_beta(R, r_ia=0.1, r_e2=1.25, lmbda_2=0.5, p_a=0.4, mu=0.2):
   return R * np.pow((1 - p_a) * (r_e2 / lmbda_2 + 1 / mu) + p_a * r_ia / mu, -1) 

def test_R_to_beta():
    R = 1.9
    beta = R_to_beta(R)
    np.testing.assert_almost_equal(beta, 0.4, delta=1e-10)

if __name__ == "__main__":
   test_R_to_beta()