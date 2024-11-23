# SVG to Fourier Animation

This project converts an SVG file containing paths or contours into a Fourier series animation. The paths are approximated using Fourier coefficients, and the animation traces the contours by calculating the points along the path using the Fourier series.
Inspired by [3Blue1Brown's video](https://www.youtube.com/watch?v=r6sGWTCMz2k) on the topic

## Features
- **SVG Path Parsing**: Parse SVG paths and extract their segments and coordinates.
- **Fourier Approximation**: Approximate the SVG paths using Fourier series for smooth animation.
- **Animation**: Animate the path using the Fourier coefficients to trace the contour smoothly.
- **Dynamic Parameters**: Adjustable resolution and other parameters to control the output.
- **Automated**: To get started, just put an svg file in the svg folder and run
 ```bash
python main.py {your_file}.svg {output_name}
```
Results are best if the shape is a closed loop

## The Project

The goal of this project was to use the Fourier Series, a mathematical series which can represent any periodic function as the sum of trigonometric functions. The equations for the pictures in the .svg files could be thought of as parametric functions,
where the real and imaginary coordinates are each their own functions. The equation I used for the series approximation was 
```math
s_N = \sum_{n=-N}^{N} C_ne^{n2\pi it} = \sum_{n=-N}^{N} C_n[cos(nt) + isin(nt)]
```
The cool thing about this equation, is that it can be thought of as a parametric equation of the real and imaginary number lines. In the real number line, the function oscillates according to $cos(ft)$ and on the imaginary number line, the function
oscillates according to $sin(ft)$. Put together, this creates a function which moves in a circle at the frequency $f$. If $f$ were 1, then it would take 1 second (or whatever unit t is in) for the function to make one full revolution. 

Here is a gif
that highlights this behavior from radartutorial.eu, in this gif, the z represents the t axis. One could imagine that when looking at the X-Y plane, a circle would be visible.
<p align="center">
  <img src="https://github.com/user-attachments/assets/ab18ba62-665d-48f3-b472-f7886ca9dbba" alt="animated" />
</p>

Though the circle is simple, hopefully you can start to imagine what more complicated waves might result in. If we can deconstruct any shape in this manner, then the task of recreating them would be more the task of recreating the real and imaginary
waves. There are many good vidoes, namely the one mentioned at the top of this page, but in short, any wave can be created as the sum of trigonometric functions. The values for each constant can be found with the following formula:
```math
C_n=\int_0^1f(t)e^{-n2\pi it}dt
```

Which is also explained very well in 3Blue1Brown's video.

To recreate any svg, I used svgpathtools to turn the .svg picture into a complex function, and I sampled a number of complex points for an evenly spaced set of t values. I then used this to apply the formula immediately above to find each constant for a
desired vector count n. Since integration would be computationally expensive that many times, I opted for a Riemann sum. The formula I used was:
```math
C_n \approx \sum_{m=0}^{r} f\left(t_m\right)e^{-n2\pi it_m}\Delta t  \hspace{35pt}  t_m = \frac{m}{r}   \hspace{35pt}   \Delta t = \frac{1}{r}
```

I could then increase or decrease r, the resolution, depending on how intricate the image was.

Adding together each vector as t increased from 0 to 1 would recreate the original picture, only now it was entirely composed of rotating vectors, each rotating at a constant speed.

### Examples

![Square](https://github.com/user-attachments/assets/da757cfa-bf1e-46f4-8fc8-5514ec322f1d)

This square was calculated with 99 vectors and 1000 sampled points from the original .svg

![Star](https://github.com/user-attachments/assets/7f3dc43f-f13a-4f5e-9491-d3544292c7f2)

This star was calculated with 127 vectors and 10000 sampled points

![Arrow](https://github.com/user-attachments/assets/384ec500-ad60-4cda-8313-a25775a3187f)

This arrow was calculated with 2047 vectors, and 100000 sampled points, by far the most difficult as it's not exactly a closed loop

If you noticed, each one has an odd number of vectors. This is because the vector associated with $n=0$ would not rotate at all, since, looking at the first equation, that specific rotating vector would evaluate to $C_0$
I removed this vector as to center each series around the origin.

## Usage

You will need the entire Fourier folder, though the examples aren't necessary. Find an .svg, a closed shape will work best but irregular shapes can work with high enough parameters. I recommend playing around with the settings in Fourier.py
to visualize with matplotlib until you find parameters you like, then go over to Animation.py and copy the same settings. To run type the following into a terminal opened in the Fourier folder
```bash
python main.py {your_file}.svg {output_name}
```

## Installation

To run this project, you need to install the following Python libraries:

- `svgpathtools`: For reading and handling SVG file components.
- `numpy`: For numerical and matrix operations, especially for Fourier transformations.
- `matplotlib`: For visualization (optional).
- `ffmpeg`: For gif creation.
- `manim`: For creating the mp4 of the Fourier visualization.

You can install them using `pip`:

### Installing Manim/FFmpeg

Rather than me explaining it crudely, I recommend going to Manim's [installation guide](https://docs.manim.community/en/stable/installation.html) and following the instructions there.

Everything besides FFmpeg can be installed using pip
```bash
pip install svgpathtools numpy smatplotlib manim
```
