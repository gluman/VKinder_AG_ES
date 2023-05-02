import psycopg2
import os
from Settings import db_name, db_host, db_user, db_pass
from time import sleep

def insert_partners(crit1, crit2, crit3):
    pass

def show_results():
    pass

def save_person_to_db(id):
    with psycopg2.connect(database=db_name, user=db_user, password=db_pass, host=db_host) as conn:
        with conn.cursor() as cur:
            cur.execute(""" 
                    INSERT INTO person(id_vk_person)
                    VALUES(%s)
                    ON CONFLICT
                    DO NOTHING;
                   """, (id,))
            conn.commit()
    return

def save_result(result, id_person, sex, age, city):
    partners_items = result
    for item in partners_items:
        name = item['first_name']
        surname = item['last_name']
        id_vk = item['id']
        with psycopg2.connect(database=db_name, user=db_user, password=db_pass, host=db_host) as conn:
            with conn.cursor() as cur:
                cur.execute("""                 
                                WITH pid as (
                                SELECT id_person 
                                FROM person
                                WHERE id_vk_person = %s
                                )
                               
                               INSERT INTO partners(
                                                id_person,
                                                id_vk_partner, 
                                                name_, 
                                                surname, 
                                                sex,
                                                age_,
                                                city
                                                )
                                VALUES((SELECT * FROM pid), %s, %s, %s , %s, %s, %s)
                                ON CONFLICT
                                DO NOTHING
                                RETURNING id_partner;
                              """, (str(id_person), str(id_vk), name, surname, sex, str(age), city))
                conn.commit()


def save_photo_to_db(owner_id, photos):
    photo_folder = 'Tempary_saved_photos/'.format(owner_id)
    for photo in photos:
        with open(os.path.join(photo_folder, '%s.jpg' % photo['id_photo']), 'rb') as f:
            with psycopg2.connect(database=db_name, user=db_user, password=db_pass, host=db_host) as conn:
                with conn.cursor() as cur:
                    cur.execute("""                 
                        WITH part_id as (
                        SELECT id_partner
                        FROM partners
                        WHERE id_vk_partner = %s
                        )
                        INSERT INTO partners_photos(
                                        id_partner, 
                                        photo, 
                                        photo_link, 
                                        num_like,
                                        )
                        VALUES((SELECT * FROM part_id), %s, %s , %s, %s)
                        ON CONFLICT
                        DO NOTHING
                        RETURNING id_partner;
                        """, (str(owner_id), psycopg2.Binary(f), photo['url_photo'],  photo['likes']))
                    conn.commit()




def update_result(info):
    pass