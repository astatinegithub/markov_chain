import streamlit as st
import pandas as pd 
import numpy as np 
df = pd.DataFrame({ "col1": np.random.randn(1000) / 50 + 37.76, "col2": np.random.randn(1000) / 50 + -122.4, "col3": np.random.randn(1000) * 100, "col4": np.random.rand(1000, 4).tolist(), })
# st.map(df, latitude='col1', longitude='col2', size='col3', color='col4')
df = pd.DataFrame({'col': np.linspace(1, 1000, 1000), "col1": np.random.randn(1000) / 50 + 37.76,})

st.header('line_chart')
st.line_chart(df)

st.header('area_chart')
st.area_chart(df)

st.header('bar_chart')
st.bar_chart(df)


# import streamlit as st 
# import numpy as np 
# import plotly.figure_factory as ff 
# # Add histogram data 
# x1 = np.random.randn(200) - 2 
# x2 = np.random.randn(200) 
# x3 = np.random.randn(200) + 2 # Group data together 
# hist_data = [x1, x2, x3] 
# group_labels = ['Group 1', 'Group 2', 'Group 3'] # Create distplot with custom bin_size 
# fig = ff.create_distplot( hist_data, group_labels, bin_size=[.1, .25, .5]) # Plot! 
# st.plotly_chart(fig, use_container_width=True)
