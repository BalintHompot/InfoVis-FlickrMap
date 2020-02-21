from bokeh.plotting import figure, ColumnDataSource
from bokeh.layouts import row, column, widgetbox
from bokeh.models import HoverTool, Slider, CustomJS
from bokeh.embed import json_item
from . import data
## pie chart imports
from math import pi

import pandas as pd
from bokeh.models import Range1d

from bokeh.io import output_file, show, save
from bokeh.palettes import Category10
from bokeh.plotting import figure
from bokeh.transform import cumsum

def split_data_to_categories(categories_meta, all_data, match_field):
	print(all_data)
	split_data = {}
	for key, val_list in categories_meta.items():
		split_data[key] = {}
		indices = []
		for val in all_data[match_field]:
			print(val)
			print(val_list)
			if val in val_list:
				print("found match")
				indices.append(all_data[match_field].index(val))
		for field_key, field_list in all_data.items():
			category_val_list = [field_list[i] for i in indices]
			split_data[key][field_key] = category_val_list

	print("split")
	print(split_data)
	return split_data

def create_hbar(area, plot_data, y_variables=data.model_vars, y_definition=data.label_def_ordered, 
y_extra_info=data.label_extra_ordered, div_name="myplot"):
	values = plot_data.to_numpy()
	values = values[0]

	all_data = ColumnDataSource(data=dict({'variables': y_variables,
				'values': values,
				'definition': y_definition,
				'variables_extra': y_extra_info}))

	tooltips = """
	<div style="width:200px;">
			<div>
                <span style="font-size: 15px; color:blue">Variable:</span>
                <span style="font-size: 12px;">@variables_extra</span>
            </div>
            <div>
                <span style="font-size: 15px; color:blue">Percentage:</span>
                <span style="font-size: 12px;">@values{1.1} %</span>
            </div>
            <div>
                <span style="font-size: 15px; color:blue">Explanation:</span>
                <span style="font-size: 12px;">@definition</span>
            </div>
        </div>
	"""

	TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"
	plot = figure(plot_height = 600, plot_width = 800, 
	          x_axis_label = 'Percentage', 
	           #y_axis_label = ,
	           x_range=(0,100), y_range=y_variables, tools=TOOLS, tooltips=tooltips)

	plot.hbar(left='values', y='variables', right=1, height=0.9, fill_color='red', line_color='black', fill_alpha = 0.75,
	        hover_fill_alpha = 1.0, hover_fill_color = 'navy', source=all_data)
	plot.title.text = "Relevant statistics about " + area
	
	part_rent_slider = Slider(start=0, end=100, value=plot_data.loc[:, 'WPARTHUUR_P'].iloc[0], step=1, title="Private rental")
	corp_rent_slider = Slider(start=0, end=100, value=plot_data.loc[:, 'WCORHUUR_P'].iloc[0], step=1, title="Housing corporation rental")
	high_rent_slider = Slider(start=0, end=100, value=plot_data.loc[:, 'WHUURHOOG_P'].iloc[0], step=1, title="High rent (> 971 euro)")
	middle_rent_slider = Slider(start=0, end=100, value=plot_data.loc[:, 'WHUURMIDDEN_P'].iloc[0], step=1, title="Middle high rent (711 - 971 euro)")
	low_rent_slider = Slider(start=0, end=100, value=plot_data.loc[:, 'WHUURTSLG_P'].iloc[0], step=1, title="Low rent (< 711 euro)")
	living_space_040 = Slider(start=0, end=100, value=plot_data.loc[:, 'WOPP0040_P'].iloc[0], step=1, title="Living space of 0-40 m2")
	living_space_4060 = Slider(start=0, end=100, value=plot_data.loc[:, 'WOPP4060_P'].iloc[0], step=1, title="Living space of 40-60 m2")
	living_space_6080 = Slider(start=0, end=100, value=plot_data.loc[:, 'WOPP6080_P'].iloc[0], step=1, title="Living space of 60-80 m2")
	living_space_80100 = Slider(start=0, end=100, value=plot_data.loc[:, 'WOPP80100_P'].iloc[0], step=1, title="Living space of 80-100 m2")
	living_space_100 = Slider(start=0, end=100, value=plot_data.loc[:, 'WOPP100PLUS_P'].iloc[0], step=1, title="Living space of > 100 m2")

	all_sliders = [part_rent_slider, corp_rent_slider, high_rent_slider,middle_rent_slider, low_rent_slider, 
	living_space_100, living_space_80100, living_space_6080, living_space_4060, living_space_040]

	callback = CustomJS(args=dict(source=all_data), code="""
		var data = source.data;
		var values = data["values"];

		var value = cb_obj.value;
		var var_text = cb_obj.title;

        var variable;
		var value_idx;
		updatePlot(value, var_text);
        socket.on('plot_update', function(msg) {
            value = msg.new_value;
            variable = msg.variable;
			value_idx = msg.index;

			values[value_idx] = value;
			data.values = values;
			source.data = data;
			source.change.emit();

			window.onmouseup = function() {
				updateModel(value, variable);
			}
        });
	""")

	for slider in all_sliders:
		slider.js_on_change('value', callback)

	layout = row(
	    plot,
	    column(*all_sliders),
		width=800
	)

	plot_json = json_item(layout, div_name)

	return plot_json

