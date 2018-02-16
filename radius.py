
import numpy as np, pandas as pd

df=pd.read_json('data_analysis.json')

# Q 1 Fill Rate: For each field, how many records have a value.
for key in df.keys():
    print key, df.dropna(subset=[key]).shape[0]


# Q2  True-Valued Fill Rate

mapping = {'' : np.nan,' ' :np.nan,'none' : np.nan,'null': np.nan} #change values of '',' ','none' and 'null' to NAN
for key in df.keys():
    df[key]=df[key].map(lambda x: mapping.get(x,x)).values

df['zip']=df.loc[:,'zip'].map(lambda x: np.nan if ((x==np.nan) | (not ((len(x.__str__())==5) & x.__str__().isdigit()))) else x).values
df['state']=df.loc[:,'state'].map(lambda x: np.nan if ((x==np.nan) | (not((len(x.__str__())==2) & x.__str__().isalpha()))) else x)
df['phone']=df.loc[:,'phone'].map(lambda x: np.nan if ((x==np.nan) | (not(sum(c.isdigit() for c in x.__str__())==10))) else x)
df['category_code']=df.loc[:,'category_code'].map(lambda x: np.nan if ((x==np.nan) | (not(2<=len(x.__str__().rstrip('0'))<=6))) else x)

for key in ['address','city','name','headcount','revenue', 'time_in_business']:
    df[key]=df.loc[:,key].map(lambda x: np.nan if ((x==np.nan) | (not((len(unicode(x)) > 1)))) else x)

for key in df.keys():
    print ' | ',key,' | ', df[key].dropna().shape[0],' | '


#Q3
df.nunique()



#plots

#fig 1
df.groupby(['revenue','headcount']).size().unstack().plot(kind='barh',stacked=True,logx=True)

#fig 2
ii=df.groupby(['state']).size().argsort().values[::-1]
df.groupby(['state','headcount']).size().unstack().iloc[ii[:-2]].plot(kind='bar',stacked=True,logy=True)

#fig 3
ii=df.groupby(['category_code','revenue']).size().unstack().sum(1).argsort()[::-1][:5].values
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
df.groupby(['category_code','revenue']).size().unstack().iloc[ii].plot(ax=ax,kind='bar',stacked=True,rot=45)
ax.set_xticklabels([' Elem. & Sec. Schools ','Offices of Lawyers','Real Estate Agents','Professional, Scient & Tech Services','Wholesale Trade'],rotation=10,fontsize='small')
