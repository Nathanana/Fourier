import svgpathtools as svg
import numpy as np
from scipy.interpolate import PchipInterpolator
import matplotlib.pyplot as plt

def distance(point1, point2):
    return abs(point1 - point2)

def path_to_complex(path, num_samples=100):
    ts = np.linspace(0, 1, num_samples)
    points = [path.point(t) for t in ts]
    return points

def svg_to_func(svg_file, f_res, resolution=10000):
    paths, _ = svg.svg2paths(svg_file)
    
    points = []
    for path in paths:
        points.extend(path_to_complex(path, num_samples=resolution))
        
    points_array = np.array(points, dtype=complex)
    
    #Scale
    max_distance = max(np.abs(points_array))
    desired_size = 6
    scale_factor = desired_size / max_distance
    points_array *= scale_factor
    
    t_values = np.linspace(0, 1, len(points))

    dt = 1 / len(points)

    n_range = list(range(-f_res, f_res + 1))
    n_range = sorted(n_range, key=lambda x: (abs(x), x < 0))
    n_range = np.array(n_range)
    exp_matrix = np.exp(-2j * np.pi * np.outer(t_values, n_range))
    coefficients = points_array @ exp_matrix * dt 

    funclist = list(zip(coefficients[1:], n_range[1:]))
    
    def fourier(t):
        return sum(c[0] * np.exp(2j * np.pi * c[1] * t) for c in funclist)
    
    return fourier, funclist

if __name__ == '__main__':
    fourier_function, _ = svg_to_func('svg/arrow.svg', 1024, 100000)
    
    import matplotlib.pyplot as plt
    resolution = 500
    t_values = np.linspace(0, 1, resolution)
    points = [fourier_function(t).real + 1j * fourier_function(t).imag for t in t_values]
    plt.plot([p.real for p in points], [p.imag for p in points])
    plt.axis("equal")
    plt.show()
    