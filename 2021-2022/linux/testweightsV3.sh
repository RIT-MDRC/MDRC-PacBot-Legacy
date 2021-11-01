python3 testweightsV3.py
if [ $? -eq 0 ]
then
  echo "exit code 0"
else
  # Redirect stdout from echo command to stderr.
  echo "exit code 1"
fi
sleep 5