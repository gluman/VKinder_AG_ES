import psycopg2

run = True
with psycopg2.connect(database="VKinderDB", user="postgres", password="123", host='localhost') as conn:
    with conn.cursor() as cur:
        while run:

            def insert_partners(crit1, crit2, crit3):
                pass

            def show_results():
                pass


