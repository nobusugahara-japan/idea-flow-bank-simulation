import random

class Agent:
    def __init__(self, agent_id):
        self.id = agent_id
        self.A = random.uniform(0.01, 0.1)
        self.B = random.uniform(0.01, 0.1)
        self.C = random.uniform(0.01, 0.1)
        self.token = 1.0

    def vote(self, ideas, votes_count):
        max_expected_value = 0
        best_idea = None
        for idea_name, idea_value in ideas.items():
            total_tokens_for_idea = self.token + votes_count[idea_name]
#             expected_value_after_voting = (self.token / total_tokens_for_idea) * idea_value
#             expected_value_after_voting = idea_value / (votes_count[idea_name] + self.token)
            expected_value_after_voting = idea_value * (self.token / (votes_count[idea_name] + self.token))

            if expected_value_after_voting > max_expected_value:
                max_expected_value = expected_value_after_voting
                best_idea = idea_name
        return best_idea

def main():
    agents = [Agent(i+1) for i in range(10)]
    
    ideas = {'A': 0, 'B': 0, 'C': 0}
    votes_count = {'A': 0, 'B': 0, 'C': 0}
    
    vote_log = []

    for agent in agents:
        ideas['A'] += agent.A
        ideas['B'] += agent.B
        ideas['C'] += agent.C

    while max(ideas.values()) < 1:
        for agent in agents:
            voted_idea = agent.vote(ideas, votes_count)
            vote_log.append({
                "agent": agent.id, 
                "voted_for": voted_idea, 
                "idea_value": getattr(agent, voted_idea),
                "current_values": ideas.copy(),
                "votes_count": votes_count.copy()
            })
            votes_count[voted_idea] += agent.token

            if voted_idea == 'A':
                ideas['A'] += agent.A
            elif voted_idea == 'B':
                ideas['B'] += agent.B
            else:
                ideas['C'] += agent.C

    print(f"最初に1に達したアイデア: {max(ideas, key=ideas.get)}")
    
    successful_idea = max(ideas, key=ideas.get)
    for agent in agents:
        agent.token += getattr(agent, successful_idea)

    for entry in vote_log:
        print(f"Agent {entry['agent']} voted for {entry['voted_for']} with value {entry['idea_value']:.2f}")
        for idea_name, idea_value in entry['current_values'].items():
            expected_value_per_token = idea_value / (entry['votes_count'][idea_name] or 1)
            print(f"Idea {idea_name}: Value {idea_value:.2f}, Votes: {entry['votes_count'][idea_name]}, Expected Value per Token: {expected_value_per_token:.2f}")
        print("------")

if __name__ == "__main__":
    main()
