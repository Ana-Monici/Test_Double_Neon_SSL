from socket import *
import json
import time
import threading

from match.match import Match
from entities.coach import COACHES

class SingletonMeta(type):
   """
   The Singleton class can be implemented in different ways in Python. Some
   possible methods include: base class, decorator, metaclass. We will use the
   metaclass because it is best suited for this purpose.
   source: https://refactoring.guru/design-patterns/singleton/python/example
   """

   _instances = {}

   def __call__(cls, *args, **kwargs):
       """
       Possible changes to the value of the `__init__` argument do not affect
       the returned instance.
       """
       if cls not in cls._instances:
           instance = super().__call__(*args, **kwargs)
           cls._instances[cls] = instance
       return cls._instances[cls]

BUFFER_SIZE = 4096

class GuiApi(metaclass=SingletonMeta):
    # TODO make sure this doesn't break if server is not running at the begining
    def __init__(self, addr, port, match: Match):
        print("Initializing GUI API")
        self.context = match
        self.gui_addr = addr
        self.gui_port = port
        self.kill_received = False

    def build_initial_message(self):
        match_data = {
            "TEAM_SIDE": self.context.team_side,
            "TEAM_COLOR": self.context.team_color,
            "COACH_NAME": self.context.coach_name,
            "ROBOT_IDS": self.context.robot_ids_list,
            "OPPOSITE_IDS": self.context.opposite_ids_list,
            "COACH_LIST": list(COACHES.keys()),
            "GOALKEEPER_ID": self.context.goalkeeper_id,
            "UPDATE_RATE": 0
        }

        if self.context.is_competition_mode():
            match_data.update({
                "GAME_STATUS": self.context.game_status
            })

        return {
            "MATCH": match_data,
            "PARAMETERS": self.context.controll_info.get_values()
        }

    def process_initial_gui_data(self, gui_data):
        self.context.apply_gui_data(gui_data)

    def build_status_message(self):
        fps = getattr(getattr(self.context, "game", None), "fps", 0) or 0
        update_rate = round(1000 / fps) if fps > 0 else 0
        robots = getattr(self.context, "robots", [])
        ball = getattr(self.context, "ball", None)

        robot_pos = {}
        strategy = {}
        battery = {}
        signal = {}
        kicker = {}

        for index, robot in enumerate(robots):
            robot_id = str(robot.robot_id)
            robot_pos[robot_id] = [robot.x, robot.y, robot.theta]

            robot_strategy = robot.get_strategy()
            strategy[robot_id] = robot_strategy.get_name() if robot_strategy is not None else None

            battery[robot_id] = max(0, 95 - index)
            signal[robot_id] = -40 - index
            kicker[robot_id] = bool(robot.kicker)

        match_data = {
            "UPDATE_RATE": update_rate,
            "FPS": fps
        }
        if self.context.is_competition_mode():
            match_data = {
                "GAME_STATUS": self.context.game_status,
                "COACH_NAME": self.context.coach_name,
                "COACH_LIST": list(COACHES.keys()),
                "UPDATE_RATE": update_rate,
                "FPS": fps
            }

        return {
            "MATCH": match_data,
            "BALL_POS": [ball.x, ball.y] if ball is not None else [0, 0],
            "ROBOT_POS": robot_pos,
            "STRATEGY": strategy,
            "BATTERY": battery,
            "SIGNAL": signal,
            "KICKER": kicker
        }
    
    def start(self):
        # Creating TCP socket
        self.obj_socket = socket(AF_INET, SOCK_STREAM)
        self.obj_socket.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)

        try:
            print("Stablishing GUI connection...")
            # Connect the socket to the server's address and port
            self.obj_socket.connect((self.gui_addr, self.gui_port)) # self.obj_socket.connect(('localhost', 9999))
            print("GUI TCP API connected.")

            initial_json = self.build_initial_message()
            self.send_json(self.obj_socket, initial_json)

            # Recebe msg inicial da GUI
            initial_msg_recv = self.recv_json(self.obj_socket)
            if initial_msg_recv is None:
                print("Server disconected.")
            else:
                self.process_initial_gui_data(initial_msg_recv)
                print(initial_msg_recv)

                # Send NeonFC's current status
                self.send_json(self.obj_socket, self.build_status_message())

                # Start communication thread
                self.comm_thread = threading.Thread(target=self.communicate)
                self.comm_thread.start()

            # Create an event to stop the threads when needed
            # stop_event = threading.Event()

            # Start threads for receiving and sending messages
            # self.recv_thread = threading.Thread(target=self.data_recv)
            # self.send_thread = threading.Thread(target=self.data_send)

            # self.recv_thread.start()
            # self.send_thread.start()

            # Wait for both threads to finish
            # receive_thread.join()
            # send_thread.join()

        except Exception as e:
            print("Error connecting to the server: ", e)
        # finally:
        #     self.obj_socket.close()
        #     print("Connection with GUI closed.")

        # start recv thread
        # start send thread

        # while True:
        #     time.sleep(1)
        #     print("THREAD")

    def communicate(self):
        print("COMMUNICATE -----------------------------")
        while not self.kill_received:
            time.sleep(0.01)
            try:
                # recv, process, send
                # Receives message from GUI
                gui_data = self.recv_json(self.obj_socket)
                if gui_data is None:
                    print("Server disconected.")
                    break
                print("Resposta do servidor: ", gui_data)
                self.context.apply_gui_data(gui_data)

                # Send NeonFC's current status to GUI
                self.send_json(self.obj_socket, self.build_status_message())
            except Exception as e:
                print("Error during GUI communication: ", e)
        
        self.obj_socket.close()
        print("Connection with GUI closed.")

    def recv_json(self, sock):
        buffer = b""
        while True:
            data = sock.recv(BUFFER_SIZE)
            if not data:
                print("Server closed connection.")
                return None  # Conexão fechada pelo servidor
            buffer += data
            if b"\n" in buffer:
                break
        mensagem = buffer.decode().strip()
        try:
            return json.loads(mensagem)
        except json.JSONDecodeError:
            print("Erro ao decodificar JSON da resposta.")
            return None
  
    def data_recv(self):
        # while not stop_event.is_set():
        while True:
            try:
                data = self.obj_socket.recv(BUFFER_SIZE)
                print(data)
                # time.sleep(1)
                if data:
                    decoded_data = json.loads(data.decode())
                    # print(decoded_data)
                    self.info_api.update_recv(decoded_data)
                    # self.decod_data = decoded_data
            except Exception as e:
                print("Error receiving message:", e)
            # finally:
                # stop_event.set()  # Signal the sending thread to stop
                # self.obj_socket.close()

    def data_send(self):
        while not self.kill_received:
            # time.sleep(1)
            data_dict = self.info_api.organize_send()
            msg = json.dumps(data_dict)
            self.obj_socket.sendall(msg.encode())

    # TODO test
    def send_custom_data(self, data):
        msg = json.dumps(data)
        # self.obj_socket.sendto(msg.encode(), (self.address, self.port))
        self.obj_socket.sendall(msg.encode())

    def send_json(self, conn, data):
        message = json.dumps(data) + "\n"  # "\n" é delimitador de fim
        conn.sendall(message.encode())
