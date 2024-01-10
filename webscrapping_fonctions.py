from urllib.request import urlopen, Request
import os
import numpy as np        
import pandas as pd
import matplotlib.pyplot as plt
import rasterio
from pylab import * 
from osgeo import gdal
import csv 
from PIL import Image
import seaborn as sns
from urllib import request
from bs4 import BeautifulSoup
import mechanicalsoup
import json
import requests   
from bs4 import BeautifulSoup   
from urllib.error import HTTPError
from collections import defaultdict


def scrap_html(url, languages_to_check =NaN, description=NaN, lang = NaN, href = NaN, img = NaN, df_url=pd.DataFrame({}), df_bouton=pd.DataFrame({}), refsite_externe = NaN,font_ref=NaN, src_js=NaN, src_css=NaN, youtube = NaN, facebook=NaN, linkedin=NaN, instagram=NaN, twitter=NaN, boutons=NaN, dd=NaN, gt="Non", ga="Non"):
    try: 
        img=[]
        vid=[]
        href=[]
        lang=[]
        srcs=[]
        fonction=[]
        font_ref=[]
        refsite_externe=[]
        font_ref=[]
        src_js=[]
        src_css=[]
        boutons=[]

        Request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"}) # headers est là pour mod security 
        #detecting the scraping bot of the urllib and blocking it. Therefore, in order to resolve it, we have to include user-agent/s in our scraper. 
        # This will ensure that we can safely scrape the website without getting blocked and running across an error. source : https://www.pythonpool.com/urllib-error-httperror-http-error-403-forbidden/
        page = urlopen(Request_site)

        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        # Get title 
        title = soup.title

        # Get images 
        img_tags = soup.find_all('img', src=True)
        for img_tag in img_tags:
            img_url = img_tag['src']
            img.append(img_url)

        # Get videos
        video_tags = soup.find_all('mov')
        for vid_tag in video_tags:
            vid_url = vid_tag['href']
            vid.append(vid_url)

        links = soup.find_all('link')
        for link in links:
            href.append(link.attrs.get("href"))

        # Description pb : ne la trouve pas systématiquement pour une raison mystère
        for script in soup.find_all('script'):
            text = script.text
            presenceF = text.find("function")
            if presenceF != -1:
                try :
                    dict = json.loads(script.text) # convert to dict to be able to have key value
                    description = dict["description"]
                except:
                    print("")

            # Sources
            src = script.get("src")
            if src is not None : 
                if(src.split('.'))[1] == "js":
                    src_js.append(src)
                if "googletagmanager" in src: 
                    gt = "oui"
                if "analytics" in src: 
                    ga = "oui"
                else: 
                     srcs.append(src)      

        # Github
        if "github" in html.lower():
            github_idx = html.find("https://github")
            fin_github = html.find(' ', github_idx) # trouve l'index du prochain espace avec que github soit trouvé dans le html
            github = html[github_idx:fin_github]
        else : 
            github = NaN
        
        dd = defaultdict(list)
        # Récupérer les boutons 
        for bouton in soup.find_all("button"):
            boutons.append(bouton.attrs)
            for k, v in bouton.attrs.items(): 
            # Append the attribute value to the corresponding key in the defaultdict
                if v is empty :
                    v = NaN
                else: 
                    dd[k].append(v) # de cette manière on aura pour chaque globes ses clés uniques avec toutes ses valeurs associées
        

        # Réference aux liens externes
        try:
            lang.append(soup.html["lang"])
        except:
            "No language in html lang="
        href = soup.find_all(lambda tag: 'href' in tag.attrs)
        url_basename = (url.split('/')[2])
        for ref in href: 
            if "https://" in str(ref["href"]):
                if url_basename not in str(ref["href"]):
                    refsite_externe.append(ref["href"])
            if 'hreflang' in str(ref):
                lang.append(ref['hreflang'])

        # Réference aux fonts 
        for ref in href:         
            if "font" in str(ref): 
                href_ref = ref["href"]
                font_ref.append(href_ref)
            if ref["href"].split('.')[-1] == "css":
                src_css.append(ref["href"])
            if "facebook" in str(ref): 
                facebook = ref["href"]
            if "instagram" in str(ref): 
                instagram = ref["href"]
            if "twitter" in str(ref): 
                twitter = ref["href"]
            if "youtube" in str(ref): 
                youtube = ref["href"]
            if "linkedin" in str(ref): 
                linkedin = ref["href"]
            


        # Créer un dataframe dtype sert à indiquer que les éléments sont des listes, le dataframe se fera dans une colonne 

        df_url = pd.DataFrame({'Titre': title,'URL':url, 'Image': [img], dtype:'list', 'Langues': [lang], dtype:'list', 'Description du projet':description, 'Sources':[srcs], dtype:'list', \
                               'Github':github,"Renvoie vers un autre site":[refsite_externe], dtype:'list', "Liens vers font":[font_ref], dtype:'list', \
                                "Scripts Javascript":[src_js], dtype:'list', "Scripts CSS": [src_css], dtype:'list', "Youtube": youtube, "Facebook": facebook, "Instagram": instagram, "Linkedin": linkedin, "twitter": twitter, "Boutons":[boutons], "GoogleTagManager": gt, "GoogleAnalytics":ga})
        df_bouton = pd.DataFrame.from_records([dd])
        df_bouton["URL"] = url
    except HTTPError:  # Est-ce qu'on relève l'erreur quand l'URL ne fonctionne pas ?
        print("HTTP Error 404: Not Found")
        print("Cet", url, "ne fonctionne pas")

    return df_url, df_bouton
