import requests
from bs4 import BeautifulSoup
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# NTV haber sitesinden veri çek
url = 'https://www.ntv.com.tr/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Başlıkları çekme (NTV'nin yapısına göre)
# Haber başlığının olduğu etiket ve class ismi :)
titles = soup.find_all('a', class_='card-text-link')

headline_list = [title.get_text().strip() for title in titles]

# Başlıkları kontrol edin
if not headline_list:
    print("Başlık bulunamadı! Lütfen HTML yapısını kontrol edin.")
else:
    print(f"{len(headline_list)} başlık bulundu.")

# Verileri Pandas DataFrame'e dönüştür
df = pd.DataFrame(headline_list, columns=['Headline'])
print(df.head())

# Başlıkların duygu analizi
# Bu kısmı doğru yapamamış olabilirim !
def get_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'Pozitif'
    elif analysis.sentiment.polarity < 0:
        return 'Negatif'
    else:
        return 'Nötr'

df['Sentiment'] = df['Headline'].apply(get_sentiment)

# Sonuçları ekrana yazdır
print(df)

# Duygu analizi sonuçlarını görselleştirme
df['Sentiment'].value_counts().plot(kind='bar', color=['green', 'red', 'blue'])
plt.title('Başlıkların Duygu Dağılımı')
plt.xlabel('Duygu')
plt.ylabel('Frekans')
plt.show()
