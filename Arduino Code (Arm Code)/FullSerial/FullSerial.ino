//elevator starts out with t-shaped piece resting on 3/32 diameter rod on hole above tape
//arm starts out folded against right side of the elevator

#include <AccelStepper.h>;
#include <Servo.h>;

#define BAUD_RATE 115200
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
#define PRECISION 50 //higher precision = lower speed
#define HALF_X_WIDTH .3536
#define JOINT_1_OFFSET -2000 //in steps
#define JOINT_2_OFFSET  -3650 //in steps
#define ELEVATOR_OFFSET -16000 //in steps

AccelStepper joint1(1, 67, 66); // 1, stp, dir
AccelStepper joint2(1, 65, 64); //1, stp, dir
AccelStepper elevator(1, 69, 68); //1, stp, dir

const double a = 6.44; // length of joint 1(closer to base) in inches
const double b = 6.54; // length of joint 2(farther from base) in inches

const double coords[20] = { // coordinate points in sets of (x,y) format, offset by 1
  999.0, 999.0  // offset
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
  joint1.setAcceleration(JOINT_1_ACCELERATION);
  joint2.setAcceleration(JOINT_2_ACCELERATION);
  elevator.setAcceleration(ELEVATOR_ACCELERATION);
  elevator.setMaxSpeed(ELEVATOR_MAX_SPEED);
  offset();
  Serial.println("Start");
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
  if (Serial.available()) {
    int inputInt = Serial.read() - '0';
    Serial.println("recieved:" + inputInt);
    if (inputInt == 0)
      xTurn = true;
    else {
      if (xTurn)
        drawX(coords[inputInt*2], coords[inputInt*2+1]);
      else
        drawCircle(coords[inputInt*2], coords[inputInt*2+1]);
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
  for (int i = 0; i < PRECISION; i++) {
    if (i == 0) {
      elevator.moveTo(ELEVATOR_DOWN); // move down to draw
      elevatorRun();
    }
    goTo(CIRCLE_RADIUS * cos(9 * PI / 4 * i / PRECISION) + x, CIRCLE_RADIUS * sin(9 * PI / 4 * i / PRECISION) + y);
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

  while (abs(joint1.distanceToGo()) > 0 || abs(joint2.distanceToGo()) > 0 || abs(elevator.distanceToGo()) > 0) {
    joint1.run();
    joint2.run();
    elevator.run();
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
