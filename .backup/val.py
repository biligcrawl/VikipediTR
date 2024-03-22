import pandas as pd

data = pd.read_csv("wikipedia.csv")

print(data.head())

data.isnull().sum()

valid_urls = data['url'].str.startswith('http://') | data['url'].str.startswith('https://')
if valid_urls.all():
    print("Tüm URL'ler geçerli.")
else:
    print("Bazı URL'ler geçerli formatta değil.")

invalid_url_count = (~valid_urls).sum()
print(f"Invalid: {invalid_url_count}")

if invalid_url_count > 0:
    print("Valid:")
    print(data.loc[~valid_urls, 'url'])
