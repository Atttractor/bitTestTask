--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4 (Debian 16.4-1.pgdg120+2)
-- Dumped by pg_dump version 16.4 (Ubuntu 16.4-0ubuntu0.24.04.2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: author; Type: TABLE; Schema: public; Owner: library_user
--

CREATE TABLE public.author (
    id integer NOT NULL,
    name character varying(64) NOT NULL
);


ALTER TABLE public.author OWNER TO library_user;

--
-- Name: author_id_seq; Type: SEQUENCE; Schema: public; Owner: library_user
--

ALTER TABLE public.author ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.author_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: book; Type: TABLE; Schema: public; Owner: library_user
--

CREATE TABLE public.book (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    count_in_library integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.book OWNER TO library_user;

--
-- Name: book_author; Type: TABLE; Schema: public; Owner: library_user
--

CREATE TABLE public.book_author (
    id integer NOT NULL,
    book_id integer NOT NULL,
    author_id integer NOT NULL
);


ALTER TABLE public.book_author OWNER TO library_user;

--
-- Name: book_author_id_seq; Type: SEQUENCE; Schema: public; Owner: library_user
--

ALTER TABLE public.book_author ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.book_author_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: book_genre; Type: TABLE; Schema: public; Owner: library_user
--

CREATE TABLE public.book_genre (
    id integer NOT NULL,
    book_id integer NOT NULL,
    genre_id integer NOT NULL
);


ALTER TABLE public.book_genre OWNER TO library_user;

--
-- Name: book_genre_id_seq; Type: SEQUENCE; Schema: public; Owner: library_user
--

ALTER TABLE public.book_genre ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.book_genre_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: book_id_seq; Type: SEQUENCE; Schema: public; Owner: library_user
--

ALTER TABLE public.book ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.book_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: genre; Type: TABLE; Schema: public; Owner: library_user
--

CREATE TABLE public.genre (
    id integer NOT NULL,
    name character varying(32) NOT NULL
);


ALTER TABLE public.genre OWNER TO library_user;

--
-- Name: genre_id_seq; Type: SEQUENCE; Schema: public; Owner: library_user
--

ALTER TABLE public.genre ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.genre_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: user; Type: TABLE; Schema: public; Owner: library_user
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    address character varying(128) NOT NULL,
    phone_number character varying(11) NOT NULL,
    email character varying(64) NOT NULL
);


ALTER TABLE public."user" OWNER TO library_user;

--
-- Name: user_has_book; Type: TABLE; Schema: public; Owner: library_user
--

CREATE TABLE public.user_has_book (
    id integer NOT NULL,
    user_id integer NOT NULL,
    book_id integer NOT NULL,
    date_of_taken date DEFAULT now() NOT NULL,
    rental_duration interval DEFAULT '30 days'::interval NOT NULL,
    returned boolean DEFAULT false NOT NULL
);


ALTER TABLE public.user_has_book OWNER TO library_user;

--
-- Name: user_has_book_id_seq; Type: SEQUENCE; Schema: public; Owner: library_user
--

ALTER TABLE public.user_has_book ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.user_has_book_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: library_user
--

ALTER TABLE public."user" ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: author author_pkey; Type: CONSTRAINT; Schema: public; Owner: library_user
--

ALTER TABLE ONLY public.author
    ADD CONSTRAINT author_pkey PRIMARY KEY (id);


--
-- Name: book_author book_author_pkey; Type: CONSTRAINT; Schema: public; Owner: library_user
--

ALTER TABLE ONLY public.book_author
    ADD CONSTRAINT book_author_pkey PRIMARY KEY (id);


--
-- Name: book_genre book_genre_pkey; Type: CONSTRAINT; Schema: public; Owner: library_user
--

ALTER TABLE ONLY public.book_genre
    ADD CONSTRAINT book_genre_pkey PRIMARY KEY (id);


--
-- Name: user book_pkey; Type: CONSTRAINT; Schema: public; Owner: library_user
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT book_pkey PRIMARY KEY (id);


--
-- Name: book book_pkey1; Type: CONSTRAINT; Schema: public; Owner: library_user
--

ALTER TABLE ONLY public.book
    ADD CONSTRAINT book_pkey1 PRIMARY KEY (id);


--
-- Name: genre genre_pkey; Type: CONSTRAINT; Schema: public; Owner: library_user
--

ALTER TABLE ONLY public.genre
    ADD CONSTRAINT genre_pkey PRIMARY KEY (id);


--
-- Name: user_has_book user_has_book_pkey; Type: CONSTRAINT; Schema: public; Owner: library_user
--

ALTER TABLE ONLY public.user_has_book
    ADD CONSTRAINT user_has_book_pkey PRIMARY KEY (id);


--
-- Name: book_author author_id; Type: FK CONSTRAINT; Schema: public; Owner: library_user
--

ALTER TABLE ONLY public.book_author
    ADD CONSTRAINT author_id FOREIGN KEY (author_id) REFERENCES public.author(id) ON DELETE CASCADE ON UPDATE NO ACTION;;


--
-- Name: book_author book_id; Type: FK CONSTRAINT; Schema: public; Owner: library_user
--

ALTER TABLE ONLY public.book_author
    ADD CONSTRAINT book_id FOREIGN KEY (book_id) REFERENCES public.book(id) ON DELETE CASCADE ON UPDATE NO ACTION;;


--
-- Name: book_genre book_id; Type: FK CONSTRAINT; Schema: public; Owner: library_user
--

ALTER TABLE ONLY public.book_genre
    ADD CONSTRAINT book_id FOREIGN KEY (book_id) REFERENCES public.book(id) ON DELETE CASCADE ON UPDATE NO ACTION;;


--
-- Name: user_has_book book_id; Type: FK CONSTRAINT; Schema: public; Owner: library_user
--

ALTER TABLE ONLY public.user_has_book
    ADD CONSTRAINT book_id FOREIGN KEY (book_id) REFERENCES public.book(id) ON DELETE CASCADE ON UPDATE NO ACTION;;


--
-- Name: book_genre genre_id; Type: FK CONSTRAINT; Schema: public; Owner: library_user
--

ALTER TABLE ONLY public.book_genre
    ADD CONSTRAINT genre_id FOREIGN KEY (genre_id) REFERENCES public.genre(id) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Name: user_has_book user_id; Type: FK CONSTRAINT; Schema: public; Owner: library_user
--

ALTER TABLE ONLY public.user_has_book
    ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE ON UPDATE NO ACTION;;


--
-- PostgreSQL database dump complete
--

