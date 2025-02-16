import streamlit as st
import pandas as pd
import plotly.express as px,time,os


hide_streamlit_style = """
            <style>
                /* Hide the Streamlit header and menu */
                header {visibility: hidden;}
                /* Optionally, hide the footer */
                .streamlit-footer {display: none;}
                /* Hide your specific div class, replace class name with the one you identified */
                .st-emotion-cache-uf99v8 {display: none;}
            </style>
            """

st.set_page_config(page_title='QB TRANSACTIONS ANALYSIS',page_icon=':bar_chart:',layout='wide')
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.title(':bar_chart: QB TRANSACTIONS ANALYSIS')
st.markdown('<style>div.block-container{padding-top:0rem;}</style>',unsafe_allow_html=True)

names=['customer_id','username','tran_id','tran_date','operation','status','acc_num','amount','currency','phone','branch','region','destbank']

@st.cache_data
def get_data():
    data=pd.read_csv('{}/qb_live1.txt'.format(os.getcwd()),names=names)
    return data
data=pd.read_csv('{}/qb_live1.txt'.format(os.getcwd()),names=names)

#content
st.sidebar.title('choose filter:')
placeholder=st.empty()
# refresh_interval = st.sidebar.slider("Refresh interval (seconds)", 5, 60, 10)
# st_autorefresh(interval=refresh_interval * 1000, key="auto")
filter = st.sidebar.multiselect('Regions', data.region.unique())
if not filter :
        data=data.copy()
else:
    data=data[data.region.isin(filter)]
with st.expander('Download Dataset') :
    st.dataframe(data,use_container_width=True)
    col1,col2,col3=st.columns(3)
    with col2:
        data=data.to_csv(columns=names,index=False)
        st.download_button('click to download',data=data,file_name='QBtransactions.csv',use_container_width=True)

while True:
    def get_data():
        data=pd.read_csv('{}/qb_live1.txt'.format(os.getcwd()),names=names)
        return data

    data=get_data()
    # st.sidebar.markdown("<span style='text-align: center;padding-right:-30px;'><h3>Choose Filters</h3></span>",unsafe_allow_html=True)

    with placeholder.container():
       
        if not filter :
            data=data.copy()
        else:
            data=data[data.region.isin(filter)]

        #the mertics
        col1,col2=st.columns(2)
        with col1:
            d=st.metric('TOTAL VOLUME OF TRANSACTIONS',data.tran_id.count())

        with col2:
            st.metric('TOTAL VOLUME OF TRANSACTIONS','{:,}'.format(data.amount.sum()))

        # the visuals:
        with col1:
            volumeby_region=data.groupby('region')['customer_id'].count().reset_index()
            fig=px.pie(volumeby_region,names='region',values='customer_id',hole=0.6,labels='region')
            fig.update_layout(title='TRANSACTION VOLUME BY REGION')
            # fig.update_traces(textposition='outside')
            st.plotly_chart(fig,use_container_width=True)
        with col2:
            volumeby_operation=data.groupby('operation')['customer_id'].count().reset_index()
            fig=px.bar(volumeby_operation,x='operation',y='customer_id',text='customer_id',labels={'customer_id':'volume'},hover_name="operation")
            fig.update_layout(title='TRANSACTION VOLUME BY OPERATION')
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig,use_container_width=True)

        with col1:
            valueby_operation=data.groupby('operation')['amount'].sum().reset_index()
            fig=px.bar(valueby_operation,x='operation',y='amount',text='amount',labels={'amount':'value'},hover_name="operation",color='operation',color_discrete_sequence= px.colors.qualitative.Antique)
            fig.update_layout(title='TRANSACTION VALUE BY OPERATION')
            fig.update_traces(texttemplate='%{text:,}',textposition='outside')
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            volumeby_region=data.groupby('region')['amount'].sum().reset_index()
            fig=px.pie(volumeby_region,names='region',values='amount',color='region',color_discrete_sequence= px.colors.qualitative.G10)
            fig.update_layout(title='TRANSACTION VALUE BY REGION')
            fig.update_traces(hoverinfo='label+percent',textfont_size=20,textinfo='label+percent',pull=[0.1,0,0.2,0.1,0.1],
            marker=dict(
            line=dict (color='#FFFFFF',width=2)
            ))
            st.plotly_chart(fig,use_container_width=True)
        #line 
        data['minute']=pd.to_datetime(data.tran_date).dt.minute
        line_data=data.groupby(['minute','operation'])['amount'].sum().reset_index()
        fig=px.line(line_data,x='minute',y='amount',color='operation',text='amount',color_discrete_sequence=px.colors.qualitative.Vivid,hover_name='operation')
        fig.update_traces(texttemplate='%{text:,}')
        fig.update_layout(title="TRANSACTIONS VALUE PER MINUTE BY OPERATION")
        st.plotly_chart(fig,use_container_width=True)

        col1, col2=st.columns(2)
        #FROR THE BRANCHES 
        with col1:
            valueby_operation=data.groupby('branch')['amount'].sum().reset_index()
            fig=px.bar(valueby_operation,x='amount',y='branch',text='amount',labels={'amount':'value'},hover_name="branch",color='branch',color_discrete_sequence= px.colors.qualitative.T10,orientation='h')
            fig.update_layout(title='VALUE BRANCH ANALYSIS')
            fig.update_traces(texttemplate='%{text:,}',textposition='outside')
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            valueby_operation=data.groupby(['branch','region'])['customer_id'].count().reset_index()
            fig=px.bar(valueby_operation,x='customer_id',y='region',text='customer_id',labels={'customer_id':'volume'},hover_name="region",color='branch',color_discrete_sequence= px.colors.qualitative.Antique,orientation='h')
            fig.update_layout(title='VOLUME BRANCH ANALYSIS')
            fig.update_traces(texttemplate='%{text:,}',textposition='outside')
            st.plotly_chart(fig,use_container_width=True)

        time.sleep(1)
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import time,os

