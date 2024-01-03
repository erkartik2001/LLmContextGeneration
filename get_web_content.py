from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests

load_dotenv()
GoogleSearch.SERP_API_KEY = os.getenv("SERPER_API_KEY")
text_file_path = os.getenv("TEXT_FILE_PATH")
print(os.getenv("SERPER_API_KEY"))


def search_query(query):
    """"
    Runs Google Search for given query and return results

    Args:
        query (str): Query to run Google Search for

    Returns:
        results (dict): A dictionary of results
    """
    params = {
        "q":query,
        "location":"Austin, Texas, United States",
        "hl":"en",
        "gl":"us",
        "google_domain":"google.com"
    }

    try:
        search = GoogleSearch(params_dict=params)
        results = search.get_dict()

    except Exception as e:
        print(f"Error getting search results : {e}")
        return None

    return results


def get_result_links(results, top_n):
    """
    Extracts and Returns links for top_n results

    Args:
        results (dict): Results generated by google search
        top_n (int): Top n links to get

    Returns:
        links (list): Returns list containing top n results
    """

    if not results:
        print("Cannot get the links")
        return None

    links = []
    for i in range(top_n):
        link = results["organic_results"][i]["link"]
        links.append(link)

    return links



def store_web_data(query, top_n=7):
    """
    Extracts and Returns text data 

    Args:
        query (str): Query to perform google search for
        top_n (int): Top n results to get text data from

    Returns:
        data (str): Returns text data for 
    """

    results = search_query(query=query)
    links = get_result_links(results=results, top_n=top_n)

    if not links:
        return None
    
    data = ""
    for link in links:

        try:
        
            response = requests.get(link)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            for element in soup(['script', 'style', 'header', 'footer']):
                element.extract()

            text = soup.get_text(separator=" ")

            data += text

        except requests.exceptions.RequestException as e:
            print(f"error fetching the url : {e}")
            continue
    
    try:
        with open(text_file_path, "w+") as file:
            file.write(data)

    except Exception as e:
        print(f"Error could not store the data : {e}")
        return False

    return True
    









