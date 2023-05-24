def generate_linear_by_two_points(p1, p2):
    k = (p2[1] - p1[1])/(p2[0] - p1[0])
    b = p1[1] - k * p1[0]
    return k, b