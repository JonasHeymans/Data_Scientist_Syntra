import random

import pandas as pd
import numpy as np
from random import shuffle

def generate_numeric_df(num_rows: int, cols:str, index_start:int=0, seed:int=101):
    cols_lst = [c for c in cols]
    np.random.seed(seed)
    return pd.DataFrame({col: [np.random.randn() for _ in range(num_rows)] for col in cols_lst
},  index = range(index_start, index_start + num_rows))


def get_example_cat_dfs(shuff=True):
    students = ['Jana', 'Sofie', 'Maaike', 'Dirk', 'Annabel']
    df1 = pd.DataFrame({'student': students,
                         'werkgever':['Delhaize', 'Google', 'Delhaize', 'LG', 'Delhaize']})

    if shuff:
        shuffle(students)

    df2 = pd.DataFrame({'student': students,
                  'jaar_opleiding': [2012, 2025, 2013, 2022, 2019]})

    df3 = pd.DataFrame({'werkgever':['Delhaize', 'Google', 'LG'],
                        'land hoofdzetel': ['Belgie', 'VS', 'Zuid-Korea'],
                        },

                       )

    df4 = pd.DataFrame({'klant': students,
                        'kostprijs': [998, 663, 998, 0, 898],
                         },

                    )

    df5 = pd.DataFrame({
        'student': ['Jana', 'Sofie', 'Maaike', 'Dirk', 'Annabel', 'Sofie'],
        'module': ['1.Python Basics', 'Eindexamen: Data Science', '1.Python Basics', '2.SQL Essentials', '3.Web Scraping',
                   '2.SQL Essentials'],
        'resultaat': [14, 18, 12, 16, 15, 19],
        'behaald': [True, True, True, True, True, True],
        'jaar': [2012, 2025, 2012, 2014, 2019, 2014],

    })

    df6 = pd.DataFrame({
        'student': [
            'Jana', 'Sofie', 'Maaike', 'Dirk', 'Annabel',
            'Tom', 'Lena', 'Wout', 'Hanna', 'Bram'
        ],
        'jaar': [
            9999, 2025, 9999, 9999, 9999,
            2020, 2024, 2021, 2018, 2017
        ],
        'start_salaris': [
            3200, 4100, 3000, 3800, 3500,
            2900, 4000, 3600, 3300, 3400
        ],
        'sector': [
            'Retail', 'Tech', 'Retail', 'Tech', 'Retail',
            'Retail', 'Tech', 'Tech', 'Logistiek', 'Retail'
        ]
    })

    df7 = pd.DataFrame({'studentnr': range(1,10),
                        'inlogcode': [random.randint(1000, 9999) for _ in range(1,10)]
                         },

                    index=range(1,10))

    return df1, df2, df3, df4, df5, df6, df7

