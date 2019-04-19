import numpy as np
import pandas as pd


def removeM(value):
    if(value[-1] == 'M'):
        value = value[:-1]
        value = float(value) * 1_000_000
    else:
        value = removeK(value)
    return value


def removeK(value):
    if(value[-1] == 'K'):
        value = value[:-1]
        value = float(value) * 1_000
    else:
        pass
    return value


dataset = pd.read_csv(
    "/home/lgcaobianco/repositorios/fifa19/src/dataset/data.csv")

dataset = dataset.drop(columns=['Photo', 'Flag', 'Club Logo', 'Real Face',
                                'International Reputation', 'Loaned From', 'Nationality', 'Contract Valid Until'])
dataset['Value'] = dataset['Value'].map(lambda x: x.lstrip('€'))
dataset['Value'] = dataset['Value'].map(removeM, dataset['Value'].all())
dataset['Value'] = pd.to_numeric(dataset['Value'])
dataset['Potential'] = pd.to_numeric(dataset['Potential'])
dataset['Overall'] = pd.to_numeric(dataset['Overall'])
gks = dataset.loc[dataset['Position'] == 'GK']
midfielders = dataset.loc[(dataset['Position'].str[-1] == 'M')]
defensors = dataset.loc[(dataset['Position'].str[-1] == 'B')]
attackers = dataset.loc[(dataset['Position'].str[-1] == 'F') | (
    dataset['Position'].str[-1] == 'W') | (dataset['Position'].str[-1] == 'T')]
attackers = attackers.drop(
    columns=['GKReflexes', 'GKPositioning', 'GKKicking', 'GKHandling', 'GKDiving'])
midfielders = midfielders.drop(
    columns=['GKReflexes', 'GKPositioning', 'GKKicking', 'GKHandling', 'GKDiving'])
defensors = defensors.drop(
    columns=['GKReflexes', 'GKPositioning', 'GKKicking', 'GKHandling', 'GKDiving'])


def findBestPlayers(param):
    param = param.assign(
        PotGrowth=(param['Potential'] - param['Overall']).values)
    param = param.rename(columns={'PotGrowth': 'Potential Growth'})
    # attacker with best growth in game
    print("Best growth in game: ")
    print(param.loc[param['Potential Growth'].idxmax()])
    future_stars = param.loc[(
        param['Potential Growth'] >= 10) & (param['Potential'] >= 85)]
    print("Players with high growths that will achieve high overalls: ")
    print(future_stars.sort_values(by='Potential', ascending=False))


findBestPlayers(attackers)
findBestPlayers(midfielders)
findBestPlayers(defensors)
findBestPlayers(gks)
