# Copied from the Dash tutorial documentation at https://dash.plotly.com/layout on 24/05/2021
# Import section modified 10/10/2021 to comply with changes in the Dash library.

# Run this crime_dash_app with `python crime_app.py` and visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_bootstrap_components as dbc
from dash import dcc, Output, Input
from dash import html
from crime_dash_app.visualization import all
from flask_login import login_required
from crime_flask_app.templates.dash_layout import html_layout

v = all()
data = {"Raw": v.df,
        "Population - 2020 GLA Estimate": v.pop2020_df,
        "Population - 2011 Census": v.pop2011_df,
        "Workday Population": v.workday_df,
        "Total Daytime Population": v.daytime_df}

# Define date slider items
date_slider_dict = {}
for i in range(0, len(v.date_list)):
    date_slider_dict[i] = {"label": v.date_list[i], "style": {"transform": "rotate(45deg)"}}

selections = set()

# Define list of data sources
def init_dashboard(flask_app):

    v = all()
    data = {"Raw": v.df,
        "Population - 2020 GLA Estimate": v.pop2020_df,
        "Population - 2011 Census": v.pop2011_df,
        "Workday Population": v.workday_df,
        "Total Daytime Population": v.daytime_df}

# Define date slider items
    date_slider_dict = {}
    for i in range(0, len(v.date_list)):
        date_slider_dict[i] = {"label": v.date_list[i], "style": {"transform": "rotate(45deg)"}}

    selections = set()

    app = dash.Dash(__name__,
                    external_stylesheets = [dbc.themes.BOOTSTRAP],
                    server=flask_app,
                    url_base_pathname="/dashboard/")

# assume you have a "long-form" data frame see https://plotly.com/python/px-arguments/ for more options
    app.index_string = html_layout
    app.layout = html.Div(children=[
        dcc.Store(id="selections"),
        dbc.Row(className="main_content", children=[

        # Display Settings Column
        dbc.Col(className="container", id="display_settings", children=[
            html.H3("Display Settings"),

            # Selecting which dataset will be used to display the data (Always show)
            html.Br(),
            html.P("Select Data"),
            dcc.RadioItems(id="data_select",
                           options=["Raw", "Population - 2020 GLA Estimate",
                                    "Population - 2011 Census",
                                    "Workday Population", "Total Daytime Population"],
                           value="Raw",
                           inline=True,
                           inputStyle={"margin-left": "20px"},
                           style={"font-size": "1vw"}),

            # Dropdown to select which type of chart will be displayed (Always show)
            html.Br(),
            html.P("Select Chart Type"),
            dcc.Dropdown(id="chart_select",
                         options=["Map", "Histogram", "Line"],
                         value="Map",
                         ),

            # Dropdown to select which crime to show a map for (Map and Line only)
            html.Br(),
            html.P("Select Crime to Display", id="crime_select_text"),
            dcc.Dropdown(id="crime_select",
                         options=[{"label": x, "value": x} for x in v.crime_list],
                         value="Drugs"
                         ),

            # Dropdown multi select to select the Borough (Histogram only)
            html.Br(),
            html.P("Select Borough(s) to Display", id="hist_checklist_title"),
            dcc.Dropdown(id="hist_checklist",
                         options=v.borough_list,
                         multi=True,  # Can choose multiple boroughs to display at once
                         value=["Camden"]),

        ], width=3, style={"background-color": "#F6F6F6"}),

        # Visualization Columns (only one will show at a time)
        dbc.Col(className="container", id="visual_charts", children=[
            # Map
            dbc.Row(id="map_row", children=[
                html.H3("Map"),
                dcc.Graph(id="map",
                          figure=v.map_2_layer(df=v.df_r,
                                               selections=selections,
                                               crime="Total Crime")),
                # Slider to select the showcased year
                dcc.Slider(id="map_slider",
                           min=0, max=len(v.date_list) - 1, step=1,
                           marks=date_slider_dict)
            ]),
            # Histogram
            dbc.Row(id="hist_row", children=[
                html.H3("Histogram"),
                dcc.Graph(id="hist",
                          figure=v.hist(date=["202109"],
                                        df=v.pop2020_df, borough=["Camden"])),
                # Slider to select the time frame
                dcc.RangeSlider(id="hist_slider",
                                min=0, max=len(v.date_list) - 1, step=1,
                                marks=date_slider_dict)
            ]),
            # Line Chart
            dbc.Row(id="line_row", children=[
                html.H3("Line Chart"),
                dcc.Graph(id="line",
                          figure=v.line_2(crime="Drugs",
                                          df=v.df_r, borough=["Camden"]))
            ])
        ], width=6
                ),

        # Statistics Column
        dbc.Col(className="container", id="statistics", children=[
            html.H3("Statistics"),
            html.P(""),
            dbc.Row(id="map_statistics", children=[
                html.P("Please select boroughs and month.", style={"font-style": "italic"}),
                html.P(""),
                html.Br()
            ]),
            dbc.Row(id="hist_statistics", children=[
                dcc.Graph(id="hist_correlation_matrix",
                          figure=v.statistics_hist(time_range=v.date_list, df=v.df_r, borough=v.borough_list))
            ]),
            dbc.Row(id="line_statistics", children=[
                # html.H4("Test Line")
            ])],
                width=3)
    ])],
        id = "dash-container")
    init_callback(app)

    for view_function in app.server.view_functions:
        if view_function.startswith(app.config.url_base_pathname):
            app.server.view_functions[view_function] = login_required(app.server.view_functions[view_function])

    return app.server