def create_piechart(area, plot_data, y_variables=data.model_vars, y_definition=data.label_def_ordered, 
y_extra_info=data.label_extra_ordered, div_name="mypiechart"):

	values = plot_data.to_numpy()
	values = values[0]

	all_data = {'variables': y_variables,
				'values': values,
				'definition': y_definition,
				'variables_extra': y_extra_info}

	tooltips = """
	<div style="width:200px;">
			<div>
                <span style="font-size: 15px; color:blue">Variable:</span>
                <span style="font-size: 12px;">@variables_extra</span>
            </div>
            <div>
                <span style="font-size: 15px; color:blue">Percentage:</span>
                <span style="font-size: 12px;">@values{1.1} %</span>
            </div>
            <div>
                <span style="font-size: 15px; color:blue">Explanation:</span>
                <span style="font-size: 12px;">@definition</span>
            </div>
        </div>
	"""

	TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

	### pie chart of owner type
	split_data = split_data_to_categories({"owner":data.all_property_types, "price":data.all_rental_prices,"area": data.all_surface_areas}, all_data, "variables")
	owner_data = split_data["owner"]
	owner_data['angle'] = owner_data['values']/sum(owner_data['values']) * 2*pi
	owner_data['color'] = Category10[len(owner_data)]

	p = figure(plot_height=400, plot_width = 400, title="Owner", toolbar_location=None,
			tools=TOOLS, tooltips=tooltips)

	p.wedge(x=0, y=1, radius=0.3,
			start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
			line_color="white", fill_color='color', legend='variables_extra', source=owner_data)

	p.xgrid.grid_line_color = None
	p.ygrid.grid_line_color = None
	p.x_range=Range1d(-0.5, 1)
	p.axis.visible = False
	
	### pie chart of price category
	price_data = split_data["price"]
	price_data['angle'] = price_data['values']/sum(price_data['values']) * 2*pi
	price_data['color'] = Category10[len(price_data)]
	plot_price = figure(plot_height=400,plot_width = 400, title="Price category", toolbar_location=None,
			tools=TOOLS, tooltips=tooltips)

	plot_price.wedge(x=0, y=1, radius=0.3,
			start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
			line_color="white", fill_color='color', legend='variables_extra', source=price_data)

	plot_price.xgrid.grid_line_color = None
	plot_price.ygrid.grid_line_color = None
	plot_price.x_range=Range1d(-0.5, 1)
	plot_price.axis.visible = False

	### pie chart of area
	area_data = split_data["area"]
	area_data['angle'] = area_data['values']/sum(area_data['values']) * 2*pi
	area_data['color'] = Category10[len(area_data)]
	plot_size = figure(plot_height=400,plot_width = 400, title="Area", toolbar_location=None,
			tools=TOOLS, tooltips=tooltips)

	plot_size.wedge(x=0, y=1, radius=0.3,
			start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
			line_color="white", fill_color='color', legend='variables_extra', source=area_data)

	plot_size.xgrid.grid_line_color = None
	plot_size.ygrid.grid_line_color = None
	plot_size.x_range=Range1d(-0.5, 1)
	plot_size.axis.visible = False
	
	layout_pie = row(
		p,
		plot_price,
		plot_size,
		width=800

	)


	plot_json_pie = json_item(layout_pie, div_name)
	return plot_json_pie