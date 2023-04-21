CREATE TABLE IF NOT EXISTS person(
	id_person serial PRIMARY KEY,
	id_vk_person varchar UNIQUE
);	

CREATE TABLE IF NOT EXISTS querys(
	id_query SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	id_person integer NOT NULL REFERENCES Person(id_person),
	partner_age integer NOT NULL,
	partner_city TEXT NOT NULL,
	parnter_sex char NOT NULL
);

CREATE TABLE IF NOT EXISTS partners(
	id_partner serial PRIMARY KEY,
	id_query integer NOT NULL REFERENCES querys(id_query),
	name TEXT NOT NULL,
	surname TEXT NOT NULL,
	sex char NOT NULL,
	profile_link TEXT NOT NULL,
	age integer NOT NULL,
	city TEXT NOT NULL,
	favorite bool NOT null
);

CREATE TABLE IF NOT EXISTS parthers_photos(
	id_photos serial PRIMARY KEY,
	id_partner integer NOT NULL REFERENCES partners(id_partner),
	photo BIT VARYING NOT NULL,
	num_like integer NOT NULL
);












