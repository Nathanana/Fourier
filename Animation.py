from manim import *
import numpy as np
from Fourier import svg_to_func

class FourierAnimation(Scene):
    def construct(self):
        resolution = 500
        fourier_func, funclist = svg_to_func("svg/target.svg", 1024, 100000)
        t_values = np.linspace(0, 1, resolution)

        vectors = VGroup()
        circles = VGroup()
        origin = ORIGIN
        for coefficient, _ in funclist:
            vector = Arrow(
                start=origin,
                end=origin + coefficient.real * RIGHT + coefficient.imag * UP,
                buff=0,
                color=WHITE
            )
            circle = Circle(
                radius=np.abs(coefficient),
                color=WHITE
            )
            circle.move_to(origin)
            circle.set_stroke(opacity=0.3, width=1)
            vector.set_stroke(width=abs(coefficient)/3)
            
            vectors.add(vector)
            circles.add(circle)
            origin = vector.get_end() 

        path = VMobject(color=BLUE)
        path.set_points_as_corners([origin])
        self.add(vectors, circles, path)

        def update(vectors, alpha):
            nonlocal origin
            origin = ORIGIN
            time = alpha
            points = []
            for circle, vector, (coefficient, frequency) in zip(circles, vectors, funclist):
                new_endpoint = (
                    origin +
                    (coefficient * np.exp(2j * np.pi * frequency * time)).real * RIGHT +
                    (coefficient * np.exp(2j * np.pi * frequency * time)).imag * UP
                )
                vector.put_start_and_end_on(origin, new_endpoint)
                circle.move_to(origin)
                origin = new_endpoint
                points.append(origin)
                
            num_points = int(alpha * resolution)
            if num_points < 1:
                return

            t = t_values[:num_points]
            points = [
                fourier_func(ti).real * RIGHT + fourier_func(ti).imag * UP
                for ti in t
            ]
                
            path.set_points_as_corners(points)

            path.set_stroke(width = 1)
            

        self.play(UpdateFromAlphaFunc(vectors, update, run_time=20, rate_func=linear)) 