from UltimateTicTacToe import TicTacToe
from TTTPlayer import *
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import copy
import tqdm
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing as mp

gridSize = 9
moveMap = []
for k in range(9):
    for i in range(3):
        for j in range(3):
            moveMap.append((k,i,j))

device = torch.device('cuda')

class TTTNet(nn.Module):
    def __init__(self):
        super(TTTNet, self).__init__()
        self.layer1 = nn.Linear(gridSize * gridSize + 9, 256)
        torch.nn.init.xavier_normal_(self.layer1.weight)
        self.layer2 = nn.Linear(256, 256)
        torch.nn.init.xavier_normal_(self.layer2.weight)
        self.layer3 = nn.Linear(256, 256)
        torch.nn.init.xavier_normal_(self.layer3.weight)
        self.layer4 = nn.Linear(256, gridSize * gridSize)
        torch.nn.init.xavier_normal_(self.layer4.weight)

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        x = F.relu(self.layer3(x))
        x = F.sigmoid(self.layer4(x))
        return x

class MLPlayer(TTTPlayer):
    def __init__(self, name, net):
        super().__init__(name)
        self.net = net
        self.name = name

    def takeTurn(self, board, possibleMoves, subgrid):
        grid = gridToOneHot(subgrid)
        input = torch.hstack((torch.Tensor(board).flatten(), grid))
        output = self.net(input)
        while True:
            index = torch.argmax(output)
            move = moveMap[index]
            if move in possibleMoves:
                break
            output[index] = 0
            if torch.sum(output) == 0:
                print("Whoops")
                return random.choice(possibleMoves)

        return move

class InputDataSet(Dataset):
    def __init__(self, inputs, labels):
        self.inputs = torch.tensor(inputs, dtype=torch.float32)
        self.labels = torch.tensor(labels, dtype=torch.float32)

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, index):
        return self.inputs[index], self.labels[index]

def moveToOneHot(move):
    i = 9 * move[0] + 3 * move[1] + move[2]
    out = torch.zeros((81,))
    out[i] = 1
    return out

def gridToOneHot(grid):
    out = torch.zeros((9))
    out[grid] = 1
    return out

def runGameVsRandom(net):
    if random.choice([0,1]) == 0:
        game = TicTacToe(MLPlayer("ML Player", net), RandomPlayer("Random Player"))
    else:
        game = TicTacToe(RandomPlayer("Random Player"), MLPlayer("ML Player", net))
    result = game.playGame()
    if len(result) == 1 and result[0].getName() == "ML Player":
        return 2
    if len(result) == 2:
        return 1
    else:
        return 0
    
if __name__ == "__main__":

    retrain = False
    if retrain:
        n = 1000
        numEpochs = 2500

        net = TTTNet().to(device)
        losses = []
        criterion = nn.BCELoss()
        optimizer = optim.Adam(net.parameters(), lr=0.001)

        boards = torch.tensor(np.load("boards.npy", allow_pickle=True).astype(np.float32)).to(device).flatten(1,3)
        grids = torch.tensor(np.load("subgrids.npy", allow_pickle=True).astype(np.float32)[np.newaxis].T).to(device)
        grids = np.load("subgrids.npy", allow_pickle=True)
        gridOneHots = [gridToOneHot(grid) for grid in grids]
        gridOneHots = torch.stack(gridOneHots).to(device)
        input = torch.hstack((boards, gridOneHots))


        moves = np.load("moves.npy", allow_pickle=True)
        moveOneHots = [moveToOneHot(move) for move in moves]
        moveOneHots = torch.stack(moveOneHots).to(device)

        inputData = InputDataSet(input, moveOneHots)

        dataloader = DataLoader(inputData, batch_size=256, shuffle=True)

        for epoch in tqdm.tqdm(range(numEpochs)):
            rLoss = 0
            for inputs, labels in dataloader:
                optimizer.zero_grad()
                outputs = net(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                rLoss += loss.item()
            losses.append(rLoss)

        torch.save(net.state_dict(), "model")

        plt.plot(losses)
        plt.show()
    else:
        numGames = 2000
        net = TTTNet()
        net.load_state_dict(torch.load("model"))
        net.eval()
        p1 = MLPlayer("ML Player", net)
        wins = 0
        draws = 0
        pool = mp.Pool(mp.cpu_count())
        nets = [net for _ in range(numGames)]
        result = pool.map(runGameVsRandom, nets)
        result = np.asarray(result)
        wins = np.count_nonzero(result == 2)
        draws = np.count_nonzero(result == 1)
        losses = np.count_nonzero(result == 0)
        """ for _ in tqdm.tqdm(range(numGames)):
            game = TicTacToe(p1, RandomPlayer("Random Player"))
            result = game.playGame()
            if len(result) == 1 and result[0].getName() == "ML Player":
                wins += 1
            if len(result) == 2:
                draws += 1 """
        losses = numGames - (wins + draws)
        print(f"Winrate = {wins / numGames}\nDrawrate = {draws / numGames}\nLossrate = {losses / numGames}")
