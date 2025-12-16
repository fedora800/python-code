from bs4 import BeautifulSoup
from bs4 import NavigableString, Tag
import pandas as pd
from collections import Counter
import re

HTML_FILE = "investengine_etfs_all.htm"

# these i need to find and populate correctly into this
# these are only substrings as the websites will often append a frequently changing hash after it to break scraping
CONTAINERS_SUBSTRINGS_OF_INTEREST = [
    # Ticker badge
    ("div", "Badge_Badge"),

    # Description text next to badge
    ("span", "Text_Text_verticalAlign"),

    # TER / Yield / Accumulating
    ("div", "ItemWithIcon_ItemWithIcon-Content__"),

    # Instrument name (bold title)
    ("div", "Text_Text_weightDesktop_600"),
]





with open(HTML_FILE, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Find all divs
divs = soup.find_all("div")

# Collect class tuples and their nesting levels
classes_levels = []
for d in divs:
    cls_tuple = tuple(d.get('class', []))
    level = len(list(d.parents)) - 1  # root is level 0
    classes_levels.append((cls_tuple, level))

# Count most common class combinations
class_counts = Counter([cls for cls, lvl in classes_levels])

# Explore top level tags
# Print all direct children of <body> (or top level)
#This shows tag names + classes at the first level.
# Helps you spot “cards”, “rows”, or divs that repeat.
print("\n--- Top-level tags under <body> ---")
for i, tag in enumerate(soup.body.find_all(recursive=False)):
    print(i, tag.name, tag.get('class'))


# Look for divs that repeat many times
# ie Count repeating patterns
# The most common class combinations are usually the repeating data rows.
# For example, your data-test-id="securityItem" div will show up multiple times.
print("\n--- Most common class combinations in divs with their nesting levels ---")
for cls, count in class_counts.most_common(20):
    # Find first occurrence to get its level
    first_lvl = next(lvl for c, lvl in classes_levels if c == cls)
    print(f"Count: {count} | Level: {first_lvl} | Class combo: {cls}")
# We will need to deeply review above output to find the actual parent row container for the peeking into at the end
# Never scrape leaf divs directly for rows in obfuscated HTML
# Find highest-level repeating container (highest nesting level among repeated class combos)
# Then extract text or numbers from its children

# Explore first few rows
# Even if you don’t know class names, you can look at attributes like data-*, id, role, etc.
# prettify() helps visually spot the content.
print("\n--- All unique data-* attributes ---")
data_attrs = set()
for tag in soup.find_all():
    for k, v in tag.attrs.items():
        if k.startswith("data-"):
            data_attrs.add((k, v))
for da in data_attrs:
    print(da)


# Extract text without knowing divs
# Extract all text in a row
# stripped_strings gives a list of all text nodes, so you can see:
#  Names
#  Tickers
#  TER / Yield
#Later, you can write a small rule to pick the right strings based on patterns.
# Optionally, auto-detect rows using common data-test-id or repeated classes
print("\n--- Sample repeating rows (first 3) ---")
rows = soup.find_all(attrs={"data-test-id": True})
for r in rows[:3]:
    print(r.prettify()[:500])  # first 500 chars

print("\n--- Extracted text from sample rows ---")
for r in rows[:3]:
    print(list(r.stripped_strings))

# --- Optional numeric extraction (TER/Yield) ---
def extract_number(s):
    if not s:
        return None
    match = re.search(r"[\d.]+", s.replace('\xa0',' '))
    return float(match.group()) if match else None

for r in rows[:3]:
    texts = list(r.stripped_strings)
    ter = next((t for t in texts if t.startswith("TER")), None)
    yld = next((t for t in texts if "Yield" in t), None)
    ter_val = extract_number(ter)
    yld_val = extract_number(yld)
    print("TER:", ter_val, "| Yield:", yld_val)


# Now, when we get to know the most common class combinations in the divs
# eg - 
# --- Most common class combinations in divs with their nesting levels ---
# Count: 2534 | Level: 9 | Class combo: ('ItemWithIcon_ItemWithIcon-Content__p2CoO',)
# Count: 1650 | Level: 21 | Class combo: ('ItemWithIcon_ItemWithIcon__pybrO', 'ItemWithIcon_ItemWithIcon_inline__5HnRc', 'ItemWithIcon_ItemWithIcon_iconPosition_right__ifo84', 'ItemWithIcon_ItemWithIcon_iconPosition_mobile_right__5klrH', 'ItemWithIcon_ItemWithIcon_iconAlign_center__VOyfu', 'ItemWithIcon_ItemWithIcon_contentAlign_center__1ErVt')
# Count: 905 | Level: 11 | Class combo: ('Grid_Grid-Cell__Ow1kU', 'Grid_Grid-Cell_size_1__7YxS7')
# Count: 883 | Level: 9 | Class combo: ('ItemWithIcon_ItemWithIcon-Icon__8tZj_',)
# Try to extract rows for a few of them
print("\n--- For the specific class of our choosing, extract text from sa few rows ---")
peek_class_name = "ItemWithIcon_ItemWithIcon__pybrO"
peek_rows = 5
rows = soup.find_all("div", class_=peek_class_name)
for r in rows[:peek_rows]:
    print(list(r.stripped_strings))

print("\n--- TEST WITH A MORE SPECIFIC FILTER --  For the specific class of our choosing, extract text from sa few rows ---")
rows = soup.find_all(
    "div",
    class_=[
        "ItemWithIcon_ItemWithIcon__pybrO",
        "ItemWithIcon_ItemWithIcon_iconPosition_left___U4Sf"  # main row variant
    ]
)
for r in rows[:peek_rows]:
    print(list(r.stripped_strings))

print("\n--- 102  Find the div that hold my known content ---")
peek_str = "JHYP"
# Find the element containing the specific text
target = soup.find(string=lambda s: s and peek_str in s)
if not target:
    print("Text ", peek_str, " not found.")
    exit()

# Start from the immediate parent
parent = target.parent

# Climb up until we find a div whose parent is not another div
# (i.e., the topmost container for this piece of text)
while parent and parent.name == "div" and parent.parent and parent.parent.name == "div":
    parent = parent.parent

# Print the HTML nicely
print(parent.prettify())

# Recursive function to print divs with level and text
def print_div_levels(tag, level=0):
    if tag.name != "div":
        return

    indent = "  " * level
    classes = tag.get('class')
    text = tag.get_text(strip=True)
    
    # Mark the div if it contains the target string
    marker = " #YOUR STRING#" if peek_str in text else ""
    
    print(f"#LEVEL {level}# {marker}  {indent}<{tag.name} class='{classes}'> Text='{text}'")
    
    for child in tag.children:
        if hasattr(child, "name"):
            print_div_levels(child, level + 1)

# Print the div tree with text and highlight target
print_div_levels(parent)




def is_allowed_container(tag):
    """
    Returns True if the tag matches one of the allowed
    (tag name + class set) definitions.
    """

    if not tag or not hasattr(tag, "name"):
        return False

    tag_name = tag.name
    tag_classes = set(tag.get("class", []))

    for allowed in ALLOWED_TEXT_CONTAINERS:
        if tag_name != allowed["tag"]:
            continue

        if allowed["classes"].issubset(tag_classes):
            return True

    return False




# def extract_unique_leaf_text(parent_container, debug=False):
#     """
#     Extract readable text from a security card.
#     Prints debug output ONLY when text belongs to an allowed semantic container.
#     Also prints the MAIN parent card for every match.
#     """

#     collected_text = []
#     seen_text = set()

#     for descendant in parent_container.descendants:

#         if not isinstance(descendant, NavigableString):
#             continue

#         text = descendant.strip()
#         if not text:
#             continue

#         matching_container = find_allowed_ancestor(
#             descendant.parent,
#             stop_at=parent_container
#         )

#         if matching_container:
#             main_parent = find_security_card(matching_container)

#             if debug:
#                 print("\n[MATCH FOUND]")
#                 print(
#                     f"  Leaf text      : '{text}'\n"
#                     f"  Matched node   : <{matching_container.name}> "
#                     f"class={matching_container.get('class', [])}"
#                 )

#                 if main_parent:
#                     print(
#                         f"  MAIN PARENT    : <div data-test-id='securityItem'> "
#                         f"class={main_parent.get('class', [])}"
#                     )
#                 else:
#                     print("  MAIN PARENT    : NOT FOUND")

#             if text not in seen_text:
#                 seen_text.add(text)
#                 collected_text.append(text)

#     return " | ".join(collected_text)



def find_security_card(tag):
    """
    Walk upwards until we find the main security card container.
    Identified by data-test-id="securityItem".
    """
    current = tag
    while current:
        if (
            current.name == "div"
            and current.attrs
            and current.attrs.get("data-test-id") == "securityItem"
        ):
            return current
        current = current.parent
    return None



# def find_allowed_ancestor(tag, stop_at):
#     """
#     Walk upward from a tag until we find a matching allowed container
#     or reach stop_at.
#     """
#     current = tag

#     while current and current != stop_at:
#         if is_allowed_container(current):
#             return current
#         current = current.parent

#     return None


# Get cleaned text from the parent div
debug = True
#print("\n\n--- 103  Get cleaned text from the parent div---")
#clean_text = extract_unique_leaf_text(parent, debug)
#print("\n\n", clean_text)



def has_allowed_class(tag, class_substring):
    return any(class_substring in cls for cls in tag.get("class", []))



def class_starts_with(tag, prefix):
    for cls in tag.get("class", []):
        if cls.startswith(prefix):
            return True
    return False



def extract_card_data(card, debug=False):
    """
    Extract structured data from a single ETF 'card' div.

    We intentionally ONLY extract text from *leaf-level semantic nodes*
    (Badge, Text, ItemWithIcon-Content) to avoid:
      - duplicated text
      - merged words
      - noisy parent containers

    Parameters
    ----------
    card : bs4.element.Tag
        A <div> with class 'Card_Card__bLarm' (the row container)
    debug : bool
        If True, prints every qualifying leaf node encountered

    Returns
    -------
    dict
        Parsed ETF data fields
    """

    # Initialise the output structure.
    # All values default to None so missing fields are explicit.
    data = {
        "name": None,
        "ticker": None,
        "description": None,
        "ter": None,
        "yield": None,
        "distribution": None,
    }

    # Walk *every* div/span under the card.
    # We do NOT restrict depth because meaningful text appears
    # at multiple nesting levels.
    for tag in card.find_all(["div", "span"]):

        # Fetch class list; many tags have no class → ignore early
        classes = tag.get("class", [])
        if not classes:
            continue

        # Join classes into a single string for easier substring checks
        cls = " ".join(classes)

        # Extract visible text only, using spaces as separators
        # (prevents word-joining issues)
        text = tag.get_text(" ", strip=True)

        # Skip empty or whitespace-only nodes
        if not text:
            continue

        # Optional debug trace showing exactly what is being parsed
        if debug:
            print(f"[LEAF] <{tag.name}> {cls} | '{text}'")

        # ==========================================================
        # TICKER SYMBOL (e.g. EMIM, QYLD, JHYP)
        # ==========================================================
        # Badge nodes are visually rendered tickers
        if tag.name == "div" and "Badge_Badge" in cls:
            data["ticker"] = text

        # ==========================================================
        # NAME & DESCRIPTION
        # ==========================================================
        # Both appear as <span class="Text_Text..."> nodes.
        # The *longer* text is usually the fund name,
        # the shorter one is the description.
        elif tag.name == "span" and "Text_Text" in cls:

            # First long text → fund name
            if data["name"] is None and len(text) > 25:
                data["name"] = text

            # Next available text → description
            elif data["description"] is None:
                data["description"] = text

        # ==========================================================
        # ITEM WITH ICON CONTENT (TER / Yield / Distribution)
        # ==========================================================
        # These are the *leaf content nodes* you discovered via
        # frequency & depth analysis:
        #   ItemWithIcon_ItemWithIcon-Content__p2CoO
        elif tag.name == "div" and "ItemWithIcon_ItemWithIcon-Content" in cls:

            # ---- Total Expense Ratio ----
            if text.startswith("TER"):
                match = re.search(r"([\d.]+)", text)
                if match:
                    data["ter"] = float(match.group(1))

            # ---- Yield ----
            elif "Yield" in text:
                match = re.search(r"([\d.]+)", text)
                if match:
                    data["yield"] = float(match.group(1))

            # ---- Distribution type ----
            elif text in ("Accumulating", "Distributing"):
                data["distribution"] = text

    # Return one clean, deduplicated record per card
    return data


# recursive function to traverse down a node and print information
def fn_get_all_subnodes_info(node, level=0, max_text_len=60):

    #print("--- fn_get_all_subnodes_info() --- start ---, level=", level)
    indent = "  " * level

    if not hasattr(node, "name") or node.name is None:
        return

    # Get class list (if any)
    classes = " ".join(node.get("class", []))

    # Get clean text preview
    text = node.get_text(" ", strip=True)
    if len(text) > max_text_len:
        text = text[:max_text_len] + "…"

    print(f"{indent}#LEVEL {level}# <{node.name}> class='{classes}' text='{text}'")

    # Recurse into children
    for child in node.find_all(recursive=False):
        fn_get_all_subnodes_info(child, level + 1, max_text_len)

    #print("--- fn_get_all_subnodes_info() --- end ---, level=", level)


# Leaf-node inspector (noise killer)
# This prints only nodes that actually contain text and have no child tags
# these are the nodes you should extract from.
def fn_print_leaf_text_nodes(card):
    print("\n--- LEAF TEXT NODES --- start ---")
    for tag in card.find_all(["div", "span"]):
        if tag.find(["div", "span"]):
            continue  # not a leaf

        text = tag.get_text(" ", strip=True)
        if not text:
            continue

        classes = " ".join(tag.get("class", []))
        print(f"<{tag.name}> class='{classes}' | text='{text}'")

    print("\n--- LEAF TEXT NODES --- end ---")



print("\n\n--- 104 Once we find the EXACT ROW CONTAINER name that is common to all the rows that we want to extract---")
# i will need to find/discover this first using browser inspect or print statment etc
container_name_for_required_rows = "Card_Card__bLarm"
#cards = soup.find_all("div", class_=container_name_for_required_rows)
# Card_Card__bLarm is used for multiple things - filter modal cards, sort dialog cards, actual ETF/security cards
# so we need to add a further filtering criteria
# <div class="Card_Card__bLarm Card_Card_hoverable__EO_wM Card_Card_background_white__KmO5f Card_Card_shadow_level3__AuN_A Card_Card_shadowOnHover_level4__ljigY" data-test-id="securityItem">
cards = soup.find_all("div", attrs={"data-test-id": "securityItem"})
print("Number of cards found for", container_name_for_required_rows, " =", len(cards))


print("\n\n--- 105 Print some cards data---")
for card in cards[:3]:
    print("\n-------- FOR LOOP ------")
    #fn_get_all_subnodes_info(card)
    #fn_print_leaf_text_nodes(card)
    print(extract_card_data(card))





# Why this is extremely useful (and why pros do this)
# This technique lets you:
# ✅ Identify stable extraction anchors
# ✅ Spot duplicated text sources
# ✅ See where React components split content
# ✅ Avoid brittle XPath / class guessing
# ✅ Build future-proof scrapers
# You’ve basically built your own DOM introspection tool
def traverse_dom_table(dom_node, level=0, max_depth=None):
    """
    Recursively walk the DOM tree and print:
    LEVEL | class / id | tag type | own text
    """

    # Stop recursion if depth limit reached
    if max_depth is not None and level > max_depth:
        return

    # ---------- TEXT NODE ----------
    if isinstance(dom_node, NavigableString):
        text = dom_node.strip()
        if text:
            print(f"{level:02d} | TEXT | text | {text}")
        return

    # ---------- TAG NODE ----------
    if isinstance(dom_node, Tag):
        tag_type = dom_node.name

        # Prefer class name, fallback to id
        class_list = dom_node.get("class", [])
        class_name = " ".join(class_list) if class_list else ""
        node_id = dom_node.get("id", "")

        node_label = class_name or node_id or "(no-class)"

        # Extract ONLY direct text (avoid duplicates)
        own_text = " ".join(
            t.strip()
            for t in dom_node.find_all(string=True, recursive=False)
            if t.strip()
        )

        print(
            f"{level:02d} | {node_label} | {tag_type} | {own_text}"
        )

        # Recurse into children
        for child in dom_node.children:
            traverse_dom_table(child, level + 1, max_depth)




# 🔍 Entire document (be careful – very verbose)
#traverse_dom_table(soup, max_depth=10)

# 🔍 Just one card (recommended)
print("\n--- 108  traverse_dom_table for 1 card ---")
card = soup.find("div", class_="Card_Card__bLarm")
traverse_dom_table(card, max_depth=8)

