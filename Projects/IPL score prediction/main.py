
import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder as lec
from sklearn.neighbors import KNeighborsRegressor as knn

batsman_ecode = lec()
bowler_encode = lec()
venue_encode = lec()
team_encode = lec()


df = pd.read_csv('G:\ml data set\match\ipl_csv2/all_matches.csv')

df = df[df['innings']<=2]
df = df[df['ball']<=5.6]
df['total_runs'] = df['runs_off_bat'] + df['extras']

df.drop(columns={'season','start_date','runs_off_bat', 'extras', 'wides', 'noballs', 'byes', 'legbyes',
       'penalty', 'wicket_type', 'player_dismissed', 'other_wicket_type',
       'other_player_dismissed'},inplace=True)


blankdf = pd.DataFrame(columns=['match_id', 'season', 'start_date', 'venue', 'innings', 'ball',
       'batting_team', 'bowling_team', 'striker', 'non_striker', 'bowler',
       'runs_off_bat', 'extras', 'wides', 'noballs', 'byes', 'legbyes',
       'penalty', 'wicket_type', 'player_dismissed', 'other_wicket_type',
       'other_player_dismissed'],index=['a'])

blankdf['striker'] = "No_one"
blankdf['bowler'] = "No_one"

df = pd.concat([df,blankdf],ignore_index=True)

batsman_ecode.fit(df['striker'])
bowler_encode.fit(df['bowler'])
df = df.drop(index=60828)

dm = df.groupby(['match_id', 'venue', 'innings', 'batting_team', 'bowling_team']).total_runs.sum().reset_index()

dp = df.groupby(['match_id','innings','bowler']).sum().reset_index()
dp = dp.groupby(['match_id','innings'])['bowler'].apply(','.join).reset_index()
data = pd.merge(dm,dp,'outer')

de = df.groupby(['match_id','innings','striker']).sum().reset_index()
de = de.groupby(['match_id','innings'])['striker'].apply(','.join).reset_index()
data = pd.merge(data,de,'outer')

data.rename(columns={'striker':'batsmen'},inplace=True)
data.drop(columns='match_id',inplace=True)

data.set_index('batting_team',inplace=True)
data = data.drop({'Kochi Tuskers Kerala','Rising Pune Supergiants','Gujarat Lions','Deccan Chargers','Rising Pune Supergiant'},axis=0)
data = data.reset_index()
data.set_index('bowling_team',inplace=True)

data = data.drop({'Kochi Tuskers Kerala','Rising Pune Supergiants','Gujarat Lions','Deccan Chargers','Rising Pune Supergiant'},axis=0)
data = data.reset_index()

data = data[['venue','innings','batting_team','bowling_team','batsmen','bowler','total_runs']]
data.rename(columns={'bowler':'bowlers'},inplace= True)

data[['1st_batsman','2nd_batsman','3rd_batsman','4th_batsman','5th_batsman','6th_batsman','7th_batsman','8th_batsman']] = data.batsmen.str.split(',',expand=True)

data[['1st_bowler','2nd_bowler','3rd_bowler','4th_bowler','5th_bowler','6th_bowler']] = data.bowlers.str.split(',',expand=True)

data = data.drop(columns=['batsmen','bowlers'])

last_col = data.pop('total_runs')
data.insert(18,'total_runs',last_col)

data = data.fillna(value="No_one")

team_encode.fit(data['batting_team'])

data['venue'] = venue_encode.fit_transform(data['venue']) #1
data.loc[:,list(data.columns)[2:4]] = data.loc[:,list(data.columns)[2:4]].apply(team_encode.transform) #2

data.loc[:,list(data.columns)[4:12]] = data.loc[:,list(data.columns)[4:12]].apply(batsman_ecode.transform) #3

data.loc[:,list(data.columns)[12:18]] = data.loc[:,list(data.columns)[12:18]].apply(bowler_encode.transform) #4

data.loc[:,list(data.columns)[4:12]] = data.loc[:,list(data.columns)[4:12]].replace(175,-1)
data.loc[:,list(data.columns)[12:18]] = data.loc[:,list(data.columns)[12:18]].replace(220,-1)

x = data.drop(columns='total_runs')
y = data['total_runs']

knnreg = knn(n_neighbors=5).fit(x,y)

joblib.dump(batsman_ecode,'batsman_ecode.joblib')
joblib.dump(bowler_encode,'bowler_encode.joblib')
joblib.dump(venue_encode,'venue_encode.joblib')
joblib.dump(team_encode,'team_encode.joblib')
joblib.dump(knnreg,'knnreg.joblib')