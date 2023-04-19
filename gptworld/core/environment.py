import threading
import time
import json
from gptworld.core.agent import GPTAgent
from typing import Dict, List, Tuple
# from gptworld.core.time_system impor, MOVEMENT_TICK
import subprocess
from gptworld.utils.logging import get_logger
import os

logger = get_logger(__file__)
logger.debug = print
logger.info =  print


def run_dev():
    subprocess.run(['npm', 'run', 'dev'], cwd='/Users/hsd/codes/MultiAgent/GPT-World/game/text_grid/frontend', capture_output=True)
    subprocess.run(['python app.py'], cwd='/Users/hsd/codes/MultiAgent/GPT-World/game/text_grid', capture_output=True)


def action_parser():
    """ Parser parses natural language to identify the broadcasting target(s).
        Broadcast the message to the observation of the relevant agent(s).
    """

    prompt = """
    Example 1
    Thought:
    I need to send a text message to my parents and tell them that I am fine
    Knowledge:
    Relationship=["Father": "Lao Wang", "Mother": "Lao Li"]
    API Call:
    "Lao Wang", "messaging", "I'm fine"
    "Lao Li", "messaging", "I'm fine"

    Example 2:
    Thought:
    I want to inform my friends that I want to have a party on Sunday
    Knowledge:
    Friend: ["Little A", "Little B", "Little C"]
    API Call:
    "Little A", "messaging", "I want to have a party on Sunday"
    "Little B", "messaging", "I want to have a party on Sunday"
    "Little C", "Text message", "I want to have a party on Sunday"

    Have you discovered the pattern? The first is the only existing named entity (not a reference), the second is the action, and the third is the specific content. If the action is given, it is best to choose from it, if you have other unprovided actions, you could use "misc". The content may not be provided.

    Here is a new scenario:
    Thought:
    I want to start the car
    Knowledge:
    ParentElement: ["Das Auto A100": "start engine", "get off", "open windows", "misc"]
    API Call:
    """
    
    return


class GPTWorldEnv:
    """ The envirnment simulator
    Maintain a pool of all AgentThread
    """
    def __init__(self, 
        env_json,
        file_dir,
        # name,
        # id,
        # size,
        # areas,
        # objects = None,
        # agents = None,
        ):
        # TODO: agents mapping from agent id to AgentThread object

        self.env_json = env_json
        self.file_dir = file_dir

        self.agents, self.objects = {}, {}

        self.load_objects_and_agents()
        
        logger.debug("Initialize Complete!")

        

        # TODO: grid mapping from position tuple to agent id
        # self.grid: Dict[Tuple[int, int], str] = {}

        # TODO: movement manager thread object
        # self.movement_manager = MovementManagementThread(self.grid, self.agents)

        # TODO: control mode mapping from agent id to mode (either 'auto' or 'human')
        # self.control_mode: Dict[str, str] = {}

        # control if operational
        # self.operational = True
        pass


    @classmethod
    def from_file(cls, file_dir, file_name ="environment.json"):
        logger.debug(file_dir)
        with open(os.path.join(file_dir, file_name), 'r') as f:
            data = json.load(f)
        return cls(**{"env_json": data, "file_dir": file_dir})
        
      
    def initialize(self, ):
        import multiprocessing

        
        process = multiprocessing.Process(target=run_dev)
        process.start()

        logger.info("View the demo at locathost:5173")


    def get_neighbor_environment(self, location: Tuple[int] = None, agent_id :str = None, critical_distance = 20):
        '''Provide the local environment of the location.

        Args:
            location (:obj:`Tuple[int]`): The center of the view point.
            agent_id (:obj:`str`): The agent id, to filter the agent itself
            critical_distance (:obj:`int`): A distance that counts as the neighborhood.
        
        Returns:
            :text: the observation text. E.g., Now you are at fields. There are tractor, Bob, around you.'
        '''

        if location is None and agent_id is not None:
            location = self.env_json['objects'][agent_id]['pos'][0]

        at_area = None
        for areaid, area in self.env_json['areas'].items():
            pos = area['pos']
            if pos[0][0] <= location[0] <= pos[1][0] and pos[0][1] <= location[1] <= pos[1][1]:
                at_area = area['name']
        
        # Find objects within the agent's reach in distance
        objects_within_distance = []
        for obj_id, obj in self.env_json['objects'].items():
            if obj_id != agent_id:
                obj_location = obj['pos']
                distance = abs(obj_location[0][0] - location[0]) + abs(obj_location[0][1] - location[1])
                if distance <= critical_distance:
                    objects_within_distance.append(obj_id)
        

        # Generate the observation
        observation = {
            "agent_location": at_area,
            "objects_within_distance": objects_within_distance
        }
        observation_text = self.get_observation_text(observation)

        return observation_text
    
    def get_observation_text(self, observation):
        prompt_template = "Now you are at {}. There are {} around you."
    
        object_text = []
        for obj_id in observation['objects_within_distance']:
            object_text.append(self.env_json['objects'][obj_id]['name'])
        object_text = ", ".join(object_text) if len(object_text) > 0 else "nothing"

        prompt = prompt_template.format(observation['agent_location'], object_text)
        return prompt


    def show(self):
        '''Show the current status of this environment in a table
        '''
        return
    
    def create_by_prompt(self, message):
        '''Create the environment through user provided message.

        Args: 
            message (:obj: List[Dict]) a message like [{'role': 'user', 'content': 'hello'},]
        
        '''
        environment = None

        return environment

    def load_objects_and_agents(self):

        # create_agent
        for obj_id, obj in self.env_json['objects'].items():
            if obj_id.startswith('a'):
                self.agents[obj_id] = GPTAgent.from_file(self.file_dir, '{}.json'.format(obj_id))
            elif obj['id'].startswith('o'):
                self.objects[obj_id] = GPTAgent.from_file(self.file_dir, '{}.json'.format(obj_id))


    def save(self, ):
        '''Save the environment to a database.
        '''
        return

    def load_agent(self, agent_id, **kwargs):
        """ Load an agent from a dump file
        """
        # TODO: load agent from a dump file, the format will approximately be a JSON formatted file? then add to self.agents
        agent_state_dict = {}
        with open("./agent_format.json", "r") as f:
            agent_state_dict = json.load(f)
        
        agent = GPTAgent(state_dict=agent_state_dict, mode="auto")

        return
    
    def action_handler(self, sender: GPTAgent, receiver: str, content: str):
        """ For an agent thread to invoke, in order to call another agent thread
        """
        # TODO: implement the message passing
        receiver_agent = self.agents.get(receiver, None)
        if receiver_agent is None:
            # fuzzy match
            pass
        else:
            receiver_agent.incoming_interactions.append({"sender": sender, "content": content})
        return

    def step(self, **kwargs):
        """ For each time frame, call step method for agents
        """

        self.movement_manager.start()

        while self.operational:
            time.sleep(1)
            for agent in self.agents:
                # run agent as thread
                thread = threading.Thread(target=agent.step)
                thread.start() 
            
            # prompt user to input control signal (in case they want to suspand the server)
            command = input("Stop? [y]=stop and save all states")
            if command == "y":
                self.operational = False
        
        # TODO: save the state of all agents to dump files

        # TODO: if necessary, send the agents dump files to user..

        self.movement_manager.join()

        return
    
    def run(self, ):
        """The main loop 
        """
        while True:
            time.sleep(10)
            self.step()
    

if __name__ == "__main__":
    # TODO: add some arguments
    env = Environment()
    dirname = 'test_env0'
    env.load_from_file(f"static_files/{dirname}/environment.json")
    env.run()
