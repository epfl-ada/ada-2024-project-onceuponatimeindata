import pandas as pd
from plotly import graph_objects as go
import numpy as np
from matplotlib import pyplot as plt
from plotly import colors
from matplotlib import colormaps as cm
from utils.evaluation_utils import inflate
from models.box_office_revenue import get_compare_first_sequel_graph_plotly

def get_compare_first_sequel_graph_rating(first_vs_rest, average_rating, get_colors):

    """
    绘制首部电影与续集电影的评分对比图。
    :param first_vs_rest: 数据框，包含首部电影和续集电影的评分
    :param average_rating: 单部电影的平均评分
    :param get_colors: 获取颜色的函数
    :return: 生成的图形对象
    """
    fig_avg = go.Figure() #使用 plotly 创建一个空图形对象 fig_avg。
    x = first_vs_rest["index"] #获取首部电影和续集电影的索引。
    y1 = first_vs_rest["first"] #获取首部电影的评分。
    y2 = first_vs_rest["rest_avg"] #获取续集电影的平均评分。

    text_first = first_vs_rest.index + "<br>First movie box average rating: " + y1.astype(str) #首部电影的评分。
    text_sequel = first_vs_rest.index + "<br>Average sequel movie rating average: " + y2.astype(str) #续集电影的平均评分。

    fig_avg.add_trace(go.Scatter(x=x, y=y1, mode='markers', name=f"First movie rating",
                                 text=text_first, marker_color=get_colors("Movie"), hoverinfo="text")) #添加首部电影评分的散点图。
    fig_avg.add_trace(go.Scatter(x=x, y=y2, mode='markers', name="Average sequel movie rating",
                                 text=text_sequel, marker_color=get_colors("Sequels"), hoverinfo="text")) #添加续集电影评分的散点图。

    for i in range(len(x)):    #循环遍历首部电影和续集电影的评分。
        if y1[i] > y2[i]:
            fig_avg.add_shape(type="line", x0=x[i], x1=x[i], y0=y1[i], y1=y2[i], line=dict(color="lightcoral", width=1)) #（浅红色）添加首部电影评分高于续集电影评分的线条。
        else:
            fig_avg.add_shape(type="line", x0=x[i], x1=x[i], y0=y1[i], y1=y2[i], line=dict(color="palegreen", width=1)) #（浅红色）添加首部电影评分低于续集电影评分的线条。

    fig_avg.add_hline(y=average_rating, line_dash="dot", line_color="peru",
                      name="Average rating of a movie", annotation_text="Average rating of a movie",)# 添加单部电影的平均评分线条。

    fig_avg.add_hline(y=y2.mean(), line_dash="dot", line_color="blue",
                        name="Average rating of a sequel movie", annotation_text="Average rating of a sequel movie",)# 添加续集电影的平均评分线条。

    fig_avg.add_hline(y=y1.mean(), line_dash="dot", line_color="red",
                        name="Average rating of a first movie", annotation_text="Average rating of a first movie",)# 添加首部电影的平均评分线条。

    fig_avg.update_layout(
        title="First movie vs Average sequel movie rating",
        xaxis_title="Collection",
        yaxis_title="Movie rating",
        width=1000,
        height=600,
        legend=dict(
            yanchor="bottom",
            y=0,
            xanchor="right",
            x=1
        )# 设置图例的位置。
    )
    return fig_avg


