# Plagiarism-Detection

### Motivation:
This project started before CSI held its 21 Days of DSA Challenge. A common issue with small-scale or club-level coding challenges is the reliance on providing problem statements from the internet, whose solutions are readily available. Our goal was to eliminate this problem by selecting a few problem statements and scraping their entire solution codebase. This allowed us to run plagiarism checks on the entries we received through our own coding challenges. 

Plagiarism Detection operates on a straightforward mechanism: we receive submissions from students based on a given problem statement and then compare their solutions against those stored in our repository. Upon comparison, a 'Similarity Score' is generated, and if it exceeds a predefined threshold, we identify the submission as copied or exhibiting plagiarism.

### Team Members:
Mentor - Viren Khatri
Web Scrapping - Rahul Metre, Shreya Mukherjee
Plagiarim Mechanism - Danish Shaikh, Harsh Kansara, Ayush Kulshesthra
Data Pipeline - Mitheelesh Katyarmal 

### Code
There are 2 main part to this project: <br>1. The similarity Checker <br>2. The Data Pipeline

#### The Similarity Checker:
**winnowing_fingerprint(text, window_size=4):**
- This function takes a text input and an optional window size parameter.
- It preprocesses the text by removing whitespace and then generates five-grams from the text.
- For each five-gram, it calculates a hash value by summing the ASCII values of its characters.
- It then creates overlapping windows of hash values with the specified window size.
- Within each window, it selects the minimum hash value as the fingerprint.
- Finally, it returns a list of fingerprints.

**jaccard_similarity(doc1, doc2):**
- This function calculates the Jaccard similarity between two sets of fingerprints (documents).
- It converts the input fingerprints into sets.
- It computes the Jaccard similarity coefficient, which is the ratio of the size of the intersection of the two sets to the size of their union.
- The result is returned as the Jaccard similarity between the two documents.
 
**check_similarity(fp_doc1, fp_doc2, threshold=0.4):**
- This function takes two sets of fingerprints representing two documents and an optional threshold parameter.
- It calls the jaccard_similarity function to compute the Jaccard similarity between the documents.
- Then, it calculates the percentage of similarity based on the Jaccard similarity coefficient.
- Finally, it returns the percentage similarity between the two documents.

#### The Data Pipeline:




