# required for visuals
export PYTHONUNBUFFERED=1
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
export DISPLAY=eliaspectre.student.rit.edu:0

# pacbot specific
export ADDRESS=eliaspectre.student.rit.edu
export PORT=11297

export USE_REAL_ARDUINO=t
export PI_SERIAL_PORT=/dev/ttyUSB0
export USE_PROJECTOR=f
export DISABLE_MOTORS=t
export FORCE_PF_POSITION=4,29

# debug, f or t
export DEBUG_JSON=f
# game state currently broken
export DEBUG_GAME_STATE=f
export DEBUG_PF_INFO=f
export DEBUG_VIS=t

export MOVE_WHEN_PAUSED=t

python3 ~/MDRC-PacBot/2022-2023/pacbot_rpi/pacbot.py
