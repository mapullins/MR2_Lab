import numpy as np
import pandas as pd

from stat_ranker import *


#Load the two data frames; main one for getting data and a reference one
df = pd.read_csv('Lab_Results.csv')
df_ref = pd.read_csv('Total_Data.csv')

#Returns basic information about Monster given type and stat and its short version
def monster_lookup(main, sub, stat, stat_short):

    #Create a DataFrame with only the monster in it
    monster_df = df_ref[(df_ref.Main == main) & (df_ref.Sub == sub)]
    
    #Save the stats in easy to understand variables
    grow = monster_df[stat + ' Gain'].iloc[0]
    base = monster_df[stat].iloc[0]
    rank = monster_df[stat_short].iloc[0]

    
    return (grow, base, rank)

#Data_Clean main function
def data_cleaner(stat, short):
    #Create an empty DataFrame to populate for the wanted data
    final_df = pd.DataFrame([], columns = ['Main_Stat', 'Main_Growth', 'Main_Base', 'Main_Base_Rank', 'Main_True_Rank', 'Sub_Stat', 'Sub_Growth', 'Sub_Base', 'Sub_Base_Rank', 'Sub_True_Rank', 'Result_Stat', 'Result_Growth', 'Result_Base', 'Result_Base_Rank', 'Result_True_Rank', 'Main_Result', 'Sub_Result', 'Type', 'Main', 'Sub', 'Rarity'])
    ind = 0

    #Loop through df to populate final_df (since there aren't too many for this to get bogged down)
    for en, row in df.iterrows():
    
        #Variables for looking up references
        main_main = row['Main 1']
        main_sub = row['Sub 1']
        main_stats = [row['Lif 1'], row['Pow 1'], row['Int 1'], row['Ski 1'], row['Spd 1'], row['Def 1']]
    
        sub_main = row['Main 2']
        sub_sub = row['Sub 2']
        sub_stats = [row['Lif 2'], row['Pow 2'], row['Int 2'], row['Ski 2'], row['Spd 2'], row['Def 2']]
    
        result_main = row['Main']
        result_sub = row['Sub']
        result_stats = [row['Lif'], row['Pow'], row['Int'], row['Ski'], row['Spd'], row['Def']]
    
        #Record stats of first monster
        main_st = row[stat + ' 1']
        main_g, main_b, main_r = monster_lookup(main_main, main_sub, stat, short)
        true_main_stats = corrected_stats(main_main, main_sub, main_stats)
    
        #Little more effort for true rank
        for i in range(len(true_main_stats)):
            if true_main_stats[i] == short:
                main_t = i+1
            
        #Record stats of second monster
        sub_st = row[stat + ' 2']
        sub_g, sub_b, sub_r = monster_lookup(sub_main, sub_sub, stat, short)
        true_sub_stats = corrected_stats(sub_main, sub_sub, sub_stats)
    
        #Little more effort for true rank
        for i in range(len(true_sub_stats)):
            if true_sub_stats[i] == short:
                sub_t = i+1    
    
        #Record stats of result monster
        result_st = row[stat]
        result_g, result_b, result_r = monster_lookup(result_main, result_sub, stat, short)
        true_result_stats = corrected_stats(result_main, result_sub, result_stats)
    
        #Little more effort for true rank
        for i in range(len(true_result_stats)):
            if true_result_stats[i] == short:
                result_t = i+1    
            
            
        #Code for the binary choice features
        if (main_main == result_main) and (main_sub == result_sub):
            main_re = 1
        
        else:
            main_re = 0
        
        if (sub_main == result_main) and (sub_sub == result_sub):
            sub_re = 1
        
        else:
            sub_re = 0
        
        #Compile the stats in a single list to add to the DataFrame
        features = [main_st, main_g, main_b, main_r, main_t, sub_st, sub_g, sub_b, sub_r, sub_t, result_st, result_g, result_b, result_r, result_t, main_re, sub_re, row['Type'], result_main, result_sub, row['Rarity']]
    
        final_df.loc[ind] = features
        ind += 1
    
    final_df.to_csv(stat+'_Data_1.csv', index = False)    
