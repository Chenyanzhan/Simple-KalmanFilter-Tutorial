import numpy as np
import pandas as pd
from utils import generate_data
from utils import show_result

class KalmanFilter:
    def __init__(self, X_true, Z, X_initial, A, Q, H, R):
        self.X_true = X_true
        self.Z = Z
        self.X_initial = X_initial
        self.A = A
        self.Q = Q
        self.H = H
        self.R = R
        self.X_hat_initial = np.array([0, 1]).reshape(-1,1)
        self.P_k_initial = np.eye(2)
        self.X_hat = []  # 后验
        self.X_hat.append(self.X_hat_initial) # iteration+1
        self.P_k = []
        self.P_k.append(self.P_k_initial) # iteration+1
        self.X_hat_p = []  #先验,iteration

    def run(self,iteration=50):
        for k in range(iteration):
            X_k_hat_p = np.dot(self.A, self.X_hat[-1])
            self.X_hat_p.append(X_k_hat_p)
            P_k_p = self.A @ self.P_k[-1] @ (self.A).T + self.Q
            K_k = P_k_p @ (self.H).T @ np.linalg.inv(self.H @ P_k_p @ (self.H).T + self.R)
            X_k_hat = X_k_hat_p + K_k @ (self.Z[k] - self.H @ X_k_hat_p)
            self.X_hat.append(X_k_hat)
            P_k = (np.eye(2) - K_k @ self.H) @ P_k_p
            self.P_k.append(P_k)

        return self.X_hat, self.X_hat_p, self.Z





if __name__ == '__main__':
    Q_convar = 1
    R_convar = 1
    A = np.array([[1, 1], [0, 1]])
    Q = np.eye(2) * Q_convar   # 控制预测模型的方差
    H = np.eye(2)
    R = np.eye(2) * R_convar  # 控制测量变量的方差

    iteration = 50
    X_initial = np.array([0, 1]) # 实际位置与实际速度的初始值
    X_true,Z = generate_data(X_initial, A, Q, H, R, iteration) # 产生KalmanFilter所需的数据

    # 构建KalmanFilter实例
    kalmanfilter = KalmanFilter(X_true, Z, X_initial, A, Q, H, R)
    X_hat, X_hat_p, Z = kalmanfilter.run(iteration)


    #可视化
    show_result(X_true,X_hat,X_hat_p,Z,Q_convar,R_convar)



















