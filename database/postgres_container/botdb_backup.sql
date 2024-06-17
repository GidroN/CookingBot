--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3 (Debian 16.3-1.pgdg120+1)
-- Dumped by pg_dump version 16.3 (Debian 16.3-1.pgdg120+1)

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
-- Name: aerich; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.aerich (
    id integer NOT NULL,
    version character varying(255) NOT NULL,
    app character varying(100) NOT NULL,
    content jsonb NOT NULL
);


ALTER TABLE public.aerich OWNER TO postgres;

--
-- Name: aerich_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.aerich_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.aerich_id_seq OWNER TO postgres;

--
-- Name: aerich_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.aerich_id_seq OWNED BY public.aerich.id;


--
-- Name: category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.category (
    id integer NOT NULL,
    title character varying(60) NOT NULL
);


ALTER TABLE public.category OWNER TO postgres;

--
-- Name: category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.category_id_seq OWNER TO postgres;

--
-- Name: category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.category_id_seq OWNED BY public.category.id;


--
-- Name: recipe; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.recipe (
    id integer NOT NULL,
    title character varying(60) NOT NULL,
    url character varying(150) NOT NULL,
    date timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    category_id integer NOT NULL,
    creator_id integer NOT NULL
);


ALTER TABLE public.recipe OWNER TO postgres;

--
-- Name: recipe_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.recipe_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.recipe_id_seq OWNER TO postgres;

--
-- Name: recipe_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.recipe_id_seq OWNED BY public.recipe.id;


