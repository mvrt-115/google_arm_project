/*  Testing Raspberry Pi to Arduino through Serial
 *  
 *  Built in LED turns ON or OFF depending on serial input
 */

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  // initialize serial:
  Serial.begin(115200);
  Serial.write('Start');
}

void loop() {
  if (Serial.available()) {
    int inputInt = Serial.read() - '0';
    light(inputInt);
  }
}

void light(int inputInt) {
  // print the string:
  Serial.println(inputInt);
  if (inputInt == 1)
    digitalWrite(LED_BUILTIN, HIGH);
  else if (inputInt == 0)
    digitalWrite(LED_BUILTIN, LOW);
}
