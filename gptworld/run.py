# A main file that activate the environent and the agent and let the game goes automatically. 

# Import necessary modules

if __name__ == "__main__":
    from gptworld.core.environment import GPTWorldEnv
    from gptworld.core.agent import GPTAgent

    # Create an instance of the environment
    env = GPTWorldEnv.from_file("static_files/test_env0/environment.json")
    env.initialize() # this start a new subprocess to start a webpage.

    # Create an instance of the agent
    agent1 = GPTAgent.from_file("static_files/test_env0/a_001.json")
    agent2 = GPTAgent.from_file("static_files/test_env0/a_002.json")

    env.mount_agent(agent1)
    env.mount_agent(agent2)

    env.run()


