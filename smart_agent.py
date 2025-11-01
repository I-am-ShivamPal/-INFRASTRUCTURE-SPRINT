import csv
import os
import json
from collections import defaultdict
import random

RL_TABLE = "rl_table.csv"
STATE_ACTION_FILE = "states_actions.json"

class SmartAgent:
    def __init__(self, alpha=0.6, gamma=0.0, epsilon=0.2):
        self.alpha = alpha       # learning rate
        self.gamma = gamma       # discount factor
        self.epsilon = epsilon   # exploration rate

        self.q_table = defaultdict(lambda: defaultdict(float))
        self.state_actions = self.load_state_actions()
        self.load_q_table()

    # ✅ Load state → action list from YAML
    def load_state_actions(self):
        if not os.path.exists(STATE_ACTION_FILE):
            # Create default state-action mapping
            default_config = {
                "actions": {
                    "connection_failed": ["restart_deployment", "rollback"],
                    "slow_response": ["rollback", "restart_deployment"],
                    "healthy": ["monitor"]
                }
            }
            with open(STATE_ACTION_FILE, "w") as f:
                json.dump(default_config, f, indent=2)
            return default_config
        
        with open(STATE_ACTION_FILE, "r") as f:
            return json.load(f)

    # ✅ Load existing Q-values from CSV
    def load_q_table(self):
        if not os.path.exists(RL_TABLE):
            return

        with open(RL_TABLE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                s = row["state"]
                a = row["action"]
                q = float(row["q_value"])
                self.q_table[s][a] = q

    # ✅ Save Q-values back to CSV
    def save_q_table(self):
        try:
            rows = []
            for s, actions in self.q_table.items():
                for a, q in actions.items():
                    rows.append([s, a, q])

            with open(RL_TABLE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["state", "action", "q_value"])
                writer.writerows(rows)
        except Exception as e:
            print(f"Warning: Could not save Q-table: {e}")

    # ✅ Get action list for a state
    def get_actions(self, state):
        return self.state_actions["actions"].get(state, [])

    # ✅ Choose action using epsilon-greedy
    def choose_action(self, state):
        actions = self.get_actions(state)

        if not actions:
            print(f"[WARNING] No actions defined for state: {state}")
            return None

        # explore
        if random.random() < self.epsilon:
            return random.choice(actions)

        # exploit
        return max(actions, key=lambda a: self.q_table[state][a])

    # ✅ RL Q-Learning reward update (automatic)
    def update(self, state, action, reward):
        current_q = self.q_table[state][action]
        new_q = current_q + self.alpha * (reward - current_q)
        self.q_table[state][action] = new_q
        self.save_q_table()

    # ✅ Human feedback Q-update (manual)
    def human_update(self, state, action, feedback):
        current_q = self.q_table[state][action]
        new_q = current_q + self.alpha * (feedback - current_q)
        self.q_table[state][action] = new_q
        self.save_q_table()


# ✅ Test (optional)
if __name__ == "__main__":
    agent = SmartAgent()

    test_state = "port_busy"
    action = agent.choose_action(test_state)
    print("Selected Action:", action)

    # Fake reward
    agent.update(test_state, action, reward=1)

    # Fake human feedback
    agent.human_update(test_state, action, feedback=1)
