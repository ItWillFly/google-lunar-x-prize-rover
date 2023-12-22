"""
Вывод графика зависимости площади
солнечной панели от угла падения лучей
на основании уравнений (39) - (43) (см. отчёт)
(c) 2023 ItWillFly (Власко М. М.)
"""

from math import sin, cos, radians, tan, asin
from matplotlib import pyplot

if __name__ == '__main__':
    data = []

    for i in range(1, 80):
        r1 = ((tan(radians(i - asin(sin(radians(i)) / 3.5)))) / (tan(radians(i + asin(sin(radians(i)) / 3.5)))))
        r2 = ((sin(radians(i - asin(sin(radians(i)) / 3.5)))) / (sin(radians(i + asin(sin(radians(i)) / 3.5)))))
        data.append(156.4 / (0.3 * 1367.6 * cos(radians(i)) * ((r1 + r2) / 2)))

    pyplot.title('Солнечная панель')
    pyplot.xlabel('Угол падения, град.')
    pyplot.ylabel('Площадь панели, кв. м')
    pyplot.grid()
    pyplot.plot(range(1, 80), data)
    pyplot.show()
