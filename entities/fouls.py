class Fouls():
    def __init__(self):
        self.foul_status = {
            'FOUL_NAME': 'KICKOFF',
            'FOUL_QUADRANT': 1,
            'FOUL_COLOR': 'yellow',
            'FOUL_IS_ACTIVE': False
        }
    
    def get_values(self):
        return self.foul_status
    
    def set_values(self, values):
        # receive dict with foul_status
        self.foul_status = values
        print("Foul status:")
        print(self.foul_status)
