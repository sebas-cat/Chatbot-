import streamlit as st
import torch
from torch.cuda import device
from torchgen import model
from data.Dataset import label2id, id2label 
import warnings
from src.model import load_model
warnings.filterwarnings("ignore")  
from src.ner import analyze, resolve_date, extract_task
from src.calendar_api import create_event, authenticate_google_calendar
from src.database import get_events_date, init_database, save_event
from src.llm import generate_response
import torch

@st.cache_resource
def initialize():
    cuda_available = torch.cuda.is_available()
    print(f"CUDA available: {cuda_available}")
    device = torch.device("cuda" if cuda_available else "cpu")
    print(f"Using: {device}")
    model_name = "saved_model"
    model, tokenizer = load_model(device, model_name, label2id, id2label)
    service = authenticate_google_calendar()
    init_database()
    return model, tokenizer, service, device

model, tokenizer, service, device = initialize()
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

user_input = st.chat_input("Help me guide you, type what you need...")
if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
    