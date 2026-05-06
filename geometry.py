import numpy as np

def create_fibonacci_sphere(samples=500):
    """
    使用斐波那契螺旋演算法生成均勻散佈在球面上的點座標 (x, y, z)
    """
    points = []
    # 黃金角度 (Golden Angle) 約為 2.399 弧度
    phi = np.pi * (3. - np.sqrt(5.)) 

    for i in range(samples):
        # y 座標從 1 均勻分布到 -1
        y = 1 - (i / float(samples - 1)) * 2 
        
        # 根據 y 的高度計算該層圓盤的半徑
        radius = np.sqrt(1 - y * y) 

        # 每個點旋轉一個黃金角度，確保分佈均勻
        theta = phi * i 

        x = np.cos(theta) * radius
        z = np.sin(theta) * radius

        points.append([x, y, z])

    return np.array(points)

def rotate_points(points, angle_x, angle_y):
    """
    使用旋轉矩陣對 3D 點雲進行旋轉運算
    """
    # 繞 X 軸旋轉矩陣 (上下旋轉)
    rx = np.array([
        [1, 0, 0],
        [0, np.cos(angle_x), -np.sin(angle_x)],
        [0, np.sin(angle_x), np.cos(angle_x)]
    ])
    
    # 繞 Y 軸旋轉矩陣 (左右旋轉)
    ry = np.array([
        [np.cos(angle_y), 0, np.sin(angle_y)],
        [0, 1, 0],
        [-np.sin(angle_y), 0, np.cos(angle_y)]
    ])

    # 矩陣相乘：先繞 X 轉再繞 Y 轉
    # 使用 @ 進行矩陣乘法，.T 是轉置矩陣
    rotated = points @ rx.T @ ry.T
    return rotated