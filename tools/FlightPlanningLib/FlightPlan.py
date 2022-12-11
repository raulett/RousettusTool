from .FlightRoute import FlightRoute


class FlightPlan(FlightRoute):
    def __init__(self, multiline, crs):
        super().__init__(multiline, crs)
        self.flight_points = None
        self.flight_alt_agl = None
        self.alt_deviation_limit = None
        self.takeoff_and_landing_point_altitude = None