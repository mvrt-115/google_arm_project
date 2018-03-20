//elevator starts out with t-shaped piece resting on 3/32 diameter rod on hole above tape
//arm starts out folded against right side of the elevator

#include <AccelStepper.h>;
#include <Servo.h>;

#define NUM_ROWS 3
#define NUM_COLUMNS 3
#define BAUD_RATE 115200
#define ELEVATOR_TOLERANCE 200
#define ARM_STEPS 6400 //steps per rotation for joint 1 and joint 2 stepper motors
#define ELEVATOR_STEPS 3200 //steps per rotation for elevator stepper motors
#define JOINT_1_ACCELERATION 800 //Acceleration is in steps/s^2 
#define JOINT_2_GEAR_REDUCTION 1.636
#define JOINT_2_ACCELERATION JOINT_1_ACCELERATION*JOINT_2_GEAR_REDUCTION
#define ELEVATOR_ACCELERATION 1500
#define ELEVATOR_MAX_SPEED 4000
#define CIRCLE_RADIUS 1
#define ELEVATOR_UP 1000
#define ELEVATOR_DOWN 0
#define PRECISION 50 //higher precision = lower speed
#define HALF_X_WIDTH .3536
#define JOINT_1_OFFSET -1840 //in steps
#define JOINT_2_OFFSET  -3970 //in steps
#define ELEVATOR_OFFSET -14050 //in steps //-16000
#define GCODE_CONSTANT 5

#define JOINT_1_MAX_SPEED 800
#define JOINT_2_MAX_SPEED JOINT_1_MAX_SPEED*JOINT_2_GEAR_REDUCTION

AccelStepper joint1(1, 67, 66); // 1, stp, dir
AccelStepper joint2(1, 65, 64); //1, stp, dir
AccelStepper elevator(1, 69, 68); //1, stp, dir

const double a = 6.473503; // length of joint 1(closer to base) in inches
const double b = 6.49; // length of joint 2(farther from base) in inches

double currentX = 0.00;
double currentY = 0.00;

boolean commandReady = false; //boolean to determine if start-up was successful.
boolean busy = true;

void setup() {
  Serial.begin(BAUD_RATE);
  while(!Serial){
    ;
  }
  busy = false;
  joint1.setAcceleration(JOINT_1_ACCELERATION);
  joint2.setAcceleration(JOINT_2_ACCELERATION);
  elevator.setAcceleration(ELEVATOR_ACCELERATION);
  elevator.setMaxSpeed(ELEVATOR_MAX_SPEED);
  joint1.setMaxSpeed(JOINT_1_MAX_SPEED);
  joint2.setMaxSpeed(JOINT_2_MAX_SPEED);
  offset();
  delay(500);
  drawLine(0, 0, 300, 300);
  /*
  elevator.moveTo(ELEVATOR_UP);
  elevatorRun();

  goTo(300, 300);
  elevator.moveTo(ELEVATOR_DOWN);
  elevatorRun();
  elevator.moveTo(ELEVATOR_UP);
  elevatorRun();


  goTo(300, 0);
  elevator.moveTo(ELEVATOR_DOWN);
  elevatorRun();
  elevator.moveTo(ELEVATOR_UP);
  elevatorRun();

  goTo(0, 300);
  elevator.moveTo(ELEVATOR_DOWN);
  elevatorRun();
  elevator.moveTo(ELEVATOR_UP);
  elevatorRun();

  goTo(0, 0);
  elevator.moveTo(ELEVATOR_DOWN);
  elevatorRun();
  elevator.moveTo(ELEVATOR_UP);
  elevatorRun();
  */
}

