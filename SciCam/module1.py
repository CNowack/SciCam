def add_rows(condition_list, n):
    for x in list(range(0, n)):
        condition_list.extend(condition_list)
    return condition_list

def get_well_coordinates(df):
    df['Row'] = df['Well'].apply(lambda x: x[0])
    df['Col'] = df['Well'].apply(lambda x: int(x[1:]))
    return df

def subset_wells(rows, columns):
    subset_list = []
    r = list(rows)
    c = list(columns)
    for x in r:
       for y in c:
          subset_list.append(f"{x}{y}")
    return subset_list

def convert_OVRFLW_columns(df, columns):
    #Pandas will automatically parse quantitative columns with 'OVRFLW' values as strings.

    #First convert whole column to floating numbers
    for col in columns:

        df[col] = pd.to_numeric(df[col], errors = 'coerce')

    #Second, replace NaN values with 'OVRFLW'
        df[col] = df[col].replace(np.nan, 'OVRFLW')

    return df

def scatter_by_group(df, x_col, y_col, group, title = None):

    #Remove OVRFLW values
    df = df[df[y_col] != 'OVRFLW']

    #Get list of conditions
    groups = list(df[group].unique())
    #create a list of lists of x and y data for each memeber of 'group'
    y_data = []
    x_data = []
    for g in groups:
        y_g = list(df[y_col][df[group]==g])
        y_data.append(y_g)
        x_g = list(df[x_col][df[group]==g])
        x_data.append(x_g)

    #Make plot
    fig, ax = plt.subplots(ncols = 1, nrows = 1, figsize=(8, 8))
    #loop graphing function over conditions
    n = 0
    colors = ['blue', 'brown', 'red', 'green', 'yellow', 'orange', 'purple']
    for g in groups:
        ax.scatter(x = x_data[n], y = y_data[n], marker = 'o', c = colors[n], alpha = 0.75, edgecolors = 'black', label = g)
        n = n + 1
    plt.legend()
    plt.xlabel(x_col)
    plt.ylabel(y_col)

    if title != None:
        ax.set_title(title)

    return fig

def bar_graph(df, y_col, group, group2 = None, title = None, colors = False):

    #remove 'OVRFLW' values
    df_ovrflw = df[df[y_col]=='OVRFLW']
    df = df[df[y_col] != 'OVRFLW']

    #Report how many OVRFLW values have been removed
    length = range(0,len(df_ovrflw))
    n = 0
    if len(df_ovrflw) > 0:
        print(str(len(df_ovrflw)) + ' OVRFLW values have been removed from the dataset.')
        print('These wells were removed:')
        for l in length:
            print(list(df_ovrflw.iloc[n]))
            n += 1

    #static variables
    bar_colors = ['blue', 'brown', 'red', 'green', 'yellow', 'orange', 'purple']
    barwidth = 0.20

    #Find average of each group in each group
    df[y_col] = df[y_col].astype('float64')
    if group2 == None:
        y_data = []
        df[y_col] = df[y_col].astype('float64')
        groups = list(df[group].unique())
        for g in groups:
            avg_value = df[y_col][df[group]==g].mean()
            y_data.append(avg_value)
    else:
        groups2 = list(df[group2].unique())
        y_data = []
        
        for g2 in groups2:
            df_g = df[df[group2]==g2]
            groups = list(df_g[group].unique())
            y_grouped_data = []
    
            for g in groups:
                avg_value = df_g[y_col][df[group]==g].mean()
                y_grouped_data.append(avg_value)

            y_data.append(y_grouped_data)

    #Make each 
    groups_str = []
    for g in groups:
        groups_str.append(str(g))
    groups = groups_str


    fig, ax = plt.subplots(figsize= ((len(groups)+2),6))

    
    if group2 != None:
        r = np.arange(len(groups))
        bar_pos =[]
        n = 0
        for g in groups2:
            r2 = r + (n*barwidth)
            r2 = list(r2)
            bar_pos.append(r2)
            fig = plt.bar(x = bar_pos[n], height = y_data[n], width = barwidth, color = bar_colors[n], edgecolor = 'white', label = g, align = 'center')
            n += 1
        plt.legend(groups2)
        ax.set_xticks((r + barwidth), groups)
    else:
        fig = plt.bar(groups, y_data, width = 0.8)


    #Add-ons
    if title != None:
        ax.set_title(title, fontweight = 'bold')
    ax.set_xlabel(group, fontweight = 'bold')
    ax.set_ylabel(y_col, fontweight = 'bold')

    return fig
def heatmap_96(df, value, title = None):

    #change OVRFLW values to float()
    #df = df.replace('OVRFLW', float(0), inplace=False)
    df = df[df[value] != 'OVRFLW']
    df[value] = df.loc[:, value].astype('float64')

    #build (almost) empty dataframe to add each column to
    nrows = list('ABCDEFGH')
    filler_data = list(range(8))
    df_plate = pd.DataFrame(data={'drop':filler_data}, index = nrows)

    #create 12 columns
    cols = list(range(1, 13))
    for c in cols:
            df_plate[c] = np.nan

    #separate df into columns
    for x in list(df['Col'].unique()):
        df_col = df[df['Col']==x]
        df_col = df_col[['Row', value]]
        #if len(df_col) > 0:
        df_rows = df_col.set_index(keys='Row', drop=True)
        df_plate[x] = df_rows[value]

    df_plate = df_plate.drop(columns='drop')

    #plot the heatmap
    fig, ax = plt.subplots(figsize=(12, 8))
    ax = sns.heatmap(df_plate, cmap='RdYlGn_r', linewidths=0.5, annot=True, square = True, linecolor = "black", fmt= 'g')
    plt.yticks(rotation = 0)

    if title != None:
        ax.set_title(title, fontweight = 'bold')
    return ax
