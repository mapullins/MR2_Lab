import numpy as np
import pandas as pd

#Import the Combined Data DataFrame for reference
df_data = pd.read_csv('Total_Data.csv')

#Returns a monster's growth stat multipliers
def growth(main, sub):

    #Dictionary for growth multipliers
    g_dict = {1:0, 2:.5, 3:1, 4:1.5, 5:2}
    
    #Access the specific monster data
    entry = df_data[(df_data.Main == main) & (df_data.Sub == sub)]
    
    #Creates a numpy array of the growth numbers
    g_nums = np.array(entry.iloc[0,15:21]).astype(int)
    
    #Applies the dictionary conversion to the growth numbers
    return np.array([g_dict[i] for i in g_nums])
    
    
#Takes an array of stats and monster type and outputs the stats
def modified_stats(main, sub, stats):
    
    #Records the growth numbers
    growth_mult = growth(main, sub)
    
    #Applies the multiplier
    actual_stats = np.array(stats) * growth_mult
    
    return [(actual_stats[0], 'L'), (actual_stats[1], 'P'), (actual_stats[2], 'I'), (actual_stats[3], 'Sk'), (actual_stats[4], 'Sp'), (actual_stats[5], 'D')]
    
    
#Takes an array of stats and monster type and returns a corrected list
def corrected_stats(main, sub, stats):

    #Get unsorted stats with multiplier applied
    mod_stats = modified_stats(main, sub, stats)
    
    #Future ordered list of stats
    correct_stats = []
    
    #Create a one entry DataFrame to use
    df_small = df_data[(df_data.Main == main) & (df_data.Sub == sub)]
    
    #Loop to populate correct_list:
    while len(mod_stats) > 0:
    
        #Record highest stat number
        max_num = max(mod_stats)[0]
        
        #Create a list of stats with highest stat number
        high_stats = [st for (num, st) in mod_stats if num == max_num]
        
        #Amend list so it includes stat order, then sort
        high_stats = [(df_small[st].iloc[0], st) for st in high_stats]
        high_stats.sort()
        
        #Add true stat order to correct stats
        for entry in high_stats:
            correct_stats.append(entry[1])
            
        #Delete recorded stats frim mod_stats
        mod_stats = [entry for entry in mod_stats if entry[0] != max_num]
        
        
    return correct_stats
        
#Counts how many corrected stats match
def stat_match(main_1, sub_1, stats_1, main_2, sub_2, stats_2):
    
    #Gets the corrected stat order
    cor_stats_1 = corrected_stats(main_1,sub_1,stats_1)
    cor_stats_2 = corrected_stats(main_2,sub_2,stats_2)
    
    #Loops to check how many positions match
    match = 0
    for i in range(len(cor_stats_1)):
        if cor_stats_1[i] == cor_stats_2[i]:
            match += 1
            
    return match

 
#Checks for any classification differences on lab type given an input DataFrame of lab results
def lab_check(df):
    
    #Create a rating dictionary
    lab_text = {0: 'Up to You', 1: 'Not Good', 2: 'Unsure', 3: 'Fine', 4: 'Good', 6: 'Great'}       
    
    #Loop through the DataFrame
    for ind, row in df.iterrows():
        
        #Track types and stats
        first_main = row['Main 1']
        first_sub = row['Sub 1']
        first_stats = [row['Lif 1'], row['Pow 1'], row['Int 1'], row['Ski 1'], row['Spd 1'], row['Def 1']]    
        
        second_main = row['Main 2']
        second_sub = row['Sub 2']
        second_stats = [row['Lif 2'], row['Pow 2'], row['Int 2'], row['Ski 2'], row['Spd 2'], row['Def 2']]
        
        #Determine how many matches there are
        match_num = stat_match(first_main, first_sub, first_stats, second_main, second_sub, second_stats)
        
        #Determine whether this matches what the results say
        match = (lab_text[match_num] == row['Type'])
        
        if match == True:
            print('Fine')
        
        if match == False:
            print(row)
            print('Predicted order was {0} for the first and {1} for the second. The match was considered {2}, but was actually {3}.'.format(corrected_stats(first_main, first_sub, first_stats), corrected_stats(second_main, second_sub, second_stats), lab_text[match_num], row['Type']))  
        
