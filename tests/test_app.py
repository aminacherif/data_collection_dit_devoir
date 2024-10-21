import pytest
from unittest.mock import MagicMock, patch
from requests import get
from bs4 import BeautifulSoup as bs
import pandas as pd
import streamlit as st
from app.data_app import load_bs

@pytest.fixture
def sample_html_villas():
    return """
    <div class="col s6 m4 l3">
        <p class="ad__card-description">Villa 4 pièces</p>
        <p class="ad__card-price">10 000 000 CFA</p>
        <p class="ad__card-location"><span>Dakar</span></p>
        <img class="ad__card-img" src="http://example.com/image1.jpg">
    </div>
    """

@pytest.fixture
def sample_html_terrains():
    return """
    <div class="col s6 m4 l3">
        <p class="ad__card-description">Terrain 500 m²</p>
        <p class="ad__card-price">5 000 000 CFA</p>
        <p class="ad__card-location"><span>Thiès</span></p>
        <img class="ad__card-img" src="http://example.com/image2.jpg">
    </div>
    """

@pytest.fixture
def sample_html_appartements():
    return """
    <div class="col s6 m4 l3">
        <p class="ad__card-description">Appartement 3 pièces</p>
        <p class="ad__card-price">7 000 000 CFA</p>
        <p class="ad__card-location"><span>Dakar</span></p>
        <img class="ad__card-img" src="http://example.com/image3.jpg">
    </div>
    """

@patch('requests.get')
def test_load_bs_villas(mock_requests_get, sample_html_villas):
    mock_requests_get.return_value.text = sample_html_villas
    with patch('streamlit.button', MagicMock(return_value=True)), patch('streamlit.dataframe'), patch('streamlit.subheader'), patch('streamlit.write'):
        load_bs(1, 'Villas', '1')

@patch('requests.get')
def test_load_bs_terrains(mock_requests_get, sample_html_terrains):
    mock_requests_get.return_value.text = sample_html_terrains
    with patch('streamlit.button', MagicMock(return_value=True)), patch('streamlit.dataframe'), patch('streamlit.subheader'), patch('streamlit.write'):
        load_bs(1, 'Terrains', '2')

@patch('requests.get')
def test_load_bs_appartements(mock_requests_get, sample_html_appartements):
    mock_requests_get.return_value.text = sample_html_appartements
    with patch('streamlit.button', MagicMock(return_value=True)), patch('streamlit.dataframe'), patch('streamlit.subheader'), patch('streamlit.write'):
        load_bs(1, 'Appartements', '3')
