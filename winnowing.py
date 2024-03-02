''' Winnowing algorithm :
Step 1 : Some text - my name is daanish and i'm trying out winnowing

Step 2 : Remove irrelevant features - mynameisdaanishandimtryingoutwinnowing

Step 3 : Sequence of 5-grams derived from the text :
[mynam yname namei ameis meisd eisda isdaa sdaan daani aanis anish nisha ishan shand handi andim ndimt dimtr imtry mtryi tryin rying yingo 
ingou ngout goutw outwi utwin twinn winno innow nnowi nowin owinw winno innin nning]

Step 4 : Generate hash values for each 5-grams
mynam: 13+25+1+14+1=54
yname: 25+14+1+13+5=58
namei: 14+1+13+5+9=42
ameis: 1+13+5+9+19=47
meisd: 13+5+9+19+4=50
eisda: 5+9+19+4+1=38
isdaa: 9+19+4+1+1=34
sdaan: 19+4+1+1+14=39
daani: 4+1+1+14+9=29
aanis: 1+1+14+9+19=44
anish: 1+14+9+19+8=51
nisha: 14+9+19+8+1=51
ishan: 9+19+8+1+14=51
shand: 19+8+1+14+4=46
handi: 8+1+14+4+9=36
andim: 1+14+4+9+13=41
ndimt: 14+4+9+13+20=60
dimtr: 4+9+13+20+18=64
imtry: 9+13+20+18+25=85
mtryi: 13+20+18+25+9=85
tryin: 20+18+25+9+14=86
rying: 18+25+9+14+7=73
yingo: 25+9+14+7+15=70
ingou: 9+14+7+15+21=66
ngout: 14+7+15+21+20=77
goutw: 7+15+21+20+23=86
outwi: 15+21+20+23+9=88
utwin: 21+20+23+9+14=87
twinn: 20+23+9+14+14=80
winno: 23+9+14+14+15=75
innow: 9+14+14+15+23=75
nnowi: 14+14+15+23+9=75
nowin: 14+15+23+9+14=75
owinw: 15+23+9+14+23=84
winno: 23+9+14+23+15=84
innin: 9+14+23+15+14=75
nning: 14+23+15+14+7=73

Sequence of hash values : [54, 58, 42, 47, 50, 38, 34, 39, 29, 44, 51, 51, 51, 46, 36, 
41, 60, 64, 85, 85, 86, 73, 70, 66, 77, 86, 88, 87, 80, 75, 75, 75, 75, 84, 75, 75, 73]

Step 5 : Generate windows of hashes of length 4 :
(54, 58, 42, 47)
(58, 42, 47, 50)
(42, 47, 50, 38)
(47, 50, 38, 34)
(50, 38, 34, 39)
(38, 34, 39, 29)
(34, 39, 29, 44)
(39, 29, 44, 51)
(29, 44, 51, 51)
(44, 51, 51, 51)
(51, 51, 51, 46)
(51, 51, 46, 36)
(51, 46, 36, 41)
(46, 36, 41, 60)
(36, 41, 60, 64)
(41, 60, 64, 85)
(60, 64, 85, 85)
(64, 85, 85, 86)
(85, 85, 86, 73)
(85, 86, 73, 70)
(86, 73, 70, 66)
(73, 70, 66, 77)
(70, 66, 77, 86)
(66, 77, 86, 88)
(77, 86, 88, 87)
(86, 88, 87, 80)
(88, 87, 80, 75)
(87, 80, 75, 75)
(80, 75, 75, 75)
(75, 75, 75, 75)
(75, 75, 75, 84)
(75, 75, 84, 75)
(75, 84, 75, 75)
(84, 75, 75, 73)
(75, 75, 73)

Step 6 : Generate fingerprints selected by winnowing for each window

DEFINITION 1 (WINNOWING). In each window select the minimum hash value. If there is more than one hash with the minimum value,
select the rightmost occurrence. Now save all selected hashes as the fingerprints of the document.

[42, 42, 38, 34, 34, 29, 29, 29, 29, 44, 46, 36, 36, 36, 36, 41, 60,
64, 41, 60, 64, 73, 70, 66, 66, 66, 66, 77, 80, 75, 75, 75, 75, 75, 75, 73]

Step 7 : Store these fingerprints with their positional information. (find another way)
eg). If the first fingerprint is stored at location row 3 column 10, then it should be stored as 
[42, 3, 10]
eg). If the next fingerprint is stored at location row 5 column 4, then it should be stored as 
[38, 5, 4]
'''

# # Example usage:
# data_to_hash = "example_data"
# hashed_value = sha256_hash(data_to_hash)
# print(f"SHA-256 Hash: {hashed_value}")

def winnowing_fingerprint(text, window_size=4):
    # Step 2: Remove irrelevant features
    text = "".join(text.split())
    print(text)

    # Step 3: Generate 5-grams
    n = len(text)
    five_grams = []
    for i in range(n - 4):
        five_grams.append(text[i:i+5])

    # Step 4: Generate hash values for each 5-gram
    hash_values = []
    for gram in five_grams:
        # hash_values.append(int(sum((ord(char)*gram.index(char)) for char in gram)/5)) 
        hash_values.append(sum(ord(char) for char in gram))
        
    # Step 5: Generate windows of hashes of specified length
    windows = []

    # Iterate through the indices for creating windows
    for i in range(len(hash_values) - window_size + 1):
        window = hash_values[i:i + window_size]
        windows.append(window)  #sliding windows algo to be more polished.

    # Step 6: Winnowing - Select minimum hash in each window
    fingerprints = [min(window) for window in windows]

    # Step 7: Store fingerprints with positional information
    # fingerprint_positions = []
    # for i, fingerprint in enumerate(fingerprints):
    #     rightmost_occurrence = len(hash_values) - hash_values[::-1].index(fingerprint) - 1
    #     fingerprint_positions.append([fingerprint, rightmost_occurrence, i+1])

    return fingerprints

    #Step 8 : Devise a comparison technique to compare fingerprints 

