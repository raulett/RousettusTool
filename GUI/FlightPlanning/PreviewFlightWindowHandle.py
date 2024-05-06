# coding=utf-8
import numpy as np
import plotly.graph_objects as go

from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QWidget, QDialog, QTableView
from PyQt5.QtCore import Qt
from qgis.core import QgsFeature

from GUI.FlightPlanning.FlightPlansTableModel import FlightPlansTableModel
from UI.FlightPlanning.flight_plot_ui import Ui_PreviewWindow
from tools.ServiceClasses.RousettusLoggerHandler import RousettusLoggerHandler


# TODO при закрытии главного окна не закрывается окно графиков.

class PreviewFlightWindowHandle(Ui_PreviewWindow, QWidget):
    def __init__(self, flights_model: FlightPlansTableModel):
        self.logger = RousettusLoggerHandler.get_handler().logger
        super().__init__()
        self.plotly_webview = QWebEngineView(self)
        self.setupUi(self)
        self.horizontalLayout.addWidget(self.plotly_webview)
        self.flights_model = flights_model
        self.flights_tableview.setModel(self.flights_model)
        self.flights_tableview.setColumnHidden(0, True)
        self.flights_tableview.setSelectionBehavior(QTableView.SelectRows)
        figure = self._init_plot()
        self.plotly_webview.setHtml(figure.to_html(include_plotlyjs='cdn') if figure else '')
        self._init_selection()
        self._init_signals()

    def _init_signals(self):
        self.flights_tableview.selectionModel().selectionChanged.connect(self._init_selection)

    def _init_selection(self):
        rows = self.flights_tableview.selectedIndexes()
        self.logger.debug(rows)
        if rows:
            flight = self.flights_model.data(rows[0], Qt.UserRole)
            self.logger.debug(flight)
            self._init_plot(flight)

    def _init_plot(self, flight: dict = None) -> go.Figure or None:
        if flight:
            features = flight.get('flight_points')
            self.logger.debug(features[0].attribute('flight_name'))
            flight_name = features[0].attribute('flight_name')
            layer_name = flight.get('layer_name')
            flight_metrics = flight.get('flight_metrics')
            flight_plan = flight.get('flight_plan')

            # создаем графики:
            # График поверхности
            gnd_graph = flight_plan.alt_points
            x_gnd = [x[0] for x in gnd_graph]
            y_gnd = [y[1] for y in gnd_graph]
            ground_trace = go.Scatter(x=x_gnd,
                                      y=y_gnd,
                                      name="ground",
                                      fill='tozeroy',
                                      fillcolor='rgba(1, 0, 0, 0.2)',
                                      line_color='rgb(0.2, 0, 0)',
                                      hovertemplate='GND<br>Distance=%{x:.1f}<br>Altitude=%{y:.1f}<extra></extra>',
                                      hoverinfo="x+y",
                                      mode='lines',
                                      )

            # Полетные точки
            # TODO в середине неправильно красит. после того, как я стану выгружать полет, поправить покрас.
            flight_points_num = [feat.attribute('point_num') for feat in features]
            flight_points_distance = [feat.attribute('distance') for feat in features]
            flight_points_alt = [feat.attribute('alt_asl') for feat in features]
            is_service_color = [feat.attribute('is_service') for feat in features]
            flight_trace = go.Scatter(x=flight_points_distance,
                                      y=flight_points_alt,
                                      mode='lines+markers+text',
                                      name="service segment",
                                      line_color='green',
                                      hovertemplate='Flight<br>Distance=%{x:.1f}<br>Altitude=%{y:.1f}<extra></extra>',
                                      hoverinfo="x+y",
                                      hoveron="points+fills",
                                      text=flight_points_num,
                                      textposition="top center",
                                      )

            colorize_points = [alt[0] if alt[1] else None for alt in zip(flight_points_alt, is_service_color)]
            self.logger.debug(colorize_points)
            colorize_line = go.Scatter(x=flight_points_distance,
                                       y=colorize_points,
                                       mode='lines+markers',
                                       name='survey segment',
                                       line_color='red',
                                       hoverinfo='none',
                                       connectgaps=False,
                                       )

            fig = go.Figure(
                data=[ground_trace, flight_trace, colorize_line],
                layout=go.Layout(
                    title=go.layout.Title(text=f'Flight {flight_name} at layer {layer_name} elevation graph.'),
                    xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text="Distance, m"),
                                          rangeslider=dict(visible=True),
                                          type="linear",
                                          ),
                    yaxis=go.layout.YAxis(title=go.layout.yaxis.Title(text="Altitude, m"),
                                          range=[min(y_gnd + flight_points_alt) - 10,
                                                 max(y_gnd + flight_points_alt) + 50],
                                          ),
                    hovermode="x unified",
                    hoverdistance=-1
                ),
            )

            self.logger.debug(flight)
            self.logger.debug(gnd_graph)
            self.logger.debug(flight_plan)
            self.plotly_webview.setHtml(fig.to_html(include_plotlyjs='cdn') if fig else '')
