def weeks_to_days(df):
    #to convert a df that has a column named Week
    #containing the day each week starts to one with
    #a column called date, and a row for each day
    #with all the other entries on this row being
    # copies of the one from week
    import pandas as pd #do subroutines need this?
    df['date'] = pd.to_datetime(df['Week'], format='%d-%m-%Y')
    df = df.set_index('date').resample('D').ffill().reset_index()
    df = df.drop(columns=['Week'])
    return df

def fancy_graph1(df_Eng,df_Wal,df_NI,df_Sco,col_name,title_str):
    #a lot of the graphs we want to make have a lot of similarities
    #i.e. are a column of a df against time, and show england on a
    # seperate axis to the other members of the union (because it has
    # far more people)

    import pandas as pd #do subroutines need this?
    import matplotlib.pyplot as plt
    import datetime as dt

    # plot the data
    fig = plt.figure()
    ax1 = plt.subplot(211)
    plt.scatter(df_Eng.Reporting_date,
                df_Eng.loc[:,col_name], label='England')
    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        top=False,  # ticks along the top edge are off
        labelbottom=False)
    plt.title(label=title_str)
    key_dates = pd.to_datetime(['2020-03-26', '2020-05-10'], format='%Y-%m-%d')
    for xc in key_dates:
        plt.axvline(x=xc)
    start_n_end   = [dt.date(2020, 3, 1), dt.date.today()]
    ax1.set_xlim(start_n_end)
    ax1.legend()

    ax2 = plt.subplot(212)
    plt.scatter(df_Sco.Reporting_date, df_Sco.loc[:, col_name], label='Scotland')
    plt.scatter(df_NI.Reporting_date,   df_NI.loc[:, col_name], label='Northern Ireland')
    plt.scatter(df_Wal.Reporting_date, df_Wal.loc[:, col_name], label='Wales')
    for xc in key_dates:
        plt.axvline(x=xc)
    plt.xticks(rotation=90)
    ax2.set_xlim(start_n_end)
    ax2.legend()
    plt.show()
    return

def fancy_graph2(df_UK,df_Eng,df_Wal,df_NI,df_Sco,col_name,title_str):
    #where we are dividing by expected deaths we don't need to
    # plot england on a seperate axis this repeats a lot of the
    # code for fancy graph 1 but plots the UK on top and each
    # member of the union together on the bootom

    import pandas as pd #do subroutines need this?
    import matplotlib.pyplot as plt
    import datetime as dt

    # plot the data
    fig = plt.figure()
    ax1 = plt.subplot(211)
    plt.scatter(df_UK.Reporting_date, df_UK.loc[:,col_name],label='UK')
    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        top=False,  # ticks along the top edge are off
        labelbottom=False)
    plt.title(label=title_str)
    key_dates = pd.to_datetime(['2020-03-26', '2020-05-10'], format='%Y-%m-%d')
    for xc in key_dates:
        plt.axvline(x=xc)
    start_n_end   = [dt.date(2020, 3, 1), dt.date.today()]
    ax1.set_xlim(start_n_end)
    ax1.legend()

    ax2 = plt.subplot(212)
    plt.scatter(df_Eng.Reporting_date, df_Eng.loc[:, col_name], label='England')
    plt.scatter(df_Wal.Reporting_date, df_Wal.loc[:, col_name], label='Wales')
    plt.scatter(df_NI.Reporting_date,  df_NI.loc[:,  col_name], label='Northern Ireland')
    plt.scatter(df_Sco.Reporting_date, df_Sco.loc[:, col_name], label='Scotland')
    plt.xticks(rotation=90)

    for xc in key_dates:
        plt.axvline(x=xc)
    ax2.set_xlim(start_n_end)
    ax2.legend()
    plt.show()
    return


