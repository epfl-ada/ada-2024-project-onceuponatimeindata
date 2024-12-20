import plotly.io as pio
import plotly.graph_objects as go

def mkdir_no_exist(path):
    """
    Function to create a directory if it does not exist already.

    Parameters
    ----------
    path: string
        Path to create
    """
    import os
    import os.path as op
    if not op.isdir(path):
        os.makedirs(path)

def set_default(template, font_family):
    pio.templates.default = template
    fig = go.Figure(layout={'title': 'Figure Title',

                            'font': {'family': font_family},

                            "xaxis": {"gridcolor": "lightgrey",
                                      "gridwidth": 1.5,
                                      },

                            "yaxis": {"gridcolor": "lightgrey",
                                      "gridwidth": 1.5,
                                      },

                            'template': "plotly_white"})

    templated_fig = pio.to_templated(fig)
    pio.templates['large_courier'] = templated_fig.layout.template
    pio.templates.default = 'large_courier'