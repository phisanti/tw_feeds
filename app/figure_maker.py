import pandas as pd
import struct
from seaborn import barplot, lineplot, clustermap
from app.tweet_analyser import word_counter, filter_correlation_matrix, word_corr
import matplotlib.pyplot as plt

def plot_wordcount(twlist, column, cutoff=10) -> bool:

    """ Generate barplot for the word counts.
    :param datapaht: datasource for the plot.
    :param cutoff: Number of words to be included in the plot.
    """
    
    # Count words
    w_count=word_counter(twlist[column])
    df = pd.DataFrame({'word_count': w_count}).reset_index()
    df['created']=twlist['created'].max()
    df=df.rename(columns={'index' : 'word'})
    df2=df.sort_values(by=['word_count'], ascending=False).head(cutoff)
    
    # Draw barplot
    fig, ax = plt.subplots(figsize=(6, 10))
    barplot(data=df2, x="word_count", 
            y="word",
            color="firebrick")
    ax.set(ylabel="",
        xlabel="Word counts")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    fig.savefig('app/dataplots/words.png')
    fig = plt.gcf()
    plt.close(fig)

    return True

def plot_timechart(twlist) -> bool:

    """" Creates a timeplot representation of the sentiment and polarity of the tweets.
    :param twlist: a pandas dataframe containing the sentiment and ploarity columns.
    """

    twlist['created_h']=twlist['created'].dt.round('H')

    summary_tw=twlist[['sentiment', 'polarity', 'created_h']].groupby('created_h').mean()
    # Add daily moving average 
    summary_tw['sentiment_ma']=summary_tw['sentiment'].rolling(24).mean()
    summary_tw['polarity_ma']=summary_tw['polarity'].rolling(24).mean()
    summary_tw=summary_tw[summary_tw.index > summary_tw.index.max() - pd.Timedelta(days=7)]

    for i in ['sentiment', 'polarity']:
        fig, ax = plt.subplots(figsize=(6, 10))
        lp=lineplot(x="created_h", y=i, data=summary_tw, ax=ax)
        lineplot(x="created_h", y=i+"_ma", data=summary_tw, ax=ax, color='red', linestyle='--')       
        lp.set_xlabel(i,fontsize=30)
        lp.set_ylabel("Time",fontsize=20)
        plt.xticks(rotation=45, ha='right')

        fig.savefig('app/dataplots/{}.png'.format(i))
    fig = plt.gcf()
    plt.close(fig)

    return True

def plot_word_correlation(twlist, column='nouns', word_list=None):

    """ Generate a heatmap for the correlation between words.
    :param twlist: a pandas dataframe containing the sentiment and ploarity columns.
    :param column: the name of the column containing the list of words.
    :param word_list: a list of words to be included in the plot.
    :return: A True value confirmin the plot has been generated.
    """
    corr_df=word_corr(twlist, target_words=word_list, column=column)
    if word_list != None:
        subset_df=filter_correlation_matrix(corr_df, word_list)
    else:
        subset_df=corr_df
    
    # plot correlation matrix
    
    cg = clustermap(subset_df, method='ward', metric='euclidean', cmap='coolwarm',
                        linewidths=0.5, cbar_pos=None, dendrogram_ratio=(.1, .1), 
                        figsize=(6, 10), row_cluster=True, col_cluster=True, annot=True, 
                        fmt=".1f", cbar_kws={"shrink": .65}, annot_kws={"size": 6},)

    # Hide the dendrogram axes and labels
    cg.ax_row_dendrogram.set_visible(False)
    cg.ax_col_dendrogram.set_visible(False)
    cg.ax_heatmap.set_xlabel('')
    cg.ax_heatmap.set_ylabel('')
    #hm= sns.heatmap(corr_df, cmap='coolwarm', annot=True)
    cg.savefig('app/dataplots/heatmap.png')
    fig = plt.gcf()
    plt.close(fig)

    return True

def check_image_size(path):
    
    with open(path, 'rb') as f:
        # read the first 24 bytes of the PNG file
        header = f.read(24)

        # unpack the width and height values from the header using the PNG format specification
        width, height = struct.unpack('>LL', header[16:24])

    print('Image size: {} x {}'.format(width, height))
    return width, height
#plot_timechart(twlist)

