# Serial Communication Protocol
This document outlines how the RPI and Arduino talk with each other to carry out specific Tic-Tac-Toe moves.

## `\n` Serves as a break inbetween all messages

## Commands:
- Line
- Arc

### Lines:
- RPI Request Format: "L <X1,Y1> <X2,Y2>"
- Arduino Action: Draw an line from point 1 to point 2.

### Arcs:
- RPI Request Format: "A <X,Y> <R> <A1> <A2>"
- Arduino Action: Draw an arc at with center at point with radius r. Starts at angle 1 and ends at angle 2.

## Responses:
- Ready/Unready
- Busy
- Accepted/Invalid
- Start/Finish

### Ready/Unready:
- This set of responses are used when the RPI send the "New Game" Command.
- If the homing procedure is successful, the Arduino replies with "Ready".
- If there was an error during homing, the Ardino replies with "Not Ready".
- If "Not Ready" is sent, the Arduino will accept no commands.
- If "Not Ready" is sent reset. If problem persists, the arm may have to be repaired.

### Busy:
- This response is used when the RPI sends a Command.
- If the RPI sends a Command while another Command is being executed, the Arduino replies with "Busy".
- If "Busy" is given, the command is ignored. The request must be resent later, when available (see other response sections).
- If there are no ongoing tasks, the Arduino will give another response (see other respose sections).

### Accepted/Invalid:
- This set of responses is used when RPI sends a Command.
- Arduino must be available as a prerequisite (see "Busy").
- If the Command given is valid, the Arduino replies with "Accepted".
- If not valid (incorrect format, invalid parameters), the Arduino replies with "Invalid".
- Invalid commands are ignored. The request must be resent.

### Start/Finish
- This set of responses is used when a Command is being executed.
- When the Arduino begins the Command, the reply "Start" is sent to the RPI.
- When the Arduino finishes the Command, the reply "Finish" is sent to the RPI.
