# web_analyzer.py
# Iraj Akbar (30146997), Azlfa Anwar (30176659)

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from collections import Counter
import string

def fetch_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status() 
        print(f"Successfully fetched content from {url}")
        return response.text
    except Exception as e:
        print(f"Error fetching content: {e}")
        return None

def main():
    url_input = input("Enter a URL (press Enter for default University of Calgary Wikipedia page): ")
    if not url_input.strip():
        url_input = "https://en.wikipedia.org/wiki/University_of_Calgary"
    
    html_content = fetch_webpage(url_input)
    if html_content is None:
        return
    
    # 2. Crawl the UoC Wikipedia webpage  
    soup = BeautifulSoup(html_content, 'html.parser')
    
    print("\nPrettified HTML content:\n")
    print(soup.prettify())
    
    # 3. Data Analysis
    headings_count = sum(len(soup.find_all(f'h{i}')) for i in range(1, 7))
    links_count = len(soup.find_all('a'))
    paragraphs = soup.find_all('p')
    paragraphs_count = len(paragraphs)
    
    print("\nData Analysis:")
    print(f"Total Headings (h1-h6): {headings_count}")
    print(f"Total Links (<a> tags): {links_count}")
    print(f"Total Paragraphs (<p> tags): {paragraphs_count}")
    
    # 4. Keywords Analysis
    keyword = input("\nEnter a keyword to search for: ")
    text_content = soup.get_text(separator=" ", strip=True)
    keyword_count = text_content.lower().count(keyword.lower())
    print(f"\nThe keyword '{keyword}' appears {keyword_count} times in the webpage content.")
    
    # 5. Word Frequency Analysis
    translator = str.maketrans('', '', string.punctuation)
    cleaned_text = text_content.translate(translator)
    words = cleaned_text.lower().split()
    word_counts = Counter(words)
    top_5 = word_counts.most_common(5)
    
    print("\nTop 5 most frequent words:")
    for word, count in top_5:
        print(f"{word}: {count}")
    
    # 6. Finding the Longest Paragraph
    longest_paragraph = ""
    max_word_count = 0
    for p in paragraphs:
        p_text = p.get_text(strip=True)
        word_list = p_text.split()
        if len(word_list) >= 5 and len(word_list) > max_word_count:
            longest_paragraph = p_text
            max_word_count = len(word_list)
    
    if longest_paragraph:
        print("\nLongest Paragraph:")
        print(longest_paragraph)
        print(f"Word Count: {max_word_count}")
    else:
        print("\nNo paragraph with at least 5 words found.")
    
    # 7. Visualizing Results
    labels = ['Headings', 'Links', 'Paragraphs']
    values = [headings_count, links_count, paragraphs_count]
    
    plt.bar(labels, values)
    plt.title('Group #: 37 ')
    plt.ylabel('Count')
    plt.show()

if __name__ == '__main__':
    main()