# Example usage
text = "my name is daanish and i'm trying out winnowing"
# fingerprints, fingerprint_positions = winnowing_fingerprint(text)
fingerprints = winnowing_fingerprint(text)
# ----------------------------------------------------------------------------------------
# Output the results
print("Sequence of hash values:", fingerprints)
# print("Fingerprints with positional information:", fingerprint_positions)
# ------------------------------------WAY ONE--------------------------------------------------

# def check_similarity(fp_doc1, fp_doc2, threshold=0.4):
#     # Get common fingerprints 
#     common = set(fp_doc1).intersection(set(fp_doc2))
    
#     # Get length of longer doc
#     len_long = max(len(fp_doc1), len(fp_doc2))
    
#     # Calculate fingerprint index 
#     fp_index = len(common) / len_long
    
#     # Check threshold 
#     if fp_index > threshold:
#         print("Documents are similar")
#     else:
#         print("Documents are dissimilar")
        
#     # Calculate and return percentage similarity
#     perc_similar = fp_index * 100
#     return perc_similar

def jaccard_similarity(doc1, doc2):
    # Convert fingerprints to sets
    set_doc1 = set(doc1)
    set_doc2 = set(doc2)
    
    # Calculate Jaccard similarity
    jaccard_sim = len(set_doc1.intersection(set_doc2)) / len(set_doc1.union(set_doc2))
    
    return jaccard_sim

def check_similarity(fp_doc1, fp_doc2, threshold=0.4):
    # Calculate Jaccard similarity
    jaccard_sim = jaccard_similarity(fp_doc1, fp_doc2)
    
    # Check threshold 
    if jaccard_sim > threshold:
        print("Documents are similar")
    else:
        print("Documents are dissimilar")
        
    # Calculate and return percentage similarity
    perc_similar = jaccard_sim * 100
    return perc_similar

text1 = "public class main {	public static void main(String[] args) {		System.out.println(factorial(10));	}	public static int factorial(int n)    {		int ret = 1;        for (int i = 1; i <= n; ++i) ret *= i;        return ret;    }}"
text2 = "	public class main {		static int currentFactor = 1;		static int currentResult = 1;		public static void main(String[] args) {			System.out.println(factorial(10));		}		public static int factorial(int n)     {			fac:			while(currentFactor!=n) {				currentResult *= currentFactor;				continue fac;			}			return currentResult;	    }	}"
fp2 = winnowing_fingerprint(text2) # fingerprints of doc 2
fp1 = winnowing_fingerprint(text1) # fingerprints of doc 1

# print("Sequence of the first set of hash values : ",fp1)
# print("Sequence of the second set of hash values : ",fp2)

perc_sim = check_similarity(fp1, fp2) 

print("Fingerprint Similarity:", perc_sim, "%")

## ------------------------------------WAY TWO--------------------------------------------------

def offset_difference_comparison(fingerprint1, fingerprint2):
    # Ensure fingerprints are sorted
    fingerprint1.sort()
    fingerprint2.sort()

    # Calculate differences between matching fingerprints
    differences = [abs(x - y) for x, y in zip(fingerprint1, fingerprint2)]

    # Calculate average offset
    average_offset = sum(differences) / len(differences) if differences else 0

    return average_offset

# Example usage:
text1 = "public class main {	public static void main(String[] args) {		System.out.println(factorial(10));	}	public static int factorial(int n)    {		int ret = 1;        for (int i = 1; i <= n; ++i) ret *= i;        return ret;    }}"
text2 = "public class main {	public static void main(String[] args) {		int ret = 1;for (int i = 1; i <= 10; ++i) ret *= i;		System.out.println(ret);	}}"

#text2 = "public class main {	public static void main(String[] args) {		System.out.println(factorial(10));	}public static long factorial(long n){long ret = 1;for (long i = 1; i <= n; ++i) ret *= i;return ret;}}"
fp1 = winnowing_fingerprint(text1) # fingerprints of doc 1
fp2 = winnowing_fingerprint(text2) # fingerprints of doc 2
average_offset = offset_difference_comparison(fp1, fp2)
print(f"Average Offset: {average_offset}")

## ------------------------------------WAY TWO--------------------------------------------------

def longest_common_sequence(fingerprint1, fingerprint2):
    # Find the length of the longest common sequence
    common_sequence = []
    current_sequence = []

    for i, fp1 in enumerate(fingerprint1):
        if fp1 in fingerprint2:
            current_sequence.append(fp1)
        else:
            if len(current_sequence) > len(common_sequence):
                common_sequence = current_sequence.copy()
            current_sequence = []

    # Check at the end of the loop
    if len(current_sequence) > len(common_sequence):
        common_sequence = current_sequence

    return common_sequence

# Example usage:
# text1 = "public class main {	public static void main(String[] args) {		System.out.println(factorial(10));	}	public static int factorial(int n)    {		int ret = 1;        for (int i = 1; i <= n; ++i) ret *= i;        return ret;    }}"
# text2 = "public class main {	public static void main(String[] args) {		System.out.println(factorial(10));	}public static long factorial(long n){long ret = 1;for (long i = 1; i <= n; ++i) ret *= i;return ret;}}"
# fp1 = winnowing_fingerprint(text1) # fingerprints of doc 1
# fp2 = winnowing_fingerprint(text2) # fingerprints of doc 2
#longest_common_seq = longest_common_sequence(fp1, fp2)
#print(f"Longest Common Fingerprint Sequence: {longest_common_seq}")