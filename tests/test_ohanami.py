import rlcard
import numpy as np
from rlcard.envs.registration import register
from rlcard.agents import RandomAgent as RandomAgent


register(
    env_id='ohanami',
    entry_point='rl_card_env.envs.ohanami:OhanamiEnv',
)

env = rlcard.make('ohanami')
random_agent_1 = RandomAgent(env.num_actions)
random_agent_2 = RandomAgent(env.num_actions)
env.set_agents([
    random_agent_1,
    random_agent_2,
])
env.reset()

while not env.is_over():
    state = env.get_state(env.get_player_id())
    env.print_state(env.get_player_id())
    legal_actions = state['raw_legal_actions']
    chosen_action = np.random.choice(legal_actions)
    env.step(chosen_action)



