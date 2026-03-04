**Полный стек для симуляции и управления роботом Fourbox в ROS2**

Монолитный workspace с пакетами для **описания робота**, **симуляции в Gazebo** и **управления реальным роботом**.

**Описание еще в разработке**

## 📦 Пакеты

| Пакет | Назначение | Запуск |
|-------|------------|--------|
| `fourbox_description` | URDF/XACRO модель, RViz визуализация | `display.launch.py` |
| `fourbox_gazebo` | Симуляция в Gazebo | `gazebo.launch.py` |
| `fourbox_bringup` | Реальный робот (hardware) | `bringup.launch.py` |
| `fourbox_control` | PID контроллеры, teleop | `control.launch.py` |
| `fourbox_navigation` | Nav2 стек | `navigation.launch.py` |

## 📋 Требования

### ROS2 + Системные пакеты:
```bash
sudo apt update && sudo apt install -y ros-$ROS_DISTRO-*gazebo* \
  ros-$ROS_DISTRO-nav2* ros-$ROS_DISTRO-robot-state-publisher* \
  ros-$ROS_DISTRO-joint-state-publisher-gui ros-$ROS_DISTRO-xacro \
  ros-$ROS_DISTRO-rviz2 ros-$ROS_DISTRO-controller-manager
```

### Автоустановка зависимостей:
```bash
rosdep install --from-paths src --ignore-src -r -y
```

## 🚀 Быстрый старт

```bash
# 1. Создать workspace
mkdir -p ~/ros2_dasbot_git_ws/src
cd ~/ros2_dasbot_git_ws

# 2. Склонировать репозиторий
# git clone <your-repo> src/

# 3. Установить зависимости
rosdep install --from-paths src --ignore-src -r -y

# 4. Сборка
colcon build --symlink-install
source install/setup.bash
```

## 🎮 Режимы запуска

### 1️⃣ **RViz Визуализация (только модель)**
```bash
ros2 launch fourbox_description display.launch.py
```

### 2️⃣ **Gazebo Симуляция**
```bash
ros2 launch fourbox_gazebo gazebo.launch.py
```

### 3️⃣ **Реальный робот**
```bash
ros2 launch fourbox_bringup bringup.launch.py
```

### 4️⃣ **Полная навигация (симуляция)**
```bash
ros2 launch fourbox_navigation navigation.launch.py
```

### 5️⃣ **Teleop управление**
```bash
ros2 launch fourbox_control teleop.launch.py
```

## 🎛️ Управление

| Команда | Назначение |
|---------|------------|
| `W/A/S/D` | Движение вперед/назад/поворот |
| `SPACE` | Стоп |
| **Joint GUI** | Слайдеры для суставов |
| **RViz2** | 2D/3D Pose, Nav2 Goal |

## 🔧 Полные сценарии

### **Симуляция + Навигация:**
```bash
# Терминал 1: Gazebo
ros2 launch fourbox_gazebo gazebo.launch.py

# Терминал 2: Навигация  
ros2 launch fourbox_navigation navigation.launch.py
```

### **Реальный робот + Teleop:**
```bash
# Терминал 1: Bringup
ros2 launch fourbox_bringup bringup.launch.py

# Терминал 2: Управление
ros2 run fourbox_control teleop_keyboard
```

## 📁 Структура workspace

```
ros2_dasbot_git_ws/
├── src/
│   ├── fourbox_description/     # URDF + RViz
│   ├── fourbox_gazebo/         # Gazebo worlds + spawns
│   ├── fourbox_bringup/        # Hardware drivers
│   ├── fourbox_control/        # Controllers + teleop
│   └── fourbox_navigation/     # Nav2 + SLAM
├── README.md                   # ← Этот файл
└── ...
```

## 🐛 Устранение неисправностей

| Ошибка | Решение |
|--------|---------|
| `Package not found` | `colcon build && source install/setup.bash` |
| `Gazebo world not found` | `sudo apt install ros-$ROS_DISTRO-gazebo-ros-pkgs` |
| `No hardware interface` | Проверьте подключение реального робота |
| `Controller Manager failed` | `ros2 control list_controllers` |
| `Nav2 map not loading` | Создайте `map.yaml` в `config/` |

## ⚙️ Параметры запуска (общие)

```bash
# Отключить RViz:  rviz:=false
# Gazebo empty world: world:=empty
# Verbose logging: log_level:=debug
ros2 launch fourbox_* *.launch.py rviz:=false world:=empty
```

## 💾 Поддерживаемые дистрибутивы

- Humble ✅
- Iron ✅
- Jazzy ✅
- Rolling ✅

## Контакты

- GitHub: [Issues](https://github.com/DASRobotDevelopment/fourbox/issues)
- Telegram: [@dasbot_support](https://t.me/dasrobot_support)

## Лицензия

**Apache License 2.0**

```
Copyright 2026 DASRobot

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

***

**🎉 Готово к использованию! От симуляции до реального робота — всё в одном workspace!**