# st.set_page_config(page_title='QB TRANSACTIONS ANALYSIS', page_icon=':bar_chart:', layout='wide')
# st.title(':bar_chart: QB TRANSACTIONS ANALYSIS')
# st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# names = ['customer_id', 'username', 'tran_id', 'tran_date', 'operation', 'status', 'acc_num', 'amount', 'currency', 'phone', 'branch', 'region', 'destbank']

# @st.cache_data
# def get_data():
#     data = pd.read_csv('{}/qb_live1.txt'.format(os.getcwd()), names=names)
#     return data

# # content
# st.sidebar.title('choose filter:')
# placeholder = st.empty()

# while True:
#     data = get_data()
#     filter = st.sidebar.multiselect('Regions', data.region.unique())
#     if not filter:
#         data = data.copy()
#     else:
#         data = data[data.region.isin(filter)]

#     with st.expander('Download Dataset'):
#         st.dataframe(data, use_container_width=True)
#         col1, col2, col3 = st.columns(3)
#         with col2:
#             csv_data = data.to_csv(columns=names, index=False)
#             st.download_button('click to download', data=csv_data, file_name='QBtransactions.csv', use_container_width=True)

#     with placeholder.container():
#         # the metrics
#         col1, col2 = st.columns(2)
#         with col1:
#             st.metric('TOTAL VOLUME OF TRANSACTIONS', data.tran_id.count())

#         with col2:
#             st.metric('TOTAL VOLUME OF TRANSACTIONS', '{:,}'.format(data.amount.sum()))

#         # the visuals:
#         with col1:
#             volumeby_region = data.groupby('region')['customer_id'].count().reset_index()
#             fig = px.pie(volumeby_region, names='region', values='customer_id', hole=0.6, labels='region')
#             fig.update_layout(title='TRANSACTION VOLUME BY REGION')
#             st.plotly_chart(fig, use_container_width=True)

#         with col2:
#             volumeby_operation = data.groupby('operation')['customer_id'].count().reset_index()
#             fig = px.bar(volumeby_operation, x='operation', y='customer_id', text='customer_id', labels={'customer_id': 'volume'}, hover_name="operation")
#             fig.update_layout(title='TRANSACTION VOLUME BY OPERATION')
#             fig.update_traces(textposition='outside')
#             st.plotly_chart(fig, use_container_width=True)

#         with col1:
#             valueby_operation = data.groupby('operation')['amount'].sum().reset_index()
#             fig = px.bar(valueby_operation, x='operation', y='amount', text='amount', labels={'amount': 'value'}, hover_name="operation", color='operation', color_discrete_sequence=px.colors.qualitative.Antique)
#             fig.update_layout(title='TRANSACTION VALUE BY OPERATION')
#             fig.update_traces(texttemplate='%{text:,}', textposition='outside')
#             st.plotly_chart(fig, use_container_width=True)

#         with col2:
#             volumeby_region = data.groupby('region')['amount'].sum().reset_index()
#             fig = px.pie(volumeby_region, names='region', values='amount', color='region', color_discrete_sequence=px.colors.qualitative.G10)
#             fig.update_layout(title='TRANSACTION VALUE BY REGION')
#             fig.update_traces(hoverinfo='label+percent', textfont_size=20, textinfo='label+percent', pull=[0.1, 0, 0.2, 0.1, 0.1],
#                               marker=dict(line=dict(color='#FFFFFF', width=2)))
#             st.plotly_chart(fig, use_container_width=True)

#         # line
#         data['minute'] = pd.to_datetime(data.tran_date).dt.minute
#         line_data = data.groupby(['minute', 'operation'])['amount'].sum().reset_index()
#         fig = px.line(line_data, x='minute', y='amount', color='operation', text='amount', color_discrete_sequence=px.colors.qualitative.Vivid, hover_name='operation')
#         fig.update_traces(texttemplate='%{text:,}')
#         fig.update_layout(title="TRANSACTIONS VALUE PER MINUTE BY OPERATION")
#         st.plotly_chart(fig, use_container_width=True)

#         col1, col2 = st.columns(2)
#         # FOR THE BRANCHES
#         with col1:
#             valueby_operation = data.groupby('branch')['amount'].sum().reset_index()
#             fig = px.bar(valueby_operation, x='amount', y='branch', text='amount', labels={'amount': 'value'}, hover_name="branch", color='branch', color_discrete_sequence=px.colors.qualitative.T10, orientation='h')
#             fig.update_layout(title='VALUE BRANCH ANALYSIS')
#             fig.update_traces(texttemplate='%{text:,}', textposition='outside')
#             st.plotly_chart(fig, use_container_width=True)

#         with col2:
#             valueby_operation = data.groupby(['branch', 'region'])['customer_id'].count().reset_index()
#             fig = px.bar(valueby_operation, x='customer_id', y='region', text='customer_id', labels={'customer_id': 'volume'}, hover_name="region", color='branch', color_discrete_sequence=px.colors.qualitative.Antique, orientation='h')
#             fig.update_layout(title='VOLUME BRANCH ANALYSIS')
#             fig.update_traces(texttemplate='%{text:,}', textposition='outside')
#             st.plotly_chart(fig, use_container_width=True)

#     time.sleep(1)
#     st.experimental_rerun()