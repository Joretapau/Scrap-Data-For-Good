# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 19:21:28 2016

@author: Lucas Bony
"""

from indeed import build_database
import sys
import json
import redis
from indeed.Cleaner import start_indeed
from monster.Cleaner import start_monster
#%%
def get_dataabse():
    pass

def clean_doubles(db_a, db_b):
    """
    Clean les doublons entre les deux bases de données en se servant
    du nom de l'entreprise
    """
    db = db_a
    for d_b in db_b:
        is_double = False
        for d_a in db:
            if (d_a["nom_du_poste"] == d_b["nom_du_poste"] and d_a["entreprise"] == d_b["entreprise"]):
                print d_a["nom_du_poste"]
                print d_a["entreprise"]
                print d_b["nom_du_poste"]
                print d_b["entreprise"]
                is_double = True
        if not is_double: 
            db.append(d_b)
    return db
#%%
if __name__ == "__main__":
    
    if len(sys.argv) > 4:
        #on récupère les chemins des fichiers où sont stockés les nom des jobs et les localisations
        #pour le scrap
        scrap_job_titles_fp = sys.argv[1]
        scrap_locations_radius_fp = sys.argv[2]
        tags_fp = sys.argv[3]
        result_nb = 1100
    else:
        scrap_job_titles_fp = "job_titles"
        scrap_locations_radius_fp = "scrap_locations"
        tags_fp = "tags"
        result_nb = 220
    
    scrap_job_titles = json.load(open(scrap_job_titles_fp, "rb"), encoding='latin-1')["titles"]
    scrap_locations_radius = json.load(open(scrap_locations_radius_fp, "rb"), encoding='latin-1')["locations"]
    tags = json.load(open(tags_fp, "rb"), encoding='latin-1')["tags"]
    
    indeed = start_indeed(scrap_job_titles, scrap_locations_radius, tags, result_nb)
    monster = start_monster(scrap_job_titles, scrap_locations_radius, tags)
    
    db = clean_doubles(indeed, monster)
    r = redis.StrictRedis(db=1)
    for cnt, offre in enumerate(db):
        r.set(str(cnt), offre)