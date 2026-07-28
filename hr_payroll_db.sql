--
-- PostgreSQL database dump
--

\restrict 064g8meSLgfpp0Nph0dn9nisaiJ9O99hPDy2he56CRxDGpOjhjnKlWvY9Ye7uh6

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employees (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    email character varying(120) NOT NULL,
    role character varying(64) NOT NULL,
    team_id integer,
    manager_id integer,
    start_date date NOT NULL,
    salary numeric(12,2) NOT NULL,
    employment_type character varying(32) NOT NULL,
    status character varying(16) DEFAULT 'Active'::character varying
);


ALTER TABLE public.employees OWNER TO postgres;

--
-- Name: employees_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.employees_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.employees_id_seq OWNER TO postgres;

--
-- Name: employees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employees_id_seq OWNED BY public.employees.id;


--
-- Name: leave_requests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.leave_requests (
    id integer NOT NULL,
    employee_id integer NOT NULL,
    leave_type character varying(32) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    status character varying(16) DEFAULT 'Pending'::character varying,
    reason text,
    approved_by integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.leave_requests OWNER TO postgres;

--
-- Name: leave_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.leave_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.leave_requests_id_seq OWNER TO postgres;

--
-- Name: leave_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.leave_requests_id_seq OWNED BY public.leave_requests.id;


--
-- Name: payroll_records; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payroll_records (
    id integer NOT NULL,
    employee_id integer NOT NULL,
    period_start date NOT NULL,
    period_end date NOT NULL,
    gross_pay numeric(12,2) NOT NULL,
    tax_deduction numeric(12,2) NOT NULL,
    social_security_deduction numeric(12,2) NOT NULL,
    unpaid_leave_deduction numeric(12,2) NOT NULL,
    net_pay numeric(12,2) NOT NULL,
    status character varying(16) DEFAULT 'Draft'::character varying,
    generated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.payroll_records OWNER TO postgres;

--
-- Name: payroll_records_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.payroll_records_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.payroll_records_id_seq OWNER TO postgres;

--
-- Name: payroll_records_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.payroll_records_id_seq OWNED BY public.payroll_records.id;


--
-- Name: teams; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.teams (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    description character varying(256)
);


ALTER TABLE public.teams OWNER TO postgres;

--
-- Name: teams_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.teams_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.teams_id_seq OWNER TO postgres;

--
-- Name: teams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.teams_id_seq OWNED BY public.teams.id;


--
-- Name: employees id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees ALTER COLUMN id SET DEFAULT nextval('public.employees_id_seq'::regclass);


--
-- Name: leave_requests id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leave_requests ALTER COLUMN id SET DEFAULT nextval('public.leave_requests_id_seq'::regclass);


--
-- Name: payroll_records id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payroll_records ALTER COLUMN id SET DEFAULT nextval('public.payroll_records_id_seq'::regclass);


--
-- Name: teams id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teams ALTER COLUMN id SET DEFAULT nextval('public.teams_id_seq'::regclass);


--
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.employees (id, name, email, role, team_id, manager_id, start_date, salary, employment_type, status) FROM stdin;
1	John Kamau	john.kamau@company.com	HR Manager	1	\N	2023-01-10	120000.00	Full-time	Active
2	Mary Wanjiku	mary.wanjiku@company.com	HR Officer	1	1	2023-03-15	80000.00	Full-time	Active
3	Peter Otieno	peter.otieno@company.com	Finance Manager	2	\N	2022-05-01	150000.00	Full-time	Active
4	Jane Achieng	jane.achieng@company.com	Accountant	2	3	2023-04-10	90000.00	Full-time	Active
5	Brian Mwangi	brian.mwangi@company.com	IT Manager	3	\N	2022-08-20	170000.00	Full-time	Active
6	Faith Njeri	faith.njeri@company.com	Software Developer	3	5	2023-01-25	120000.00	Full-time	Active
7	Kevin Kiptoo	kevin.kiptoo@company.com	Sales Manager	4	\N	2022-10-15	140000.00	Full-time	Active
8	Mercy Chebet	mercy.chebet@company.com	Sales Executive	4	7	2023-06-01	70000.00	Full-time	Active
9	Samuel Ouma	samuel.ouma@company.com	Marketing Officer	5	\N	2023-02-12	85000.00	Contract	Active
10	Lucy Atieno	lucy.atieno@company.com	Customer Support Officer	6	\N	2023-07-05	65000.00	Part-time	Active
11	Benson	ombati0003@gmail.com	devops	3	2	2026-07-15	15000.00	Full-time	Active
\.


--
-- Data for Name: leave_requests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.leave_requests (id, employee_id, leave_type, start_date, end_date, status, reason, approved_by, created_at) FROM stdin;
1	2	Annual	2025-08-04	2025-08-08	Approved	Family vacation	1	2026-07-28 22:10:50.200419
2	4	Sick	2025-07-14	2025-07-16	Approved	Medical treatment	3	2026-07-28 22:10:50.200419
4	8	Unpaid	2025-07-20	2025-07-25	Approved	Personal reasons	7	2026-07-28 22:10:50.200419
5	10	Sick	2025-06-10	2025-06-11	Approved	Hospital visit	\N	2026-07-28 22:10:50.200419
6	2	Annual	2025-10-01	2025-10-03	Pending	Travel	1	2026-07-28 22:10:50.200419
7	4	Annual	2025-08-15	2025-08-18	Rejected	Vacation	3	2026-07-28 22:10:50.200419
8	6	Sick	2025-07-01	2025-07-02	Approved	Flu	5	2026-07-28 22:10:50.200419
9	8	Annual	2025-11-10	2025-11-15	Pending	Wedding	7	2026-07-28 22:10:50.200419
10	9	Unpaid	2025-08-01	2025-08-04	Approved	Family matters	\N	2026-07-28 22:10:50.200419
3	6	Annual	2025-09-01	2025-09-05	Approved	Holiday	1	2026-07-28 22:10:50.200419
11	11	Sick	2026-07-02	2026-07-11	Pending	nk	\N	2026-07-28 21:41:03.154307
12	4	Sick	2026-08-01	2026-08-03	Pending	Medical treatment	\N	2026-07-28 21:41:14.414085
\.


--
-- Data for Name: payroll_records; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.payroll_records (id, employee_id, period_start, period_end, gross_pay, tax_deduction, social_security_deduction, unpaid_leave_deduction, net_pay, status, generated_at) FROM stdin;
1	1	2025-07-01	2025-07-31	120000.00	12000.00	6000.00	0.00	102000.00	Finalized	2026-07-28 22:12:56.881228
2	2	2025-07-01	2025-07-31	80000.00	6000.00	4000.00	0.00	70000.00	Finalized	2026-07-28 22:12:56.881228
3	3	2025-07-01	2025-07-31	150000.00	18000.00	7500.00	0.00	124500.00	Finalized	2026-07-28 22:12:56.881228
4	4	2025-07-01	2025-07-31	90000.00	8000.00	4500.00	0.00	77500.00	Finalized	2026-07-28 22:12:56.881228
5	5	2025-07-01	2025-07-31	170000.00	22000.00	8500.00	0.00	139500.00	Finalized	2026-07-28 22:12:56.881228
6	6	2025-07-01	2025-07-31	120000.00	12000.00	6000.00	0.00	102000.00	Finalized	2026-07-28 22:12:56.881228
7	7	2025-07-01	2025-07-31	140000.00	16000.00	7000.00	0.00	117000.00	Finalized	2026-07-28 22:12:56.881228
8	8	2025-07-01	2025-07-31	70000.00	5000.00	3500.00	4500.00	57000.00	Finalized	2026-07-28 22:12:56.881228
9	9	2025-07-01	2025-07-31	85000.00	7000.00	4250.00	3000.00	70750.00	Finalized	2026-07-28 22:12:56.881228
10	10	2025-07-01	2025-07-31	65000.00	4500.00	3250.00	0.00	57250.00	Finalized	2026-07-28 22:12:56.881228
11	1	2026-07-01	2026-07-31	120000.00	23300.00	6000.00	0.00	90700.00	Draft	2026-07-28 21:51:21.116459
12	2	2026-07-01	2026-07-31	80000.00	15300.00	4000.00	0.00	60700.00	Draft	2026-07-28 21:51:21.123574
13	3	2026-07-01	2026-07-31	150000.00	29300.00	7500.00	0.00	113200.00	Draft	2026-07-28 21:51:21.127473
14	4	2026-07-01	2026-07-31	90000.00	17300.00	4500.00	0.00	68200.00	Draft	2026-07-28 21:51:21.1307
15	5	2026-07-01	2026-07-31	170000.00	33300.00	8500.00	0.00	128200.00	Draft	2026-07-28 21:51:21.133407
16	6	2026-07-01	2026-07-31	120000.00	23300.00	6000.00	0.00	90700.00	Draft	2026-07-28 21:51:21.136727
17	7	2026-07-01	2026-07-31	140000.00	27300.00	7000.00	0.00	105700.00	Draft	2026-07-28 21:51:21.140411
18	8	2026-07-01	2026-07-31	70000.00	13300.00	3500.00	0.00	53200.00	Draft	2026-07-28 21:51:21.144082
19	9	2026-07-01	2026-07-31	85000.00	16300.00	4250.00	0.00	64450.00	Draft	2026-07-28 21:51:21.146664
21	11	2026-07-01	2026-07-31	8225.81	945.16	411.29	0.00	6869.35	Draft	2026-07-28 21:51:21.151769
20	10	2026-07-01	2026-07-31	65000.00	12300.00	3250.00	0.00	49450.00	Finalized	2026-07-28 21:51:21.149484
\.


--
-- Data for Name: teams; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.teams (id, name, description) FROM stdin;
1	Human Resources	Manages employee welfare and recruitment
2	Finance	Handles accounting and financial operations
3	Information Technology	Maintains company IT infrastructure
4	Sales	Responsible for product sales
5	Marketing	Handles company branding and advertising
6	Customer Support	Provides customer assistance
7	Operations	Oversees daily business operations
8	Procurement	Manages purchasing activities
9	Legal	Handles legal affairs
10	Administration	General administrative services
13	Security	Responsible for campaigns and brand growth
14	platform	frumenties
\.


--
-- Name: employees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.employees_id_seq', 11, true);


--
-- Name: leave_requests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.leave_requests_id_seq', 12, true);


--
-- Name: payroll_records_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.payroll_records_id_seq', 21, true);


--
-- Name: teams_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.teams_id_seq', 14, true);


--
-- Name: employees employees_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_email_key UNIQUE (email);


--
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id);


--
-- Name: leave_requests leave_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leave_requests
    ADD CONSTRAINT leave_requests_pkey PRIMARY KEY (id);


--
-- Name: payroll_records payroll_records_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payroll_records
    ADD CONSTRAINT payroll_records_pkey PRIMARY KEY (id);


--
-- Name: teams teams_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_name_key UNIQUE (name);


--
-- Name: teams teams_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_pkey PRIMARY KEY (id);


--
-- Name: employees employees_manager_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_manager_id_fkey FOREIGN KEY (manager_id) REFERENCES public.employees(id);


--
-- Name: employees employees_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_team_id_fkey FOREIGN KEY (team_id) REFERENCES public.teams(id);


--
-- Name: leave_requests leave_requests_approved_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leave_requests
    ADD CONSTRAINT leave_requests_approved_by_fkey FOREIGN KEY (approved_by) REFERENCES public.employees(id);


--
-- Name: leave_requests leave_requests_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leave_requests
    ADD CONSTRAINT leave_requests_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employees(id);


--
-- Name: payroll_records payroll_records_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payroll_records
    ADD CONSTRAINT payroll_records_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employees(id);


--
-- PostgreSQL database dump complete
--

\unrestrict 064g8meSLgfpp0Nph0dn9nisaiJ9O99hPDy2he56CRxDGpOjhjnKlWvY9Ye7uh6

