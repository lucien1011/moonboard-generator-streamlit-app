import streamlit as st
import numpy as np
from io import BytesIO
import os
import pandas as pd
from PIL import Image, ImageDraw
import random
import requests

st.set_page_config(page_title = "MB Problem Generator", page_icon="", layout = "wide", initial_sidebar_state = "expanded")

purple_btn_colour = """
                        <style>
                            div.stButton > button:first-child {background-color: #4b0082; color:#ffffff;}
                            div.stButton > button:hover {background-color: RGB(0,112,192); color:#ffffff;}
                            div.stButton > button:focus {background-color: RGB(47,117,181); color:#ffffff;}
                        </style>
                    """
horizontal_bar = "<hr style='margin-top: 0; margin-bottom: 0; height: 1px; border: 1px solid #635985;'><br>"    # thin divider line
lightup_hold = """<span style='font-size: 24px;
                   border-radius: 7px;
                   text-align: center;
                   display:inline;
                   padding-top: 3px;
                   padding-bottom: 3px;
                   padding-left: 0.2em;
                   padding-right: 0.2em;
                   '>
                   |fill_variable|
                   </span>"""

base_dir = './'
num_column = 11
num_row = 18

generate_url = 'https://hhbueku1d8.execute-api.eu-north-1.amazonaws.com/generate/{:s}'

state = st.session_state
if not hasattr(state,'generate_problem'): state.generate_problem = False
if not hasattr(state,'show_problem'): state.show_problem = False
#if not hasattr(state,'board_setup'): state.board_setup = '2016'
if not hasattr(state,'board_light'): state.board_light = {}

def DrawImage(state):
    image = Image.open(os.path.join(base_dir,'image/mbsetup-{:s}.jpg'.format(state.board_setup)))
    draw = ImageDraw.Draw(image)
    x0 = 75
    dx = 51
    y0 = -10
    dy = 51
    radius = 50
    circle_width = 5
    orda = ord('a')
    image_height = 1023
    circleColors = {
        'start': 'green',
        'seq': 'blue',
        'end': 'red',
    }
    if state.board_light:
        for key,holds in state.board_light.items():
            if key not in ['start','seq','end']: continue
            for hold in holds:
                x_pos = x0 + dx * (ord(hold[0]) - orda)
                y_pos = y0 + dy * hold[1]
                leftUpPoint = (x_pos,image_height-y_pos-radius)
                rightDownPoint = (x_pos + radius,image_height-y_pos)
                draw.ellipse([leftUpPoint,rightDownPoint], fill=None, outline=circleColors[key],width=circle_width)
    buffer = BytesIO()
    image.save(buffer,format='png')
    return buffer

def Board(state):
    st.markdown("<style> div[class^='css-1vbkxwb'] > p { font-size: 1.5rem; } </style> ", unsafe_allow_html=True)  # make button face bi
    with st.container(border=True):
        col1,_,col2 = st.columns([0.60,0.10,0.30])
        buffer = DrawImage(state)
        col1.image(buffer)
        col2.radio('How is this problem?', options=('Very good!', 'Good!', 'OK!', 'Meh!', 'Unclimbable!'))
        col2.button('Rate')

def BoardPage(state):
    st.markdown('<style>[data-testid="stSidebar"] > div:first-child {width: 310px;}</style>', unsafe_allow_html=True,)  # reduce sidebar width
    st.markdown(purple_btn_colour, unsafe_allow_html=True)
    if state.generate_problem:
        response = requests.get(url = generate_url.format(state.board_setup))
        state.board_light = response.json()['content']
        state.generate_problem = False
    if state.show_problem:
        st.header('Generated Problem')
        st.markdown(horizontal_bar, True)
        Board(state)                

def Main():
    BoardPage(state)
    with st.sidebar:
        st.subheader("Moonboard Problem Generator")
        st.markdown(horizontal_bar, True)
        state.board_setup = st.radio('Board Setup:', options=('2016','2017','2019','2024'), index=1, horizontal=True, )
        if st.button("Generate"):
            state.generate_problem = True
            state.show_problem = True
            st.rerun()
        if st.button("Clear"):
            state.show_problem = False
            st.rerun()

if 'runpage' not in state: state.runpage = Main
state.runpage()
