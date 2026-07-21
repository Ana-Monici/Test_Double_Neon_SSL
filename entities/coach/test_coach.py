from entities import strategies

class Coach(object): # heranca da classe abstrata
    NAME = "TEST"
    def __init__(self):
        print("INIT COACH TEST")
        self.goalkeeper_id = 0
        self.change_strat_time = 0
        # self.animation_frame = 0
        self.initial_strategies = [
            strategies.Goalkeeper,
            strategies.MainAttacker,
            strategies.SideAttacker,
            strategies.Midfielder,
            strategies.Defender,
            strategies.Defender2
        ]
        self.secondary_strategies = [
            strategies.Goalkeeper,
            strategies.Defender2,
            strategies.Defender,
            strategies.Midfielder,
            strategies.SideAttacker,
            strategies.MainAttacker
        ]

    def get_name(self):
        return self.NAME

    def start(self, robots):
        self.robots = robots

        i = 0
        for robot in self.robots:
            robot.set_strategy(self.initial_strategies[i])
            i = i + 1
        
        self.goalkeeper_id = 0
    
    def update(self, anim_frame):
        if anim_frame > 358:
            self.change_strat_time += 1
            if self.change_strat_time == 7:
                i = 0
                for robot in self.robots:
                    robot.set_strategy(self.secondary_strategies[i])
                    i = i + 1
        
        # for robot in self.robots:
        #     robot.strategy.animate(anim_frame)

    def get_robot_by_id(self, robot_id):
        for robot in self.robots:
            if robot.robot_id == robot_id:
                return robot
        return None

    def set_goalkeeper(self, new_goalkeeper_id):
        current_goalkeeper = None
        for robot in self.robots:
            if robot.get_strategy().get_name() == "Goalkeeper":
                current_goalkeeper = robot
                break

        new_goalkeeper = self.get_robot_by_id(new_goalkeeper_id)
        if new_goalkeeper is None:
            print("Invalid goalkeeper id:")
            print(new_goalkeeper_id)
            return

        if current_goalkeeper is not None and new_goalkeeper.robot_id == current_goalkeeper.robot_id:
            self.goalkeeper_id = new_goalkeeper_id
            return

        if current_goalkeeper is None:
            new_goalkeeper.set_strategy(strategies.Goalkeeper)
        else:
            strategy_to_switch = new_goalkeeper.get_strategy()
            new_goalkeeper.set_strategy(strategies.Goalkeeper)
            current_goalkeeper.set_strategy(strategy_to_switch)

        self.goalkeeper_id = new_goalkeeper_id
        print("New goalkeeper:")
        print(self.goalkeeper_id)
    
    def get_goalkeeper_id(self):
        return self.goalkeeper_id
