"""
Import team data that was downloaded from the cfbd site to ensure my names/IDs are consistent
with where I'm pulling game data
"""
import psycopg2
import csv
from env import CONNECTION_STRING

team_data_file = 'team_data/team_info_from_cfbd_2022.csv'
sql = """INSERT INTO teams(team_name, conference, cfbd_team_id, mascot, division, team_abbr, 
                            cfbd_venue_id, location_city, timezone, location_state, location_capacity, location_venue)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

conn = psycopg2.connect(CONNECTION_STRING)
cur = conn.cursor()

with open(team_data_file, newline='', encoding='utf-8-sig') as f:
    teamReader = csv.DictReader(f, delimiter=',')
    for row in teamReader:
        print(f'row: {row}')
        record_list = (row['school'], row['conference'], row['id'], row['mascot'], row['division'],
                       row['abbreviation'], row['location.venue_id'], row['location.city'],
                       row['location.timezone'], row['location.state'], row['location.capacity'], row['location.name'])
        cur.execute(sql, record_list)
        conn.commit()

cur.close()

