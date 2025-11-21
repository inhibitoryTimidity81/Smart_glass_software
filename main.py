import time
import signal
import sys
from config import *
from gui import SmartGlassGUI
from caption_handler import CaptionHandler
from trigger_detector import TriggerDetector
from vibration_controller import VibrationController

class SmartGlassApp:
    def __init__(self):
        '''
        Initialize
        '''

        self.gui= SmartGlassGUI(GUI_WIDTH, GUI_HEIGHT)
        self.caption_handler=CaptionHandler(
            BACKEND_URL,
            API_KEY,
            POLLING_INTERVAL
        )
        self.trigger_detector=TriggerDetector(TRIGGER_WORDS)
        self.vibration_controller=VibrationController(
            VIBRATION_PIN,
            VIBRATION_DURATION
        )

        self.running=True

        #signal handler
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        print("\n All components initialized")
        print(f"Monitoring {len(TRIGGER_WORDS)} trigger words")
        print(f"Backend: {BACKEND_URL}")
        print("=" * 50)

    def signal_handler(self, signum, frame):
        '''Handle abrupt shutdown'''
        print("Shutting down")
        self.shutdown()
        sys.exit(0)
    
    def start(self):
        '''Start the App'''
        print("\n Starting Smart Glass App")

        #start caption handler
        self.caption_handler.start()

        #start main loop
        print("Entering Main loop")
        self.run_loop()

    def run_loop(self):
        '''Main App loop'''
        try:
            while self.running:
                caption=self.caption_handler.get_latest_caption()

                if caption:
                    self.gui.update_caption(caption)

                    is_triggered, detected_words=self.trigger_detector.check_triggers(caption)

                    if is_triggered:
                        #Alert in GUI
                        self.gui.show_alert(detected_words)

                        #trigger vibration 
                        print(f"Triggering Vibration")

                        self.vibration_controller.vibrate()
                # Update GUI (process events)
                self.gui.update()
                
                # Small delay to prevent CPU overload
                time.sleep(0.05)
        except KeyboardInterrupt:
            print("\n\nKeyboard interrupt detected")
            self.shutdown()
        except Exception as e:
            print(f"\n[ERROR] Unexpected error: {e}")
            self.shutdown()
        
        def shutdown(self):
            '''Clean shutdown for all components'''
            print("\n Shutting down all components")
            self.running=False

            #caption_handler
            self.caption_handler.stop()

            #clean GPIO
            self.vibration_controller.cleanup()

            #closing GUI 
            try:
                self.gui.close()
            except:
                pass

            print("Shutdown Complete")

def main():
    '''App Entry'''
    app=SmartGlassApp()
    app.start()

if __name__=="__main__":
    main()