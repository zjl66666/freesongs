# import streamlit as st
# import requests as rq
#
# example = 'https://zj.v.api.aa1.cn/api/qqmusic/?songName=稻香&singerName=周杰伦&pageNum=1&pageSize=3&type=qq'
#
# def main():
#     st.balloons()
#     st.sidebar.write('API:https://api.aa1.cn/doc/qq-music.html')
#     st.sidebar.write('tips:加载可能有些缓慢，请耐心等待😴')
#     st.write('音乐是最纯粹的艺术，希望它能带给你美好的一天😀')
#     # 获取请求参数
#     basic_rq = f'https://zj.v.api.aa1.cn/api/qqmusic/?type=qq&pageNum=1'
#     singerName = st.sidebar.text_input('请输入歌手名🎤(可选)')
#     if singerName:
#         basic_rq += f'&singerName={singerName}'
#     songName = st.sidebar.text_input('请输入歌曲名🎵(可选)')
#     if songName:
#         basic_rq += f'&songName={songName}'
#     song_num = st.sidebar.selectbox('选择返回歌曲的数量🎈', [i for i in range(1, 61)], index=9)
#     if song_num:
#         basic_rq += f'&pageSize={song_num}'
#     listen_num = st.sidebar.selectbox('选择需要听第几首歌🎧', [i for i in range(1, 11)], index=0)
#     # 发起请求
#     if songName or singerName:
#         song_data = rq.get(basic_rq, timeout=30).json()
#         # 展示请求结果
#         st.write(song_data['msg'] + '😉')
#         for i in range(song_num):
#             col1, col2, col3 = st.columns(3)
#             col1.write(i + 1, end='\t')
#             col2.write(song_data['list'][i]['name'], end='\t\t\t')
#             col3.write(song_data['list'][i]['singer'], end='\t\t\t')
#         song_url = song_data['list'][listen_num - 1]['url']
#         song_cover = song_data['list'][listen_num - 1]['cover']
#         # st.write(song_cover)
#         # st.write(song_url)
#         st.image(rq.get(song_cover).content)
#         st.write(song_data['list'][listen_num - 1]['name'])
#         st.audio(rq.get(song_url).content)
#         st.write('可下载歌曲保存至电脑后，导入手机的音乐软件😎')
#
#
# main()

# 下载功能,忽视缓存问题
import streamlit as st
import requests as rq

example = 'https://zj.v.api.aa1.cn/api/qqmusic/?songName=稻香&singerName=周杰伦&pageNum=1&pageSize=3&type=qq'

st.balloons()
st.sidebar.write('数据来源：夏柔API https://api.aa1.cn/doc/qq-music.html')
st.write('音乐是最纯粹的艺术，希望它能带给你美好的一天😀')
# 获取请求参数
basic_rq = f'https://zj.v.api.aa1.cn/api/qqmusic/?type=qq&pageNum=1'
singerName = st.sidebar.text_input('请输入歌手名🎤(可选)')
if singerName:
    basic_rq += f'&singerName={singerName}'
songName = st.sidebar.text_input('请输入歌曲名🎵(可选)')
if songName:
    basic_rq += f'&songName={songName}'
song_num = st.sidebar.selectbox('选择返回歌曲的数量🎈', [i for i in range(1, 61)], index=9)
if song_num:
    basic_rq += f'&pageSize={song_num}'


def main():
    song_data = get_songdata(basic_rq)
    if song_data:
        show(song_data)


@st.cache_data(ttl = 1200)
def get_songdata(basic_rq):
    # 发起请求
    if songName or singerName:
        try:
            with st.spinner('tips:加载可能有些缓慢，请耐心等待😴'):
                song_data = rq.get(basic_rq, timeout=20).json()
            return song_data
        except:
            st.error('出错了😟，请稍后再试，', icon="🚨")

# 不可使用@st.cache_data，否则无法选择listen_num，因为一开始就缓存了
def show(song_data):
    st.success(song_data['msg'] + '😉')
    try:
        listen_num = st.sidebar.selectbox('选择需要听第几首歌🎧', [i for i in range(1, song_num+1)], index=0)
        song_url = song_data['list'][listen_num - 1]['url']
        song_cover = song_data['list'][listen_num - 1]['cover']
        for i in range(song_num):
            name = song_data['list'][i]['name']
            singer = song_data['list'][i]['singer']
            col1, col2, col3 = st.columns(3)
            col1.write(i + 1)
            col2.write(name)
            col3.write(singer)
        st.image(rq.get(song_cover).content)
        st.write(song_data['list'][listen_num - 1]['name'])
        st.audio(rq.get(song_url).content)
        st.write('可下载歌曲保存至电脑后，导入手机的音乐软件😎')
        with st.expander('歌曲下载资源(复制链接到浏览器下载即可)😎'):
            for i in range(song_num):
                name = song_data['list'][i]['name']
                singer = song_data['list'][i]['singer']
                col1, col2, col3 = st.columns(3)
                col1.write(i + 1)
                col2.write(name)
                col3.write(singer)
                st.write(song_data['list'][i]['url'])
    except:
        st.error('出错了😟，请待会再试🚨')


main()
