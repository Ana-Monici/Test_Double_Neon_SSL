class Controller():
    def __init__(self):
        self.controll_params = {
            'PID_KP': 1,
            'KI': 0,
            'KD': 0,
            'KW': 3.5,
            'VM': 0.5,
            'RM': 0.44,
            'UNI_KP': 1
        }
    
    def get_values(self):
        return self.controll_params
    
    def set_values(self, values):
        # receive dict with controll_params
        self.controll_params = values
        print("New controll parameters:")
        print(self.controll_params)