def compare_first_sequel_ratings(movie_frame, ratings_path_list): 

    """
    比较系列电影中首部电影和续集的评分。
    :param movie_frame: 一个包含电影信息的数据库对象
    :param ratings_path_list: 包含额外评分信息的文件路径列表
    :return: 图表对象
    """

    for ratings_path in ratings_path_list: #遍历额外评分信息的文件路径列表。加载每个 CSV 文件的评分数据。将评分数据按电影 id 合并到 movie_frame.movie_df_sequel_original 数据框中。确保不会重复添加 vote_average 列。

        ratings = pd.read_csv(ratings_path)
        movie_frame.movie_df_sequel_original = pd.merge(movie_frame.movie_df_sequel_original, ratings[["id", "vote_average"]],
                                                        on="id", how="inner") if "vote_average" not in movie_frame.movie_df_sequel_original.columns \
                                                        else movie_frame.movie_df_sequel_original 


    # 计算首部电影的评分。
    ratings_first_movie = movie_frame.movie_df_sequel_original.sort_values("release_date").groupby("collection").first()[
        "vote_average"]


    # 计算续集电影的评分-首部电影的评分。
    ratings_remainder = movie_frame.movie_df_sequel_original.groupby("collection")["vote_average"].agg(
        'sum') - ratings_first_movie

    # 计算续集电影的平均评分。
    ratings_remainder_avg = ratings_remainder / (
                movie_frame.movie_df_sequel_original.groupby("collection").count()["Movie name"] - 1)

    first_vs_rest = pd.DataFrame() #创建一个数据框 first_vs_rest，包含首部电影和续集电影的评分。
    first_vs_rest["first"] = ratings_first_movie #首部电影的评分。
    first_vs_rest["rest"] = ratings_remainder #续集电影的评分。
    first_vs_rest["rest_avg"] = ratings_remainder_avg #续集电影的平均评分。
    first_vs_rest = first_vs_rest.dropna() #删除缺失值。
    first_vs_rest = first_vs_rest[first_vs_rest["first"] > 0] #首部电影评分大于 0。
    first_vs_rest = first_vs_rest[first_vs_rest["rest"] > 0] #续集电影评分大于 0。
    first_vs_rest = first_vs_rest[first_vs_rest["rest_avg"] > 0]   #续集电影平均评分大于 0。
    first_vs_rest = first_vs_rest.sort_values("first",
                                              ascending=True)  # 按首部电影的评分升序排列数据框 first_vs_rest。
    first_vs_rest['index'] = range(0, len(first_vs_rest)) #添加索引列。

    average_rating = movie_frame.movie_df_sequel_original["vote_average"].mean() #计算单部电影的平均评分。

    fig_avg = get_compare_first_sequel_graph_rating(first_vs_rest, average_rating, movie_frame.get_color_discrete) #绘制首部电影与续集电影的评分对比图。


    return fig_avg



def plot_ratings_vs_revenue(ratings_df, box_office_revenue, collection_size):
    """
    Plot the budget vs box office revenue
    :param budget_df: dataframe with the budget for each collection
    :param box_office_revenue: dataframe with the box office revenue for each collection
    :param collection_size: number of movies in each collection
    :return: figure containing the plot
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ratings_df,
        y=box_office_revenue,
        mode='markers',
        marker=dict(
            size=collection_size * 3,
            color=np.log(box_office_revenue),
            colorscale='sunset',
        ),
        text = ratings_df.index,
        hoverinfo='text',
        showlegend=False,
    ))


    fig.add_trace(go.Scatter(
    x=[3, 8.1],  # 假设评分范围是 0 到 10
    y=[1e6, 1e10],  # 假设低评分对应低票房，高评分对应高票房
    mode='lines+text',
    text='Higher ratings -> Higher revenue',
    line=dict(color='gray', width=2, dash='dash'),
    textposition="top left",
    showlegend=True,
    name="Hypothetical Line"
))



    fig.update_layout(
        xaxis_title="Rating",
        yaxis_title="Box office revenue",
        title="Rating vs Box office revenue",
        yaxis_type="log",
        yaxis=dict(
            range = [5.5, 10.5],
            tickvals=[1e6, 1e7, 1e8, 1e9, 1e10],
            ticktext=["1M", "10M", "100M", "1B", "10B"]
        ),
        xaxis=dict(
            range=[3, 10],  # 线性范围，从 0 到 10
            tickvals=list(range(3, 10)),  # 刻度值为 0 到 10 的整数
            ticktext=[str(i) for i in range(3, 10)],  # 刻度显示为对应的整数评分
            title="Average Rating"  # 坐标轴标题
        )

    )

    return fig

def get_ratings_vs_revenue(movie_frames, sequels_extended_file_list):
    """
    plot the budget vs box office revenue
    :param movie_frames: The MovieFrame class with the movies
    :param sequels_extended_file_list: list of files with additional budget information
    :return: the figure with the plot
    """

    collection_size = movie_frames.movie_df_sequel_original.groupby("collection").count()["Movie name"]

    # total inflation adjusted box office revenue for each collection

    box_office_revenue = movie_frames.movie_df_sequel_original.groupby("collection")["Movie box office revenue inflation adj"].agg(
        'sum')

    movie_df_sequel_original_all = None
    for sequels_extended_file in sequels_extended_file_list:
        sequels_extended = pd.read_csv(sequels_extended_file)  # dataframe with additional budget information
        movie_df_sequel_original = pd.merge(movie_frames.movie_df_sequel_original, sequels_extended[["id", "vote_average"]],
                                            on="id", how="inner")  if "vote_average" not in movie_frames.movie_df_sequel_original.columns \
                                                                   else movie_frames.movie_df_sequel_original
        if movie_df_sequel_original_all is None:
            movie_df_sequel_original_all = movie_df_sequel_original
        else:
            movie_df_sequel_original_all = pd.concat([movie_df_sequel_original_all, movie_df_sequel_original])


    # # total budget for each collection

    # movie_df_sequel_original_all["budget inflation adj"] = movie_df_sequel_original_all.swifter.apply(
    #     lambda x: inflate(x["budget"], x["release_date"]), axis=1)
    # budget_df = movie_df_sequel_original_all.groupby("collection")["budget inflation adj"].agg('sum')
    ratings_df = movie_df_sequel_original_all.groupby("collection")["vote_average"].agg('mean')
    # #remove where bugdet is nan
    # budget_df = budget_df.dropna()
    ratings_df = ratings_df.dropna()
    box_office_revenue = box_office_revenue.loc[ratings_df.index]
    collection_size = collection_size.loc[ratings_df.index]

    fig = plot_ratings_vs_revenue(ratings_df, box_office_revenue, collection_size)

    return fig


# def compare_revenue_sequel_ratings(movie_frame, ratings_path_list): 
#     """
#     compare the box office revenue of the first movie and the sequel movie
#     :param movie_frame: the database with the movies
#     :param ratings_path_list: list of files with additional ratings information
#     :return: the figure with the plot
#     """
#     """
#     比较系列电影中首部电影和续集的评分。
#     :param movie_frame: 一个包含电影信息的数据库对象
#     :param ratings_path_list: 包含额外评分信息的文件路径列表
#     :return: 图表对象
#     """

