import os
import entities
from concurrent import futures

CATEGORIES = {
    '3v3': 3, '5v5': 5, '6v6': 6
}

class Match(object):
    def __init__(
        self,
        game,
        team_side,
        team_color,
        coach_name=None,
        category="3v3",
        robot_ids=[],
        opposite_ids=[],
        simulate_game_status=True,
        status_change_interval=300,
        game_status_sequence=None
    ):
        super().__init__()
        self.game = game
        
        self.coach_name = os.environ.get('COACH_NAME', coach_name) 
        self.team_side = os.environ.get('TEAM_SIDE', team_side) 
        self.team_color = os.environ.get('TEAM_COLOR', team_color)
        self.category = os.environ.get('CATEGORY', category)
        self.n_robots = CATEGORIES.get(self.category)

        self.opposite_team_color = 'yellow' if self.team_color == 'blue' else 'blue'

        self.robot_ids_list = os.environ.get('ROBOT_IDS', robot_ids)
        self.opposite_ids_list = os.environ.get('OPPOSITE_IDS', opposite_ids)

        self.game_status = 'STOP'
        self.gui_mode = 'training'
        self.read_only = False
        self.simulate_game_status = simulate_game_status
        self.game_status_sequence = game_status_sequence or ["GAME_ON", "HALT", "STOP"]
        self.game_status_index = (
            self.game_status_sequence.index(self.game_status)
            if self.game_status in self.game_status_sequence
            else 0
        )
        self.status_frame_counter = 0
        self.status_change_interval = status_change_interval
        self.foul_info = entities.Fouls()
        self.controll_info = entities.Controller()
        self.animation_frame = 0

        self.goalkeeper_id = self.robot_ids_list[0]
    
    def start(self):
        print("Starting match module starting ...")
        self.ball = entities.Ball(self.game)

        if not self.opposite_ids_list:
            self.opposites = [
                entities.Robot(self.game, i, self.opposite_team_color) for i in range(self.n_robots)
            ]
        else:
            self.opposites = [
                entities.Robot(self.game, i, self.opposite_team_color) for i in self.opposite_ids_list
            ]

        if not self.robot_ids_list:
            self.robots = [
                entities.Robot(self.game, i, self.team_color) for i in range(self.n_robots)
            ]
        else:
            self.robots = [
                entities.Robot(self.game, i, self.team_color) for i in self.robot_ids_list
            ]

        self.coach = entities.coach.COACHES[self.coach_name]()
        print(f"Match started! coach is [{self.coach.NAME}]")
        self.coach.start(self.robots)
        self.goalkeeper_id = self.coach.get_goalkeeper_id()

        for robot in self.robots:
            robot.start()

    # def restart(self, team_color):
    #     self.team_color = team_color
    #     self.opposite_team_color = 'yellow' if self.team_color == 'blue' else 'blue'

    #     self.opposites = [
    #         entities.Robot(self.game, i, self.opposite_team_color) for i in range(self.n_robots)
    #     ]

    #     self.robots = [
    #         entities.Robot(self.game, i, self.team_color) for i in range(self.n_robots)
    #     ]

    #     self.coach.decide()

    #     for robot in self.robots:
    #         robot.start()

    def normalize_gui_mode(self, mode):
        mode_aliases = {
            "treino": "training",
            "training": "training",
            "trainning": "training",
            "competicao": "competition",
            "competition": "competition"
        }
        if isinstance(mode, str):
            normalized_mode = mode.strip().lower()
            return mode_aliases.get(normalized_mode, normalized_mode)
        return self.gui_mode

    def update_gui_mode(self, gui_data):
        if "GUI_MODE" in gui_data:
            self.gui_mode = self.normalize_gui_mode(gui_data["GUI_MODE"])

        if "READ_ONLY" in gui_data:
            read_only = gui_data["READ_ONLY"]
            if isinstance(read_only, bool):
                self.read_only = read_only
            elif isinstance(read_only, str):
                self.read_only = read_only.strip().lower() == "true"

    def is_competition_mode(self):
        return self.read_only or self.gui_mode == "competition"

    def update_game_status_simulation(self):
        if not self.simulate_game_status or not self.is_competition_mode():
            return

        self.status_frame_counter += 1

        if self.status_frame_counter >= self.status_change_interval:
            self.status_frame_counter = 0
            self.game_status_index = (self.game_status_index + 1) % len(self.game_status_sequence)
            self.game_status = self.game_status_sequence[self.game_status_index]

    def update(self):
        self.update_game_status_simulation()

        if self.game_status == "GAME_ON":
            self.animation_frame += 1

        if self.animation_frame > 360:
            self.animation_frame = 0

        self.coach.update(self.animation_frame)

        self.ball.update(self.animation_frame)

        # for entity in self.opposites:
        #     entity.update(self.animation_frame)
        
        for entity in self.robots:
            entity.update(self.animation_frame)


    def update_information(self, **kwargs): #Function to update values recieved in api
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def apply_gui_data(self, gui_data):
        """Apply state received from the GUI API."""
        self.update_gui_mode(gui_data)

        if self.is_competition_mode():
            print("Modo competição")
            return

        match_info = gui_data.get("MATCH", {})
        fouls_info = gui_data.get("FOULS", {})
        parameters = gui_data.get("PARAMETERS", {})

        if "GAME_STATUS" in match_info:
            game_status = match_info["GAME_STATUS"]
            self.game_status = game_status.upper() if isinstance(game_status, str) else game_status

        if "TEAM_SIDE" in match_info:
            self.team_side = match_info["TEAM_SIDE"]

        if "TEAM_COLOR" in match_info:
            self.team_color = match_info["TEAM_COLOR"]
            self.opposite_team_color = 'yellow' if self.team_color == 'blue' else 'blue'

        if "COACH_NAME" in match_info:
            self.coach_name = match_info["COACH_NAME"]

        if "GOALKEEPER_ID" in match_info:
            goalkeeper_id = match_info["GOALKEEPER_ID"]
            if isinstance(goalkeeper_id, str) and goalkeeper_id.lstrip("-").isdigit():
                goalkeeper_id = int(goalkeeper_id)
            self.goalkeeper_id = goalkeeper_id
            coach = getattr(self, "coach", None)
            robots = getattr(coach, "robots", []) if coach is not None else []
            robot_ids = [robot.robot_id for robot in robots]
            if (
                coach is not None
                and hasattr(coach, "set_goalkeeper")
                and isinstance(goalkeeper_id, int)
                and goalkeeper_id in robot_ids
            ):
                coach.set_goalkeeper(goalkeeper_id)

        if fouls_info:
            current_fouls = self.foul_info.get_values().copy()
            current_fouls.update(fouls_info)
            self.foul_info.set_values(current_fouls)

        if parameters:
            current_parameters = self.controll_info.get_values().copy()
            current_parameters.update(parameters)
            self.controll_info.set_values(current_parameters)

    # def decide(self):
    #     commands = []
    #     commands_futures = []
    #     '''
    #     https://docs.python.org/3/library/concurrent.futures.html
    #     '''
    #     self.coach.decide()

    #     with futures.ThreadPoolExecutor(max_workers=self.n_robots) as executor:
    #         commands_futures = [
    #             executor.submit(robot.decide) for robot in self.robots
    #         ]

    #     for future in futures.as_completed(commands_futures):
    #         commands.append(future.result())

    #     return commands

"""
import time

coach = Coach(lista_de_robos)
coach.set_game_state("rodando")

while True:
    coach.update()
    time.sleep(0.016)  # ~60 FPS
"""
