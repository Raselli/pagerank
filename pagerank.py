import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probability_distribution = {key: 0 for key in corpus}
    
    # Links from page
    next_pages = corpus[page[0]]
    
    # Case: Page has outgoing links
    if next_pages:    
        p_next_page = damping_factor / len(next_pages)
        for next_page in next_pages:
            probability_distribution[next_page] = p_next_page
    
        # Besides outgoing links: Equal probability of choosing a page randomly
        p_choose_randomly = (1 - damping_factor) / len(probability_distribution)
        
    # Case: Page has no outgoing links -> Equal probability of choosing a page randomly
    else:
        p_choose_randomly = 1 / len(probability_distribution)  
    
    # Update probability distribution
    for webpage in probability_distribution:
        probability_distribution[webpage] += p_choose_randomly
    return probability_distribution    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    page_ranks = {key: 0 for key in corpus}
    
    # Get random key to begin with & make a first transition model  
    random_page = random.choice(list(corpus.items()))
    current_transition_model = transition_model(corpus, random_page, damping_factor)  
    
    # Pick n random pages
    for _ in range(n - 1):
        page_ranks[random_page[0]] += 1 / n
        random_page = random.choices(
                list(current_transition_model.keys()), 
                list(current_transition_model.values())
            )    
        current_transition_model = transition_model(corpus, random_page, damping_factor)
    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    
    # Assigning each page a rank of 1 / N
    initial_rank = 1 / N
    page_ranks = {key: initial_rank for key in corpus}

    # Probability of choosing a page at random 
    p_choosing_random_page = (1 - damping_factor) / N
    
    # Repetition until convergence of 0.001% is reached
    convergence = set()
    while len(convergence) < N:
        convergence.clear()

        # Iteration: PR(p) - Calculation of PageRank for page "p"
        for page_p in corpus.keys():
            
            # Sum of (probabilities of visiting page "p") / (number of links)
            sum_i = 0

            # Iteration: Each possible page "i" linked to page "p"
            for page_i, linked_pages in corpus.items():
                rank_page_i = page_ranks[page_i]
                
                # Case: Page "p" in pages linked to page "i"
                if page_p in linked_pages:
                    num_links = len(linked_pages)
                    sum_i += rank_page_i / num_links

                # Case: Page without links
                elif not linked_pages:
                    sum_i += 1 / N

            # Calculate PageRank for a page "p"
            sum_i *= damping_factor
            new_page_rank = p_choosing_random_page + sum_i

            # Check PageRank convergence of page "p"
            if abs(page_ranks[page_p] - new_page_rank) < 0.001:
                convergence.add(page_p)
            
            # Update the calculated PageRank of page "p"
            page_ranks[page_p] = new_page_rank

    # Adjust the PageRanks so that they add up to 1
    sum_pageranks = sum(page_ranks[k] for k in page_ranks)
    page_ranks = {pake_rank_key: page_rank_value / sum_pageranks for\
        pake_rank_key, page_rank_value in page_ranks.items()}
    return page_ranks


if __name__ == "__main__":
    main()
