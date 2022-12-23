import numpy as np
# Создает экземпляр функции линейного сплайна на основе таблично заданной функции. Таблично заданная функция передается
# в виде списка кортежей (аргумент, значение).
# кортежи будут отсортированы по значению аргумента
class OutOfRangeException(Exception):
    pass


class ImpossibleException(Exception):
    pass


class LinearSpline:
    # Конструктор принимает на вход список кортежей (x, y), Значений таблично заданной функции

    def __init__(self, table):
        def get_key(item):
            return item[0]

        table = sorted(table, key=get_key)

        self.spline_argument_domain = (table[0][0], table[len(table) - 1][0])

        self.spline = []
        for i in range(len(table)):
            if i == 0:
                continue
            else:
                try:
                    k = (table[i - 1][1] - table[i][1]) / (table[i - 1][0] - table[i][0])
                    b = table[i - 1][1] - (table[i - 1][1] - table[i][1]) / (table[i - 1][0] - table[i][0]) * table[i - 1][0]
                except ZeroDivisionError:
                    #print("Div by zero error(time i-1 = {}, time i = {})".format(table[i-1][0], table[i][0]))
                    continue
                function_domain = (table[i - 1][0], table[i][0])
                self.spline.append((k, b, function_domain))
        self.spline = np.array(self.spline, dtype=object)



    def get_spline_domain(self):
        return self.spline_argument_domain

    def get_function_domain(self, func_number):
        return self.spline[func_number][2]

    def get_value(self, argument):
        #print("LinarSpline. search argument: {}, left: {}, right: {}".format(argument, self.spline_argument_domain[0], self.spline_argument_domain[1]))
        prev_middle = 0
        # Проверка, что передаваемый аргумент внутри области определения сплайна
        if argument < self.spline_argument_domain[0] or argument > self.spline_argument_domain[1]:
            raise OutOfRangeException("argument out of range")
        left_boarder = 0
        right_boarder = len(self.spline) - 1
        while True:

            middle = int((right_boarder + left_boarder) / 2)
            if prev_middle == middle:
                if argument < self.get_function_domain(middle)[0]:
                    middle -= 1 if middle > 0 else middle
                if argument > self.get_function_domain(middle)[1]:
                    middle += 1 if middle < right_boarder else middle
            if middle < 0 or middle > right_boarder: raise ImpossibleException("impossible exception")
            #print('argument: {}. current borders: {}, current middle {}'.format(argument, (self.get_function_domain(middle)[0], self.get_function_domain(middle)[1]), middle))

            if self.get_function_domain(middle)[0] <= argument <= self.get_function_domain(middle)[1]:
                return self.spline[middle][0] * argument + self.spline[middle][1]

            else:
                if argument < self.get_function_domain(middle)[0]:
                    right_boarder = middle

                if argument > self.get_function_domain(middle)[1]:
                    left_boarder = middle
            prev_middle = middle
