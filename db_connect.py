import shutil

import psycopg2
import os
from Settings import db_name, db_host, db_user, db_pass


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


def update_result(info):
    pass
