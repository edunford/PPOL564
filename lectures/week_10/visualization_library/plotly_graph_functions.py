'''
Plotly library for multivariate functions
'''

# Import plotly...
from plotly.offline import init_notebook_mode, plot, iplot
import plotly.figure_factory as ff
import plotly.graph_objs as go
from sympy import lambdify, symbols
import numpy as np
init_notebook_mode(connected=True)

class multivar:

    def __init__(self):
        self.x = symbols('x')
        self.y = symbols('y')
    

    def plot_3d(self,func,w=800,h=500,bounds = [-5,5],seperate_window=False,n=20):
        '''Generate a 3D surface plot for a sympy defined function
        '''

        # Convert function wrapper
        f = lambdify([self.x,self.y],func,'numpy')

        # Define numerical space 
        x_range = np.linspace(bounds[0], bounds[1] ,n)
        y_range = np.linspace(bounds[0], bounds[1] ,n)
        x_, y_ = np.meshgrid(x_range, y_range)
        z = f(x_,y_)

        # Define surface feature
        surface = go.Surface(x=x_, y=y_, z=z,
                             colorscale="Portland",opacity=1,
                             contours=go.surface.Contours(
                                 z=go.surface.contours.Z(
                                      show=True,
                                      usecolormap=True,
                                      highlightcolor="#42f462",
                                      project=dict(z=True))))

        # Store surface feature as data 
        data = [surface]

        # Outline of graph settings
        graph_design = dict(gridcolor='#dee0e2',
                            zerolinecolor='#dee0e2',
                            showbackground=False)

        # Define layout 
        layout = go.Layout(showlegend=False,width=w,height=h,
                           scene=dict(xaxis=graph_design,
                                      yaxis=graph_design,
                                      zaxis=graph_design))
        # Generate figure
        fig = go.Figure(data=data, layout=layout)

        # Show 
        if seperate_window:
            plot(fig,show_link=False)
        else:
            iplot(fig,show_link=False)

    def plot_contour(self,func,w=700,h=500,bounds = [-5,5],seperate_window=False,n=20):
        '''
        '''

        # Convert function wrapper
        f = lambdify([self.x,self.y],func,'numpy')

        # Define numerical space 
        x_range = np.linspace(bounds[0], bounds[1] ,n)
        y_range = np.linspace(bounds[0], bounds[1] ,n)
        x_, y_ = np.meshgrid(x_range, y_range)
        z_ = f(x_,y_)

        fig = [
            go.Contour(
                z = z_,x=x_range,y=y_range,opacity=.95
            )]

        # Show 
        if seperate_window:
            plot(fig,show_link=False)
        else:
            iplot(fig,show_link=False)
            
    def plot_gradient(self,func,bounds=[-5,5],seperate_window=False):
        '''Quiver plot to the visualize the gradient. 
        '''
        f_x = func.diff(self.x)
        f_y = func.diff(self.y)
        fx = lambdify([self.x,self.y],f_x,'numpy')
        fy = lambdify([self.x,self.y],f_y,'numpy')

        # Define numerical space 
        x_range = np.arange(bounds[0], bounds[1] ,1)
        y_range = np.arange(bounds[0], bounds[1] ,1)
        x_, y_ = np.meshgrid(x_range, y_range)
        u = fx(x_,y_)
        v = fy(x_,y_)

        fig = ff.create_quiver(x_, y_, u, v)

        # Show 
        if seperate_window:
            plot(fig,show_link=False)
        else:
            iplot(fig,show_link=False)


print('loaded!')
