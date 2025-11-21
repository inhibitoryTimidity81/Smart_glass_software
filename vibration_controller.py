try:
    import RPi.GPIO as GPIO #type: ignore
except (RuntimeError, ImportError):
    import Mock.GPIO as GPIO
import time
import threading

class VibrationController:

    def __init__(self, pin, duration=0.8):

        '''
        Vibration motor setting

        Args:
            pin: GPIO pin number (BCM mode)
            duration: how long the motor vibrates
            is_vibrating: check if already vibrating to avoid overlapping
        '''
        self.pin=pin
        self.duration=duration
        self.is_vibrating=False  

        #GPIO setting
        GPIO.setmode(GPIO.BCM)  #BCM method
        GPIO.setup(self.pin, GPIO.OUT) #sets pin to output
        GPIO.output(self.pin, GPIO.LOW) #initially low means no vibration

        print(f"[VibrationController] Initialized on GPIO pin {self.pin}")

    def vibrate(self, duration):
        '''
        Trigger vibration for duration
        '''

        if self.is_vibrating:
            print("Already vibrating")
            return
        
        duration=duration or self.duration
        self.is_vibrating=True

        #seperate thread for vibration
        thread=threading.Thread(target=self.vibrate_thread, args=(duration, ))
        thread.daemon=True
        thread.start()
    
    def vibrate_thread(self, duration):
        '''
        Method to handle vibration in a seperate thread
        '''
        try:
            print(f"Vibrating for {duration}s")
            GPIO.output(self.pin, GPIO.HIGH) #activated vibration
            time.sleep(duration)
            GPIO.output(self.pin, GPIO.LOW)
        finally:
            self.is_vibrating=False 
    
    def vibrate_pattern(self, pattern):
        '''
        Vibrate in a specific patter

        Args: 
            pattern: list of tuples [on, off, ..]
        '''

        thread=threading.Thread(target=self.pattern_thread, args=(pattern, ))
        thread.daemon=True
        thread.start()
    
    def pattern_thread(self, pattern):
        '''Internal method for pattern vibration'''

        self.is_vibrating=True
        try:
            for on_time, off_time in pattern:
                GPIO.output(self.pin, GPIO.HIGH)
                time.sleep(on_time)
                GPIO.output(self.pin, GPIO.LOW)
                if off_time>0:
                    time.sleep(off_time)
        finally:
            self.is_vibrating=False
    
    def cleanup(self):
        GPIO.cleanup()
        print("GPIO cleaned up")




