import requests
import threading
import time
import queue

class CaptionHandler:
    def __init__(self, backend_url, api_key=None, polling_interval=0.5):
        self.backend_url=backend_url
        self.api_key=api_key
        self.polling_interval=polling_interval
        self.caption_queue=queue.Queue()
        self.is_running=False       #check if polling thread is running
        self.thread=None
        self.last_caption="" #tracking the last caption so avoid duplication

    def start(self):
        '''
        Start polling backend
        '''
        if self.is_running:
            print("Already running")
            return
        
        self.is_running=True
        self.thread=threading.Thread(target=self.polling_loop, daemon=True)
        self.thread.start()
        print("Started polling backend")

    def stop(self):
        #stop calling
        self.is_running=False
        if self.thread:
            self.thread.join(timeout=2)
        print("Stopped Polling")
    
    def polling_loop(self):
        '''
        Internal polling loop
        '''
        while self.is_running:
            try:
                caption=self.fetch_caption()
                if caption and caption!=self.last_caption:
                    self.caption_queue.put(caption)
                    self.last_caption=caption
            except Exception as e:
                print(f"Error Fetching caption: {e}")
            
            time.sleep(self.polling_interval)
    
    def fetch_caption(self):
        '''
        Fetch caption from backend
        Return: 
            String: latest caption text
        '''
        try:
            headers={}  #dictionary to store HTTP request header
            if self.api_key:
                headers['Authorization']=f'Bearer {self.api_key}'

            #can adjust according to backend API structure
            response=requests.get(
                self.backend_url, 
                headers=headers,
                timeout=2
            )

            if response.status_code==200:  #success
                data=response.json()

                #name according to backend response
                return data.get('caption', data.get('text', ''))
        except:
            pass

        return None
    
    def get_latest_caption(self):
        '''
        latest caption from queue
        Return: 
            String: Caption text or None if queue is empty
        '''
        try:
            return self.caption_queue.get_nowait()
        except queue.Empty:
            return None
    

    def get_all_captions(self): 
        '''
        Get all pending captions also
        Return : 
            List of caption string 
        '''
        captions = []
        while not self.caption_queue.empty():
            try:
                captions.append(self.caption_queue.get_nowait())
            except queue.Empty:
                break
        return captions
    


