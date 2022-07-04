"""
Import team data that was downloaded from the cfbd site to ensure my names/IDs are consistent
with where I'm pulling game data
"""
import psycopg2
import csv

team_data_file = 'team_info_from_cfbd.csv'
sql = """INSERT INTO teams(team_name, conference, cfbd_team_id, mascot, division, team_abbr, 
                            cfbd_venue_id, location_city, timezone, location_state, location_capacity, location_venue)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

conn = psycopg2.connect("dbname='cfb_rankings' user='postgres' password='postgres' host='localhost' port=5433")
cur = conn.cursor()

with open(team_data_file, newline='') as f:
    teamReader = csv.DictReader(f, delimiter=',')
    for row in teamReader:
        record_list = (row['school'], row['conference'], row['id'], row['mascot'], row['division'],
                       row['abbreviation'], row['location.venue_id'], row['location.city'],
                       row['location.timezone'], row['location.state'], row['location.capacity'], row['location.name'])
        cur.execute(sql, record_list)
        conn.commit()

cur.close()