void serialEvent() {
  if(!busy){
    busy = true;
    String incomingCommand = String();
    char nextChar = '*';
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
    else if(commandReady && firstChar == 'L'){
      Serial.println("Accepted");
      Serial.println("Start");
      // Parse data and send to drawLine()
      Serial.println("Finish");
      
    }
    else if(commandReady && firstChar == 'A'){
      Serial.println("Accepted");
      Serial.println("Start");
      // Parse data and send to drawArc()
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

void newGame(){
  joint1.setAcceleration(JOINT_1_ACCELERATION);
  joint2.setAcceleration(JOINT_2_ACCELERATION);
  elevator.setAcceleration(ELEVATOR_ACCELERATION);
  elevator.setMaxSpeed(ELEVATOR_MAX_SPEED);
  offset();
  commandReady = true;
  Serial.println("Ready");
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

void goTo(double x, double y) {
  
  x /= 50;
  x *= -1;
  x += 3;
  y /= 50;
  y += 4;

  if (x >= 0) {
    double joint1move = (90 - (D1(x, y) + D2(x, y))) * ARM_STEPS / 360;
    double joint2move = (180 - Z(x, y)) * ARM_STEPS * JOINT_2_GEAR_REDUCTION / 360;
    if(abs(joint1move - joint1.currentPosition()) + abs(joint2move - joint2.currentPosition()) > 3000) {
      delay(500);
      elevator.moveTo(ELEVATOR_UP);
      elevatorRun();
      joint1.moveTo(joint1move);
      joint2.moveTo(joint2move);
      while (abs(joint1.distanceToGo()) > 0 || abs(joint2.distanceToGo()) > 0 || abs(elevator.distanceToGo()) > 0) {
          joint1.run();
          joint2.run();
          elevator.run();
        }
      elevator.moveTo(ELEVATOR_DOWN);
      elevatorRun();
    }
    else {
      joint1.moveTo(joint1move);
      joint2.moveTo(joint2move);
    }

  }
  if (x < 0) {
    double joint1move = (90 - (D1(x, y) - D2(x, y))) * ARM_STEPS / 360;
    double joint2move = (Z(x, y) - 180) * ARM_STEPS * JOINT_2_GEAR_REDUCTION / 360;
    if(abs(joint1move - joint1.currentPosition()) + abs(joint2move - joint2.currentPosition()) > 3000) {
      delay(500);
      elevator.moveTo(ELEVATOR_UP);
      elevatorRun();
      joint1.moveTo(joint1move);
      joint2.moveTo(joint2move);
      while (abs(joint1.distanceToGo()) > 0 || abs(joint2.distanceToGo()) > 0 || abs(elevator.distanceToGo()) > 0) {
          joint1.run();
          joint2.run();
          elevator.run();
        }
      elevator.moveTo(ELEVATOR_DOWN);
      elevatorRun();
    }

    else {
      joint1.moveTo(joint1move);
      joint2.moveTo(joint2move);
    }


  }

  while (abs(joint1.distanceToGo()) > 0 || abs(joint2.distanceToGo()) > 0 || abs(elevator.distanceToGo()) > 0) {
    joint1.run();
    joint2.run();
    elevator.run();
  }
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
  currentX = 0.0;
  currentY = a + b;
}

void loop() {
}

void drawLine(double startX, double startY, double endX, double endY) {  
  elevator.moveTo(ELEVATOR_UP);
  elevatorRun();
  goTo(startX, startY);
  elevator.moveTo(ELEVATOR_DOWN);
  elevatorRun();
  double slope = (endY - startY)/(endX - startX);
  for(double i = startX; i < endX; i+= .1) {
    goTo(startX + i, startY + slope*i);
  }
}

void drawArc(double startX, double startY, double radius, double startA, double endA) {  
  elevator.moveTo(ELEVATOR_UP);
  elevatorRun();
  // Draw Arc using data
}

//Draws circle at (x,y) with radius .5 in
void drawCircle(double x, double y) {
  elevator.moveTo(ELEVATOR_UP); //move up to avoid writing on board
  elevatorRun();
  goTo(CIRCLE_RADIUS + x, y);
  for (int i = 0; i < PRECISION; i++) {
    goTo(CIRCLE_RADIUS * cos(9 * PI / 4 * i / PRECISION) + x, CIRCLE_RADIUS * sin(9 * PI / 4 * i / PRECISION) + y);
    if (i == 0) {
      elevator.moveTo(ELEVATOR_DOWN);
      elevatorRun();
    }
  }
  elevator.moveTo(ELEVATOR_UP); //move up to avoid writing on board
  elevatorRun();
}

void elevatorRun() {
  while (abs(elevator.distanceToGo()) > 0) {
    elevator.run();
  }
  delay(500);
}

//Generates a coordinate lookup table based off of two corners of the table.
//The coordinates fed in must be the positions of A1 and C3, in that order.
boolean generateTable(double x1, double y1, double x2, double y2) {
  double deltaX = (x2 - x1) / 3.0;
  double deltaY = (y2 - y1) / 3.0;
  for (int i = 0; i < NUM_ROWS; i++) { //Rows A, B, C
    for (int j = 0; j < NUM_COLUMNS; j++) { //Columns 1, 2, 3
      coords[6 * i + 2 * j] = x1 + deltaX * (double)(i);
      coords[6 * i + 2 * j + 1] = y1 + deltaY * (double)(j);
      Serial.println(coords[6 * i + 2 * j]);
      Serial.println(coords[6 * i + 2 * j + 1]);
    }
  }
}

