cd ../
python3 gameEngine/server.py > tests/currenttest/GameServer.txt &
python3 botCode/server.py > tests/currenttest/BotServer.txt &
sleep 1
python3 botCode/pacbotCommsModule.py > tests/currenttest/botComms.txt &
python3 botCode/highLevelPacman.py > tests/currenttest/Pacman.txt &
python3 gameEngine/gameEngine.py > tests/currenttest/GameEngine.txt