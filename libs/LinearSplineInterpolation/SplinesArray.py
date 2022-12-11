#FIXME Сделать обработку ситуации, когда магнитка есть, а вариаций нет.
import datetime

from .LinearSpline import LinearSpline


class IncorrectSplineBordersException(Exception):
    pass


class ValueNotFoundException(Exception):
    pass


class SplinesArray:
    debug = 0
    def __init__(self):
        self.spline_array = []
        self.left_border = 0
        self.right_border = 0
        self.cached_last_spline = None

    # Подает на вход список кортежей (x, y), например (time, value)
    def add_spline(self, table):
        #print("enter_add spline table = {}".format(table))
        inserted = 0
        spline = LinearSpline(table)

        if len(self.spline_array) == 0:
            self.left_border = spline.get_spline_domain()[0]
            self.right_border = spline.get_spline_domain()[1]
        else:
            if spline.get_spline_domain()[1] <= self.left_border:
                # self.spline_array.append(spline)
                self.left_border = spline.get_spline_domain()[0]
            elif spline.get_spline_domain()[0] >= self.right_border:
                # self.spline_array.append(spline)
                self.right_border = spline.get_spline_domain()[1]
            else:

                for i in range(len(self.spline_array)-1):
                    if ((self.spline_array[i].get_spline_domain()[1] <= spline.get_spline_domain()[0]) and
                            (spline.get_spline_domain()[1] < self.spline_array[i+1].get_spline_domain()[0])):
                        self.spline_array.insert(i, spline)
                        inserted = 1
                        break
                if inserted == 0:
                    if self.debug:
                        print("Incorrect spline borders. Array borders ({0}, {1}), "
                          "Adding spline borders ({2}, {3})".format(self.left_border,
                                                                    self.right_border,
                                                                    spline.get_spline_domain()[0],
                                                                    spline.get_spline_domain()[1]))
                    raise IncorrectSplineBordersException()
        if inserted == 0:
            self.spline_array.append(spline)
            if self.debug:
                print("Adding spline borders arr_borders ({}, {}), spline_domain ({}, {})".format(self.left_border, self.right_border,
                                                 spline.get_spline_domain()[0], spline.get_spline_domain()[1]))

    def get_value(self, argument):
        #print('got argument {}'.format(argument))
        if self.cached_last_spline is not None:
            #print('cached spline left: {}, right: {}'.format(self.cached_last_spline.get_spline_domain()[0], self.cached_last_spline.get_spline_domain()[1]))
            if self.cached_last_spline.get_spline_domain()[0] <= argument <= self.cached_last_spline.get_spline_domain()[1]:
                value = self.cached_last_spline.get_value(argument)
                return value
        if self.left_border <= argument <= self.right_border:
            for spline in self.spline_array:
                if spline.get_spline_domain()[0] <= argument <= spline.get_spline_domain()[1]:
                    value = spline.get_value(argument)
                    self.cached_last_spline = spline
                    return value
                else:
                    continue
            raise ValueNotFoundException()
        else:
            raise ValueNotFoundException()

    def show_splines(self):
        print("left border {}, right border {}".format(datetime.datetime.fromtimestamp(self.left_border), datetime.datetime.fromtimestamp(self.right_border)))
        print("there is {} splines".format(len(self.spline_array)))
        for i in range(len(self.spline_array)):
            print("{}) left spline border {}, right spline border {}".format(i, datetime.datetime.fromtimestamp(self.spline_array[i].spline_argument_domain[0]), datetime.datetime.fromtimestamp(self.spline_array[i].spline_argument_domain[1])))