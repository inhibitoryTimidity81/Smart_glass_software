
# Backend API Configuration
BACKEND_URL = "http://your-backend-server.com/api/captions" #backend URL
API_KEY = "your_api_key_here"  # API key for authentication
POLLING_INTERVAL = 0.5  #sends request every 500ms

TRIGGER_WORDS = [
    "alarm",
    "emergency",
    "fire",
    "help",
    "NAME",  # Replace with actual name
    "stop",
    "danger",
    "thud",
    "crash"
]

#vibration setting
VIBRATION_PIN=27 #R Pi 0 2 W
VIBRATION_DURATION=0.8
VIBRATION_INTENSITY=1.0      
'''
Using Max intensity for all words. one idea is to use different
intensity for different.
'''
                                

#gui setting
GUI_WIDTH=800
GUI_HEIGHT=480
CAPTION_HISTORY_LIMIT=10 #only last 10 messages at a time 

