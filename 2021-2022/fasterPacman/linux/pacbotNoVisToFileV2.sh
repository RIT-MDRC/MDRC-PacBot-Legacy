cd ../
mkdir -p linux/tests/currenttest_$1
python3 -u gameEngine/server.py $1 $2 > linux/tests/currenttest_$1/GameServer.txt &
python3 -u botCode/server.py $1 $2 > linux/tests/currenttest_$1/BotServer.txt &
sleep 10
python3 -u botCode/pacbotCommsModule.py $1 $2 > linux/tests/currenttest_$1/botComms.txt &
python3 -u botCode/highLevelPacman.py $1 $2 > linux/tests/currenttest_$1/Pacman.txt &
python3 -u gameEngine/gameEngine.py $1 $2 << linux/p.txt > linux/tests/currenttest_$1/GameEngine.txt
sleep 5