"""
#Fonctions 
        if "function" in html.lower():

            # [a-z]{14,20} = cherche 0 à 20 lettres de l'alphabet, [(+*)]{2} cherche 2 caractères dans : '(', '+', '*' ou ')'

            # TROUVE LE TOUT DEBUT DE LA FONCTION - A NE PAS MODIFIER
            idx_debut = re.search("function [a-z]{0,20}[(+*)]{2}{", html).span()[0] 

            # morceau de la fonction qu'on analyse
            idx_i = re.search("function [a-z]{0,20}[(+*)]{2}{", html).span()[-1]

            # Trouve l'index du prochain } du html // span() donne l'index de début et de fin d'une chaine

            idx_fin_i = html.find('}', int(idx_debut)) 
            fonctions = html[idx_debut:idx_fin_i+1] 
            # S'il y a une autre { qui s'ouvre avant que le } se ferme
            if html.find('{', idx_i) < idx_fin_i: 
                # On trouve la prochaine { == fonctions imbriquées
                idx_i = html.find('{', int(idx_i)) 
                fonction.append(html[idx_debut:idx_fin_i+1])
            else : 
                fonction.append(html[idx_debut:idx_fin_i+1])
        else : 
            fonctions = NaN

            'Fonctions':[fonctions],dtype:'list',
            
"""


def reseau_sociaux(url_instagram = NaN, url_facebook=NaN , df_sortie=pd.DataFrame({}), Followers = NaN, Following= NaN,  Posts=NaN,  jaime=NaN, en_parle=NaN, pers_ici=NaN, followers_fb=NaN, description= NaN):

# Trouve les followers, following et nombre de posts instagram
    if not pd.isna(url_instagram) and str(url_instagram).lower() != "nan" :
        Request_site = Request(url_instagram, headers={"User-Agent": "Mozilla/5.0"})
        page = urlopen(Request_site)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        soup = BeautifulSoup(html, "html.parser") # La requête renvoie tantôt vers la page instagram du globe ou vers le portail de login, ce qui rend le parsage impossible

        meta_insta = soup.find_all("meta")
        for mi in meta_insta: 
            if "See Instagram photos and videos from" in str(mi).lower():
                texte = str(mi)
                Followers, Following, Posts = texte.split(',')
                #Posts = re.search("[0-9,]+\s* Posts", str(mi)).group()
                #Followers = re.search("[0-9,]+\s |[0-9]+ K \s Followers", str(mi)).group() # group() permet d'avoir le match, le [0-9,]+ permet d'avoir tous les chiffres avec des virgules
                #Following = re.search("[0-9,]+\s* Following", str(mi)).group()
                print(Posts, Followers, Following)

# Trouve les mentions j'aime, en parlent et personnes ici sur la page facebook
    if not pd.isna(url_facebook) and str(url_facebook).lower() != "nan" : 
        Request_site = Request(url_facebook, headers={"User-Agent": "Mozilla/5.0"}) 
        page = urlopen(Request_site)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        meta_fb = soup.find_all("meta")
        for mf in meta_fb: 
            if "aime" in str(mf).lower():
                for i in (str(mf)).split('.'):
                    # condition pour trouver le nombre de j'aime
                    if "aime" in str(i):
                        if len(i.split('·')) == 3: 
                            jaime, en_parle, pers_ici = i.split('·')
                        if len(i.split('·')) == 2: 
                            jaime, en_parle = i.split('·')
                        if len(i.split('·')) == 1: 
                            jaime = i
                    # faire une condition pour trouver une phrase (genre si il y a plus de 5 espaces dans la chaine de caractères)
                    if len(i.split(' ')) > 5 and "aime" not in str(i): 
                        description = i

    df_sortie = pd.DataFrame({'Instagram': [url_instagram], "Facebook":[url_facebook],'Followerss': [Followers],'Followingg':[Following], 'Postss': [Posts], 'Followers FB': [followers_fb], 'Jaime': [jaime], 'En_parle':[en_parle], 'Pers_ici' : [pers_ici], "Description facebook": [description]})
    return(df_sortie)



def serveur(url):
    # !pip install futures # à décommenter 
    # !pip install python-whois # à décommenter

    import whois

    dm_info = whois.whois(url)
    dm_info.expiration_date  # dates converted to datetime object
    datetime.datetime(2022, 8, 13, 4, 0)
    dm_info.text

    df_sortie = pd.DataFrame({"URL": [url],  "Entreprise": [dm_info.registrar], "Date de création": [dm_info.creation_date], "Date d'expiration": [dm_info.expiration_date],"Pays": [dm_info.country], "Ville": [dm_info.city], "Emails": [dm_info.emails]})
    return df_sortie