#     for ratings_path in ratings_path_list: #遍历额外评分信息的文件路径列表。加载每个 CSV 文件的评分数据。将评分数据按电影 id 合并到 movie_frame.movie_df_sequel_original 数据框中。确保不会重复添加 vote_average 列。

#         ratings = pd.read_csv(ratings_path)
#         movie_frame.movie_df_sequel_original = pd.merge(movie_frame.movie_df_sequel_original, ratings[["id", "vote_average"]],
#                                                         on="id", how="inner") if "vote_average" not in movie_frame.movie_df_sequel_original.columns \
#                                                         else movie_frame.movie_df_sequel_original 


#     # 计算首部电影的评分。
#     ratings_first_movie = movie_frame.movie_df_sequel_original.sort_values("release_date").groupby("collection").first()["vote_average"]
#     revenue_first_movie = movie_frame.movie_df_sequel_original.sort_values("release_date").groupby("collection").first()["revenue"]


#     # 计算续集电影的评分-首部电影的评分。
#     ratings_remainder = movie_frame.movie_df_sequel_original.groupby("collection")["vote_average"].agg('sum') - ratings_first_movie
#     revenue_remainder = movie_frame.movie_df_sequel_original.groupby("collection")["revenue"].agg('sum') - revenue_first_movie

#     # 计算续集电影的平均评分。
#     ratings_remainder_avg = ratings_remainder / (movie_frame.movie_df_sequel_original.groupby("collection").count()["Movie name"] - 1)
#     revenue_remainder_avg = revenue_remainder / (movie_frame.movie_df_sequel_original.groupby("collection").count()["Movie name"] - 1)

#     first_vs_rest = pd.DataFrame() #创建一个数据框 first_vs_rest，包含首部电影和续集电影的评分。
#     first_vs_rest["first"] = ratings_first_movie #首部电影的评分。
#     first_vs_rest["rest"] = ratings_remainder #续集电影的评分。
#     first_vs_rest["rest_avg"] = ratings_remainder_avg #续集电影的平均评分。
#     first_vs_rest = first_vs_rest.dropna() #删除缺失值。
#     first_vs_rest = first_vs_rest[first_vs_rest["first"] > 0] #首部电影评分大于 0。
#     first_vs_rest = first_vs_rest[first_vs_rest["rest"] > 0] #续集电影评分大于 0。
#     first_vs_rest = first_vs_rest[first_vs_rest["rest_avg"] > 0]   #续集电影平均评分大于 0。
#     first_vs_rest = first_vs_rest.sort_values("first",ascending=True)  # 按首部电影的评分升序排列数据框 first_vs_rest。
#     first_vs_rest['index'] = range(0, len(first_vs_rest)) #添加索引列。

#     average_rating = movie_frame.movie_df_sequel_original["vote_average"].mean() #计算单部电影的平均评分。

