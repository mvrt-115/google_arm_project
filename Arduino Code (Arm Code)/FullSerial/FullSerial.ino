//elevator starts out with t-shaped piece resting on 3/32 diameter rod on hole above tape
//arm starts out folded against right side of the elevator

#include <AccelStepper.h>
#include <MultiStepper.h>
#include <Servo.h>

#define NUM_ROWS 3
#define NUM_COLUMNS 3
#define BAUD_RATE 115200
#define ELEVATOR_TOLERANCE 200
#define ARM_STEPS 6400 //steps per rotation for joint 1 and joint 2 stepper motors
#define ELEVATOR_STEPS 3200 //steps per rotation for elevator stepper motors
#define JOINT_1_ACCELERATION 1000 //Acceleration is in steps/s^2
#define JOINT_2_ACCELERATION 2000
#define ELEVATOR_ACCELERATION 1000
#define ELEVATOR_MAX_SPEED 3000
#define JOINT_2_GEAR_REDUCTION 1.636
#define CIRCLE_RADIUS 1
#define ELEVATOR_UP 1000
#define ELEVATOR_DOWN -50 //to account for tilted surface and the fact that the nema 23 doesn't go completely down when you press the switch
#define PRECISION 50 //higher precision = lower speed
#define HALF_X_WIDTH .3536
#define JOINT_1_OFFSET -2000 //in steps
#define JOINT_2_OFFSET  -3650 //in steps
#define ELEVATOR_OFFSET -16000 //in steps

boolean commandReady = false; //boolean to determine if start-up was successful.
boolean busy = true;

AccelStepper joint1(1, 67, 66); // 1, stp, dir
AccelStepper joint2(1, 65, 64); //1, stp, dir
AccelStepper elevator(1, 69, 68); //1, stp, dir

const double a = 6.44; // length of joint 1(closer to base) in inches
const double b = 6.54; // length of joint 2(farther from base) in inches

double coords[18] = { // coordinate points in sets of (x,y) format
  -5, 4.75, // position A1
  -1, 4, // position A2
  3, 6, // position A3
  -5, 6.75, // position B1
  -1, 6, // position B2
  3, 8, // position B3
  -5, 8.75, // position C1
  -1, 8, // position C2
  3, 10  // position C3
};

boolean xTurn = true; // Used to track turns

void setup() {
  Serial.begin(BAUD_RATE);
  while(!Serial){
    ;
  }
  pinMode(13,OUTPUT);
  digitalWrite(13,LOW);
  busy = false;
}

boolean newGame(){
  joint1.setAcceleration(JOINT_1_ACCELERATION);
  joint2.setAcceleration(JOINT_2_ACCELERATION);
  elevator.setAcceleration(ELEVATOR_ACCELERATION);
  elevator.setMaxSpeed(ELEVATOR_MAX_SPEED);
  offset();
  commandReady = true;
  Serial.println("Ready");
}

void offset() {
  joint1.moveTo(JOINT_1_OFFSET);
  joint2.moveTo(JOINT_2_OFFSET);
  elevator.moveTo(ELEVATOR_OFFSET);
  while (abs(joint1.distanceToGo()) > 0 || abs(joint2.distanceToGo()) > 0 || abs(elevator.distanceToGo()) > 0) {
    joint1.run();
    joint2.run();
    elevator.run();
  }
  joint1.setCurrentPosition(0);
  joint2.setCurrentPosition(0);
  elevator.setCurrentPosition(0);
  elevator.moveTo(ELEVATOR_UP); //move up to avoid writing on board
  elevatorRun();
}

void loop() {
}

