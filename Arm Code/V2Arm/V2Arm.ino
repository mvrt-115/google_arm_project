//arm starts out folded against right side of the elevator
//everything is measured with respect to a 300 by 300 grid

#include <AccelStepper.h>;

#define BAUD_RATE 115200

#define ARM_STEPS 6400 //steps per rotation for joint 1 and joint 2 stepper motors
#define JOINT_1_ACCELERATION 1600 //Acceleration is in steps/s^2 
#define JOINT_1_MAX_SPEED 8000

#define JOINT_2_GEAR_REDUCTION 1.636
#define JOINT_2_ACCELERATION JOINT_1_ACCELERATION*JOINT_2_GEAR_REDUCTION
#define JOINT_2_MAX_SPEED JOINT_1_MAX_SPEED*JOINT_2_GEAR_REDUCTION

#define ELEVATOR_STEPS 3200 //steps per rotation for elevator stepper motors
#define ELEVATOR_ACCELERATION 1600
#define ELEVATOR_MAX_SPEED 8000

#define ARM_SPEED 500

#define ELEVATOR_UP 300
#define ELEVATOR_DOWN -500

#define JOINT_1_OFFSET -1840 //in steps
#define JOINT_2_OFFSET  -3980 //in steps
#define ELEVATOR_OFFSET -15000 //in steps //-16000

#define PRECISION 100 //higher precision = lower speed
#define LINE_STEP 1
#define ARC_STEP .5

AccelStepper joint1(1, 4, 3); // 1, stp, dir
AccelStepper joint2(1, 13, 12); //1, stp, dir
AccelStepper elevator(1, 6, 7); //1, stp, dir

const double a = 6.473503; // length of joint 1(closer to base) in inches
const double b = 6.4963; // length of joint 2(farther from base) in inches

double currentX = 0.00;
double currentY = 0.00;

boolean busy = false;
boolean commandReady = true;

double angle1 = 0.0;
double angle2 = 90.0;

void setup() {
  Serial.begin(BAUD_RATE);
  while (!Serial) {
    ;
  }
  Serial.print("Connected");
  joint1.setAcceleration(JOINT_1_ACCELERATION);
  joint2.setAcceleration(JOINT_2_ACCELERATION);
  elevator.setAcceleration(ELEVATOR_ACCELERATION);
  elevator.setMaxSpeed(ELEVATOR_MAX_SPEED);
  joint1.setMaxSpeed(JOINT_1_MAX_SPEED);
  joint2.setMaxSpeed(JOINT_2_MAX_SPEED);
}

