# google_arm_project

## Resources:
- [Google EAP SDK](https://developers.google.com/assistant/sdk/eap/) (Must be in EAP Google group)
- [Custom Traits](https://developers.google.com/assistant/sdk/eap/device-actions/partner/register-custom-actions?authuser=1) (Must be in EAP Google group)
- [gactions CLI](https://developers.google.com/actions/tools/gactions-cli)
- [TTS library being used](https://github.com/pndurette/gTTS)

## Raspberry Pi Commands:
- Start Virtual Enviroment: `source /env/bin/activate`
- Navigate to code folder: `cd google-assistant-sdk-0.4.0/googlesamples/assistant/grpc`
- Edit pushToTalk.py: `nano pushToTalk<version>.py`
  - `ctrl+w` and `@device` to trait code
  - `ctrl+x` to save
- Run pushToTalk.py: `python pushToTalk<version>.py --device-id ARM`
  - Note: More details are on the folder under the pi, please update the info (manufacturer, name, model, etc.) when possible
- Steps for changing custom traits and testing them:
  - Edit the custom trait: `nano <trait>_trait.json`
  - Update the trait for testing: `./gactions test --action_package <trait>_trait.json --project tic-tac-toe-115`
    - Note: Only the trait entered above will be testable, AFAIK you must redo the step above and the following steps to change the trait being tested.
  - Reupdate the model:
    ```
    googlesamples-assistant-devicetool register-model --manufacturer "<Manufacturer>" \
    --product-name "<Name>" --type LIGHT --trait action.devices.traits.OnOff \
    --trait StartGame --trait SetLetter --ChooseLetter --model <model>
    ```
  - Reupdate the device:
    ```
    googlesamples-assistant-devicetool register-device \
    --model <model> --device <device>`
    ```
