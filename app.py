import streamlit as st
import requests
import os
from components.ui import render_result

API_BASE = os.getenv('BACKEND_URL','http://backend:8000')

st.set_page_config(page_title='AI Log Insights')

st.title('AI Log Insights Dashboard')

st.sidebar.header('Actions')
mode = st.sidebar.selectbox('Mode', ['Upload logs', 'Search', 'Daily summary'])

if mode == 'Upload logs':
    uploaded = st.file_uploader('Upload a log file (one JSON per line or plain text)', type=['log','txt','json'])
    if uploaded:
        content = uploaded.read().decode('utf-8')
        lines = content.splitlines()
        successful = 0
        for line in lines:
            try:
                import json
                try:
                    obj = json.loads(line)
                except Exception:
                    obj = {"timestamp": None, "level":"INFO","message": line}
                r = requests.post(API_BASE + '/api/logs/ingest', json=obj)
                if r.status_code == 200:
                    successful += 1
            except Exception as e:
                st.error(f'Error ingesting line: {e}')
        st.success(f'Ingested {successful} lines')

if mode == 'Search':
    q = st.text_input('Semantic query')
    k = st.slider('Top K', 1, 20, 5)
    if st.button('Search') and q:
        res = requests.get(API_BASE + '/api/logs/search', params={'q': q, 'k': k})
        if res.status_code == 200:
            for r in res.json().get('results',[]):
                render_result(r)
        else:
            st.error(res.text)

if mode == 'Daily summary':
    date = st.date_input('Select date')
    if st.button('Generate summary'):
        st.info('This will call the backend analyze endpoint (example)')
        st.warning('Make sure to add logs first or wire a real query')
        st.write('Not implemented: server-side date range query; use /api/logs/analyze with batch payload')


