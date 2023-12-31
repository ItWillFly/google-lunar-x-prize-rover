# GOOGLE LUNAR X PRIZE ROVER

----------------
### _Проектная работа по дисциплине «Введение в авиационную и ракетно-космическую технику»_
#### Выполнена учащимися 108 группы 1 курса кафедры 806 института №8 Московского Авиационного Института (национального исследовательского университета) (МАИ) 

----------------
***ОБЩИЕ СВЕДЕНИЯ***

Целью работы является моделирование исследовательской миссии лунохода, удовлетворяющего условиям
премии [Google Lunar X PRIZE](https://ru.wikipedia.org/wiki/Google_Lunar_X_PRIZE), а именно:
- Мягкая посадка на поверхность Луны.
- Перемещение по поверхности не менее чем на 500 метров.
- Передача на Землю изображений и видео в высоком разрешении.

В рамках проведения исследовательской работы было проведено построение физико-математических моделей
процессов, происходящих во время мягкой посадки лунохода и его дальнейшего перемещения по поверхности Луны.

Проведены расчёты и построения графиков зависимостей различных параметров (скорость, угол наклона,
высота) на всех этапах процесса мягкой посадки с помощью различных расширений языка Python (```scipy```, 
```matplotlib```), разработано [приложение](/calculations/main_equation.py) с графическим интерфейсом для 
упрощения вычислений.

Рассмотрены различные аспекты работы лунохода на поверхности (действующие на аппарат силы,
необходимая для развития определённой скорости мощность двигателей, характеристики и мощность передающей
антенны). На основании оценки мощности всех вышеперечисленных устройств получены необходимые для её обеспечения
характеристики энергетических установок (солнечной панели или аккумулятора).

Проведено моделирование внешнего вида и перемещения лунохода в среде физической симуляции с использованием
модуля ```PyBullet```. Проведён анализ данных, полученных в процессе этого моделирования.

-----------------

***РЕЗУЛЬТАТЫ***

- Составлен отчёт о [научно-исследовательской работе](https://drive.google.com/file/d/1PwoNhlBfU5G3LuODS3cMaJ4mPd60qW7k/view?usp=sharing).
- Создан [видеоматериал](https://youtu.be/bfBmrlZduzs) и [презентация](https://docs.google.com/presentation/d/1zfeQYwUeYD5N8CDFuzjC3Xt9FlDYG2F-/edit?usp=sharing&ouid=117813514880364357401&rtpof=true&sd=true), раскрывающие суть и результаты работы.
- Составлены программные модули для проведения расчётов (представлены в директории [calculations](/calculations)).
- Составлены программные модули, обеспечивающие моделирование в среде ```PyBullet``` (представлены в 
директории [pybullet](/pybullet))
---------------------
***УЧАСТНИКИ РАБОТЫ***

Команда _ItWillFly_:

| Участник         | Вклад                                                                              |
|------------------|------------------------------------------------------------------------------------|
| Власко М. М.     | Разработка физико-математических моделей, проведение расчётов, составление отчёта. | 
| Гаврилов Н. В.   | Создание моделей в PyBullet, проведение моделирования                              | 
| Переверзев А. О. | Участие в разработке физико-математических моделей                                 | 
| Щапов А. Д.      | Создание презентации                                                               | 

---------------------
_Москва, 2023_
