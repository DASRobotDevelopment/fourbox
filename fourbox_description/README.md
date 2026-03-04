**Пакет описания робота Fourbox для ROS2**

Пакет содержит URDF/XACRO модель робота, launch-файлы для визуализации и конфигурацию RViz.

## Требования

### Системные зависимости ROS2:
```bash
sudo apt update
sudo apt install ros-$ROS_DISTRO-joint-state-publisher-gui \
                 ros-$ROS_DISTRO-robot-state-publisher \
                 ros-$ROS_DISTRO-rviz2 \
                 ros-$ROS_DISTRO-xacro
```

### Автоматическая установка всех зависимостей:
```bash
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
```

## Быстрый запуск

```bash
# 1. Создать workspace (если не существует)
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws

# 2. Клонировать пакет в src/
# git clone https://github.com/DasbotDev/fourbox.git src/fourbox

# 3. Сборка
colcon build --packages-select fourbox_description
source install/setup.bash

# 4. Запуск визуализации
ros2 launch fourbox_description display.launch.py
```

## Структура пакета

```
fourbox_description/
├── CMakeLists.txt         # Минимальный (только install)
├── package.xml            # Зависимости: xacro, rviz2, publishers
├── description/           # URDF/XACRO файлы
│   └── fourbox.urdf.xacro
├── launch/                # Launch файлы
│   └── display.launch.py  # Основной launch (RViz + publishers)
└── config/                # RViz конфигурация
    └── fourbox_description_config.rviz
```

## Управление

- **Joint State Publisher GUI**: Синий слайдеры для управления суставами
- **RViz2**: 3D визуализация робота

## Параметры запуска

```bash
# Без RViz
ros2 launch fourbox_description display.launch.py rviz:=false
```

## 🐛 Устранение неисправностей

| Ошибка | Решение |
|--------|---------|
| `No executable found: joint_state_publisher_gui` | `sudo apt install ros-$ROS_DISTRO-joint-state-publisher-gui` |
| `Package 'fourbox_description' not found` | `colcon build && source install/setup.bash` |
| `xacro: No such file` | `sudo apt install ros-$ROS_DISTRO-xacro` |
| `NameError in launch` | `rm -rf build/ install/ && colcon build` |

## 📋 Зависимости (package.xml)

```xml
<exec_depend>xacro</exec_depend>
<exec_depend>rviz2</exec_depend>
<exec_depend>robot_state_publisher</exec_depend>
<exec_depend>joint_state_publisher_gui</exec_depend>
```

## 💾 Поддерживаемые дистрибутивы

- Humble
- Iron  
- Jazzy
- Rolling

## 📄 Лицензия

Apache License 2.0

```
Copyright [2026] [DASRobot]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## Контакты

- GitHub: [Issues](https://github.com/DASRobotDevelopment/fourbox/issues)
- Telegram: [@dasbot_support](https://t.me/dasrobot_support)