import config as cfg
import os
import streamlit as st
import requests
import logging

from pathlib import Path

__author__ = cfg.AUTHOR #TODO hardcoden --> doctools lesen direkt sourcecode
__title__ = cfg.APP_TITLE
__version__ = cfg.VERSION


os.chdir(Path(__file__).parent)
logging.basicConfig(filename='fastapi.log', level=logging.INFO) #TODO logging.ini nutzen
logger = logging.getLogger() #TODO logging auf front- und backend aufgteilen

def create_frontend():
    """creates frontend of app
    """
    st.title("Evaluate Text")
    text = st.text_input("Text to evaluate.")
    logger.info("Received text to evaluate.")
    if st.button("Evaluate"):
        result_blob = post_request(text) #TODO inline docs
        if result_blob.status_code == 200:
            st.header("TextBlob", divider=True)
            col1, col2 = st.columns(2)
            logger.info(f"API-request for blob-analyzer successful.")
            result_blob = result_blob.json()
            col1.metric("Polarity", round(result_blob["polarity"], 2))
            col2.metric("Subjectivity", round(result_blob["subjectivity"], 2))
            logger.info(f"\nResults:\n\tInput: {text}\n\tPolarity: {round(result_blob["polarity"], 2)}\n\tSubjectivity: {round(result_blob["subjectivity"], 2)}")
        else:
            logger.info(f"API-request for blob-analyzer failed with code: {result_blob.status_code}")
        
        result_transformer = post_request(text, analyzer="transformer")
        if result_transformer.status_code == 200:
            st.header("Transformer", divider=True)
            col1, col2 = st.columns(2)
            logger.info(f"API-request for transfomer-analyzer successful.")
            result_transformer = result_transformer.json()
            col1.metric("Label", result_transformer["label"])
            col2.metric("Polarity", round(result_transformer["score"], 2))
            logger.info(f"\nResults:\n\tInput: {text}\n\tPolarity: {round(result_transformer["score"], 2)}")
        else:
            logger.info(f"API-request for transfomer-analyzer failed with code: {result_transformer.status_code}")


def post_request(input: str, analyzer: str="blob") -> object:
    """Sends post request to backend.
    Backend has to run at "http://localhost:8000/"

    Args:
        input (str): string to analyze
        analyzer (str, optional): determines which analyzer is used. Defaults to "blob".

    Returns:
        dict: api-result
    """
    URL = f"http://localhost:8000/analyze_{analyzer}"
    data = {"text": input}
    logger.info("Sending API-request...")
    result = requests.post(URL, json = data)
    return result

def main():
    create_frontend()

if __name__ =="__main__":
    logger.info(f"Started APP:\n\tTitle: {__title__}\n\tAuthor: {__author__}\n\tVersion: {__version__}")
    main()
    logger.info("Application Closed!")