cd ../
mkdir linux/tests
mkdir linux/tests/currenttest
python3 -u gameEngine/server.py > linux/tests/currenttest/GameServer.txt &
python3 -u botCode/server.py > linux/tests/currenttest/BotServer.txt &
sleep 1
python3 -u botCode/pacbotCommsModule.py > linux/tests/currenttest/botComms.txt &
python3 -u botCode/highLevelPacman.py > linux/tests/currenttest/Pacman.txt &
python3 -u gameEngine/gameEngine.py > linux/tests/currenttest/GameEngine.txt
sleep 5