--
-- Name: report; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.report (
    id integer NOT NULL,
    reason character varying(100),
    recipe_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.report OWNER TO postgres;

--
-- Name: report_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.report_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.report_id_seq OWNER TO postgres;

--
-- Name: report_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.report_id_seq OWNED BY public.report.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    tg_id character varying(10) NOT NULL,
    username character varying(32),
    name character varying(129) NOT NULL,
    is_admin boolean DEFAULT false NOT NULL,
    is_active boolean DEFAULT true NOT NULL
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_id_seq OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: userfavouriterecipe; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.userfavouriterecipe (
    id integer NOT NULL,
    recipe_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.userfavouriterecipe OWNER TO postgres;

--
-- Name: userfavouriterecipe_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.userfavouriterecipe_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.userfavouriterecipe_id_seq OWNER TO postgres;

--
-- Name: userfavouriterecipe_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.userfavouriterecipe_id_seq OWNED BY public.userfavouriterecipe.id;


--
-- Name: userwarn; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.userwarn (
    id integer NOT NULL,
    date timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    reason character varying(100) NOT NULL,
    admin_id integer NOT NULL,
    recipe_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.userwarn OWNER TO postgres;

--
-- Name: userwarn_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.userwarn_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.userwarn_id_seq OWNER TO postgres;

--
-- Name: userwarn_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.userwarn_id_seq OWNED BY public.userwarn.id;


--
-- Name: aerich id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.aerich ALTER COLUMN id SET DEFAULT nextval('public.aerich_id_seq'::regclass);


--
-- Name: category id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category ALTER COLUMN id SET DEFAULT nextval('public.category_id_seq'::regclass);


--
-- Name: recipe id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recipe ALTER COLUMN id SET DEFAULT nextval('public.recipe_id_seq'::regclass);


--
-- Name: report id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report ALTER COLUMN id SET DEFAULT nextval('public.report_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Name: userfavouriterecipe id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userfavouriterecipe ALTER COLUMN id SET DEFAULT nextval('public.userfavouriterecipe_id_seq'::regclass);


--
-- Name: userwarn id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userwarn ALTER COLUMN id SET DEFAULT nextval('public.userwarn_id_seq'::regclass);


--
-- Data for Name: aerich; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.aerich (id, version, app, content) FROM stdin;
\.


--
-- Data for Name: category; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.category (id, title) FROM stdin;
1	🍲 Супы
2	🥗 Салаты
3	🍝 Паста
4	🍛 Мясные блюда
5	🍣 Морепродукты
6	🥘 Ризотто и пловы
7	🍕 Пицца
8	🥙 Закуски
9	🥞 Завтрак
10	🍰 Десерты
\.


--
-- Data for Name: recipe; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.recipe (id, title, url, date, is_active, category_id, creator_id) FROM stdin;
2	Борщ с говядиной	https://telegra.ph/Borshch-s-govyadinoj-06-13	2024-06-13 17:38:50.320048+00	t	1	1
3	Куриный суп с лапшой	https://telegra.ph/Kurinnyj-sup-s-lapshoj-06-13	2024-06-13 17:46:30.578674+00	t	1	1
4	Грибной крем-суп	https://telegra.ph/Gribnoj-krem-sup-06-13-2	2024-06-13 17:48:52.977892+00	t	1	1
5	Харчо	https://telegra.ph/Harcho-06-13	2024-06-13 17:48:53.021564+00	t	1	1
6	Греческий салат	https://telegra.ph/Grecheskij-salat-06-13-2	2024-06-13 17:54:47.471051+00	t	2	1
7	Цезарь с курицей	https://telegra.ph/Cezar-s-kuricej-06-13	2024-06-13 17:54:47.490497+00	t	2	1
8	Салат с тунцом	https://telegra.ph/Salat-s-tuncom-06-13	2024-06-13 17:54:47.529088+00	t	2	1
9	Винегрет	https://telegra.ph/Vinegret-06-13	2024-06-13 17:54:47.557383+00	t	2	1
10	Карбонара	https://telegra.ph/Karbonara-06-14	2024-06-14 10:28:56.380347+00	t	3	1
11	Паста с морепродуктами	https://telegra.ph/Pasta-s-moreproduktami-06-14	2024-06-14 10:28:56.438126+00	t	3	1
12	Лазанья Болоньезе	https://telegra.ph/Lazanya-Boloneze-06-14	2024-06-14 10:28:56.464548+00	t	3	1
13	Песто с курицей	https://telegra.ph/Pesto-s-kuricej-06-14	2024-06-14 10:28:56.484696+00	t	3	1
14	Стейк на гриле	https://telegra.ph/Stejk-na-grile-06-14	2024-06-14 10:28:56.514916+00	t	4	1
15	Тефтели в томатном соусе	https://telegra.ph/Tefteli-v-tomatnom-souse-06-14	2024-06-14 10:28:56.534467+00	t	4	1
16	Курица по-китайски	https://telegra.ph/Kurica-po-kitajski-06-14	2024-06-14 10:28:56.551689+00	t	4	1
17	Свинина в медово-горчичном соусе	https://telegra.ph/Svinina-v-medovo-gorchichnom-souse-06-14	2024-06-14 10:28:56.569703+00	t	4	1
18	Ризотто с грибами	https://telegra.ph/Rizotto-s-gribami-06-14	2024-06-14 10:43:03.170133+00	t	5	1
19	Плов с бараниной	https://telegra.ph/Plov-s-baraninoj-06-14	2024-06-14 10:43:03.170133+00	t	5	1
20	Ризотто с креветками	https://telegra.ph/Rizotto-s-krevetkami-06-14	2024-06-14 10:43:03.170133+00	t	5	1
21	Вегетарианский плов	https://telegra.ph/Vegetarianskij-plov-06-14	2024-06-14 10:43:03.170133+00	t	5	1
22	Маргарита	https://telegra.ph/Margarita-06-14-4	2024-06-14 10:43:03.197259+00	t	6	1
23	Пепперони	https://telegra.ph/Pepperoni-06-14	2024-06-14 10:43:03.197259+00	t	6	1
24	Четыре сыра	https://telegra.ph/CHetyre-syra-06-14	2024-06-14 10:43:03.197259+00	t	6	1
25	Вегетарианская пицца	https://telegra.ph/Vegetarianskaya-picca-06-14	2024-06-14 10:43:03.197259+00	t	6	1
26	Суши роллы	https://telegra.ph/Sushi-rolly-06-14	2024-06-14 12:49:56.602643+00	t	7	1
27	Запеченная рыба с лимоном	https://telegra.ph/Zapechennaya-ryba-s-limonom-06-14	2024-06-14 12:49:56.602643+00	t	7	1
28	Креветки в чесночном соусе	https://telegra.ph/Krevetki-v-chesnochnom-souse-06-14	2024-06-14 12:49:56.602643+00	t	7	1
29	Мидии в белом вине	https://telegra.ph/Midii-v-belom-vine-06-14	2024-06-14 12:49:56.602643+00	t	7	1
30	Брускетта с помидорами	https://telegra.ph/Brusketta-s-pomidorami-06-14	2024-06-14 12:49:56.64234+00	t	8	1
31	Хумус с овощами	https://telegra.ph/Humus-s-ovoshchami-06-14	2024-06-14 12:49:56.64234+00	t	8	1
32	Мини-кесадильи	https://telegra.ph/Mini-kesadili-06-14	2024-06-14 12:49:56.64234+00	t	8	1
33	Креветочные коктейли	https://telegra.ph/Krevetochnye-koktejli-06-14	2024-06-14 12:49:56.64234+00	t	8	1
34	Омлет с овощами	https://telegra.ph/Omlet-s-ovoshchami-06-14	2024-06-14 12:58:18.778249+00	t	9	1
35	Банановые панкейки	https://telegra.ph/Bananovye-pankejki-06-14	2024-06-14 12:58:18.778249+00	t	9	1
36	Смузи боул	https://telegra.ph/Smuzi-boul-06-14	2024-06-14 12:58:18.778249+00	t	9	1
37	Авокадо-тост	https://telegra.ph/Avokado-tost-06-14	2024-06-14 12:58:18.778249+00	t	9	1
38	Тирамису	https://telegra.ph/Tiramisu-06-14-2	2024-06-14 12:58:18.81985+00	t	10	1
39	Чизкейк	https://telegra.ph/CHizkejk-06-14-2	2024-06-14 12:58:18.81985+00	t	10	1
40	Пирог с яблоками	https://telegra.ph/Pirog-s-yablokami-06-14	2024-06-14 12:58:18.81985+00	t	10	1
41	Брауни	https://telegra.ph/Brauni-06-14-3	2024-06-14 12:58:18.81985+00	t	10	1
\.


--
-- Data for Name: report; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.report (id, reason, recipe_id, user_id) FROM stdin;
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, tg_id, username, name, is_admin, is_active) FROM stdin;
1	511952153	GidroNn	Anton ill 🇦🇹	f	t
\.


--
-- Data for Name: userfavouriterecipe; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.userfavouriterecipe (id, recipe_id, user_id) FROM stdin;
\.


--
-- Data for Name: userwarn; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.userwarn (id, date, reason, admin_id, recipe_id, user_id) FROM stdin;
\.


--
-- Name: aerich_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.aerich_id_seq', (SELECT MAX(id) FROM public.aerich) + 1, false);


--
-- Name: category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.category_id_seq', (SELECT MAX(id) FROM public.category) + 1, false);


--
-- Name: recipe_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.recipe_id_seq', (SELECT MAX(id) FROM public.recipe) + 1, false);


--
-- Name: report_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.report_id_seq', (SELECT MAX(id) FROM public.report) + 1, false);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', (SELECT MAX(id) FROM public.user) + 1, true);


--
-- Name: userfavouriterecipe_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.userfavouriterecipe_id_seq', (SELECT MAX(id) FROM public.userfavouriterecipe) + 1, false);


--
-- Name: userwarn_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.userwarn_id_seq', (SELECT MAX(id) FROM public.userwarn) + 1, false);


--
-- PostgreSQL database dump complete
--

