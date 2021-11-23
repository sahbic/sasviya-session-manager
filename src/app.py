import streamlit as st
import pandas as pd
import swat

from utils import *

st.sidebar.title('Configuration')

with st.sidebar.form("my_form"):
    st.write('Enter your credentials')
    viya_url = st.text_input("Enter URL")
    user_input = st.text_input("Enter username")
    password = st.text_input("Enter your password", type="password")
    submitted = st.form_submit_button("Submit")
    if submitted:
        if viya_url[-1] == "/":
            viya_url = viya_url[:-1]
        s = swat.CAS(viya_url + "/cas-shared-default-http", username=user_input, password=password)
        st.session_state.session = s
        st.session_state.viya_url = viya_url
        token = get_token(viya_url, user_input, password)
        st.session_state.token = token
    if ('session' in st.session_state) & ('token' in st.session_state):
        s = st.session_state.session
        st.sidebar.success('Connected')
        st.sidebar.header('System Info')
        server_status = flatten_data(s.serverStatus().About)
        df = pd.DataFrame.from_records([server_status],index=["values"]).astype(str)
        st.sidebar.table(df.T.iloc[[14,15],:])

if 'session' in st.session_state:
    s = st.session_state.session

    if True | st.button("Refresh"):
        st.header('Sessions')
        sess = s.session.listSessions().Session
        st.dataframe(sess.drop(columns=['UUID']))

        if 'token' in st.session_state:
            token = st.session_state.token
            viya_url = st.session_state.viya_url
            st.header('Manage session')
            option = st.selectbox("Select session", list(sess.SessionName))
            st.table(sess[sess.SessionName == option])
            session_id = sess[sess.SessionName == option].UUID.values[0]
            if st.button("Terminate"):
                r = delete_session(viya_url, token, session_id)
                st.write(r.text)
                if r.status_code == 200:
                    st.markdown("Session **{}** terminated".format(option))

