cd ../
python3 gameEngine/server.py &
python3 botCode/server.py &
sleep 1
python3 botCode/pacbotCommsModule.py &
python3 botCode/highLevelPacman.py &
python3 gameEngine/gameEngine.py