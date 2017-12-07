//arm must start out straight at (0, 12.98)
//elevator must start out with nema 23 touching the base(hold it down and then press switch) because we want to define that as the lowest possible position

#include <AccelStepper.h>;
#include <Servo.h>;

#define NUM_ROWS 3
#define NUM_COLUMNS 3
#define BAUD_RATE 9600
#define ELEVATOR_TOLERANCE 200
#define ARM_STEPS 6400 //steps per rotation for joint 1 and joint 2 stepper motors
#define ELEVATOR_STEPS 3200 //steps per rotation for elevator stepper motors
#define JOINT_1_ACCELERATION 1000 //Acceleration is in steps/s^2
#define JOINT_2_ACCELERATION 2000
#define ELEVATOR_ACCELERATION 1000
#define ELEVATOR_MAX_SPEED 3000
#define JOINT_2_GEAR_REDUCTION 1.636
#define CIRCLE_RADIUS .5
#define ELEVATOR_UP 1000
#define ELEVATOR_DOWN -50 //to account for tilted surface and the fact that the nema 23 doesn't go completely down when you press the switch
#define PRECISION 100 //higher precision = lower speed
#define HALF_X_WIDTH .3536

AccelStepper joint1(1, A1, A0); // stp A1, dir A0
AccelStepper joint2(1, A3, A2); //stp A3, dir A2
AccelStepper elevator(1, A5, A4); //stp A5, dir A4

const double a = 6.44; // length of joint 1(closer to base) in inches
const double b = 6.54; // length of joint 2(farther from base) in inches

double coords[20] = { // coordinate points in sets of (x,y) format, offset by 1
  999.0, 999.0  // offset
  1.0, 1.0, // position A1
  2.0, 2.0, // position A2
  3.0, 3.0, // position A3
  4.0, 4.0, // position B1
  5.0, 5.0, // position B2
  6.0, 6.0, // position B3
  7.0 ,7.0, // position C1
  8.0, 8.0, // position C2
  9.0, 9.0  // position C3
};

boolean xTurn = true; // Used to track turns

void setup() {
  Serial.begin(BAUD_RATE);
  joint1.setAcceleration(JOINT_1_ACCELERATION);
  joint2.setAcceleration(JOINT_2_ACCELERATION);
  elevator.setAcceleration(ELEVATOR_ACCELERATION);
  elevator.setMaxSpeed(ELEVATOR_MAX_SPEED);
  while (elevator.distanceToGo() > 0) {
    elevator.run();
    Serial.println(elevator.distanceToGo());
  }
  //drawX(5, 5);
  //drawCircle(-5, 5);
  Serial.write("Start");
}

void loop() {}

void serialEvent() {
  if (Serial.available()) {
    int inputInt = Serial.read() - '0';
    if (inputInt == 0)
      xTurn = true;
    else {
      if (xTurn)
        drawX(coords[inputInt*2], coords[inputInt*2+1]);
      else
        drawCircles(coords[inputInt*2], coords[inputInt*2+1]);
      xTurn = !xTurn;
    }
  }
}

void elevatorRun() {
  while (elevator.distanceToGo() > 0) {
    elevator.run();
  }
}

//draws an X at a given (x,y) coordinate, where each line in the X has a length of 1 inch

void drawX(double x, double y) {
  elevator.moveTo(ELEVATOR_UP); //move up to avoid writing on board
  elevatorRun();
  goTo(x - HALF_X_WIDTH, y - HALF_X_WIDTH); // move to bottom left of x
  elevator.moveTo(ELEVATOR_DOWN); // move down to draw
  elevatorRun();
  for (double i = 0.00; i < PRECISION; i++) {
    goTo((x - HALF_X_WIDTH) + i / PRECISION, (y - HALF_X_WIDTH) + i / PRECISION);
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

//draws circle at (x,y) with radius .5 in

void drawCircle(double x, double y) {
  elevator.moveTo(ELEVATOR_UP); //move up to avoid writing on board
  elevatorRun();
  for (double i = 0.00; i < PRECISION; i++) {
    if (i == 1) {
      elevator.moveTo(ELEVATOR_DOWN); // move down to draw
      elevatorRun();
    }
    goTo(CIRCLE_RADIUS * cos(2 * PI * i / PRECISION) + x, CIRCLE_RADIUS * sin(2 * PI * i / PRECISION) + y);
  }
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

  //for debugging

  Serial.print("Z: ");
  Serial.print(Z(x, y));
  Serial.print(" D1: ");
  Serial.print(D1(x, y));
  Serial.print(" D2: ");
  Serial.println(D2(x, y));

  while (abs(joint1.distanceToGo()) > 0 || abs(joint2.distanceToGo()) > 0 || abs(elevator.distanceToGo()) > 0) {
    joint1.run();
    joint2.run();
    elevator.run();
  }
}

//Generates a coordinate lookup table based off of two corners of the table.
//The coordinates fed in must be the positions of A1 and C3, in that order.
boolean generateTable(double x1, double y1, double x2, double y2){
  deltaX = (x2-x1)/3.0;
  deltaY = (y2-y1)/3.0;;
  for (int i = 0, i < NUM_ROWS, i++){//Rows A, B, C
    for (int j = 0, j < NUM_COLUMNS, j++){//Columns 1, 2, 3
      coords[6*i+2*j+2] = x1 + deltaX*(double)(i);
      coords[6*i+2*j+3] = y1 + deltaY*(double)(j);
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