void serialEvent() {
  if (!busy) {
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
    if (firstChar == 'N') {
      Serial.println("Accepted");
      Serial.println("Start");
      offset();
      Serial.println("Finish");
    }
    else if (commandReady && firstChar == 'L') {
      Serial.println("Accepted");
      Serial.println("Start");
      // Parse data and send to drawLine()
      int firstSpace = incomingCommand.indexOf(" ");
      int secondSpace = incomingCommand.indexOf(" ", firstSpace + 1);
      int firstComma = incomingCommand.indexOf(",");
      int secondComma = incomingCommand.indexOf(",", firstComma + 1);
      String point1[] = {incomingCommand.substring(firstSpace + 1, firstComma), incomingCommand.substring(firstComma + 1, secondSpace)};
      String point2[] = {incomingCommand.substring(secondSpace + 1, secondComma), incomingCommand.substring(secondComma + 1)};
      drawLine(point1[0].toInt(), point1[1].toInt(), point2[0].toInt(), point2[1].toInt());
      Serial.println("Finish");

    }
    else if (commandReady && firstChar == 'A') {
      Serial.println("Accepted");
      Serial.println("Start");
      // Parse data and send to drawArc()
      int firstSpace = incomingCommand.indexOf(" ");
      int secondSpace = incomingCommand.indexOf(" ", firstSpace + 1);
      int thirdSpace = incomingCommand.indexOf(" ", secondSpace + 1);
      int fourthSpace = incomingCommand.indexOf(" ", thirdSpace + 1);
      int comma = incomingCommand.indexOf(",");
      int point[] = {incomingCommand.substring(firstSpace + 1, comma).toInt(), incomingCommand.substring(comma + 1, secondSpace).toInt()};
      int radius = incomingCommand.substring(secondSpace + 1, thirdSpace).toInt();
      int angles[] = {incomingCommand.substring(thirdSpace + 1, fourthSpace).toInt(), incomingCommand.substring(fourthSpace + 1).toInt()};
      drawCircle(point[0], point[1], radius);
      Serial.println("Finish");
    }
    else if (commandReady && firstChar == 'U') {
      Serial.println("Accepted");
      Serial.println("Start");
      elevator.moveTo(ELEVATOR_UP);
      elevatorRun();
      Serial.println("Finish");
    }
    else if (commandReady && firstChar == 'D') {
      Serial.println("Accepted");
      Serial.println("Start");
      elevator.moveTo(ELEVATOR_DOWN);
      elevatorRun();
      Serial.println("Finish");
    }
    else {
      Serial.println("Invalid");
    }
    busy = false;
  }
  else {
    Serial.flush();
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

void newGame() {
  joint1.setAcceleration(JOINT_1_ACCELERATION);
  joint2.setAcceleration(JOINT_2_ACCELERATION);
  elevator.setAcceleration(ELEVATOR_ACCELERATION);
  elevator.setMaxSpeed(ELEVATOR_MAX_SPEED);
  offset();
  commandReady = true;
  Serial.println("Ready");
}

void drawBoard() {
  drawLine(0, 100, 300, 100);
  drawLine(0, 200, 300, 200);
  drawLine(100, 0, 100, 300);
  drawLine(200, 0, 200, 300);
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

void goTo(double x, double y, boolean fast) {

  double distBtwnNewAndPrevious = (x - currentX) * (x - currentX) + (y - currentY) * (x - currentY);

  x /= 50;
  x *= -1;
  x += 8;
  y /= 50;
  y += 4;

  double joint1move = 0.0;
  double joint2move = 0.0;

  if (x >= 0) {
    joint1move = (90 - (D1(x, y) + D2(x, y))) * ARM_STEPS / 360;
    joint2move = (180 - Z(x, y)) * ARM_STEPS * JOINT_2_GEAR_REDUCTION / 360;
    //if it's going to do the weird thing, move up to avoid writing on the board
    joint1.moveTo(joint1move);
    joint2.moveTo(joint2move);
  }
  if (x < 0) {
    joint1move = (90 - (D1(x, y) - D2(x, y))) * ARM_STEPS / 360;
    joint2move = (Z(x, y) - 180) * ARM_STEPS * JOINT_2_GEAR_REDUCTION / 360;
    joint1.moveTo(joint1move);
    joint2.moveTo(joint2move);
  }

  if (!fast) runLoop();
  else {
    if (joint1.targetPosition() >= joint1.currentPosition())
      joint1.setSpeed(ARM_SPEED);
    else
      joint1.setSpeed(-ARM_SPEED);
    if (joint2.targetPosition() >= joint2.currentPosition())
      joint2.setSpeed(ARM_SPEED);
    else
      joint2.setSpeed(-ARM_SPEED);
    while (abs(joint1.distanceToGo()) > 0 || abs(joint2.distanceToGo()) > 0) {
      joint1.runSpeed();
      joint2.runSpeed();
    }
  }

  //runLoop();

  currentX = x;
  currentY = y;
}

void runLoop() {
  while (abs(joint1.distanceToGo()) > 0 || abs(joint2.distanceToGo()) > 0 || abs(elevator.distanceToGo()) > 0) {
    joint1.run();
    joint2.run();
    elevator.run();
  }
}

void elevatorRun() {
  while (abs(elevator.distanceToGo()) > 0) {
    elevator.run();
  }
  delay(100);
}

void loop() {
}

void drawLine(double startX, double startY, double endX, double endY) {
  //  elevator.moveTo(ELEVATOR_UP);
  //  elevatorRun();
  goTo(startX, startY, false);
  delay(500);
  elevator.moveTo(ELEVATOR_DOWN);
  elevatorRun();
  double slope = (endY - startY) / (endX - startX);
  if (endX - startX != 0) { //to deal with vertical lines
    if (endX > startX) {
      for (double i = 0; i <= endX - startX; i += LINE_STEP) {
        goTo(startX + i, startY + slope * i, true);
      }
    }
    else {
      for (double i = 0; i <= startX - endX; i += LINE_STEP) {
        goTo(startX - i, startY - slope * i, true);
      }
    }
  }
  else {
    if (endY > startY) {
      for (double i = 0; i <= endY - startY; i += LINE_STEP) {
        goTo(startX, startY + i, true);
      }
    }
    else {
      for (double i = 0; i <= startY - endY; i += LINE_STEP) {
        goTo(startX, startY - i, true);
      }
    }
  }
  //  elevator.moveTo(ELEVATOR_UP); //move up to avoid writing on board
  //  elevatorRun();
}

void drawArc(double centerX, double centerY, double radius, double startAngle, double endAngle) {
  double startX = centerX + radius * cos(startAngle);
  double startY = centerY + radius * sin(startAngle);

  elevator.moveTo(ELEVATOR_UP);
  elevatorRun();
  goTo(startX, startY, false);
  elevator.moveTo(ELEVATOR_DOWN);
  elevatorRun();

  double angle = endAngle - startAngle;

  if (angle > 0) {

    for (double i = startAngle; i <= endAngle; i += ARC_STEP) {
      goTo(radius * cos(i) + centerX, radius * sin(i) + centerY, true);
    }
  }
  else {
    for (double i = startAngle; i >= endAngle; i -= ARC_STEP) {
      goTo(radius * cos(i) + centerX, radius * sin(i) + centerY, true);
    }
  }
}

//draws circle at (x,y) with radius
void drawCircle(double x, double y, double radius) {
  elevator.moveTo(ELEVATOR_UP); //move up to avoid writing on board
  elevatorRun();
  goTo(radius + x, y, false);
  for (int i = 0; i < PRECISION; i++) {
    goTo(radius * cos(9 * PI / 4 * i / PRECISION) + x, radius * sin(9 * PI / 4 * i / PRECISION) + y, true);
    if (i == 0) {
      elevator.moveTo(ELEVATOR_DOWN);
      elevatorRun();
    }
  }
  elevator.moveTo(ELEVATOR_UP); //move up to avoid writing on board
  elevatorRun();
}
