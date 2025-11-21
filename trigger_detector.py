import re

class TriggerDetector:

    def __init__(self, trigger_words):
        self.trigger_words=[word.lower() for word in trigger_words]
        print(f"Monitoring {len(self.trigger_words)} trigger words")
    
    def check_triggers(self, text):
        '''
        check if text contains trigger words

        Args: 
            text: input text to check

        Return:
            Tuple: (is_triggerd (bool), list of detected words)
        '''

        if not text:
            return False, []
        
        text_lower=text.lower #convert in lower case
        detected_words = []

        for trigger in self.trigger_words:
            #word boundaries for accuracy
            pattern=r'\b' + re.escape(trigger) + r'\b'
            if re.search(pattern, text_lower):
                detected_words.append(trigger)
        
        if detected_words:
            print(f"Trigger words detected: {detected_words}")
            return True, detected_words
        
        return False, []