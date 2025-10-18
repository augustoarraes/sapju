--
-- PostgreSQL database dump
--

\restrict srf2ufAHSalzBbNS26PFdYApnd5PPFOWeasl09I92PC69pHeVAunlaEEjyRhzBd

-- Dumped from database version 13.22
-- Dumped by pg_dump version 13.22

-- Started on 2025-10-18 18:12:01 UTC

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

--
-- TOC entry 3 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

-- CREATE SCHEMA public;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 201 (class 1259 OID 16395)
-- Name: documento; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.documento (
    id bigint NOT NULL,
    documento_id character varying,
    processo_id character varying,
    status character varying,
    checksum character varying,
    texto text,
    data_upload timestamp with time zone DEFAULT now()
);


--
-- TOC entry 200 (class 1259 OID 16385)
-- Name: processo; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.processo (
    id bigint NOT NULL,
    classe character varying,
    numero integer,
    processo_id character varying,
    orgao_origem character varying,
    data_abertura timestamp with time zone DEFAULT now()
);


--
-- TOC entry 203 (class 1259 OID 16408)
-- Name: sapju_documento_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sapju_documento_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3094 (class 0 OID 0)
-- Dependencies: 203
-- Name: sapju_documento_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sapju_documento_id_seq OWNED BY public.documento.id;


--
-- TOC entry 202 (class 1259 OID 16405)
-- Name: sapju_processo_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sapju_processo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3095 (class 0 OID 0)
-- Dependencies: 202
-- Name: sapju_processo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sapju_processo_id_seq OWNED BY public.processo.id;


--
-- TOC entry 2950 (class 2604 OID 16410)
-- Name: documento id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.documento ALTER COLUMN id SET DEFAULT nextval('public.sapju_documento_id_seq'::regclass);


--
-- TOC entry 2947 (class 2604 OID 16407)
-- Name: processo id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.processo ALTER COLUMN id SET DEFAULT nextval('public.sapju_processo_id_seq'::regclass);


--
-- TOC entry 3086 (class 0 OID 16395)
-- Dependencies: 201
-- Data for Name: documento; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 3085 (class 0 OID 16385)
-- Dependencies: 200
-- Data for Name: processo; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 3096 (class 0 OID 0)
-- Dependencies: 203
-- Name: sapju_documento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.sapju_documento_id_seq', 1, false);


--
-- TOC entry 3097 (class 0 OID 0)
-- Dependencies: 202
-- Name: sapju_processo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.sapju_processo_id_seq', 1, false);


--
-- TOC entry 2954 (class 2606 OID 16404)
-- Name: documento documento_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.documento
    ADD CONSTRAINT documento_pkey PRIMARY KEY (id);


--
-- TOC entry 2952 (class 2606 OID 16394)
-- Name: processo processo_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.processo
    ADD CONSTRAINT processo_pkey PRIMARY KEY (id);


-- Completed on 2025-10-18 18:12:08 UTC

--
-- PostgreSQL database dump complete
--

\unrestrict srf2ufAHSalzBbNS26PFdYApnd5PPFOWeasl09I92PC69pHeVAunlaEEjyRhzBd