def main():
    import pandas as pd
    import matplotlib.pyplot as plt
    import xlrd
    import os
    import glob
    from pathlib import Path

    #get the lates file from .gov
    extension = 'csv'
    file_list = glob.glob('deaths*.{}'.format(extension))
    s_list = sorted([fname for fname in file_list])
    File1  =s_list[-1]

    #File1='deaths_latest_2020-06-25.csv'
    Deaths_Prov=pd.read_csv(File1)

    #replace spaces with underscores in column names
    Deaths_Prov.columns = Deaths_Prov.columns.str.replace('\s+', '_')

    #delete unwanted columns
    del Deaths_Prov['Area_code']
    del Deaths_Prov['Area_type']

    # make the dates into dates rather than strings
    #put everything in date order
    Deaths_Prov['Reporting_date'] = pd.to_datetime(Deaths_Prov['Reporting_date'], format='%Y-%m-%d')
    Deaths_Prov                   = Deaths_Prov.sort_values('Reporting_date')

    #seperate the data
    Deaths_Eng=Deaths_Prov.query('`Area_name`=="England"')
    Deaths_Sco=Deaths_Prov.query('`Area_name`=="Scotland"')
    Deaths_NI =Deaths_Prov.query('`Area_name`=="Northern Ireland"')
    Deaths_Wal=Deaths_Prov.query('`Area_name`=="Wales"')
    Deaths_UK =Deaths_Prov.query('`Area_name`=="United Kingdom"')

    #plot the data
    column_name ='Daily_change_in_deaths'
    title_str   ='Daily Coronavirus Deaths \n as reported at coronavirus.data.gov.uk '
    fancy_graph1(Deaths_Eng, Deaths_Wal, Deaths_NI, Deaths_Sco,column_name,title_str)

    print("A lot of the noise comes from the fact that fewer"
          " deaths are reported on weekends. As a result it "
          "is useful to view the data via a 7 day average." )

    print("Notably for our data, the surrounding 7 days will "
          "be used, so that comparisons involving dates can still"
          " be made")

    Deaths_UK['Rolling'] = Deaths_UK.Daily_change_in_deaths.rolling(7, center=True).mean()
    Deaths_Eng['Rolling'] = Deaths_Eng.Daily_change_in_deaths.rolling(7, center=True).mean()
    Deaths_Sco['Rolling'] = Deaths_Sco.Daily_change_in_deaths.rolling(7, center=True).mean()
    Deaths_NI['Rolling'] = Deaths_NI.Daily_change_in_deaths.rolling(7, center=True).mean()
    Deaths_Wal['Rolling'] = Deaths_Wal.Daily_change_in_deaths.rolling(7, center=True).mean()

    #plot the data
    column_name ='Rolling'
    title_str   ='Rolling average of Daily Coronavirus Deaths \n as reported at coronavirus.data.gov.uk '
    fancy_graph1(Deaths_Eng, Deaths_Wal, Deaths_NI, Deaths_Sco,column_name,title_str)

    #read in historic death data
    Xls=pd.ExcelFile('Death_registrations2.xlsx')
    Hist_UK      = pd.read_excel(Xls, 0)
    Hist_Eng_Wal = pd.read_excel(Xls, 1)
    Hist_Sco     = pd.read_excel(Xls, 2)
    Hist_NI      = pd.read_excel(Xls, 3)

    #col names with spaces cause problems
    Hist_UK.columns         = Hist_UK.columns.str.replace('\s+', '_')
    Hist_Eng_Wal.columns    = Hist_Eng_Wal.columns.str.replace('\s+', '_')
    Hist_Sco.columns        = Hist_Sco.columns.str.replace('\s+', '_')
    Hist_NI.columns         = Hist_NI.columns.str.replace('\s+', '_')

    #the columns we want are in every case 2 and 9
    #it seems that when pandas imports the df they can get moved around
    Hist_UK      = Hist_UK.loc[:,      ['Week', 'Ave']]
    Hist_Eng_Wal = Hist_Eng_Wal.loc[:, ['Week', 'Ave']]
    Hist_Sco     = Hist_Sco.loc[:,     ['Week', 'Ave']]
    Hist_NI      = Hist_NI.loc[:,      ['Week', 'Ave']]

    Hist_UK      = weeks_to_days(Hist_UK)
    Hist_Eng_Wal = weeks_to_days(Hist_Eng_Wal)
    Hist_Sco     = weeks_to_days(Hist_Sco)
    Hist_NI      = weeks_to_days(Hist_NI)

    # convert weekly deaths to estimated daily
    Hist_UK.Ave      = Hist_UK.Ave / 7
    Hist_Eng_Wal.Ave = Hist_Eng_Wal.Ave / 7
    Hist_Sco.Ave     = Hist_Sco.Ave / 7
    Hist_NI.Ave      = Hist_NI.Ave / 7

    #split Eng_Wal_Hist
    Eng_pop      =  67852951
    Wal_pop      =   3063456
    Eng_Wal_pop  =  Eng_pop+Wal_pop

    Hist_Eng     = Hist_Eng_Wal.copy()
    Hist_Wal     = Hist_Eng_Wal.copy()
    Hist_Eng.Ave = Hist_Eng.Ave * (Eng_pop / Eng_Wal_pop)
    Hist_Wal.Ave = Hist_Wal.Ave * (Wal_pop / Eng_Wal_pop)

    #merge into bigger dfs
    Hist_UK      = pd.merge(Hist_UK, Deaths_UK, left_on='date', right_on='Reporting_date')
    Hist_Eng     = pd.merge(Hist_Eng, Deaths_Eng, left_on='date', right_on='Reporting_date')
    Hist_Wal     = pd.merge(Hist_Wal, Deaths_Wal, left_on='date', right_on='Reporting_date')
    Hist_Sco     = pd.merge(Hist_Sco, Deaths_Sco, left_on='date', right_on='Reporting_date')
    Hist_NI      = pd.merge(Hist_NI, Deaths_NI, left_on='date', right_on='Reporting_date')

    'i wanted graphs showing deaths against expected deaths'
    '''
    fig, ax = plt.subplots()
    for col in ['Ave', 'Daily_change_in_deaths']:
        ax.scatter(Hist_UK.date, Hist_UK[col], label=col)
        # or
         #Hist_UK.scatter(x='date', y=col, label=col, ax=ax)
    plt.show()

    fig, ax1 = plt.subplots()
    for col in ['Ave', 'Daily_change_in_deaths']:
        ax1.scatter(Hist_Eng.date, Hist_Eng[col], label=col)
        # or
        #Hist_Eng.scatter(x='date', y=col, label=col, ax=ax)
    plt.show()

    ax2 = plt.subplots()
    for col in ['Ave', 'Daily_change_in_deaths']:
        ax2.scatter(Hist_Wal.date, Hist_Wal[col], label=col)
        # or
         #Hist_Wal.scatter(x='date', y=col, label=col, ax=ax)
    plt.show()
    '''

    'ratio between expected deaths and CV12 deaths'
    Hist_UK['Death_ratio']  = Hist_UK.Daily_change_in_deaths/Hist_UK.Ave
    Hist_Eng['Death_ratio'] = Hist_Eng.Daily_change_in_deaths/Hist_Eng.Ave
    Hist_Wal['Death_ratio'] = Hist_Wal.Daily_change_in_deaths/Hist_Wal.Ave
    Hist_Sco['Death_ratio'] = Hist_Sco.Daily_change_in_deaths/Hist_Sco.Ave
    Hist_NI['Death_ratio']  = Hist_NI.Daily_change_in_deaths/Hist_NI.Ave

    # plot the data
    column_name = 'Death_ratio'
    title_str = 'ratio average of Daily Coronavirus Deaths \n as reported at coronavirus.data.gov.uk '
    fancy_graph2(Hist_UK,Hist_Eng, Hist_Wal, Hist_NI, Hist_Sco, column_name, title_str)

    'ratio between expected deaths and 7 day rolling average of CV12 deaths'
    Hist_UK['Rolling_Death_ratio']  = Hist_UK.Rolling/Hist_UK.Ave
    Hist_Eng['Rolling_Death_ratio'] = Hist_Eng.Rolling/Hist_Eng.Ave
    Hist_Wal['Rolling_Death_ratio'] = Hist_Wal.Rolling/Hist_Wal.Ave
    Hist_Sco['Rolling_Death_ratio'] = Hist_Sco.Rolling/Hist_Sco.Ave
    Hist_NI['Rolling_Death_ratio']  = Hist_NI.Rolling/Hist_NI.Ave

    # plot the data
    column_name = 'Rolling_Death_ratio'
    title_str = 'ratio of rolling Coronavirus Deaths \n as reported at coronavirus.data.gov.uk '
    fancy_graph2(Hist_UK,Hist_Eng, Hist_Wal, Hist_NI, Hist_Sco, column_name, title_str)
    return 0
