"""
Вывод графиков зависимости преодолеваемого
расстояния от массы аккумулятора
на основании уравнения (45) (см. отчёт).
(с) 2023 ItWillFly (Власко М. М.)
"""

from matplotlib import pyplot

if __name__ == '__main__':
    data, _data = [], []
    for i in range(101):
        data.append((i * 150 * 0.083 * 3.6) / 156.4)
        _data.append((i * 150 * 0.083 * 3.6) / 66.4)
    pyplot.title('Аккумулятор')
    pyplot.xlabel('Масса аккумулятора, кг')
    pyplot.ylabel('Преодолеваемое расстояние, м')
    pyplot.grid()
    a = pyplot.plot(range(101), data)
    b = pyplot.plot(range(101), _data)
    pyplot.show()