void serialEvent() {
  if(!busy){
    busy = true;
    String incomingCommand = String();
    char nextChar = '$';
    while (Serial.available()) {
      nextChar = Serial.read();
      Serial.println(nextChar);
      incomingCommand.concat(nextChar);
      Serial.println(incomingCommand);
    }
    char firstChar = incomingCommand.charAt(0);
    if(firstChar == 'N'){
      Serial.println("Accepted");
      Serial.println("Start");
      newGame();
      Serial.println("Finish");
    }
    else if(commandReady && firstChar == 'P'){
      int toMark = incomingCommand.charAt(4) - '0';
      if(toMark < 1 || toMark > 9){
        Serial.println("Invalid");
      }
      if(incomingCommand.charAt(2) == '1'){
        Serial.println("Accepted");
        Serial.println("Start");
        drawX(coords[toMark*2-2], coords[toMark*2-1]);
        Serial.println("Finish");
      }
      else if(incomingCommand.charAt(2) == '2'){
        Serial.println("Accepted");
        Serial.println("Start");
        drawCircle(coords[toMark*2-2], coords[toMark*2-1]);
        Serial.println("Finish");
      }
      else{
        Serial.println("Invalid");
      }
    }
    else if(commandReady && firstChar == 'C'){
      String positionsStr = incomingCommand.substring(4);
      String firstPosition = positionsStr.substring(0,positionsStr.indexOf(' '));
      String secondPosition = positionsStr.substring(positionsStr.indexOf(' ') + 1);
      double x = firstPosition.toDouble();
      double y = secondPosition.toDouble();
      if(incomingCommand.charAt(2) == '1'){
        Serial.println("Accepted");
        Serial.println("Start");
        drawX(x, y);
        Serial.println("Finish");

      }
      else if(incomingCommand.charAt(2) == '2'){
        Serial.println("Accepted");
        Serial.println("Start");
        drawCircle(x, y);
        Serial.println("Finish");
      }
      else{
        Serial.println("Invalid");
      }
    }
    else if(commandReady && firstChar == 'W'){
      int firstPosition = incomingCommand.substring(2,3).toInt();
      int secondPosition = incomingCommand.substring(4,5).toInt();
      Serial.println("Accepted");
      Serial.println("Start");
      winningLine(coords[firstPosition*2-2], coords[firstPosition*2-1], coords[secondPosition*2-2], coords[secondPosition*2-1]);
      Serial.println("Finish");
    }
    else{
      Serial.println("Invalid");
    }
    busy = false;
  }
  else{
    Serial.flush();
  }
}

void elevatorRun() {
  while (elevator.distanceToGo() > 0) {
    elevator.run();
  }
}

void winningLine(double x1, double y1, double x2, double y2){
  elevator.moveTo(ELEVATOR_UP); //move up to avoid writing on board
  elevatorRun();
  goTo(x1, y1);
  elevator.moveTo(ELEVATOR_DOWN); // move down to draw
  elevatorRun();
  goTo(x2, y2);
  elevator.moveTo(ELEVATOR_UP); //move up to avoid writing on board
  elevatorRun();
}

//draws an X at a given (x,y) coordinate, where each line in the X has a length of 1 inch

void drawX(double x, double y) {
  elevator.moveTo(ELEVATOR_UP); //move up to avoid writing on board
  elevatorRun();
  goTo(x - HALF_X_WIDTH, y - HALF_X_WIDTH); // move to bottom left of x
  //Serial.println("Test 1");
  elevator.moveTo(ELEVATOR_DOWN); // move down to draw
  elevatorRun();
  for (double i = 0.00; i < PRECISION; i++) {
    goTo((x - HALF_X_WIDTH) + i / PRECISION, (y - HALF_X_WIDTH) + i / PRECISION);
    //Serial.println(i);
  }
  elevator.moveTo(ELEVATOR_UP); //move up to avoid writing on board
  elevatorRun();
  goTo(x - HALF_X_WIDTH, y + HALF_X_WIDTH); // move to top left of x
  elevator.moveTo(ELEVATOR_DOWN); // move down to draw
  elevatorRun();
  for (double i = 0.00; i < PRECISION; i++) {
    goTo((x - HALF_X_WIDTH) + i / PRECISION, (y + HALF_X_WIDTH) - i / PRECISION);
  }
}

