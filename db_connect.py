import psycopg2


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

def save_value_for_search(id, age, sex, city):
    with psycopg2.connect(database="VKinderDB", user="postgres", password="123", host='localhost') as conn:
        with conn.cursor() as cur:
            name_ = f'{id}_{age}_{sex}_{city}'
            cur.execute(""" 
                                WITH pid as (
                                SELECT id_person 
                                FROM person
                                WHERE id_vk_person = %s
                                )
                                
                                INSERT INTO querys(
                                                name_, 
                                                id_person, 
                                                partner_age, 
                                                partner_city, 
                                                parnter_sex
                                                )
                                VALUES(%s, (SELECT * FROM pid), %s , %s, %s)
                                ON CONFLICT
                                DO NOTHING
                                RETURNING id_query;
                              """, (str(id), name_, str(age), city, sex))
            result_id = cur.fetchall()
            conn.commit()
            return result_id

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


def save_result_photo(_result):
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