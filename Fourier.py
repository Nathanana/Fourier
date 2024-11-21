#Play around with vector and sample count in this file until the shape looks good before animating, since animating can take a long time
#Beyond the two parameters at the top, there is one more you can play with at the bottom for super complex shapes that may help

import svgpathtools as svg
import numpy as np

VECTOR_COUNT = 64 #High runtime impact, Number of arrows spinning around in the animation
SAMPLE_COUNT = 1000 #Medium runtime impact, Number of points sampled from svg
SVGFILEPATH = "yourfile" #Replace yourfile with the name of your svg

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

    #Here's finding each constant!
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
    import matplotlib.pyplot as plt
    
    fourier_function, _ = svg_to_func(f'svg/{SVGFILEPATH}.svg', VECTOR_COUNT, SAMPLE_COUNT)
    
    import matplotlib.pyplot as plt
    resolution = 500 #Keep this, it only samples points from the already established approximation so increasing it won't increase accuracy unless shape is super complex
    t_values = np.linspace(0, 1, resolution)
    points = [fourier_function(t).real + 1j * fourier_function(t).imag for t in t_values]
    plt.plot([p.real for p in points], [p.imag for p in points])
    plt.axis("equal")
    plt.show()
    