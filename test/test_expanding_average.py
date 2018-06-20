import numpy as np
import pandas as pd

import unittest

class TestExpandingAverage(unittest.TestCase):
    def setUp(self):
        self.data = pd.read_csv('../dat/expanding_avg_1983-2017.csv', index_col=0).sort_values(['SEASON_ID','TEAM_ID', 'GAME_DATE'])
        
    def test_expanding_averages(self):
        STATS = ['PTS', 'AST', 'DREB']
        AVG_STATS = ['AVG_PTS', 'AVG_AST', 'AVG_DREB']
        seasons = self.data['SEASON_ID'].unique()
        for season in seasons:
            if season == 21984:
                continue
            s_df = self.data.loc[self.data['SEASON_ID'] == season]
            teams = s_df['TEAM_ID'].unique()
            for team in teams:
                t_df = s_df.loc[s_df['TEAM_ID'] == team].sort_values(['SEASON_ID','TEAM_ID', 'GAME_DATE'])
                self.assertTrue(np.all(t_df.head(1)[AVG_STATS].isna(), axis=1), 'first game has averages')
                correct = t_df[STATS].expanding().mean().shift(1).iloc[1:]
                t_df = t_df.iloc[1:]
                diff = np.abs(correct[STATS].values-t_df[AVG_STATS].values) < 1e-4
                #self.assertTrue(np.all(diff), pd.concat([t_df[AVG_STATS], correct[STATS]], axis=1))
                self.assertTrue(np.all(diff), 'error in season {} team {}'.format(season, team))
                print('passed season {} team {}'.format(season, team))
        #phi_2017 = self.data.loc[(self.data['SEASON_ID'] == 22017) & (self.data['TEAM_ABBREVIATION'] == 'PHI')].fillna(0)
        #correct = phi_2017['PTS'].expanding().mean().shift(1).fillna(0)
        #self.assertTrue(np.all(np.abs(correct - phi_2017['AVG_PTS']) < 1e-4))
        
if __name__ == '__main__':
    unittest.main()