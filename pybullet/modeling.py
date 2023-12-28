"""
После импорта модуля pybullet первое, что нужно сделать,
это "подключиться" к физическому симулятору. pybullet разработан на основе
клиент-серверного API: клиент посылает команды, а физический сервер возвращает статус.
pybullet имеет несколько встроенных физических серверов: DIRECT и GUI.
"""

import pybullet as p
import pybullet_data
import time
import matplotlib.pyplot as plt

physicsClient = p.connect(p.GUI)

p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
p.configureDebugVisualizer(p.COV_ENABLE_SHADOWS, 0)
p.resetDebugVisualizerCamera(2, 75, -30, [0, 0, 0])
p.setGravity(0, 0, -1.62)  # Лунная гравитация

# Загружаем лунную поверхность
moon_orientation = p.getQuaternionFromEuler([1.57, 0, 0])
plane1 = p.loadURDF("lunar_surface.urdf", baseOrientation=moon_orientation)

# Загружаем внешний вид поверхности
lunar_surface = p.loadTexture("1_Roughness.jpg")
p.changeVisualShape(plane1, -1, textureUniqueId=lunar_surface)

# Устанавливаем начальные координаты и загружаем модель
start_pos = [0, 200, -14]
bittle_id = p.loadURDF("model.urdf", start_pos)

# Загружаем визуализацию солнечной панели
solar_panel = p.loadTexture("solar_panel.png")
p.changeVisualShape(bittle_id, 11, textureUniqueId=solar_panel)

ids = []
for j in range(p.getNumJoints(bittle_id)):
    info = p.getJointInfo(bittle_id, j)
    jointName = info[1]
    jointType = info[2]
    print(jointName, jointType, j)
    ids.append(j)


def move(tp):
    """
    Функция для автоматизации движения лунохода
    """
    for joint in range(p.getNumJoints(bittle_id)):
        if joint not in []:
            p.setJointMotorControl2(bittle_id,
                                    joint,
                                    p.POSITION_CONTROL,
                                    targetPosition=tp,
                                    force=300,
                                    maxVelocity=25)


# Запускаем симуляцию
i = 0
a, b, c = [], [], []
while True:
    position = p.getBasePositionAndOrientation(bittle_id)[0]
    velocity = p.getBaseVelocity(bittle_id)[0]
    a.append(position[0])
    b.append(position[1])
    c.append(position[2])
    print(position, velocity)  # Выводим расположение и скорость лунохода
    p.resetDebugVisualizerCamera(cameraDistance=1.5, cameraYaw=180, cameraPitch=-30, cameraTargetPosition=position)
    move(i)
    i += 1
    time.sleep(1/1000)
    p.stepSimulation()

# Если заменить бесконечный цикл на конечный,
# Вызываем вывод графика
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(a, b, c)
plt.show()

