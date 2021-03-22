from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.plotting import figure, output_file, show
from bokeh.tile_providers import CARTODBPOSITRON_RETINA, ESRI_IMAGERY, get_provider
from bokeh.models import ColumnDataSource, RangeSlider, Div, CheckboxGroup, CustomJS, LinearColorMapper, ColorBar, CDSView, BooleanFilter
from bokeh.models.tools import HoverTool, BoxZoomTool, ResetTool
from bokeh.models.formatters import NumeralTickFormatter
from bokeh.palettes import Viridis256, Inferno256
from bokeh.themes import built_in_themes

from utils.util import process_data
from os.path import dirname, join

# import time
# import logging
# start = time.time()
# done = time.time()
# logging.info("Process Data: {:.2f}s".format(done-start))


# Load Data
uri = join(dirname(__file__), 'data', 'modified_buffalo_assessment_2020-2021.csv')
df = load_data(uri)

# Initial Data
x_range = (df['x'].min(),df['x'].max())
y_range = (df['y'].min(),df['y'].max())
date_range = (df['DEED YEAR'].min(),df['DEED YEAR'].max())
initial_date = (2013,2019)
df_temp = df[(df['DEED YEAR'] >= initial_date[0]) & (df['DEED YEAR'] <= initial_date[1])]
df_temp = df_temp[(df_temp['PROPERTY CLASS'] >= 200) & (df_temp['PROPERTY CLASS'] < 300)]
source = ColumnDataSource(df_temp)


# Initialize Figure
tile_provider = get_provider(CARTODBPOSITRON_RETINA)
# tile_provider = get_provider(ESRI_IMAGERY)

p = figure(x_range=x_range, 
           y_range=y_range,
           x_axis_type="mercator", 
           y_axis_type="mercator",
           aspect_ratio=.9,
           sizing_mode='scale_both',
           align='center',
           output_backend="webgl",
)
p.add_tile(tile_provider)
p.add_tools(HoverTool(
    tooltips=[
        ( 'Year Sold','@{DEED YEAR}' ),
        ( 'Price','$@{SALE PRICE}{0,0,0}' ),
        ( 'Property Type', '@{PROP CLASS DESCRIPTION}'),
        ( 'Address', '@{ADDRESS}'),
    ],
))

# create linear color mapper and color bar
color_mapper = LinearColorMapper(palette=Viridis256 , low=10000, high=200000)
formatter = NumeralTickFormatter(format='($ 0 a)')
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=12, formatter=formatter)
p.add_layout(color_bar, 'right')

# Add Points
points = p.circle(
    x='x',
    y='y',
    source=source,
    color={'field': "SALE PRICE", 'transform': color_mapper},
    size=5,
)

# set up Text Area (div)
div = Div(
    text="""
          <h2>A Visualization of Property Sales in Buffalo, NY</h2>
          <h3>City of Buffalo -- 2020-2021 Assesment Roll </h3>
          <p>This data consists of the mpst recent sale of all buffalo properties. </p>
          """,
    width=200,
    height=30,
    align='center',
)

def update_data(start_year, end_year):

    df_temp = df[(df['DEED YEAR'] >= start_year) & (df['DEED YEAR'] <= end_year)]

    if 0 not in checkbox_group.active:
        df_temp = df_temp[(df_temp['PROPERTY CLASS'] < 200) | (df_temp['PROPERTY CLASS'] >= 300)]
    if 1 not in checkbox_group.active:
        df_temp = df_temp[(df_temp['PROPERTY CLASS'] < 300) | (df_temp['PROPERTY CLASS'] >= 400)]
    if 2 not in checkbox_group.active:
        df_temp = df_temp[(df_temp['PROPERTY CLASS'] < 400) | (df_temp['PROPERTY CLASS'] >= 500)]
    if 3 not in checkbox_group.active:
        df_temp = df_temp[(df_temp['PROPERTY CLASS'] < 500) | (df_temp['PROPERTY CLASS'] >= 600)]
    if 4 not in checkbox_group.active:
        df_temp = df_temp[(df_temp['PROPERTY CLASS'] < 600) | (df_temp['PROPERTY CLASS'] >= 700)]
    if 5 not in checkbox_group.active:
        df_temp = df_temp[(df_temp['PROPERTY CLASS'] < 700) | (df_temp['PROPERTY CLASS'] >= 800)]
    if 6 not in checkbox_group.active:
        df_temp = df_temp[(df_temp['PROPERTY CLASS'] < 800) | (df_temp['PROPERTY CLASS'] >= 900)]
    if 7 not in checkbox_group.active:
        df_temp = df_temp[(df_temp['PROPERTY CLASS'] < 900) | (df_temp['PROPERTY CLASS'] >= 1000)]
        
    source.data = ColumnDataSource.from_df(df_temp)

# set up RangeSlider 
def range_slider_update(attrname, old, new):
    start_year = range_slider.value[0]
    end_year   = range_slider.value[1]
    range_slider.value = (start_year,end_year)
    update_data(start_year, end_year)

range_slider = RangeSlider(
    title="Adjust Date", # a title to display above the slider
    start=date_range[0],  # set the minimum value for the slider
    end=date_range[1],  # set the maximum value for the slider
    step=1,  # increments for the slider
    value=initial_date,  # initial values for slider
    )
range_slider.on_change('value',range_slider_update)

# Set up CheckboxGroup
def checkbox_group_update(attrname):
    start_year = range_slider.value[0]
    end_year   = range_slider.value[1]
    update_data(start_year, end_year)

LABELS = ["Residential", "Vacant Land","Commercial","Entertainment","Community Services","Industrial","Public Services","Parks"]
default = [0]
checkbox_group = CheckboxGroup(labels=LABELS, active=default, margin=(5,5,5,5), inline=True)
checkbox_group.on_click(checkbox_group_update)


# create layout
layout = layout(
    [
        [div],
        [range_slider],
        [checkbox_group],
        [p],
    ],
    sizing_mode="stretch_width",
    margin=(10,50,10,50),


)

curdoc().add_root(layout)
curdoc().title = "Visual"
