CREATE ROLE admin WITH SUPERUSER;

DROP DATABASE IF EXISTS docker_tut;
CREATE DATABASE docker_tut;
\c docker_tut;

CREATE TABLE public.pet (
    pet_id SERIAL PRIMARY KEY,
    name VARCHAR(1024) NOT NULL,
    species VARCHAR(1024),
    breed VARCHAR(1024),
    owner_id VARCHAR(1024),

    created TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    last_modified TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

INSERT INTO public.pet (pet_id, name, species, breed, owner_id) VALUES
  (1, 'Spot', 'dog', 'pointer', 1),
  (2, 'Max', 'dog', 'german shepherd', 1),
  (3, 'Luna', 'dog', 'beagle', 2),
  (4, 'Dug', 'dog', 'golden retriever', 2),
  (5, 'Oliver', 'cat', 'maine coon', 2),
  (6, 'Boots', 'cat', 'bengal', 2),
  (7, 'Cleo', 'cat', 'persian', 2),
  (8, 'Pickles', 'cat', 'ragdoll', 3);

ALTER SEQUENCE public.pet_pet_id_seq RESTART WITH 9;
