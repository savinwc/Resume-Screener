import os
import pdfminer
import pdfminer.high_level
import pdfminer.layout
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import io
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
from io import BytesIO
from pdfminer.high_level import extract_text
import webbrowser
import base64
from django.shortcuts import render
def preprocess_text(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stop_words]
    preprocessed_text = ' '.join(words)
    return preprocessed_text


def screen_resume(pdf_path, job_description):
    with open(pdf_path, 'rb') as f:
        out = io.StringIO()
        pdfminer.high_level.extract_text_to_fp(f, outfp=out, laparams=pdfminer.layout.LAParams())
        text = out.getvalue()
    preprocessed_resume = preprocess_text(text)
    preprocessed_job_description = preprocess_text(job_description)
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([preprocessed_resume, preprocessed_job_description])
    similarity_score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return similarity_score, preprocessed_resume


def find_best_resumes(directory_path, job_description):
    resumes = []
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(directory_path, file_name)
            similarity_score, preprocessed_resume = screen_resume(file_path, job_description)
            resumes.append((file_path, similarity_score, preprocessed_resume))
    resumes.sort(key=lambda x: x[1], reverse=True)
    if not resumes:
        return 'Sorry we have no suitable candidates for the job'
    else:
        top_resumes = resumes[:3]
        ranked_resumes = [(i+1, resume[0], resume[1], resume[2]) for i, resume in enumerate(top_resumes)]
        return ranked_resumes


def job_result(job_description):
    directory_path = r'C:\Users\rodri\OneDrive\Desktop\resume_screener\resumescreener\static\data\resumes'
    ranked_resumes = find_best_resumes(directory_path, job_description)
    
    if isinstance(ranked_resumes, str):
        # No suitable candidates found
        print(ranked_resumes)
        return
        
    # Print job description and top 3 resumes with their ranking
    print(f'\nEntered job description: {job_description}\n')
    print('Top 3 Resumes:\n')
    for rank, resume_path, similarity_score, preprocessed_resume in ranked_resumes:
        print(f'Rank: {rank}')
        print(f'Resume PDF: {resume_path}')
        print(f'Similarity score: {similarity_score}\n')
    
    # Extract text from the best matching resume PDF
    best_resume_path = ranked_resumes[0][1]
    # resume_text = extract_text(best_resume_path)
    
    # # Generate the wordcloud based on the text from the best matching resume
    # wordcloud = WordCloud().generate(resume_text)
    
    # # Display the wordcloud
    # webbrowser.open(best_resume_path)
    # image_bytes = BytesIO()
    # wordcloud.to_image().save(image_bytes, format='PNG')
    # image_data_base64 = base64.b64encode(image_bytes.getvalue()).decode('utf-8')
    # image_data_url = 'data:image/png;base64,' + image_data_base64
    return job_description, best_resume_path, ranked_resumes, best_resume_path
    

def search(request):
    if request.method=='POST':
        jd=request.POST.get('search-data','')
        job_description,best_resume,best_similarity_score,best_resume=job_result(jd)
        # return HttpResponse(job_description+best_resume+str(best_similarity_score))
        return render(request,'demo.html',{'job_description':job_description,'best_resume':best_resume,'best_similarity_score':best_similarity_score,'resume_url':best_resume})
    
        
    return render(request,'search.html')



    




    # import pandas as pd
    # import matplotlib.pyplot as plt
    # import warnings
    # import seaborn as sns
    # warnings.filterwarnings('ignore')


    # resumeDataSet = pd.read_csv(r'C:\Users\rodri\OneDrive\Desktop\new_resume\resume_dataset.csv' ,encoding='utf-8')
    # resumeDataSet['cleaned_resume'] = ''
    # resumeDataSet.head()

    # print ("Displaying the distinct categories of resumes uploaded -")
    # print (resumeDataSet['Category'].unique())

    # print ("Displaying the distinct categories of resume and the number of records belonging to each category -")
    # print (resumeDataSet['Category'].value_counts())


    # plt.figure(figsize=(30,15))
    # plt.xticks(rotation=90)
    # sns.countplot(y="Category", data=resumeDataSet)
    # plt.show()


    # import re
    # def cleanResume(resumeText):
    #     resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
    #     resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
    #     resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
    #     resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
    #     resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)  # remove punctuations
    #     resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText) 
    #     resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    #     return resumeText
        
    # resumeDataSet['cleaned_resume'] = resumeDataSet.Resume.apply(lambda x: cleanResume(x))
