import pandas as pd
import numpy as np

#Batter Scoring
bSingle = 1 #Single
bDouble = 2 #Double
bTriple = 3 #Triple
bHR = 4 #Homerun
bRuns = 2 #Runs
bRBI = 2 #RBIs
bSO = -1 #Strikeouts
bBB = 1 #Walks
bHBP = 1 #Hit-by-pitch
bSB = 2 #Stolen base
bCS = -1 #Caught stealing

#Pitcher Scoring (* indicates not projected by Steamer)
pBS = -2 #Blown saves*
pER = -3 #Earned runs
pGF = 1 #Games finished*
pGS = 1 #Games started
pH = -1 #Hits
pHLD = 4 #Holds*
pIP = 3 #Innings pitched
pL = -2 #Losses
pW = 5 #Wins
pQS = 8 #Quality starts*
pSO = 1 #Strikeouts
pBB = -1 #Walks
pSV = 6 #Saves


#Read in data from files
BatterDF = pd.read_csv('Data/2019_Steamer_Batters.csv')
PitcherDF = pd.read_csv('Data/2019_Steamer_Pitchers.csv')
ProspectDF = pd.read_csv('Data/Prospects.csv')


#Use regression model to project BS, HLD, and QS for pitchers
PitcherDF['QS'] = ((PitcherDF['GS']/(PitcherDF['ER']*(PitcherDF['GS']/PitcherDF['G'])))*(PitcherDF['IP']*(PitcherDF['GS']/PitcherDF['G']))*
                   (((PitcherDF['GS']+PitcherDF['G'])/(4*PitcherDF['G']))**2))

PitcherDF['HLD'] = 0
PitcherDF['QS'] = 0
for i, row in PitcherDF.iterrows():
    if ( row['SV'] < 6 and row['GS'] < 4):
        HLDs = (row['G']/row['ERA']) + 5
        PitcherDF.at[i, 'HLD'] = HLDs
    if (row['GS'] > 0):
        QSs = (row['GS']/(row['ER']*(row['GS']/row['G'])))*(row['IP']*(row['GS']/row['G']))*(((row['GS']+row['G'])/(4*row['G']))**2)
        PitcherDF.at[i, 'QS'] = QSs

#BS are TODO

#Calculate scoring for batters and pitchers
BatterDF['Fantasy PTS'] = (((BatterDF['H']-(BatterDF['2B']+BatterDF['3B']+BatterDF['HR']))*bSingle) + (BatterDF['2B']*bDouble) + (BatterDF['3B']*bTriple)
                          + (BatterDF['HR']*bHR) + (BatterDF['R']*bRuns) + (BatterDF['RBI']*bRBI) + (BatterDF['SO']*bSO) + (BatterDF['BB']*bBB)
                          + (BatterDF['HBP']*bHBP) + (BatterDF['SB']*bSB) + (BatterDF['CS']*bCS))

#Add blown saves if they are done at some point
PitcherDF['Fantasy PTS'] = ((PitcherDF['ER']*pER) + (PitcherDF['SV']*pGF) + (PitcherDF['GS']*pGS) + (PitcherDF['H']*pH) + (PitcherDF['HLD']*pHLD)
                           + (PitcherDF['IP']*pIP) + (PitcherDF['L']*pL) + (PitcherDF['W']*pW) + (PitcherDF['QS']*pQS) + (PitcherDF['SO']*pSO)
                           + (PitcherDF['BB']*pBB) + (PitcherDF['SV']*pSV))

#Calculate prospect value for fantasy
ProspectDF['ETA'].replace(2018, 2019, inplace=True)
ProspectDF['FV'] = ProspectDF['FV'].replace({'\+':''}, regex = True)
ProspectDF['FV'] = ProspectDF['FV'].astype(str).astype(int)

ProspectDF['Fantasy Value'] = ProspectDF['FV']/(ProspectDF['ETA']-2018)


#Select the stuff to export
Prospect_to_export = ProspectDF[['Name', 'Tm', 'Pos', 'FV', 'ETA', 'Risk', 'Fantasy Value']]
Batter_to_export = BatterDF[['Name', 'Team', 'wOBA', 'wRC+', 'WAR', 'Fantasy PTS']]
Pitcher_to_export = PitcherDF[['Name', 'Team', 'ERA', 'FIP', 'WAR', 'Fantasy PTS']]

Prospect_to_export.to_csv('Data\Prospect_Fantasy.csv')
Batter_to_export.to_csv('Data\Batter_Fantasy.csv')
Pitcher_to_export.to_csv('Data\Pitcher_Fantasy.csv')
