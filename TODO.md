# TODO
## Improvements and Bug Fixing (Both arm and Pi)
- [ ] **! Spring Mount !**
- [ ] Fix communication
  - Currently basic commication works, but the busy signal does not as commands simply get tacked on to the end of current action
  - On PI side, the finished signal code does not work, so script does not wait for the arm to finish
- [ ] Reset board when starting new games
- [x] Add small delay so TTS does not get cut off
- [ ] Arm currently moves to far down sometimes
- [ ] Finish enclosure for electronics

## Optional
- [ ] limit switches for auto homing
- [ ] Never going to happen but: self erasing

## Arm / Arduino
- [X] Coordinate system
- [X] Draw Xs and Os
- [X] Communicate with Pi
- [X] Integrate code w/ coords and Serial comms.
- [x] Test simplified drawing cycles
- [X] Create scalable table feature
- [X] Test scalable table feature
- [x] Work with RPI group to standarize Serial comm syntax

## Rasberry Pi / Google Stuff
- [x] Get example to run
- [x] PoC of rPi to Arduino via serial
- [x] Trigger example with button
- [x] Add LED that lights up when prompting
- [x] Write our own custom traits
- [x] Figure out how to enable mutliple custom traits at once
- [x] Integrate traits into code
  - Each `@devicehandler` serves as a method call when the trait is triggered
  - Inside each method, use the TTTARM code to play the game
- [x] Convert current TTT code into a class so it can be used as library
  - The overall structure is on top of the TTTARM.py file
- [x] Use created library/class to enable TTT in pushtotalk.py
- [ ] Everything [else](https://imgur.com/gallery/RadSf)

## Other
- [ ] Make entire thing "Google" worthy
- [ ] Let Andy go to CES
