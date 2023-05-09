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
        link = 'https://vk.com/' + item['screen_name']
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
                                                profile_link,
                                                age_,
                                                city
                                                )
                                VALUES((SELECT * FROM pid), %s, %s, %s , %s, %s, %s, %s)
                                ON CONFLICT
                                DO NOTHING
                                RETURNING id_partner;
                              """, (str(id_person), str(id_vk), name, surname, sex, link, str(age), city))
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

def db_get_partners(criteria, owner_id):
    select = """ SELECT id_partner, id_person, id_vk_partner, name_, surname, sex, profile_link, age_, city
                  FROM partners
              """
    if criteria == 'top':
        where = 'WHERE partners.favorite = True and '
        select += where
    elif criteria == 'all':
        where = 'WHERE '
        select += where
    else:
        where = f'WHERE partners.id_partner in {criteria} and '
        select += where

    select += f"partners.id_person = (SELECT id_person FROM person WHERE person.id_vk_person = '{owner_id}');"

    with psycopg2.connect(database=db_name, user=db_user, password=db_pass, host=db_host) as conn:
        with conn.cursor() as cur:
            cur.execute(select)
            result = cur.fetchall()
            conn.commit()
    return result

def db_get_current_partner(id):
    where = f"WHERE id_partner = {id}"
    select = f"""
                SELECT id_partner, id_person, id_vk_partner, name_, surname, sex, profile_link, age_, city 
                FROM partners
                {where};
                 """


    with psycopg2.connect(database=db_name, user=db_user, password=db_pass, host=db_host) as conn:
        with conn.cursor() as cur:
            cur.execute(select)
            result = cur.fetchall()
            conn.commit()
    return result

def db_attach_current_partner_photo(id):
    select = """ SELECT id_photos, id_partner, id_vk_photo, photo, photo_link, num_like 
                 FROM partners_photos
                 """
    where = f'WHERE partners_photos.id_partner = {id}'
    select += where
    select += ';'
    with psycopg2.connect(database=db_name, user=db_user, password=db_pass, host=db_host) as conn:
        with conn.cursor() as cur:
            cur.execute(select)
            result = cur.fetchall()
            conn.commit()
    return result

def db_change_favorites(id, context):
    if context == 'add':
        favorite_bool = 'true'
    elif context == 'rem':
        favorite_bool = 'false'

    update = f""" UPDATE partners 
                SET favorite={favorite_bool}
                """
    where = f'WHERE id_partner = {id}'
    update += where
    update += ';'
    with psycopg2.connect(database=db_name, user=db_user, password=db_pass, host=db_host) as conn:
        with conn.cursor() as cur:
            cur.execute(update)
            conn.commit()
    return True

def db_del_photo_from_db(id):
    delete = f"""DELETE FROM partners_photos 
             WHERE id_partner={id};
             """
    with psycopg2.connect(database=db_name, user=db_user, password=db_pass, host=db_host) as conn:
        with conn.cursor() as cur:
            cur.execute(delete)
            conn.commit()


def db_del_from_db(id):
    db_del_photo_from_db(id)

    delete = f""" DELETE FROM partners 
                    WHERE id_partner={id};
                """
    with psycopg2.connect(database=db_name, user=db_user, password=db_pass, host=db_host) as conn:
        with conn.cursor() as cur:
            cur.execute(delete)
            conn.commit()
    return True
