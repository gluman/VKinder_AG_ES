
CREATE TABLE IF NOT EXISTS person (
	id_person serial4 NOT NULL,
	id_vk_person varchar NULL,
	CONSTRAINT person_id_vk_person_key UNIQUE (id_vk_person),
	CONSTRAINT person_pkey PRIMARY KEY (id_person)
);


CREATE TABLE IF NOT EXISTS partners (
	id_partner serial4 NOT NULL,
	id_person int NOT NULL,
	id_vk_partner int NOT NULL,
	name_ text NOT NULL,
	surname text NOT NULL,
	sex bpchar(1) NOT NULL,
	profile_link text NULL,
	age_ int4 NOT NULL,
	city text NOT NULL,
	favorite bool NULL,
	CONSTRAINT parthers FOREIGN KEY (id_person) REFERENCES person(id_person),
	CONSTRAINT partners_pkey PRIMARY KEY (id_partner),
	CONSTRAINT u_partner_unique UNIQUE (id_person, id_vk_partner, name_, surname, sex, age_, city)
);

CREATE TABLE IF NOT EXISTS partners_photos(
	id_photos serial4 NOT NULL,
	id_partner int4 NOT NULL,
	id_vk_photo int4 NOT NULL,
	photo bytea NOT NULL,
	photo_link TEXT,
	num_like int4 NOT NULL,
	CONSTRAINT partners_photos_pkey PRIMARY KEY (id_photos),
	CONSTRAINT partners_photos_id_partner_fkey FOREIGN KEY (id_partner) REFERENCES partners(id_partner),
	CONSTRAINT unic_photo UNIQUE (id_partner, id_vk_photo)
);