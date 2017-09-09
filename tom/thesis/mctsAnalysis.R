library(tidyverse)
boxplot(MovesMade~GameLimit, data = mcts_level1, main = 'Simple Eval: Moves Taken to Finish Game',
        xlab='Games Simulated', ylab='Moves taken to win')

boxplot(MovesMade~GameLimit, data = mcts_standard, main = 'Standard MCTS: Moves Taken to Finish Game',
        xlab='Games Simulated', ylab='Moves taken to win')

boxplot(MovesMade~GameLimit, data = mcts_level1[mcts_level1$MoveLimit==1,], main = 'Moves taken to finish with MCTS depth 1',
        xlab='Games Simulated', ylab='Moves taken to win')

boxplot(MovesMade~GameLimit, data = mcts_level1[mcts_level1$MoveLimit==3,],
        main = 'Moves taken to finish with MCTS depth 3',
        xlab='Games Simulated', ylab='Moves taken to win')

boxplot(MovesMade~GameLimit, data = mcts_level1[mcts_level1$MoveLimit==5,],
        main = 'Moves taken to finish with MCTS depth 5',
        xlab='Games Simulated', ylab='Moves taken to win')

boxplot(MovesMade~GameLimit, data = mcts_level1[mcts_level1$MoveLimit==10,],
        main = 'Moves taken to finish with MCTS depth 10',
        xlab='Games Simulated', ylab='Moves taken to win')

boxplot(MovesMade~GameLimit, data = mcts_level1[mcts_level1$MoveLimit==20,],
        main = 'Moves taken to finish with MCTS depth 20',
        xlab='Games Simulated', ylab='Moves taken to win')

boxplot(MovesMade~MoveLimit, data = mcts_level1[mcts_level1$GameLimit==50,],
        main = 'Moves Taken to Finish with Game Limit 50',
        xlab='MCTS Move Limit', ylab='Moves taken to win')

boxplot(MovesMade~MoveLimit, data = mcts_level1[mcts_level1$GameLimit==100,],
        main = 'Moves Taken to Finish with Game Limit 100',
        xlab='MCTS Move Limit', ylab='Moves taken to win')

boxplot(MovesMade~MoveLimit, data = mcts_level1[mcts_level1$GameLimit==200,],
        main = 'Moves Taken to Finish with Game Limit 200',
        xlab='MCTS Move Limit', ylab='Moves taken to win')

boxplot(MovesMade~MoveLimit, data = mctsRNGDepth[mctsRNGDepth$GameLimit==50,],
        main = 'RNG: Moves Taken to Finish with Game Limit 50',
        xlab='MCTS Move Limit', ylab='Moves taken to win')

boxplot(MovesMade~MoveLimit, data = mctsRNGDepth[mctsRNGDepth$GameLimit==100,],
        main = 'RNG: Moves Taken to Finish with Game Limit 100',
        xlab='MCTS Move Limit', ylab='Moves taken to win')

boxplot(MovesMade~GameLimit, data = mcts_DL,
        main = 'DL Eval: Moves Taken to Finish Game',
        xlab='Games Simulated', ylab='Moves taken to win')

boxplot(MovesMade~Type, data = testing_heuristic_eval,
        main = 'Testing Heuristic Features',
        xlab='Feature', ylab='Moves taken to win')