def init_callback(app):
    @app.callback(
    # Setting up callbacks for different parts of the web crime_dash_app
    Output("map_row", "style"),
    Output("hist_row", "style"),
    Output("line_row", "style"),
    Output("hist_checklist", "style"),
    Output("hist_checklist_title", "style"),
    Output("crime_select", "style"),
    Output("crime_select_text", "style"),
    Output("map_statistics", "style"),
    Output("hist_statistics", "style"),
    Output("line_statistics", "style"),
    Input("chart_select", "value")
)
    def hide(chart_select):
    # Hides/Shows parts of the web crime_dash_app based off which chart is selected
        if chart_select == "Map":
            return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, \
               {'display': 'none'}, {'display': 'block'}, {'display': 'block'}, \
               {'display': 'block'}, {'display': 'none'}, {'display': 'none'}
        if chart_select == "Histogram":
            return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}, {'display': 'block'}, {
            'display': 'block'}, {'display': 'none'}, {'display': 'none'}, \
               {'display': 'none'}, {'display': 'block'}, {'display': 'none'}
        if chart_select == "Line":
            return {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, {'display': 'block'}, {
            'display': 'block'}, {'display': 'block'}, {'display': 'block'}, \
               {'display': 'none'}, {'display': 'none'}, {'display': 'block'}


    @app.callback(
    # Interactivity for histogram (data, borough, timeframe)
    Output("hist", "figure"),
    Input("data_select", "value"),
    Input("hist_checklist", "value"),
    Input("hist_slider", "value")
    )
    def update_data(data_select, hist_checklist, hist_slider):
    # Updates the data used for the histogram based on the slider date range
        if hist_slider is not None:
            if hist_slider[0] != hist_slider[1]:
                fig = v.hist(df=data[data_select],
                         date=[date_slider_dict[i]["label"] for i in list(range(hist_slider[0], hist_slider[1] + 1))],
                         borough=hist_checklist)
            else:
                fig = v.hist(df=data[data_select],
                         date=date_slider_dict[hist_slider[0]]["label"],
                         borough=hist_checklist)
        else:
            fig = v.hist(df=data[data_select],
                     date=v.date_list,
                     borough=hist_checklist)
        return fig


    @app.callback(
    # Get selected boroughs from clicking on the map
    Output("selections", "data"),
    [Input("map", "clickData")]
    )
    def selections_data(clickData):
        if clickData is not None:
            location = clickData['points'][0]['location']

            if location not in selections:
                selections.add(location)
            else:
                selections.remove(location)
        return list(selections)


    @app.callback(
    # Callbacks for updating the map
    Output("map", "figure"),
    Input("selections", "data"),
    Input("crime_select", "value"),
    Input("data_select", "value"),
    Input("map_slider", "value")
    )
    def update_figure(data_1, crime_select, data_select, map_slider):
    # Updates the map when the date range slider changes
        selections = data_1
        if map_slider is not None:
            fig = v.map_2_layer(df=v.reformat(
                data[data_select])[v.reformat(data[data_select])["Date"] == date_slider_dict[map_slider]["label"]],
                            selections=selections,
                            crime=crime_select)
        else:
            fig = v.map_2_layer(df=v.reformat(
            data[data_select])[v.reformat(data[data_select])["Date"] == date_slider_dict[0]["label"]],
                            selections=selections,
                            crime=crime_select)
        return fig


    @app.callback(
    Output("map_statistics", "children"),
    Input("selections", "data"),
    Input("crime_select", "value"),
    Input("data_select", "value"),
    Input("map_slider", "value")
    )
    def update_map_stats(boroughs, crime_select, data_select, map_slider):
        stat_list = []
        if map_slider is not None:
            selected_month = date_slider_dict[map_slider]["label"]
        else:
            selected_month = "201910"
    # Defines how stats are calculated
        last_month = v.statistics_map(df=v.reformat(data[data_select]),
                                  month=selected_month,
                                  crime=crime_select,
                                  selected_areas=boroughs,
                                  m=1)
        last_three_months = v.statistics_map(df=v.reformat(data[data_select]),
                                         month=selected_month,
                                         crime=crime_select,
                                         selected_areas=boroughs,
                                         mmm=1)
        last_year = v.statistics_map(df=v.reformat(data[data_select]),
                                 month=selected_month,
                                 crime=crime_select,
                                 selected_areas=boroughs,
                                 y=1)
        for i in boroughs:
        # Calculates the stats for each borough and appends them to a list
            stat_list.append(html.H4(f"Changes for {i}:"))

            stat_list.append(html.H6("Last month:"))
            if type(last_month[i]) is not str:
                if last_month[i] > 0:
                    stat_list.append(html.H6(f'+{round(last_month[i] * 100, 2)}%', style={'color': "red"}))
                else:
                    stat_list.append(html.H6(f'{round(last_month[i] * 100, 2)}%', style={'color': "green"}))
            elif type(last_month[i]) is str:
                stat_list.append(html.H6(last_month[i], style={'color': "black"}))

            stat_list.append(html.H6("Last 3-months average:"))
            if type(last_three_months[i]) is not str:
                if last_three_months[i] > 0:
                    stat_list.append(html.H6(f'+{round(last_three_months[i] * 100, 2)}%', style={'color': "red"}))
                else:
                    stat_list.append(html.H6(f'{round(last_three_months[i] * 100, 2)}%', style={'color': "green"}))
            elif type(last_three_months[i]) is str:
                stat_list.append(html.H6(last_three_months[i], style={'color': "black"}))

            stat_list.append(html.H6("Last year:"))
            if type(last_year[i]) is not str:
                if last_year[i] > 0:
                    stat_list.append(html.H6(f'+{round(last_year[i] * 100, 2)}%', style={'color': "red"}))
                else:
                    stat_list.append(html.H6(f'{round(last_year[i] * 100, 2)}%', style={'color': "green"}))
            elif type(last_year[i]) is str:
                stat_list.append(html.H6(last_year[i], style={'color': "black"}))

            stat_list.append(html.Br())
        return html.Div(stat_list, style={"maxHeight": "500px", "overflow": "scroll"})


    @app.callback(
    Output("line", "figure"),
    Input("crime_select", "value"),
    Input("data_select", "value"),
    Input("hist_checklist", "value")
    )
    def update_line(crime, data_select, borough):
    # Hides/shows different boroughs on the line chart based oh borough(s) selected
        fig = v.line_2(crime=crime, df=v.reformat(data[data_select]), borough=borough)
        return fig


    @app.callback(
    Output("line_statistics", "children"),
    Input("crime_select", "value"),
    Input("data_select", 'value')
    )
    def update_line_stats(crime, data_select):
    # Defines the different crime rate calculations
        worst_average_borough, average_bad, best_average_borough, average_good, worst_instance_borough, \
        year_max, max, best_borough, year_min, min = v.statistics_line(crime=crime,
                                                                   df=v.reformat(data[data_select]))
        stats_list_bad = [
            html.H5(f"Highest Average {crime} Rate:"),
            html.P(f'{worst_average_borough}, with rate: {round(average_bad, 3)}'),
            html.H5(f"Highest Recorded {crime} Rate:"),
            html.P(f'{worst_instance_borough}, with rate: {round(max, 3)}'),
            html.P(f'Recorded: {year_max[4:]}/{year_max[0:4]}', style={"font-style": "italic", "color": "grey"}),
            html.Br()]

        stats_list_good = [
            html.H5(f"Lowest Average {crime} Rate:"),
            html.P(f'{best_average_borough}, with rate: {round(average_good, 3)}'),
            html.H5(f"Lowest Recorded {crime} Rate:"),
            html.P(f'{best_borough}, with rate: {round(min, 3)}'),
            html.P(f'Recorded: {year_min[4:]}/{year_min[0:4]}', style={"font-style": "italic", "color": "grey"}),
            html.Br()]

    # Returns list of the stats to display in two lists
        return html.Div(children=[
            dbc.Row(className="container", children=stats_list_bad),
            dbc.Row(className="container", children=stats_list_good)
        ])


    @app.callback(
    Output("hist_correlation_matrix", "figure"),
    Input("data_select", "value"),
    Input("hist_checklist", "value"),
    Input("hist_slider", "value")
    )
    def update_hist_stats(data_select, borough, time_range):
    # Updates histogram statistics based on the borough and time range
        if time_range is not None:
            if time_range[0] != time_range[1]:
                fig = v.statistics_hist(
                    time_range=[date_slider_dict[i]["label"] for i in list(range(time_range[0], time_range[1] + 1))],
                    df=v.reformat(data[data_select]),
                    borough=borough)
            else:
                fig = v.statistics_hist(
                    time_range=[date_slider_dict[time_range[0]]["label"]],
                    df=v.reformat(data[data_select]),
                    borough=borough)
        else:
            fig = v.statistics_hist(time_range=v.date_list,
                                df=v.reformat(data[data_select]),
                                borough=v.borough_list)
        return fig


#if __name__ == '__main__':
#    app.run_server(debug=True)