//Draws an X with four goTo() commands instead of 100
void drawXSimple(double x, double y) {
  elevator.moveTo(ELEVATOR_UP); //move up to avoid writing on board
  elevatorRun();
  goTo(x - HALF_X_WIDTH, y - HALF_X_WIDTH); // move to bottom left of x
  elevator.moveTo(ELEVATOR_DOWN); // move down to draw
  elevatorRun();
  goTo((x - HALF_X_WIDTH) + 1, (y - HALF_X_WIDTH) + 1);
  elevator.moveTo(ELEVATOR_UP); //move up to avoid writing on board
  elevatorRun();
  goTo(x - HALF_X_WIDTH, y + HALF_X_WIDTH); // move to top left of x
  elevator.moveTo(ELEVATOR_DOWN); // move down to draw
  elevatorRun();
  goTo((x - HALF_X_WIDTH) + 1, (y + HALF_X_WIDTH) - 1);
}

//draws circle at (x,y) with radius .5 in
void drawCircle(double x, double y) {
  elevator.moveTo(ELEVATOR_UP); //move up to avoid writing on board
  elevatorRun();
  elevator.moveTo(ELEVATOR_DOWN); //move up to avoid writing on board
  elevatorRun();
  goTo(CIRCLE_RADIUS + x, y);
  for (int i = 0; i < PRECISION; i++) {
    goTo(CIRCLE_RADIUS * cos(9 * PI  / 4 * i / PRECISION) + x, CIRCLE_RADIUS * sin(9 * PI  / 4 * i / PRECISION) + y);
  }
  elevator.moveTo(ELEVATOR_UP); //move up to avoid writing on board
  elevatorRun();
}

//draws "circle" composed of five points instead of 50
void drawCircleSimple(double x, double y) {
  elevator.moveTo(ELEVATOR_UP); //move up to avoid writing on board
  elevatorRun();
  goTo(CIRCLE_RADIUS + x, y);
  elevator.moveTo(ELEVATOR_DOWN); //move up to avoid writing on board
  elevatorRun();
  for (int i = 0; i < 6; i++) {
    goTo(CIRCLE_RADIUS * cos(5 * PI  / 2 * i / 5) + x, CIRCLE_RADIUS * sin(5 * PI  / 2 * i / 5) + y);
  }
  elevator.moveTo(ELEVATOR_UP); //move up to avoid writing on board
  elevatorRun();
}

void goTo(double x, double y) {
  if (x >= 0) {
    joint1.moveTo((90 - (D1(x, y) + D2(x, y))) * ARM_STEPS / 360);
    joint2.moveTo((180 - Z(x, y)) * ARM_STEPS * JOINT_2_GEAR_REDUCTION / 360);
  }
  if (x < 0) {
    joint1.moveTo((90 - (D1(x, y) - D2(x, y))) * ARM_STEPS / 360);
    joint2.moveTo((Z(x, y) - 180) * ARM_STEPS * JOINT_2_GEAR_REDUCTION / 360);
  }

  while (abs(joint1.distanceToGo()) > 0 || abs(joint2.distanceToGo()) > 0 || abs(elevator.distanceToGo()) > 0) {
    joint1.run();
    joint2.run();
    elevator.run();
  }
}

//Generates a coordinate lookup table based off of two corners of the table.
//The coordinates fed in must be the positions of A1 and C3, in that order.
boolean generateTable(double x1, double y1, double x2, double y2){
  double deltaX = (x2-x1)/3.0;
  double deltaY = (y2-y1)/3.0;;
  for (int i = 0; i < NUM_ROWS; i++){//Rows A, B, C
    for (int j = 0; j < NUM_COLUMNS; j++){//Columns 1, 2, 3
      coords[6*i+2*j+2] = x1 + deltaX*(double)(i);
      coords[6*i+2*j+3] = y1 + deltaY*(double)(j);
    }
  }
}

//D1 = angle between x-axis and hypotenuse

double D1(double x, double y) {
  if (x != 0) {
    return degrees(atan2(y, x));
  }
  if (x == 0) {
    return 90; //accounting for the fact that when x = 0 atan2 is undefined
  }
}

//D2 = angle between hypotenuse and 1st joint

double D2(double x, double y) {
  double c = sqrt(x * x + y * y);
  return degrees(acos((a * a + c * c - b * b) / (2 * a * c)));
}

// Z = angle between 1st and 2nd joint

double Z(double x, double y) {
  double c = sqrt(x * x + y * y);
  return degrees(acos((a * a + b * b - c * c) / (2 * a * b)));
}
