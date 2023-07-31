# CPUBasedPythonRenderEngine
A rasterization render engine written in python for educational purpose (Pre-alpha VERSION is in pure python using pygame to draw things on screen, further versions are going to use numpy and numba with different techniques to improve perfomance and to give us pixel per pixel control over readability).

Pre-Alpha:
To move around the world use W,A,S,D. To rotate the camera around the z axis use Q,E. There is no inclination of the camera (you can`t look up or down, only sideways). To change the rendered object update the file directory passed as string to the 'load_obj' function (This functions lives inside utils), and of course, use an obj format for the 3D model. To move faster or slower change movement_factor and rotation_factor (the movement is frame dependent so different objects will influence your velocity).
