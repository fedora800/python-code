from collections import Counter
from bs4 import BeautifulSoup, ResultSet, Tag
import re

HTML_FILE = "investengine_etfs_all.htm"
#TEXT_TO_MATCH = "VUS"     # this should match VUSC, MVUS and VUSA
TEXT_TO_MATCH = "."

# Match anywhere inside the element, including nested tags, without worrying about class names, IDs, or other attributes.
# Returns the string if found
def fn_element_contains_text(element, text_str) -> str:
  return text_str in element.get_text(separator=" ", strip=True)

		
# To get only the human-readable text inside a document or tag.
# This will return all the text in it (and sub elements) as a single Unicode string
# Below is an example of usage :
# markup = '<a href="http://example.com/">\nI linked to <i>example.com</i> so please visit it\n</a>'	
# >>> soup.get_text()
# '\nI linked to example.com so please visit it\n'
# >>> soup.i.get_text()
# 'example.com'
# >>> soup.get_text("|")          # You can specify a string to be used to join the bits of text together
# '\nI linked to |example.com| so please visit it\n'
# >>> soup.get_text("|", strip=True)         # You can tell Beautiful Soup to strip whitespace from the beginning and end of each bit of text
# 'I linked to|example.com|so please visit it'
# >>> for text in soup.stripped_strings:    	# You can access the individual blocks of text
# ...     print(text)
# ... 
# I linked to
# example.com
# so please visit it
# >>> texts = list(soup.stripped_strings)
# >>> print(texts)
# ['I linked to', 'example.com', 'so please visit it']
def fn_get_text_only_from_element(element) -> str:
  # (prevents word-joining issues)
  text_str = element.get_text(separator=" ][ ", strip=True)
  # collapse multiple spaces and newlines into a single space.
  text_str = re.sub(r'\s+', ' ', text_str)
  return text_str


def fn_analyze_elements(elements, fd):
  for element in elements:
    if fn_element_contains_text(element, TEXT_TO_MATCH):
      fn_pretty_print_element(element, "text_only", fd)

# text_only, html_only, both
def fn_pretty_print_element(element, option, fd):
  print("=" * 80)
  #print(element)
  if option == "html_only" or option == "both":
    # Pretty-printed HTML subtree
    print("\n[HTML - prettify()]")
    print(element.prettify())
  if option == "text_only" or option == "both":
    cleaned_text = fn_get_text_only_from_element(element)
    print("\n[TEXT - get_text()] = ", cleaned_text)
    # File (SAFE UTF-8) writing
    fd.write(cleaned_text + "\n")
  print("=" * 80)




def fn_list_all_tags(soup, option):
  MAX_SHOW = 50   # to avoid printing all the tags for a long html doc
  counter = 0

  if option == "all":
    for element in soup.descendants:
      if element .name:
          e_name = element.name[0:6]
          e_text = element.get_text(strip=True)
          e_text = e_text[0:50]
          e_classes = ", ".join(element.get("class", []))
          print(f"name={e_name} | classes={e_classes} | text={e_text}")
          counter = counter + 1
          if counter >= MAX_SHOW:
            return
 
  # Only give a count of uniquely occurring tags
  if option == "unique":
    tag_counts = Counter(tag.name for tag in soup.find_all(True))
    for tag, count in tag_counts.most_common():
      print(f"{tag:8} {count}")



# this will find all the divs that have a specific class
# note that it will also print all child tags under it as well as text and it's own opening and closing tag
# NOTE: bs4 will treat this as a match if the div CONTAINS the class_name
def fn_find_all_divs_by_class(soup, class_name, debug) -> ResultSet[Tag]:
  div_elements = soup.find_all("div", class_=class_name)
  print("Number of elements found for [", class_name, "]=", len(div_elements))
  if debug:
    counter=0
    for element in div_elements:
      counter = counter + 1
      print("counter=", counter, "-----------[")
      #print(element)
      print(" ]---------------")
  return div_elements


def main():
  with open(HTML_FILE, "r", encoding="utf-8") as fp:
    soup = BeautifulSoup(fp, "html.parser")
  
  output_fp = open("output.txt", "w", encoding="utf-8")

  fn_list_all_tags(soup, "all")
  #fn_find_all_elements_of_a_type(soup, "div")
  class_to_find = "Card_Card__bLarm"
  divs_of_interest = fn_find_all_divs_by_class(soup, class_to_find, debug=False)
  fn_analyze_elements(divs_of_interest, output_fp)
  output_fp.close()

if __name__ == "__main__":
    main()


