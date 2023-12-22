"""
Приложение с графическим интерфейсом для
вычисления параметров скорости, угла наклона и
высоты посадочного модуля на основании уравнений
(11) - (14) и (21) (см. отчёт).
(с) 2023 ItWillFly (Власко М. М.)
"""

import os.path
from tkinter import (
    Tk,
    Label,
    Entry,
    ttk,
    messagebox
)
from scipy.integrate import odeint
from scipy.optimize import fsolve
from numpy import array
from math import sin, cos, pi, log
from matplotlib import pyplot
from pickle import load, dump


def center_window(root, width, height):
    """
    Функция для размещения окон в центре экрана.
    """

    # Получение ширины и высоты экрана монитора
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Расчёт координаты верхнего левого угла окна
    x_coord = int((screen_width / 2) - (width / 2))
    y_coord = int((screen_height / 2) - (height / 2))

    # Установка рассчитанной геометрии
    root.geometry(f'{width}x{height}+{x_coord}+{y_coord}')


class App:
    def __init__(self):
        """
        Инициализация элементов графического интерфейса.
        """
        # Создание объекта основного окна
        self.window = Tk()
        # Установка заголовка окна
        self.window.title('Моделирование посадки на Луну')
        # Установка размера и центрирование окна
        center_window(self.window, 390, 690)
        # Установка процедур, выполняющихся в момент нажатия кнопки "Х"
        self.window.protocol('WM_DELETE_WINDOW', self.on_closing)
        # Запрет изменения размеров окна
        self.window.resizable(False, False)

        # Инициализация элементов графического интерфейса
        Label(self.window, text='Моделирование посадки на Луну', font=('Arial Bold', 16)).place(x=20, y=20)

        Label(self.window, text='Введите массу посадочного модуля (кг):').place(x=20, y=70)
        self.mass_inp = Entry(self.window, width=35)
        self.mass_inp.place(x=20, y=110)

        Label(self.window, text='Введите начальную скорость посадочного модуля (м/с):').place(x=20, y=150)
        self.velocity_inp = Entry(self.window, width=35)
        self.velocity_inp.place(x=20, y=190)

        Label(self.window, text='Введите начальную высоту посадочного модуля (м):').place(x=20, y=230)
        self.height_inp = Entry(self.window, width=35)
        self.height_inp.place(x=20, y=270)

        Label(self.window, text='Введите силу тяги двигателя (Н):').place(x=20, y=310)
        self.force_inp = Entry(self.window, width=35)
        self.force_inp.place(x=20, y=350)

        Label(self.window, text='Введите удельный импульс двигателя (м/с):').place(x=20, y=390)
        self.j_inp = Entry(self.window, width=35)
        self.j_inp.place(x=20, y=430)

        Label(self.window, text='Введите временной параметр (с):').place(x=20, y=470)
        self.time_inp = Entry(self.window, width=35)
        self.time_inp.place(x=20, y=510)

        # Заполнение полей ввода сохранёнными данными, если таковые имеются
        if os.path.exists('data.dat'):
            with open('data.dat', 'rb') as f:
                data = load(f)
                self.mass_inp.insert(0, data[0])
                self.velocity_inp.insert(0, data[1])
                self.height_inp.insert(0, data[2])
                self.force_inp.insert(0, data[3])
                self.j_inp.insert(0, data[4])
                self.time_inp.insert(0, data[5])

        Label(self.window, text='Показать:').place(x=20, y=560)

        ttk.Button(self.window, text='Скорость', command=self.calc).place(x=20, y=590)
        ttk.Button(self.window, text='Угол', command=lambda: self.calc(mode='a')).place(x=20, y=620)
        ttk.Button(self.window, text='Высота', command=lambda: self.calc(mode='h')).place(x=20, y=650)

        self.fuel_label = Label(self.window)
        self.fuel_label.place(x=110, y=590)

        self.time_1_label = Label(self.window)
        self.time_1_label.place(x=110, y=610)

        self.time_2_label = Label(self.window)
        self.time_2_label.place(x=110, y=630)

        self.time_3_label = Label(self.window)
        self.time_3_label.place(x=110, y=650)

    def calc(self, mode='v'):
        """
        Расчёт процесса посадки и вывод графиков
        :param mode: Выводимый график: v - скорость, h - высота, a - угол.
        """
        # Закрытие окна графика, если таковое было открыто ранее
        pyplot.close()

        def first_model(args, t):
            """
            Функция, возвращающая odeint дифференциальные уравнения
            """
            return (
                g * cos(args[1]) - p / (m0 - ((p * t) / j)),
                (-g / args[0]) * sin(args[1]),
                -args[0] * cos(args[1])
            )

        # Считывания введённых параметров и проверка на корректность
        try:
            p = float(self.force_inp.get())
            m0 = float(self.mass_inp.get())
            j = float(self.j_inp.get())
            v0 = float(self.velocity_inp.get())
            h0 = float(self.height_inp.get())
            time = int(self.time_inp.get())
            g = 1.622
        except ValueError:
            messagebox.showwarning('Ошибка', 'Введены некорректные значения!')
            return

        # Инициализация списков изменяющихся величин
        velocity, angle, height = [], [], []
        # Расход топлива
        k = p / j
        # Массив численного решения на этапе гравитационного разворота
        first_res = odeint(first_model, [v0, pi / 2, h0], [i for i in range(time)])

        # Перенос данных в отдельные списки до тех пор...
        temp = float('inf')
        for i in first_res:
            # ... пока разворот не завершится
            if float(i[1]) >= temp or not float(i[1]) or float(i[0]) < 0:
                angle.append(float(i[1]))
                break

            velocity.append(-float(i[0]))
            angle.append(float(i[1]))
            height.append(float(i[2]))
            temp = float(i[1])

        # Расход топлива на этапе разворота
        fuel = k * len(angle)
        # продолжительность разворота
        first_time = len(velocity)

        def solve(t):
            """
            Функция, возвращающая fsolve уравнения для решения
            """
            return (
                velocity[-1] - g * (t[0] + t[1]) - j * log((m0 - k * t[0]) / m0),
                height[-1] + velocity[-1] * (t[0] + t[1]) - (g * (t[0] + t[1]) ** 2) / 2 - j *
                ((t[0] - m0 / k) * (log(1 - (k * t[0]) / m0) - 1) - m0 / k)
            )

        # Корни системы уравнений
        a, b = list(fsolve(solve, array([0, 0])))

        def second_model(args, t):
            """
            Функция, возвращающая odeint дифференциальные уравнения
            """
            return (
                -g,
                args[0]
            )
        # Решение уравнений на пассивном участке
        res = odeint(second_model, [velocity[-1], height[-1]], [i for i in range(abs(int(b)) + 1)])
        for i in res:
            velocity.append(float(i[0]))
            height.append(float(i[1]))

        def third_model(args, t):
            """
            Функция, возвращающая odeint дифференциальные уравнения
            """
            return (
                -g + (p / (m0 - ((p * t) / j))),
                args[0]
            )

        # Решение уравнений на активном участке
        third_res = odeint(third_model, [velocity[-1], height[-1]], [i for i in range(abs(int(a)) + 1)])
        fuel += (abs(int(a)) + 1) * k

        for i in third_res:
            velocity.append(float(i[0]))
            height.append(float(i[1]))

        # Вывод данных в основное окно и консоль
        self.fuel_label.configure(text=f'Расход топлива: {fuel:.2f} кг')
        self.time_1_label.configure(text=f'Гравитационный разворот: {first_time} с')
        self.time_2_label.configure(text=f'Пассивный участок вертикального спуска: {b:.2f} с')
        self.time_3_label.configure(text=f'Активный участок вертикального спуска: {a:.2f} с')
        print(f'Отклонение от нуля:\nv = {velocity[-1]} м/с\nh = {height[-1]} м')

        # Словарь для конфигурации вывода графиков
        pars = {
            'v': ('Скорость', 'Скорость, м/с', velocity),
            'a': ('Угол', 'Угол, радиан', angle),
            'h': ('Высота', 'Высота, м', height[:-1])
        }

        # Вывод графика в отдельном окне
        pyplot.title(pars[mode][0])
        pyplot.xlabel('Время, с')
        pyplot.ylabel(pars[mode][1])
        pyplot.grid()
        pyplot.plot(range(len(pars[mode][2])), pars[mode][2])
        pyplot.show()

    def on_closing(self):
        """
        Процедура сохранения введённых данных в
        файл в момент закрытия окна
        """
        with open('data.dat', 'wb') as f:
            dump([
                self.mass_inp.get(),
                self.velocity_inp.get(),
                self.height_inp.get(),
                self.force_inp.get(),
                self.j_inp.get(),
                self.time_inp.get()
            ], f)
        # Ручной выход из программы
        self.window.quit()


if __name__ == '__main__':
    # Инициализация объекта приложения
    app = App()
    # Вызов метода mainloop для предотвращения авто закрытия окна
    app.window.mainloop()
