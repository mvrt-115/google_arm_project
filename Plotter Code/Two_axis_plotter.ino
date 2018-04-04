//plotter starts out at bottom left
//steppers moving in same dir - x-axis
//steppers moving in opposite dir - y-axis



#include <AccelStepper.h>;
#include <Servo.h>;

#define BAUD_RATE 115200
#define STEPS 800
#define PEN_UP 180
#define PEN_DOWN 0
#define ACCELERATION 1000
#define MAX_SPEED 3000
#define PULLEY_CIRCUMFRENCE 3.1 //cm

AccelStepper stepper1(1, 12, 11); // 1, stp, dir
AccelStepper stepper2(1, 5, 4); //1, stp, dir

double currentX = 0.0;
double currentY = 0.0;

void setup() {
  Serial.begin(BAUD_RATE);
  stepper1.setAcceleration(ACCELERATION);
  stepper2.setAcceleration(ACCELERATION);
  stepper1.setMaxSpeed(MAX_SPEED);
  stepper2.setMaxSpeed(MAX_SPEED);
  goTo(0, 2);
}

void goTo(double x, double y) {
  /*

    assuming the pen is on the side close to you:

    giving both positive values makes it go to the left
    giving both negative values makes it go the right
    giving stepper1 a positive value and stepper2 a negative value
    makes it go towards you
    giving stepper1 a negative value and stepper2 a positive value
    makes it go away from you

    towards you is a higher value of y
    to the right is a higher value of x

    with 2 steppers moving twice as much movement happens
    1 rotation of 2 steppers makes it move 2 rotations worth of belt?

  */

  double slope = (y - currentY) / (x - currentX);

  if (slope == 0) { //if horizontal line

    if (x > currentX) {

      stepper1.setSpeed(-1000);
      stepper2.setSpeed(-1000);

      while (x > currentX) {
        stepper1.runSpeed();
        stepper2.runSpeed();
        currentX += (1.00 / STEPS) * PULLEY_CIRCUMFRENCE;
        delay(1);
      }

    }

    else if (x < currentX) {

      stepper1.setSpeed(1000);
      stepper2.setSpeed(1000);

      while (x < currentX) {
        stepper1.runSpeed();
        stepper2.runSpeed();
        currentX -= (1.00 / STEPS) * PULLEY_CIRCUMFRENCE;
        delay(1);
      }
    }
/* FIX
    if (x == currentX && y != currentY) { //if vertical line
      

      if (y > currentY) {

        stepper1.setSpeed(1000);
        stepper2.setSpeed(-1000);

        while (y > currentY) {
          stepper1.runSpeed();
          stepper2.runSpeed();
          currentY += (1.00 / STEPS) * PULLEY_CIRCUMFRENCE;
          delay(1);
        }
      }

      else if (y < currentY) {

        stepper1.setSpeed(-1000);
        stepper2.setSpeed(1000);

        while (y < currentY) {
          stepper1.runSpeed();
          stepper2.runSpeed();
          currentY -= (1.00 / STEPS) * PULLEY_CIRCUMFRENCE;
          delay(1);
        }
      }
    }
    */
  }
}

void loop() {
  // put your main code here, to run repeatedly:

}
