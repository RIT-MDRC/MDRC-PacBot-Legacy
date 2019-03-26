const int numReadings = 70;

int readingsRight[numReadings];      // the readings from the analog input
int readingsLeft[numReadings];      // the readings from the analog input
int readIndexR = 0;              // the index of the current reading
int readIndexL = 0; 
int totalR = 0;                  // the running total
int averageR = 0;                // the average
int totalL = 0;                  // the running total
int averageL = 0;                // the average

int rightSensor = A0;
int leftSensor = A1;

void setup() {
  // initialize serial communication with computer:
  Serial.begin(9600);
  // initialize all the readings to 0:
  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    readingsRight[thisReading] = 0;
  }
  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    readingsLeft[thisReading] = 0;
  }
}

void loop() {
  Serial.print(inRangeRight());
  Serial.println(inRangeLeft());
}

boolean inRangeRight(){
    // subtract the last reading:
  totalR = totalR - readingsRight[readIndexR];
  // read from the sensor:
  readingsRight[readIndexR] = analogRead(rightSensor);
  // add the reading to the total:
  totalR = totalR + readingsRight[readIndexR];
  // advance to the next position in the array:
  readIndexR = readIndexR + 1;

  // if we're at the end of the array...
  if (readIndexR >= numReadings) {
    // ...wrap around to the beginning:
    readIndexR = 0;
  }

  // calculate the average:
  averageR = totalR / numReadings;
  // send it to the computer as ASCII digits
  if(averageR < 435 && averageR > 378){
      return true;
    }else {return false;}
  
  }


  String inRangeLeft(){
    // subtract the last reading:
  totalL = totalL - readingsLeft[readIndexL];
  // read from the sensor:
  readingsLeft[readIndexL] = analogRead(leftSensor);
  // add the reading to the total:
  totalL = totalL + readingsLeft[readIndexL];
  // advance to the next position in the array:
  readIndexL = readIndexL + 1;

  // if we're at the end of the array...
  if (readIndexL >= numReadings) {
    // ...wrap around to the beginning:
    readIndexL = 0;
  }

  // calculate the average:
  averageL = totalL / numReadings;
  // send it to the computer as ASCII digits
  if(averageL < 201 || averageL > 231){
      return "flase";
    }else {return "ture";}
  
  }
