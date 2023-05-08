import shutil

import psycopg2
import os
from Settings import db_name, db_host, db_user, db_pass


def show_results():
    pass


def db_save_person_to_db(id):
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


def db_save_result(result, id_person, sex, age, city):
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


def db_save_photo_to_db(owner_id, photos):
    for photo in photos:
        photo_path = os.path.join('Tempary_saved_photos', f'{owner_id}', f"{photo['id_photo']}.jpg")
        with open(photo_path, 'rb') as f:
            with psycopg2.connect(database=db_name, user=db_user, password=db_pass, host=db_host) as conn:
                with conn.cursor() as cur:
                    data = f.read()
                    _exec = cur.execute("""                 
                        WITH part_id as (
                        SELECT id_partner
                        FROM partners
                        WHERE id_vk_partner = %s
                        )
                        INSERT INTO partners_photos(
                                        id_partner,
                                        id_vk_photo, 
                                        photo, 
                                        photo_link, 
                                        num_like
                                        )
                        VALUES((SELECT * FROM part_id), %s, %s, %s , %s)
                        ON CONFLICT
                        DO NOTHING
                        RETURNING id_partner;
                        """, (str(owner_id), str(photo['id_photo']), psycopg2.Binary(data), photo['url_photo'], str(photo['likes'])))
                    conn.commit()

    shutil.rmtree(os.path.join('Tempary_saved_photos', f'{owner_id}'))

def db_get_partners(criteria):
    select = """ SELECT id_partner, id_person, id_vk_partner, name_, surname, sex, profile_link, age_, city, favorite 
                  FROM partners
              """
    if criteria == 'favorites':
        where = 'WHERE partners.favorive = True'
        select += where
    if criteria == 'all':
        select = select
    else:
        where = f'WHERE partners.id_partner in {criteria}'
        select += where

    with psycopg2.connect(database=db_name, user=db_user, password=db_pass, host=db_host) as conn:
        with conn.cursor() as cur:
            cur.execute(select)
            result = cur.fetchall()
            conn.commit()
    return result

def db_get_current_partner(id):
    select = """ SELECT id_partner, id_person, id_vk_partner, name_, surname, sex, profile_link, age_, city, favorite 
                         FROM partners
                     """
    where = f'WHERE partners.id_partner = {id}'
    select += where
    with psycopg2.connect(database=db_name, user=db_user, password=db_pass, host=db_host) as conn:
        with conn.cursor() as cur:
            cur.execute(select)
            result = cur.fetchall()
            conn.commit()
    return result

def db_attach_current_partner_photo():
    pass

