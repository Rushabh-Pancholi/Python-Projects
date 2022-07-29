import joblib

from sklearn.model_selection import train_test_split as tts
from sklearn.preprocessing import LabelEncoder as lec
import pandas as pd

def predict_runs(data):
    
    blankdata = pd.DataFrame(columns=['venue', 'innings', 'batting_team', 'bowling_team', '1st_batsman',
       '2nd_batsman', '3rd_batsman', '4th_batsman', '5th_batsman',
       '6th_batsman', '7th_batsman', '8th_batsman', '1st_bowler', '2nd_bowler',
       '3rd_bowler', '4th_bowler', '5th_bowler', '6th_bowler'],index=['a'])
    
    data = pd.concat([data,blankdata],ignore_index=True)
    data = data.drop(index=1)
    
    with open('G:\python\hackathon/batsman_ecode.joblib','rb') as f:
        batsman_ecode = joblib.load(f)
        
    with open('G:\python\hackathon/bowler_encode.joblib','rb') as f:
        bowler_ecode = joblib.load(f)
        
    with open('G:\python\hackathon/venue_encode.joblib','rb') as f:
        venue_ecode = joblib.load(f)
        
    with open('G:\python\hackathon/team_encode.joblib','rb') as f:
        team_ecode = joblib.load(f)
        
    with open('G:\python\hackathon\knnreg.joblib','rb') as f:
        knnreg = joblib.load(f)
        

    data[['1st_batsman','2nd_batsman','3rd_batsman','4th_batsman','5th_batsman','6th_batsman','7th_batsman','8th_batsman']] = data.batsmen.str.split(',',expand=True)

    data[['1st_bowler','2nd_bowler','3rd_bowler','4th_bowler','5th_bowler','6th_bowler']] = data.bowlers.str.split(',',expand=True)

    data = data.drop(columns=['batsmen','bowlers'])

    last_col = data.pop('total_runs')
    data.insert(18,'total_runs',last_col)

    data = data.fillna(value="No_one")

    data['venue'] = venue_ecode.transform(data['venue']) #1
    data.loc[:,list(data.columns)[2:4]] = data.loc[:,list(data.columns)[2:4]].apply(team_ecode.transform) #2

    data.loc[:,list(data.columns)[4:12]] = data.loc[:,list(data.columns)[4:12]].apply(batsman_ecode.transform) #3

    data.loc[:,list(data.columns)[12:18]] = data.loc[:,list(data.columns)[12:18]].apply(bowler_ecode.transform) #4

    data.loc[:,list(data.columns)[4:12]] = data.loc[:,list(data.columns)[4:12]].replace(175,-1)
    data.loc[:,list(data.columns)[12:18]] = data.loc[:,list(data.columns)[12:18]].replace(220,-1)
    
    return knnreg.predict(data)

data = pd.read_csv('G:\python\hackathon/ipl1.csv')
predict_runs(data)