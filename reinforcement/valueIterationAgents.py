# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        # for every iteration k in iterations
        for k in range(iterations):
            # copy the values 
            new_values = self.values.copy()
            # for each state in the mdp states 
            for state in mdp.getStates():
                # check if it is at terminal state, if it is not
                if not mdp.isTerminal(state):
                    # compute the new value for the state from computeQValueFromValues and computeActionFromValues
                    new_values[state] = self.computeQValueFromValues(state, self.computeActionFromValues(state))
                # now put the new values as a copy to the values 
                self.values = new_values.copy()

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action): 
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # initiate the q_value as 0 
        q_value = 0
        # for each transition in mdp.getTransitionStatesAndProbs()
        for transition in mdp.getTransitionStatesAndProbs():
            # q_value = q_value + the second element of the trasnition * the reward from the first element of this transition ( because it is a tuple ) 
            # and action + (discount and the value of the transition)
            q_value += transition[1] * ((self.mdp.getReward(transition[0], action) + (self.discount * self.getValue(transition[0]))))
            # now return the computed q_value
            return q_value

    def computeActionFromValues(self, state): 
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # get all possible actions from mdp.getPossibleActions(state)
        new_possible_actions = self.mdp.getPossibleActions(state)
        # if the state is not at the terminal 
        if self.mdp.isTerminal(state) == False:
            # initiate the best_action as the first element of new_possible_actions
            best_action = new_possible_actions[0]
            # get the best_q_value from getQValue(state, best_action) because we need to see what the best_action gives us
            best_q_value = self.getQValue(state, best_action)
            # for each action in new_possible_actions
            for action in new_possible_actions:
                # if the QValue from teh state and action is higher that the best_q_value
                if self.getQValue(state, action) > best_q_value:
                    # that becomes the best_q_value
                    best_q_value = self.getQValue(state, action)
                    # and the best_action is the action we should go for 
                    best_action = action
            # return the best_action
            return best_action

        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
