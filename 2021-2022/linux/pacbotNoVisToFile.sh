cd ../
python3 gameEngine/server.py > linux/tests/currenttest/GameServer.txt &
python3 botCode/server.py > linux/tests/currenttest/BotServer.txt &
sleep 1
python3 botCode/pacbotCommsModule.py > linux/tests/currenttest/botComms.txt &
python3 botCode/highLevelPacman.py > linux/tests/currenttest/Pacman.txt &
python3 gameEngine/gameEngine.py > linux/tests/currenttest/GameEngine.txt