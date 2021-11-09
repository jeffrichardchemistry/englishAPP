import streamlit as st
import pandas as pd
import numpy as np
import time

class BackEnd:
    def __init__(self):
        self.df = BackEnd.__runData(self)
        self.words_sampleds = BackEnd.__loadCollectedWords(self)
    
    @st.cache(allow_output_mutation=True)
    def __runData(self):
        path = 'data/db.csv'
        df = pd.read_csv(path)
        
        return df
    
    def __loadCollectedWords(self):
        path = 'sorted_words.dat'
        f = open(path, 'r')
        word_list = f.read()
        f.close()
        word_list = [i for i in word_list.splitlines()]
        return word_list

    def getDF_of_collecteds(self):
        get_indexes = np.array([np.array(self.df.loc[self.df["Palavra"]==word].index) for word in self.words_sampleds]).ravel()
        df_of_sampleds = self.df.iloc[get_indexes, :]
        return df_of_sampleds
        
    def sampleWords(self, df, n_words):
        df_sorted = df.sample(n_words)
        return df_sorted
    
    def storeWords(self, words_list):
        for i in words_list:
            f = open('sorted_words.dat', 'a')
            f.write('{}\n'.format(i))
            f.close()
            
    def clearWords(self):
        f = open('sorted_words.dat', 'w')
        f.write('')
        f.close()
    
    #def dropWords(self):
    #    get_indexes = np.array(BackEnd.getDF_of_collecteds(self).index)
    #    print('indexes to drop\n', get_indexes)
    #    get_df_new = self.df.drop(get_indexes, axis=0, inplace=False)
    #    st.write(get_df_new)
        

class FrontEnd(BackEnd):
    def __init__(self):
        super().__init__()
        FrontEnd.main(self)
    
    def main(self):
        nav = FrontEnd.navbar(self)
        if nav == "APP":
            col1, col2, col3 = st.columns(3)
            n_words = col2.text_input("Type the number of words to sample.", 5)
            run = col2.button('Run')
            
            if run:                
                df_sorted = FrontEnd.sampleWords(self, df=self.df, n_words=int(n_words))
                st.table(df_sorted)
                list_words = df_sorted.iloc[:, 0].values
                FrontEnd.storeWords(self, list_words)
                
        
        if nav == "Collected Words":
            c1,c2,c3 = st.columns(3)
            clear = c2.button('Clear')
            if clear:
                FrontEnd.clearWords(self)
                time.sleep(0.5)
                c2.button('Refresh')                
            else:
                get_df_sorteds = FrontEnd.getDF_of_collecteds(self)
                st.table(get_df_sorteds)
                            
        
    def navbar(self):
        nav = st.sidebar.radio('Go to:', ['APP', 'Collected Words'])
        
        return nav
    

FrontEnd()