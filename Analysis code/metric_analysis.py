#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 11:57:33 2023

@author: sean
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
pio.renderers.default='browser'
data = pd.read_csv('article_metric_data_analysis.csv')

data_cat = data
data_cols = data_cat.columns.values.tolist()
data_cat['topic'] = data.topic.astype('category')
data_cat['entity_interaction_type'] = data.entity_interaction_type.astype('category')
data_cat['common_description'] = data.common_description.astype('category')

data_cat_top = data_cat.iloc[:,0:2]
data_cat_top_uni = data_cat_top.drop_duplicates()
data_cat_sub = data_cat.iloc[:,0:3]
data_cat_sub_uni = data_cat_sub.drop_duplicates()

topic_counts = data_cat_top_uni['topic'].value_counts()
entity_counts = data_cat_sub_uni['entity_interaction_type'].value_counts()
common_counts = data_cat['common_description'].value_counts()
topic_prop = data_cat_top_uni['topic'].value_counts(normalize=True)
entity_prop = data_cat_sub_uni['entity_interaction_type'].value_counts(normalize=True)
common_prop = data_cat['common_description'].value_counts(normalize=True)

topic_df = topic_counts.to_frame().reset_index()
entity_df = entity_counts.to_frame().reset_index()
common_df = common_counts.to_frame().reset_index()

colours = px.colors.qualitative.Pastel

topic_fig = go.Figure(data=[go.Bar(x=topic_df['index'], y=topic_df['topic'], marker_color=colours)])
topic_fig.update_layout(yaxis=dict(
                             title='Frequency',
                             titlefont_size=18,
                             tickfont_size=16),
                         xaxis=dict(
                             title='Topic',
                             titlefont_size=18,
                             tickfont_size=16))
topic_fig.show()
entity_fig = go.Figure(data=[go.Bar(x=entity_df['index'], y=entity_df['entity_interaction_type'], marker_color=colours)])
entity_fig.update_layout(yaxis=dict(
                             title='Frequency',
                             titlefont_size=18,
                             tickfont_size=16),
                         xaxis=dict(
                             title='Entity interaction type',
                             titlefont_size=18,
                             tickfont_size=16))
entity_fig.show()
common_fig = go.Figure(data=[go.Bar(x=common_df['index'].iloc[0:8], y=common_df['common_description'].iloc[0:8], marker_color=colours)])
common_fig.update_layout(#title=dict(
                         #    text='Common metric description frequency',
                         #    font_size=20),
                         yaxis=dict(
                             title='Frequency',
                             titlefont_size=18,
                             tickfont_size=16),
                         xaxis=dict(
                             title='Common metric description',
                             titlefont_size=18,
                             tickfont_size=16))
common_fig.show()

three_col = data_cat.value_counts(['topic','entity_interaction_type','common_description'])
three_col = three_col.reset_index()
two_col = data_cat.value_counts(['entity_interaction_type','common_description'])
two_col_dict = two_col.to_dict()

data_cat['real_world_category'] = data_cat.real_world_category.astype('category')
dat_cat_sub_rw = data_cat.iloc[:,[0,5]]
data_cat_sub_rw_uni = dat_cat_sub_rw.drop_duplicates()
df_rw_articles_uni = data_cat_sub_rw_uni.groupby('real_world_category')['article'].apply(list)


df_rw_desc = data_cat.groupby('real_world_category')['common_description'].apply(list)
article_count_list = list()
met_count_list = list()
uni_met_count_list = list()
for i in range(len(df_rw_desc)):
    article_count_list.append(len(df_rw_articles_uni[i]))
    met_count_list.append(len(df_rw_desc[i]))
    uni_met_tmp = pd.DataFrame(df_rw_desc[i])
    uni_met_tmp.drop_duplicates(inplace=True)
    uni_met_count_list.append(len(uni_met_tmp))

rw_cats = df_rw_desc.index.values.tolist()
rw_cat_sum_df = pd.DataFrame([rw_cats,met_count_list,article_count_list,uni_met_count_list]).transpose()
rw_cat_sum_df.columns = ['Real world category','Frequency of occurrence','Unique article frequency', 'Unique metric frequency']
rw_cat_sum_df.to_csv('correlates_and_metrics_summary_table.csv', sep=',', index=False)


df_collate = data_cat.groupby('common_description')['real_world_correlate'].apply(list)
df_collate_dict = df_collate.to_dict()

output_dict = dict()
for i in df_collate_dict.keys():
    output_dict[i] = '; '.join(map(str, df_collate_dict[i]))

output_df = pd.DataFrame.from_dict(output_dict, orient='index').reset_index()
output_df.columns = ['Common metric name','Real world correlate']
output_df.to_csv('metrics_and_correlates.csv', sep=',', index=False)

df_rw_desc = data_cat.groupby('real_world_category')['common_description'].apply(list)
df_rw_desc_dict = df_rw_desc.to_dict()

df_rw_corr = data_cat.groupby('real_world_category')['real_world_correlate'].apply(list)
df_rw_corr_dict = df_rw_corr.to_dict()

rw_desc_out_dict = dict()
for i in df_rw_desc_dict.keys():
    rw_desc_out_dict[i] = ' \n'.join(map(str, df_rw_desc_dict[i]))
    
rw_corr_out_dict = dict()
for i in df_rw_corr_dict.keys():
    rw_corr_out_dict[i] = ' \n'.join(map(str, df_rw_corr_dict[i]))

rw_desc_out_df = pd.DataFrame.from_dict(rw_desc_out_dict, orient='index').reset_index()
rw_corr_out_df = pd.DataFrame.from_dict(rw_corr_out_dict, orient='index').reset_index()

rw_desc_out_df['corr'] = rw_corr_out_df.iloc[:,1]
rw_desc_out_df.columns = ['Real world category', 'Common metric name', 'Real world correlate']
rw_desc_out_df.to_csv('correlates_and_metrics.csv', sep=',', index=False)

rw_out_df = pd.DataFrame([rw_desc_out_df.iloc[:,0:2],rw_corr_out_df.iloc[:,1]]).transpose()

rw_output_dict = dict()
for i in df_rw_desc_dict.keys():
    rw_output_dict[i] = ' ~ '.join(map(str, [df_rw_desc_dict[i], df_rw_corr_dict[i]]))

rw_output_dict = dict()
for i in df_rw_desc_dict.keys():
    tmp_list = list()
    for j in range(len(df_rw_desc_dict[i])):
        tmp_list.append(' ~ '.join(map(str, [df_rw_desc_dict[i][j], df_rw_corr_dict[i][j]])))
    rw_output_dict[i] = tmp_list

rw_final_output_dict = dict()
for i in rw_output_dict.keys():
    rw_final_output_dict[i] = ' \n'.join(map(str, rw_output_dict[i]))