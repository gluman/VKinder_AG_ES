import psycopg2
import os

def insert_partners(crit1, crit2, crit3):
    pass

def show_results():
    pass

def save_person_to_db(id):
    with psycopg2.connect(database="VKinderDB", user="postgres", password="123", host='localhost') as conn:
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
        with psycopg2.connect(database="VKinderDB", user="postgres", password="123", host='localhost') as conn:
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
    try:
        for photo in photos:
            with open(os.path.join(photo_folder, '%s.jpg' % photo['id_photo']), 'wb') as f:
                for buf in r.iter_content(1024):
                    if buf:
                        f.write(buf)
                        sleep(2)
        return 1
    except:
        return 0





    photos = _result
    for item in _result:
        photos_partner = item['respose']['items']
        for photo in photos_partner:
            owner = photo['owner_id']
        with psycopg2.connect(database="VKinderDB", user="postgres", password="123", host='localhost') as conn:
            with conn.cursor() as cur:
                cur.execute("""                 
                               INSERT INTO partners_photos(
                                                id_partner, 
                                                photo, 
                                                photo_link, 
                                                num_like,
                                                )
                                VALUES((SELECT * FROM pid), %s, %s , %s, %s, %s)
                                ON CONFLICT
                                DO NOTHING
                                RETURNING id_partner;
                              """, (str(id_person), name, surname, sex, str(age), city))
                conn.commit()




def update_result(info):
    pass