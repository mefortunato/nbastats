import numpy as np
import pandas as pd

import unittest

def check_avg(df_, season, team, stats):
    avg_stats = ['AVG_'+stat for stat in stats]
    df = df_.loc[(df_['SEASON_ID'] == season)& (df_['TEAM_ABBREVIATION'] == team)].sort_values('GAME_DATE')
    avg = df[stats].expanding().mean().shift(1)
    # use index [1:] because first value is na
    diff = np.abs(df[avg_stats].values[1:] - avg[stats].values[1:])
    by_stat = np.all(diff<1e-4, axis=0)
    #print(season, team, np.argwhere(by_stat == False)) # debug print
    return(np.all(diff<1e-4))

class TestExpandingAverage(unittest.TestCase):
    def setUp(self):
        self.data = pd.read_csv('../dat/expanding_avg_1983-2017.csv', index_col=0).sort_values(['SEASON_ID','TEAM_ID', 'GAME_DATE'])
        
    def test_expanding_stat(self):
        stats = ['PTS', 'FG2M', 'FG2A', 'FG2_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'DREB', 'OREB', 'AST', 'STL', 'BLK', 'TOV', 'PF']
        avg_stats = ['AVG_'+stat for stat in stats]
        for season in self.data['SEASON_ID'].unique():
            for team in self.data.loc[self.data['SEASON_ID']==season]['TEAM_ABBREVIATION'].unique():
                test_df = self.data.loc[(self.data['SEASON_ID']==season) & (self.data['TEAM_ABBREVIATION']==team)]
                test_df = test_df.sort_values('GAME_DATE')
                self.assertTrue(test_df.iloc[0][avg_stats].isna().all(), 'error in season {} team {}: first game has averages')
                self.assertTrue(check_avg(self.data, season, team, stats), 'error in season {} team {}: expanding averages inaccurate'.format(season, team))
        
if __name__ == '__main__':
    unittest.main()