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
                    ON CONFLICT (id_person)
                    DO NOTHING;
                   """, (id,))
            conn.commit()

    return

