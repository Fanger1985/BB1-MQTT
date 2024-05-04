import requests
import numpy as np
import random
import time

# Configuration for the ESP32 web server
ESP32_IP = '192.168.1.149'
PORT = '80'
BASE_URL = f'http://{ESP32_IP}:{PORT}'

# Define the state space and action space
num_distance_states = 10  # Example distance partitioned states
presence_states = 2  # 0 for no presence, 1 for presence
states = range(num_distance_states * presence_states)
actions = ['forward', 'backward', 'left', 'right', 'stop']

# Initialize Q-table
Q = np.zeros((len(states), len(actions)))

# Hyperparameters
alpha = 0.1  # Learning rate
gamma = 0.6  # Discount factor
epsilon = 0.1  # Exploration rate

def get_state_from_sensors():
    """ Fetch sensor data and compute the current state. """
    response = requests.get(f"{BASE_URL}/sensors")
    data = response.json()
    distance = data['distance']
    presence = data['presence']  # Assuming presence data is boolean: True or False
    distance_state = min(int(distance / 10), num_distance_states - 1)
    presence_state = 1 if presence else 0
    state = distance_state + presence_state * num_distance_states
    return state

def choose_action(state):
    """ Choose an action based on the current state and Q-table. """
    if random.uniform(0, 1) < epsilon:
        return random.choice(actions)  # Explore action space
    else:
        return actions[np.argmax(Q[state])]  # Exploit learned values

def send_command(action):
    """ Send a command to the ESP32. """
    requests.get(f"{BASE_URL}/{action}")

def get_reward():
    """ Retrieve reward based on the last action's outcome. """
    response = requests.get(f"{BASE_URL}/reward")
    reward = response.json()['reward']
    return reward

def update_q_table(state, action, reward, new_state):
    """ Update the Q-table using the Q-learning algorithm. """
    old_value = Q[state, actions.index(action)]
    future_optimal_value = np.max(Q[new_state])
    new_value = (1 - alpha) * old_value + alpha * (reward + gamma * future_optimal_value)
    Q[state, actions.index(action)] = new_value

def save_q_table(Q, filename='q_table.npy'):
    """ Save the Q-table to a file. """
    np.save(filename, Q)
    print("Q-table saved to", filename)

def load_q_table(filename='q_table.npy'):
    """ Load the Q-table from a file. """
    try:
        Q = np.load(filename)
        print("Q-table loaded from", filename)
        return Q
    except FileNotFoundError:
        print("File not found, starting with a new Q-table")
        return np.zeros((len(states), len(actions)))

def main():
    Q = load_q_table()  # Load the existing Q-table if available

    try:
        for episode in range(1000):  # Run for a certain number of episodes
            state = get_state_from_sensors()

            action = choose_action(state)
            send_command(action)

            time.sleep(1)  # Delay for the state to change
            new_state = get_state_from_sensors()
            reward = get_reward()

            update_q_table(state, action, reward, new_state, Q)

            if episode % 100 == 0:  # Save the Q-table every 100 episodes
                save_q_table(Q)

            print(f"Episode {episode}: State={state}, Action={action}, Reward={reward}")

    finally:
        save_q_table(Q)  # Ensure the Q-table is saved at the end

if __name__ == "__main__":
    main()
