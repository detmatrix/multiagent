# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        GhostStates = currentGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        if action == 'Stop':
            return -1
        capsules = currentGameState.getCapsules()
        distTo = util.manhattanDistance
        distList = []
        if capsules:
            capsulesCost = map(lambda x: distTo(x, newPos), capsules)
            capsulesDist = min(capsulesCost)
            if capsulesDist < 2:
                return 100
        for ghostState in GhostStates:
            if ghostState.scaredTimer == 0 and distTo(ghostState.getPosition(),newPos) < 3:
                #print "hide"
                return -1000
            else:
                time = ghostState.scaredTimer
                if time > 0:
                    dist = distTo(newPos, ghostState.getPosition())
                    if dist == 0:
                        #print "eatGhost"
                        print "500"
                        return 500
                    if dist * 2 <= time:  # eat ghost gain no points?
                        print "near Ghost", 1.0 / dist * 100
                        distList.append(1.0 / dist * 100)
                else:
                    distList = []
        if distList != []:
            #print "eatGhost"
            return max(distList)
        Food = currentGameState.getFood()  #tricky based on current game state!
        foodList = Food.asList()
        #print "foodlist", foodList
        foodCostList = map(lambda x: distTo(x, newPos), foodList)
        # print "foodCostList", foodCostList
        #foodList = map(lambda x: 1.0 / x * 10, foodCostList)
        # print "foodlist2", foodList
        for cost in foodCostList:
            if cost == 0:
                #print "food!"
                return 50
        food = min(foodCostList)
        #print "foodNear", 1.0 / food * 10#max(foodList)
        return 1.0 / food * 10
        #return successorGameState.getScore() - currentGameState.getScore()
        #print "score", successorGameState.getScore() - currentGameState.getScore()
        #return successorGameState.getScore() - currentGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def minimax_value(lastState, action, lastAgentIndex, depth_left):
            currentState = lastState.generateSuccessor(lastAgentIndex, action)
            if depth_left == 0 or currentState.isWin() or currentState.isLose():
                return self.evaluationFunction(currentState)
            else:
                num_agent = currentState.getNumAgents()
                agentIndex = lastAgentIndex + 1
                if agentIndex >= num_agent:
                    agentIndex = 0
                    depth_left -= 1
                    if depth_left == 0:
                        return self.evaluationFunction(currentState)
                # else:
                actions = currentState.getLegalActions(agentIndex)
                if agentIndex == 0:
                    retVal = max(map(lambda x: minimax_value(currentState, x, agentIndex, depth_left), actions))
                else:
                    retVal = min(map(lambda x: minimax_value(currentState, x, agentIndex, depth_left), actions))
                agentIndex += 1
                return retVal

                # agent_left -= 1
                # actions = currentState.getLegalActions(agentIndex)
                # if status == 'max':
                #     return max(map(lambda x: minimax_value(currentState, x, agent_left), actions))
                # else:
                #     return min(map(lambda x: minimax_value(currentState, x, agent_left), actions))

        # for i in range(0, self.depth):
        #     num_agent = gameState.getNumAgents()
        #     num_ghost = num_agent - 1
        actions = gameState.getLegalActions(0)
        #     for agentIndex in range(0, num_agent):

        return max(actions, key=lambda x: minimax_value(gameState, x, 0, self.depth))




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

