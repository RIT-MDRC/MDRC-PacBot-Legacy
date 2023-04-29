# required for visuals
export PYTHONUNBUFFERED=1
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
#export DISPLAY=eliaspectre.student.rit.edu:0

# pacbot specific
export ADDRESS=192.168.0.100
export PORT=11297

export USE_REAL_ARDUINO=t
export PI_SERIAL_PORT=/dev/ttyUSB0
export USE_PROJECTOR=t
export DISABLE_MOTORS=f
#export FORCE_PF_POSITION=4,29

# HEURISTIC or MCTS
export PATH_TYPE=HEURISTIC

# debug, f or t
export DEBUG_JSON=f
# game state currently broken
export DEBUG_GAME_STATE=f
export DEBUG_PF_INFO=f
export DEBUG_VIS=f

export MOVE_WHEN_PAUSED=f

python3 ~/MDRC-PacBot/2022-2023/pacbot_rpi/pacbot.py
