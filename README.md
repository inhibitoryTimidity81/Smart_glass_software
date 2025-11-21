1. Config.py (start from here)-->
     Backend URL needed.
     Can add trigger words (where vibration is needed)
     all settings

2. main.py
     connects whole system
     just run

3. caption_handler.py
     gets caption from the backend
     pigs every 500ms

4. trigger_detector.py
     checks if any trigger words in the caption
     returns if found

5. vibration_controller.py
     Makes vibration.
     GPIO pin 27 (good for R Pi 0 2 W)

6. gui.py
     can show live captions if needed
     alers when trigger words detected
     if no captions needed then can remove it.
     
