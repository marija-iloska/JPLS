import numpy as np
from numpy import linalg as la
import LS_updates as LS

def pred_error(y, Hk, k, K, t, t0, var_y):

    k = len(Hk[1,:])-1

    # START k x k
    Dk = la.inv(Hk[:t0, :k].T @ Hk[:t0, :k])
    theta_k = Dk @ Hk[:t0, :k].T @ y[:t0]

    # Update to k+1 x k+1
    theta_kk, Dkk, _,_ = LS.orls_ascend(y, Hk, k, K, 0, t0, Dk, theta_k)

    # Initialize
    G = 0
    THETA = theta_k

    # Time increments
    for i in range(t0, t+1):

        # Compute Ai
        A = Hk[i, :k] @ (-Dkk[:k,k]/Dkk[k,k]) - Hk[i, k]

        # Compute Gi
        G = np.hstack([G, A*theta_kk[-1]])

        # Store THETAs using t0 elements
        THETA = np.hstack( [ THETA, theta_k])

        # Update thetas
        theta_kk, Dkk = LS.trls_update(y[i], Hk[i, :k+1], theta_kk, Dkk, var_y)
        theta_k, Dk = LS.trls_update(y[i], Hk[i, :k], theta_k, Dk, var_y)

    # Residual error (ignore initialized element in THETA)
    temp = Hk[t0:t+1, :k] * THETA[:,:][:,1:].T
    E = y[t0:t+1] - np.sum(temp, axis=1).reshape(t-t0+1,1)

    # Ignore initialized element, and reshape
    G = G[1:].reshape(t-t0+1,1)

    return G, E