CREATE ROLE admin WITH SUPERUSER;

DROP DATABASE IF EXISTS docker_tut;
CREATE DATABASE docker_tut;
\c docker_tut;

CREATE TABLE public.owner (
    owner_id SERIAL PRIMARY KEY,
    name VARCHAR(1024) NOT NULL,
    age SMALLINT,

    created TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    last_modified TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

INSERT INTO public.owner (owner_id, name, age) VALUES
  (1, 'Alice', 20),
  (2, 'Bob', 21),
  (3, 'Chris', 22);

ALTER SEQUENCE public.owner_owner_id_seq RESTART WITH 4;