#     fig_avg = get_compare_first_sequel_graph_rating(first_vs_rest, average_rating, movie_frame.get_color_discrete) #绘制首部电影与续集电影的评分对比图。

    
#     revenue_vs_rating = pd.DataFrame() #创建一个数据框 revenue_vs_rating，包含首部电影和续集电影的评分和票房。
#     revenue_vs_rating["first"] = revenue_first_movie #首部电影的票房。
#     revenue_vs_rating["rest"] = revenue_remainder #续集电影的票房。
#     revenue_vs_rating["rest_avg"] = revenue_remainder_avg #续集电影的平均票房。
#     revenue_vs_rating["first_rating"] = ratings_first_movie #首部电影的评分。
#     revenue_vs_rating["rest_rating"] = ratings_remainder #续集电影的评分。
#     revenue_vs_rating["rest_avg_rating"] = ratings_remainder_avg #续集电影的平均评分。
#     revenue_vs_rating = revenue_vs_rating.dropna() #删除缺失值。
#     revenue_vs_rating = revenue_vs_rating[revenue_vs_rating["first"] > 0] #首部电影票房大于 0。
#     revenue_vs_rating = revenue_vs_rating[revenue_vs_rating["rest"] > 0] #续集电影票房大于 0。
#     revenue_vs_rating = revenue_vs_rating[revenue_vs_rating["rest_avg"] > 0]   #续集电影平均票房大于 0。
#     revenue_vs_rating = revenue_vs_rating.sort_values("first",ascending=True)  # 按首部电影票房升序排列数据框 revenue_vs_rating。
#     revenue_vs_rating['index'] = range(0, len(revenue_vs_rating)) #添加索引列。
    
#     average_revenue = movie_frame.movie_df_sequel_original["revenue"].mean() #计算单部电影的平均票房。
#     fig_revenue = get_compare_first_sequel_graph_plotly(revenue_vs_rating, average_revenue, movie_frame.get_color_discrete) #绘制首部电影与续集电影的票房对比图。


#     return fig_revenue

# def get_compare_first_sequel_graph_rating(first_vs_rest, average_rating, get_colors):
  
#     """
#     绘制首部电影与续集电影的评分对比图。
#     :param first_vs_rest: 数据框，包含首部电影和续集电影的评分
#     :param average_rating: 单部电影的平均评分
#     :param get_colors: 获取颜色的函数
#     :return: 生成的图形对象
#     """
#     fig_avg = go.Figure() #使用 plotly 创建一个空图形对象 fig_avg。
#     x = first_vs_rest["index"] #获取首部电影和续集电影的索引。
#     y1 = first_vs_rest["first"] #获取首部电影的评分。
#     y2 = first_vs_rest["rest_avg"] #获取续集电影的平均评分。

#     text_first = first_vs_rest.index + "<br>First movie box average rating: " + y1.astype(str) #首部电影的评分。
#     text_sequel = first_vs_rest.index + "<br>Average sequel movie rating average: " + y2.astype(str) #续集电影的平均评分。

#     fig_avg.add_trace(go.Scatter(x=x, y=y1, mode='markers', name=f"First movie rating",
#                                  text=text_first, marker_color=get_colors("Movie"), hoverinfo="text")) #添加首部电影评分的散点图。
#     fig_avg.add_trace(go.Scatter(x=x, y=y2, mode='markers', name="Average sequel movie rating",
#                                  text=text_sequel, marker_color=get_colors("Sequels"), hoverinfo="text")) #添加续集电影评分的散点图。

#     for i in range(len(x)):    #循环遍历首部电影和续集电影的评分。
#         if y1[i] > y2[i]:
#             fig_avg.add_shape(type="line", x0=x[i], x1=x[i], y0=y1[i], y1=y2[i], line=dict(color="lightcoral", width=1)) #（浅红色）添加首部电影评分高于续集电影评分的线条。
#         else:
#             fig_avg.add_shape(type="line", x0=x[i], x1=x[i], y0=y1[i], y1=y2[i], line=dict(color="palegreen", width=1)) #（浅红色）添加首部电影评分低于续集电影评分的线条。

#     fig_avg.add_hline(y=average_rating, line_dash="dot", line_color="peru",
#                       name="Average rating of a movie", annotation_text="Average rating of a movie",)# 添加单部电影的平均评分线条。

#     fig_avg.add_hline(y=y2.mean(), line_dash="dot", line_color="blue",
#                         name="Average rating of a sequel movie", annotation_text="Average rating of a sequel movie",)# 添加续集电影的平均评分线条。

#     fig_avg.add_hline(y=y1.mean(), line_dash="dot", line_color="red",
#                         name="Average rating of a first movie", annotation_text="Average rating of a first movie",)# 添加首部电影的平均评分线条。

#     fig_avg.update_layout(
#         title="First movie vs Average sequel movie rating",
#         xaxis_title="Collection",
#         yaxis_title="Movie rating",
#         width=1000,
#         height=600,
#         legend=dict(
#             yanchor="bottom",
#             y=0,
#             xanchor="right",
#             x=1
#         )# 设置图例的位置。
#     )
#     return fig_avg
