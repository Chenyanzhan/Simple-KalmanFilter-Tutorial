import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def generate_data(X_initial, A, Q, H, R, iteration=50):
    # 产生实际位置、速度；过程误差、测量误差
    W = np.random.multivariate_normal((0, 0),Q,size=iteration+1) # 产生过程误差
    V = np.random.multivariate_normal((0, 0),R,size=iteration) # 产生测量误差
    X_true = []
    X_true.append(X_initial.reshape(-1,1))
    Z = []
    for index in range(iteration):
        X_k = np.dot(A, X_true[-1]) + W[index].reshape(-1,1)
        X_true.append(X_k)
        Z_k = np.dot(H, X_true[-1]) + V[index].reshape(-1,1)
        Z.append(Z_k)
    return X_true, Z



# Visualization
def show_result(X_true,X_hat,X_hat_p,Z,Q_convar,R_convar):
    # 位置与速度的真实值
    X_true_x = [item[0,0] for item in X_true]
    X_true_y = [item[1,0] for item in X_true]
    x_min = min(X_true_x)
    x_max = max(X_true_x)
    y_min = min(X_true_y)
    y_max = max(X_true_y)
    # 后验估计值
    X_hat_x = [item[0, 0] for item in X_hat]
    X_hat_x.insert(0,X_true_x[0])
    X_hat_y = [item[1, 0] for item in X_hat]
    X_hat_y.insert(0,X_true_y[0])
    # 先验估计值
    X_hat_p_x = [item[0, 0] for item in X_hat_p]
    X_hat_p_x.insert(0, X_true_x[0])
    X_hat_p_y = [item[1, 0] for item in X_hat_p]
    X_hat_p_y.insert(0, X_true_y[0])
    # 观测值
    Z_x = [item[0, 0] for item in Z]
    Z_x.insert(0, X_true_x[0])
    Z_y = [item[1, 0] for item in Z]
    Z_y.insert(0, X_true_y[0])

    plt.subplot(3, 2, 1)
    plt.plot([i for i in range(len(X_true_x))], X_true_x, label='true')
    plt.plot([i for i in range(len(X_hat_x))], X_hat_x, label='pre_x_hat')
    plt.ylim([x_min,x_max])
    plt.legend()

    plt.subplot(3, 2, 2)
    plt.plot([i for i in range(len(X_true_y))], X_true_y, label='true')
    plt.plot([i for i in range(len(X_hat_y))], X_hat_y, label='pre_y_hat')
    plt.ylim([y_min, y_max])
    plt.legend()

    plt.subplot(3, 2, 3)
    plt.plot([i for i in range(len(X_true_x))], X_true_x, label='true')
    plt.plot([i for i in range(len(X_hat_p_x))], X_hat_p_x, label='pre_x_p')
    plt.ylim([x_min, x_max])
    plt.legend()

    plt.subplot(3, 2, 4)
    plt.plot([i for i in range(len(X_true_y))], X_true_y, label='true')
    plt.plot([i for i in range(len(X_hat_p_y))], X_hat_p_y, label='pre_y_p')
    plt.ylim([y_min, y_max])
    plt.legend()

    plt.subplot(3, 2, 5)
    plt.plot([i for i in range(len(X_true_x))], X_true_x, label='true')
    plt.plot([i for i in range(len(Z_x))], Z_x, label='pre_x_m')
    plt.ylim([x_min, x_max])
    plt.legend()

    plt.subplot(3, 2, 6)
    plt.plot([i for i in range(len(X_true_y))], X_true_y, label='true')
    plt.plot([i for i in range(len(Z_y))], Z_y, label='pre_x_m')
    plt.ylim([y_min, y_max])
    plt.legend()

    plt.tight_layout()
    plt.savefig(str(Q_convar)+'-'+str(R_convar)+'.png')
    plt.show()
