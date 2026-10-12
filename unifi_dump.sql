--
-- PostgreSQL database dump
--

\restrict kCX6EWnmISkzZtUpIW9H63wOvn0sDcoZBdyx3QaOmv3dK2cZ71sZqwiLRo4lNCN

-- Dumped from database version 16.15 (Homebrew)
-- Dumped by pg_dump version 16.15 (Homebrew)

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
-- Name: customer_summaries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.customer_summaries (
    login_id text NOT NULL,
    summary text NOT NULL,
    recommendation text,
    model text,
    generated_at timestamp without time zone DEFAULT now()
);


--
-- Name: customers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.customers (
    login_id text NOT NULL,
    account_no text NOT NULL,
    name text NOT NULL,
    contact_no text,
    email_address text,
    address text,
    contract_term integer,
    commitment_start timestamp without time zone,
    commitment_end timestamp without time zone
);


--
-- Name: devices; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.devices (
    mac_address text NOT NULL,
    login_id text NOT NULL,
    friendly_name text,
    manufacturer text,
    brand text,
    device_type text,
    cloud_device_type text,
    link_type text,
    ip_address inet,
    ssid_2_4ghz text,
    ssid_5ghz text,
    channel_2_4ghz integer,
    channel_5ghz integer,
    antenna_2_4ghz text,
    antenna_5ghz text,
    protocol_2_4ghz text,
    protocol_5ghz text,
    rssi integer,
    rx_rate integer,
    tx_rate integer,
    last_seen timestamp without time zone,
    parent_mac text,
    platform text,
    bandwidth_2_4ghz text,
    bandwidth_5ghz text
);


--
-- Name: routers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.routers (
    serial_number text NOT NULL,
    login_id text NOT NULL,
    manufacturer text,
    model text,
    cpu_usage_pct integer,
    cpu_temperature_c integer,
    memory_usage_pct integer,
    monthly_usage_gb numeric(9,1),
    rx_power_dbm numeric(5,1)
);


--
-- Data for Name: customer_summaries; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.customer_summaries (login_id, summary, recommendation, model, generated_at) FROM stdin;
\.


--
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.customers (login_id, account_no, name, contact_no, email_address, address, contract_term, commitment_start, commitment_end) FROM stdin;
ticksew19@unifi	1045308028	TAN TICK SEW	60127200488	tstan.tstan@gmail.com	21 JALAN ANGGERIK ARANDA 31/32 40460 SHAH ALAM SELANGOR MALAYSIA	2	2019-12-01 11:58:55	2021-12-01 11:58:55
azlinamohd444@unifi	1023986457	AZLINA BINTI MOHD NOOR	60310202362	azlinamohd26@hotmail.com	75 JALAN DELIMA 40460 SHAH ALAM SELANGOR MALAYSIA	2	2025-08-05 09:51:52	2027-08-05 09:51:52
muhammadda300@unifi	1051820497	MUHAMMAD DANIAL BIN ZAKARIA	60731153610	muhammadda43@yahoo.com	19 JALAN MAWAR 30450 IPOH PERAK MALAYSIA	3	2021-12-25 09:51:52	2024-12-24 09:51:52
tanticksew53@unifi	1082740922	TAN TICK SEW	605608216466	tanticksew92@hotmail.com	46 JALAN MAWAR 93350 KUCHING SARAWAK MALAYSIA	2	2022-02-20 09:51:52	2024-02-20 09:51:52
kennethloh334@unifi	1099031136	KENNETH LOH KAH SENG	608945741570	kennethloh14@hotmail.com	28 JALAN CEMPAKA 40460 SHAH ALAM SELANGOR MALAYSIA	3	2022-12-28 09:51:52	2025-12-27 09:51:52
hasnahsall843@unifi	1047943729	HASNAH BINTI SALLEH	601194355680	hasnahsall97@gmail.com	82 JALAN BUNGA RAYA 80100 JOHOR BAHRU JOHOR MALAYSIA	1	2019-11-08 09:51:52	2020-11-07 09:51:52
chongkahfa740@unifi	1079349586	CHONG KAH FAI	608403553046	chongkahfa62@gmail.com	58 JALAN KIARA 40460 SHAH ALAM SELANGOR MALAYSIA	1	2019-01-16 09:51:52	2020-01-16 09:51:52
arunkrishn780@unifi	1030173983	ARUN A/L KRISHNAN	60542953575	arunkrishn49@gmail.com	92 JALAN CEMPAKA 80100 JOHOR BAHRU JOHOR MALAYSIA	2	2021-05-11 09:51:52	2023-05-11 09:51:52
zainalabid371@unifi	1095169786	ZAINAL ABIDIN BIN MOHD	605804332372	zainalabid41@gmail.com	64 JALAN BUNGA RAYA 30450 IPOH PERAK MALAYSIA	2	2022-05-31 09:51:52	2024-05-30 09:51:52
divyarajen754@unifi	1074528751	DIVYA A/P RAJENDRAN	60059307488	divyarajen49@hotmail.com	91 JALAN MERANTI 50000 KUALA LUMPUR WILAYAH PERSEKUTUAN MALAYSIA	1	2022-07-13 09:51:52	2023-07-13 09:51:52
mohdrizalo944@unifi	1093187389	MOHD RIZAL BIN OMAR	603396711589	mohdrizalo53@hotmail.com	61 JALAN MAWAR 30450 IPOH PERAK MALAYSIA	3	2025-04-26 09:51:52	2028-04-25 09:51:52
leechinhua764@unifi	1056028297	LEE CHIN HUA	60802337528	leechinhua92@yahoo.com	34 JALAN ANGGERIK ARANDA 80100 JOHOR BAHRU JOHOR MALAYSIA	3	2023-04-06 09:51:52	2026-04-05 09:51:52
limweiming953@unifi	1027867691	LIM WEI MING	604581184463	limweiming2@hotmail.com	27 JALAN DELIMA 80100 JOHOR BAHRU JOHOR MALAYSIA	2	2023-10-07 09:51:52	2025-10-06 09:51:52
gohsoonhua435@unifi	1035107651	GOH SOON HUAT	605903868017	gohsoonhua30@gmail.com	41 JALAN ANGGERIK ARANDA 80100 JOHOR BAHRU JOHOR MALAYSIA	2	2022-09-24 09:51:52	2024-09-23 09:51:52
norhayatio609@unifi	1027113426	NORHAYATI BINTI OSMAN	601828065122	norhayatio10@outlook.com	84 JALAN BUNGA RAYA 80100 JOHOR BAHRU JOHOR MALAYSIA	3	2021-10-19 09:51:52	2024-10-18 09:51:52
leechinhua381@unifi	1069644554	LEE CHIN HUA	60848903813	leechinhua65@hotmail.com	43 JALAN DELIMA 80100 JOHOR BAHRU JOHOR MALAYSIA	1	2023-05-09 09:51:52	2024-05-08 09:51:52
gohsoonhua109@unifi	1017844986	GOH SOON HUAT	602744038660	gohsoonhua55@yahoo.com	10 JALAN CEMPAKA 40460 SHAH ALAM SELANGOR MALAYSIA	2	2019-12-26 09:51:52	2021-12-25 09:51:52
divyarajen16@unifi	1079710041	DIVYA A/P RAJENDRAN	60129696549	divyarajen91@gmail.com	22 JALAN KIARA 40460 SHAH ALAM SELANGOR MALAYSIA	2	2022-05-25 09:51:52	2024-05-24 09:51:52
vigneshsub201@unifi	1078466190	VIGNESH A/L SUBRAMANIAM	60550971469	vigneshsub84@gmail.com	68 JALAN MERANTI 10450 GEORGE TOWN PULAU PINANG MALAYSIA	3	2024-02-04 09:51:52	2027-02-03 09:51:52
divyarajen359@unifi	1096652477	DIVYA A/P RAJENDRAN	608461475128	divyarajen54@yahoo.com	50 JALAN KIARA 93350 KUCHING SARAWAK MALAYSIA	2	2024-01-13 09:51:52	2026-01-12 09:51:52
wongmeilin430@unifi	1032087272	WONG MEI LING	604334101237	wongmeilin70@hotmail.com	90 JALAN BUNGA RAYA 40460 SHAH ALAM SELANGOR MALAYSIA	2	2024-12-12 09:51:52	2026-12-12 09:51:52
chongkahfa258@unifi	1082150993	CHONG KAH FAI	606081319779	chongkahfa19@gmail.com	58 JALAN MERANTI 10450 GEORGE TOWN PULAU PINANG MALAYSIA	3	2023-06-08 09:51:52	2026-06-07 09:51:52
nuraisyahh315@unifi	1010283776	NUR AISYAH BINTI HASSAN	602067117411	nuraisyahh40@hotmail.com	71 JALAN KIARA 40460 SHAH ALAM SELANGOR MALAYSIA	2	2020-10-11 09:51:52	2022-10-11 09:51:52
gohsoonhua794@unifi	1034188867	GOH SOON HUAT	60119943875	gohsoonhua85@hotmail.com	29 JALAN DELIMA 80100 JOHOR BAHRU JOHOR MALAYSIA	3	2022-03-20 09:51:52	2025-03-19 09:51:52
zainalabid756@unifi	1084846085	ZAINAL ABIDIN BIN MOHD	60929681168	zainalabid93@hotmail.com	57 JALAN BUNGA RAYA 88100 KOTA KINABALU SABAH MALAYSIA	2	2018-11-17 09:51:52	2020-11-16 09:51:52
teohbeecho755@unifi	1054357614	TEOH BEE CHOO	60229626076	teohbeecho15@hotmail.com	23 JALAN BUNGA RAYA 80100 JOHOR BAHRU JOHOR MALAYSIA	3	2019-11-17 09:51:52	2022-11-16 09:51:52
kennethloh149@unifi	1098996328	KENNETH LOH KAH SENG	604898884659	kennethloh78@hotmail.com	12 JALAN MERANTI 40460 SHAH ALAM SELANGOR MALAYSIA	2	2020-06-29 09:51:52	2022-06-29 09:51:52
divyarajen791@unifi	1028410614	DIVYA A/P RAJENDRAN	60009837754	divyarajen40@outlook.com	14 JALAN SAGA 30450 IPOH PERAK MALAYSIA	2	2022-02-09 09:51:52	2024-02-09 09:51:52
yapkeansen529@unifi	1013041289	YAP KEAN SENG	60947903920	yapkeansen54@outlook.com	21 JALAN ANGGERIK ARANDA 93350 KUCHING SARAWAK MALAYSIA	1	2018-08-18 09:51:52	2019-08-18 09:51:52
arunkrishn436@unifi	1034825180	ARUN A/L KRISHNAN	60911938671	arunkrishn51@outlook.com	13 JALAN ANGGERIK ARANDA 40460 SHAH ALAM SELANGOR MALAYSIA	2	2021-06-02 09:51:52	2023-06-02 09:51:52
azlinamohd728@unifi	1006695114	AZLINA BINTI MOHD NOOR	60611058036	azlinamohd97@hotmail.com	36 JALAN KIARA 30450 IPOH PERAK MALAYSIA	2	2025-03-16 09:51:52	2027-03-16 09:51:52
rajeshmuru987@unifi	1086625751	RAJESH A/L MURUGAN	603700944218	rajeshmuru86@yahoo.com	78 JALAN MAWAR 40460 SHAH ALAM SELANGOR MALAYSIA	2	2024-11-07 09:51:52	2026-11-07 09:51:52
kennethloh57@unifi	1058990808	KENNETH LOH KAH SENG	60478743555	kennethloh28@outlook.com	7 JALAN CEMPAKA 88100 KOTA KINABALU SABAH MALAYSIA	2	2021-12-18 09:51:52	2023-12-18 09:51:52
rajeshmuru498@unifi	1015485571	RAJESH A/L MURUGAN	600050407675	rajeshmuru37@outlook.com	90 JALAN SAGA 40460 SHAH ALAM SELANGOR MALAYSIA	1	2022-03-19 09:51:52	2023-03-19 09:51:52
sitizaleha592@unifi	1009080674	SITI ZALEHA BINTI IBRAHIM	60536252574	sitizaleha5@gmail.com	32 JALAN SAGA 40460 SHAH ALAM SELANGOR MALAYSIA	1	2024-05-16 09:51:52	2025-05-16 09:51:52
leechinhua468@unifi	1012204755	LEE CHIN HUA	606873020433	leechinhua24@hotmail.com	57 JALAN BUNGA RAYA 93350 KUCHING SARAWAK MALAYSIA	3	2025-05-16 09:51:52	2028-05-15 09:51:52
arunkrishn822@unifi	1099322864	ARUN A/L KRISHNAN	60873151613	arunkrishn9@outlook.com	89 JALAN SAGA 40460 SHAH ALAM SELANGOR MALAYSIA	3	2018-09-10 09:51:52	2021-09-09 09:51:52
teohbeecho43@unifi	1023779518	TEOH BEE CHOO	60763780407	teohbeecho47@gmail.com	69 JALAN SAGA 50000 KUALA LUMPUR WILAYAH PERSEKUTUAN MALAYSIA	2	2023-07-27 09:51:52	2025-07-26 09:51:52
mohamadhaf651@unifi	1002804539	MOHAMAD HAFIZ BIN ISMAIL	601581950888	mohamadhaf9@yahoo.com	55 JALAN MAWAR 80100 JOHOR BAHRU JOHOR MALAYSIA	2	2023-03-07 09:51:52	2025-03-06 09:51:52
muhammadda162@unifi	1083569176	MUHAMMAD DANIAL BIN ZAKARIA	60616940653	muhammadda89@yahoo.com	67 JALAN ANGGERIK ARANDA 30450 IPOH PERAK MALAYSIA	1	2022-05-21 09:51:52	2023-05-21 09:51:52
rosliahmad669@unifi	1030831127	ROSLI BIN AHMAD	608354958345	rosliahmad1@outlook.com	39 JALAN KIARA 88100 KOTA KINABALU SABAH MALAYSIA	1	2024-02-10 09:51:52	2025-02-09 09:51:52
mohamadhaf31@unifi	1029101709	MOHAMAD HAFIZ BIN ISMAIL	605491449705	mohamadhaf72@yahoo.com	22 JALAN ANGGERIK ARANDA 50000 KUALA LUMPUR WILAYAH PERSEKUTUAN MALAYSIA	2	2020-10-23 09:51:52	2022-10-23 09:51:52
tanchweeme791@unifi	1082200910	TAN CHWEE MENG	600261035923	tanchweeme60@gmail.com	74 JALAN CEMPAKA 30450 IPOH PERAK MALAYSIA	3	2022-11-17 09:51:52	2025-11-16 09:51:52
gohsoonhua194@unifi	1099034878	GOH SOON HUAT	601832273610	gohsoonhua26@yahoo.com	86 JALAN ANGGERIK ARANDA 50000 KUALA LUMPUR WILAYAH PERSEKUTUAN MALAYSIA	1	2019-02-05 09:51:52	2020-02-05 09:51:52
tanchweeme843@unifi	1078219053	TAN CHWEE MENG	602480406349	tanchweeme70@hotmail.com	54 JALAN DELIMA 93350 KUCHING SARAWAK MALAYSIA	1	2019-06-18 09:51:52	2020-06-17 09:51:52
rajeshmuru682@unifi	1091485313	RAJESH A/L MURUGAN	60711520619	rajeshmuru18@yahoo.com	54 JALAN KIARA 88100 KOTA KINABALU SABAH MALAYSIA	1	2025-06-08 09:51:52	2026-06-08 09:51:52
priyasamy35@unifi	1023262347	PRIYA A/P SAMY	608871928758	priyasamy93@gmail.com	45 JALAN KIARA 30450 IPOH PERAK MALAYSIA	1	2021-05-11 09:51:52	2022-05-11 09:51:52
saifulazma630@unifi	1070683300	SAIFUL AZMAN BIN RAMLI	601157834702	saifulazma2@gmail.com	31 JALAN DELIMA 10450 GEORGE TOWN PULAU PINANG MALAYSIA	3	2024-07-16 09:51:52	2027-07-16 09:51:52
saifulazma901@unifi	1038586241	SAIFUL AZMAN BIN RAMLI	605784974164	saifulazma12@gmail.com	13 JALAN BUNGA RAYA 30450 IPOH PERAK MALAYSIA	2	2024-03-02 09:51:52	2026-03-02 09:51:52
rosliahmad948@unifi	1094703002	ROSLI BIN AHMAD	600664685835	rosliahmad5@hotmail.com	8 JALAN SAGA 93350 KUCHING SARAWAK MALAYSIA	1	2019-10-26 09:51:52	2020-10-25 09:51:52
zainalabid85@unifi	1017865237	ZAINAL ABIDIN BIN MOHD	60274964336	zainalabid33@yahoo.com	69 JALAN KIARA 30450 IPOH PERAK MALAYSIA	2	2024-04-19 09:51:52	2026-04-19 09:51:52
tanticksew84@unifi	1069395005	TAN TICK SEW	60827827655	tanticksew32@outlook.com	10 JALAN KIARA 80100 JOHOR BAHRU JOHOR MALAYSIA	2	2024-11-27 09:51:52	2026-11-27 09:51:52
wongmeilin187@unifi	1062430245	WONG MEI LING	603689641204	wongmeilin1@outlook.com	5 JALAN KIARA 30450 IPOH PERAK MALAYSIA	2	2019-08-22 09:51:52	2021-08-21 09:51:52
rosliahmad846@unifi	1059894854	ROSLI BIN AHMAD	606489020405	rosliahmad41@outlook.com	49 JALAN MERANTI 80100 JOHOR BAHRU JOHOR MALAYSIA	1	2021-03-11 09:51:52	2022-03-11 09:51:52
cheahsweel70@unifi	1085049257	CHEAH SWEE LAN	606994697573	cheahsweel72@outlook.com	84 JALAN DELIMA 30450 IPOH PERAK MALAYSIA	3	2022-12-28 09:51:52	2025-12-27 09:51:52
arunkrishn86@unifi	1051452866	ARUN A/L KRISHNAN	60007656289	arunkrishn34@gmail.com	24 JALAN DELIMA 50000 KUALA LUMPUR WILAYAH PERSEKUTUAN MALAYSIA	2	2021-01-05 09:51:52	2023-01-05 09:51:52
farahnabil856@unifi	1052819112	FARAH NABILA BINTI YUSOF	60225379990	farahnabil33@outlook.com	48 JALAN ANGGERIK ARANDA 10450 GEORGE TOWN PULAU PINANG MALAYSIA	1	2021-10-19 09:51:52	2022-10-19 09:51:52
chongkahfa371@unifi	1020763293	CHONG KAH FAI	607570302327	chongkahfa6@gmail.com	51 JALAN CEMPAKA 93350 KUCHING SARAWAK MALAYSIA	2	2019-03-09 09:51:52	2021-03-08 09:51:52
kennethloh698@unifi	1022381829	KENNETH LOH KAH SENG	60480842146	kennethloh12@gmail.com	28 JALAN ANGGERIK ARANDA 80100 JOHOR BAHRU JOHOR MALAYSIA	3	2019-05-28 09:51:52	2022-05-27 09:51:52
arunkrishn716@unifi	1037071473	ARUN A/L KRISHNAN	601933878887	arunkrishn32@gmail.com	28 JALAN DELIMA 40460 SHAH ALAM SELANGOR MALAYSIA	1	2019-04-27 09:51:52	2020-04-26 09:51:52
gohsoonhua731@unifi	1087494471	GOH SOON HUAT	60793728533	gohsoonhua36@gmail.com	22 JALAN SAGA 40460 SHAH ALAM SELANGOR MALAYSIA	3	2023-09-26 09:51:52	2026-09-25 09:51:52
chongkahfa498@unifi	1070186717	CHONG KAH FAI	601004942269	chongkahfa94@yahoo.com	30 JALAN KIARA 30450 IPOH PERAK MALAYSIA	2	2018-12-15 09:51:52	2020-12-14 09:51:52
kumaransiv303@unifi	1038521891	KUMARAN A/L SIVAM	60020462209	kumaransiv67@yahoo.com	72 JALAN CEMPAKA 40460 SHAH ALAM SELANGOR MALAYSIA	1	2022-07-28 09:51:52	2023-07-28 09:51:52
rajeshmuru762@unifi	1034330081	RAJESH A/L MURUGAN	60999732680	rajeshmuru24@outlook.com	66 JALAN MERANTI 50000 KUALA LUMPUR WILAYAH PERSEKUTUAN MALAYSIA	3	2021-02-01 09:51:52	2024-02-01 09:51:52
sitizaleha49@unifi	1026935570	SITI ZALEHA BINTI IBRAHIM	60779463143	sitizaleha12@outlook.com	45 JALAN ANGGERIK ARANDA 10450 GEORGE TOWN PULAU PINANG MALAYSIA	2	2025-07-29 09:51:52	2027-07-29 09:51:52
kumaransiv245@unifi	1016634086	KUMARAN A/L SIVAM	60800166523	kumaransiv27@hotmail.com	42 JALAN MAWAR 40460 SHAH ALAM SELANGOR MALAYSIA	3	2019-01-16 09:51:52	2022-01-15 09:51:52
cheahsweel339@unifi	1062456502	CHEAH SWEE LAN	60370801989	cheahsweel10@outlook.com	36 JALAN SAGA 88100 KOTA KINABALU SABAH MALAYSIA	3	2025-08-22 09:51:52	2028-08-21 09:51:52
arunkrishn480@unifi	1029286027	ARUN A/L KRISHNAN	60515734186	arunkrishn78@gmail.com	7 JALAN MERANTI 88100 KOTA KINABALU SABAH MALAYSIA	1	2021-09-06 09:51:52	2022-09-06 09:51:52
\.


--
-- Data for Name: devices; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.devices (mac_address, login_id, friendly_name, manufacturer, brand, device_type, cloud_device_type, link_type, ip_address, ssid_2_4ghz, ssid_5ghz, channel_2_4ghz, channel_5ghz, antenna_2_4ghz, antenna_5ghz, protocol_2_4ghz, protocol_5ghz, rssi, rx_rate, tx_rate, last_seen, parent_mac, platform, bandwidth_2_4ghz, bandwidth_5ghz) FROM stdin;
30:f9:47:d3:fe:0e	ticksew19@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	ChandranVilla_2.4G	ChandranVilla_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
64:ff:0a:f3:35:9b	ticksew19@unifi	64:ff:0a:f3:35:9b	WNC Corporation	Wnc	STA	Access Point	5 GHz	192.168.0.234	\N	\N	\N	\N	2x2	2x2	11ac	11ac	-83	243	650	2026-10-12 09:51:17	30:f9:47:d3:fe:0e	\N	\N	\N
d0:04:19:00:16:23	ticksew19@unifi	OPPO-A57	BBK Electronics Corp., Ltd.	Oppo	STA	Client	5 GHz	192.168.0.60	ChandranVilla_2.4G	ChandranVilla_5G	\N	48	1x1	3x3	11n	11n	-63	240	1111	2026-10-11 16:25:52	30:f9:47:d3:fe:0e	SKYWORTH	40 MHz	160 MHz
e6:20:95:30:2d:c8	ticksew19@unifi	V2332	vivo Mobile Communication Co., Ltd.	Vivo	STA	Repeater	5 GHz	192.168.0.158	ChandranVilla_2.4G	ChandranVilla_5G	\N	36	1x1	3x3	11n	11n	-43	265	836	2026-10-10 14:00:52	30:f9:47:d3:fe:0e	iOS	20 MHz	160 MHz
ef:26:96:14:cd:82	ticksew19@unifi	realme-Note-50	Realme Chongqing Mobile Telecommunications Corp.	Realme	STA	Repeater	2.4 GHz	192.168.0.51	ChandranVilla_2.4G	ChandranVilla_5G	1	\N	1x1	3x3	11n	11n	-63	1090	89	2026-10-08 09:45:52	30:f9:47:d3:fe:0e	Android	20 MHz	160 MHz
d3:56:f7:f7:61:29	ticksew19@unifi	Redmi-13C-5G	Xiaomi Communications Co., Ltd.	Xiaomi	STA	Repeater	2.4 GHz	192.168.0.221	ChandranVilla_2.4G	ChandranVilla_5G	1	\N	2x2	2x2	11n	11n	-74	970	935	2026-10-10 22:54:52	30:f9:47:d3:fe:0e	SKYWORTH	20 MHz	80 MHz
42:32:dd:57:76:ef	azlinamohd444@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	SeriMawar_2.4G	SeriMawar_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
cd:2a:cd:63:32:2f	azlinamohd444@unifi	ESP32-Node	Espressif Inc.	Espressif	STA	Client	2.4 GHz	192.168.0.150	SeriMawar_2.4G	SeriMawar_5G	1	\N	4x4	3x3	11n	11n	-51	1015	75	2026-10-09 13:31:52	42:32:dd:57:76:ef	iOS	40 MHz	80 MHz
be:d2:08:8e:e2:1c	azlinamohd444@unifi	TP-Link-Repeater	TP-Link Technologies Co., Ltd.	TP-Link	STA	Client	5 GHz	192.168.0.194	SeriMawar_2.4G	SeriMawar_5G	\N	153	2x2	1x1	11ax	11ax	-75	48	753	2026-10-11 12:31:52	42:32:dd:57:76:ef	\N	40 MHz	80 MHz
3f:81:88:39:57:23	azlinamohd444@unifi	Sonoff-TH16	ITEAD Intelligent Systems Co., Ltd.	Sonoff	STA	IoT	2.4 GHz	192.168.0.199	SeriMawar_2.4G	\N	1	\N	1x1	1x1	11n	\N	-73	121	147	2026-10-10 19:03:52	42:32:dd:57:76:ef	\N	20 MHz	\N
d3:83:88:26:f3:a7	azlinamohd444@unifi	Sonoff-POW	ITEAD Intelligent Systems Co., Ltd.	Sonoff	STA	IoT	2.4 GHz	192.168.0.241	SeriMawar_2.4G	\N	6	\N	1x1	1x1	11n	\N	-55	131	40	2026-10-08 21:52:52	42:32:dd:57:76:ef	\N	20 MHz	\N
d4:a1:ee:eb:5a:59	azlinamohd444@unifi	Shelly-1	Allterco Robotics EOOD	Shelly	STA	IoT	2.4 GHz	192.168.0.223	SeriMawar_2.4G	\N	11	\N	1x1	1x1	11n	\N	-50	149	118	2026-10-07 19:43:52	42:32:dd:57:76:ef	\N	20 MHz	\N
bf:44:6f:04:00:53	muhammadda300@unifi	Root	Fiberhome Telecommunication Technologies Co., Ltd.	FiberHome	Root	Access Point	Ethernet	192.168.0.1	TamanAman_2.4G	TamanAman_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	FIBERHOME	40 MHz	160 MHz
e1:1b:9a:58:6f:33	muhammadda300@unifi	e1:1b:9a:58:6f:33	Shenzhen Skyworth Digital Technology CO.	Skyworth	STA	Gateway	2.4 GHz	192.168.0.248	TamanAman_2.4G	TamanAman_5G	11	\N	3x3	2x2	11n	11n	-84	128	1080	2026-10-11 11:49:52	bf:44:6f:04:00:53	Windows	40 MHz	80 MHz
10:22:66:e9:81:74	muhammadda300@unifi	TP-Link-Repeater	TP-Link Technologies Co., Ltd.	TP-Link	STA	Gateway	2.4 GHz	192.168.0.168	TamanAman_2.4G	TamanAman_5G	11	\N	4x4	4x4	11n	11n	-83	851	26	2026-10-08 08:45:52	bf:44:6f:04:00:53	iOS	40 MHz	80 MHz
1a:57:2a:b8:37:22	muhammadda300@unifi	iPad-Air	Apple, Inc.	Apple	STA	Client	2.4 GHz	192.168.0.100	TamanAman_2.4G	TamanAman_5G	1	\N	3x3	1x1	11ac	11ac	-87	926	50	2026-10-07 10:41:52	bf:44:6f:04:00:53	Linux	20 MHz	80 MHz
e3:8f:a8:ac:80:49	muhammadda300@unifi	realme-Note-50	Realme Chongqing Mobile Telecommunications Corp.	Realme	STA	Client	5 GHz	192.168.0.214	TamanAman_2.4G	TamanAman_5G	\N	48	3x3	2x2	11ax	11ax	-56	149	487	2026-10-09 18:36:52	bf:44:6f:04:00:53	\N	20 MHz	80 MHz
85:88:96:45:79:d4	muhammadda300@unifi	OPPO-Reno8	BBK Electronics Corp., Ltd.	Oppo	STA	Client	5 GHz	192.168.0.117	TamanAman_2.4G	TamanAman_5G	\N	44	4x4	2x2	11ac	11ac	-89	1115	438	2026-10-11 18:12:52	bf:44:6f:04:00:53	Android	40 MHz	80 MHz
38:f3:bb:c1:ff:39	tanticksew53@unifi	Root	Fiberhome Telecommunication Technologies Co., Ltd.	FiberHome	Root	Access Point	Ethernet	192.168.0.1	ChandranVilla_2.4G	ChandranVilla_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	FIBERHOME	40 MHz	160 MHz
73:87:19:c7:e0:be	tanticksew53@unifi	OnePlus-Nord	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Client	5 GHz	192.168.0.198	ChandranVilla_2.4G	ChandranVilla_5G	\N	44	3x3	2x2	11ac	11ac	-32	849	1074	2026-10-09 08:41:52	38:f3:bb:c1:ff:39	\N	40 MHz	160 MHz
7f:01:94:92:26:21	tanticksew53@unifi	OnePlus-11	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Gateway	5 GHz	192.168.0.104	ChandranVilla_2.4G	ChandranVilla_5G	\N	44	3x3	3x3	11ac	11ac	-38	32	128	2026-10-09 18:16:52	38:f3:bb:c1:ff:39	\N	20 MHz	80 MHz
06:68:ec:47:35:d3	tanticksew53@unifi	OnePlus-Nord	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Repeater	5 GHz	192.168.0.44	ChandranVilla_2.4G	ChandranVilla_5G	\N	40	4x4	2x2	11ac	11ac	-73	615	59	2026-10-08 03:30:52	38:f3:bb:c1:ff:39	Windows	40 MHz	160 MHz
0c:4f:5b:55:c3:79	tanticksew53@unifi	Hue-Bridge	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.233	ChandranVilla_2.4G	\N	11	\N	1x1	1x1	11n	\N	-65	54	124	2026-10-11 03:47:52	38:f3:bb:c1:ff:39	\N	20 MHz	\N
10:5f:bb:56:67:60	tanticksew53@unifi	Shelly-Plus-1PM	Allterco Robotics EOOD	Shelly	STA	IoT	2.4 GHz	192.168.0.9	ChandranVilla_2.4G	\N	1	\N	1x1	1x1	11n	\N	-43	99	82	2026-10-07 06:33:52	38:f3:bb:c1:ff:39	\N	20 MHz	\N
0b:0a:84:6a:23:db	tanticksew53@unifi	Tuya-SmartPlug	Tuya Smart Inc.	Tuya	STA	IoT	2.4 GHz	192.168.0.152	ChandranVilla_2.4G	\N	1	\N	1x1	1x1	11n	\N	-63	77	128	2026-10-09 01:21:52	38:f3:bb:c1:ff:39	\N	20 MHz	\N
45:05:5f:eb:d1:29	kennethloh334@unifi	Root	Fiberhome Telecommunication Technologies Co., Ltd.	FiberHome	Root	Access Point	Ethernet	192.168.0.1	BayuHome_2.4G	BayuHome_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	FIBERHOME	40 MHz	160 MHz
e1:aa:a9:1d:96:a1	kennethloh334@unifi	ESP32-Node	Espressif Inc.	Espressif	STA	Repeater	5 GHz	192.168.0.166	BayuHome_2.4G	BayuHome_5G	\N	44	4x4	3x3	11n	11n	-70	1046	1031	2026-10-11 11:28:52	45:05:5f:eb:d1:29	\N	20 MHz	160 MHz
73:81:92:e3:3f:15	kennethloh334@unifi	V2332	vivo Mobile Communication Co., Ltd.	Vivo	STA	Gateway	5 GHz	192.168.0.91	BayuHome_2.4G	BayuHome_5G	\N	157	2x2	1x1	11n	11n	-30	35	1131	2026-10-11 21:31:52	45:05:5f:eb:d1:29	Windows	20 MHz	160 MHz
fa:bc:3f:16:8f:ec	kennethloh334@unifi	WNC-Client	WNC Corporation	Wnc	STA	Repeater	2.4 GHz	192.168.0.13	BayuHome_2.4G	BayuHome_5G	11	\N	1x1	3x3	11ax	11ax	-79	898	843	2026-10-09 23:19:52	45:05:5f:eb:d1:29	SKYWORTH	40 MHz	160 MHz
dd:d8:6f:26:b6:a4	kennethloh334@unifi	dd:d8:6f:26:b6:a4	Samsung Electronics Co., Ltd.	Samsung	STA	Client	2.4 GHz	192.168.0.73	BayuHome_2.4G	BayuHome_5G	1	\N	3x3	1x1	11n	11n	-74	554	116	2026-10-09 16:25:52	45:05:5f:eb:d1:29	\N	20 MHz	80 MHz
3d:41:4d:97:4f:f0	kennethloh334@unifi	ESP32-Node	Espressif Inc.	Espressif	STA	Repeater	2.4 GHz	192.168.0.80	BayuHome_2.4G	BayuHome_5G	1	\N	4x4	1x1	11n	11n	-34	946	301	2026-10-09 19:24:52	45:05:5f:eb:d1:29	SKYWORTH	20 MHz	160 MHz
ab:46:5a:bf:ac:65	kennethloh334@unifi	iPad-Air	Apple, Inc.	Apple	STA	Repeater	2.4 GHz	192.168.0.51	BayuHome_2.4G	BayuHome_5G	1	\N	4x4	3x3	11ac	11ac	-51	587	1023	2026-10-11 07:16:52	45:05:5f:eb:d1:29	SKYWORTH	40 MHz	80 MHz
07:f7:c9:9f:90:48	kennethloh334@unifi	ESP8266-Sensor	Espressif Inc.	Espressif	STA	IoT	2.4 GHz	192.168.0.113	BayuHome_2.4G	\N	11	\N	1x1	1x1	11n	\N	-74	131	115	2026-10-09 12:42:52	45:05:5f:eb:d1:29	\N	20 MHz	\N
09:ab:71:22:09:a8	kennethloh334@unifi	Tuya-SmartPlug	Tuya Smart Inc.	Tuya	STA	IoT	2.4 GHz	192.168.0.68	BayuHome_2.4G	\N	1	\N	1x1	1x1	11n	\N	-40	128	19	2026-10-07 15:55:52	45:05:5f:eb:d1:29	\N	20 MHz	\N
05:24:47:4e:15:bd	hasnahsall843@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	SeriMawar_2.4G	SeriMawar_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
d3:cd:2f:26:96:ab	hasnahsall843@unifi	OnePlus-11	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Repeater	5 GHz	192.168.0.140	SeriMawar_2.4G	SeriMawar_5G	\N	36	2x2	3x3	11ac	11ac	-76	122	678	2026-10-09 12:39:52	05:24:47:4e:15:bd	Windows	20 MHz	160 MHz
46:be:7a:b1:83:49	hasnahsall843@unifi	46:be:7a:b1:83:49	WNC Corporation	Wnc	STA	Repeater	2.4 GHz	192.168.0.2	SeriMawar_2.4G	SeriMawar_5G	1	\N	2x2	1x1	11ac	11ac	-65	1111	1081	2026-10-08 17:12:52	05:24:47:4e:15:bd	SKYWORTH	20 MHz	80 MHz
a7:f3:e2:11:06:cb	hasnahsall843@unifi	decoMeshM4	TP-Link Systems Inc.	Tp Link	STA	Access Point	5 GHz	192.168.0.93	SeriMawar_2.4G	SeriMawar_5G	\N	161	2x2	4x4	11ax	11ax	-44	299	407	2026-10-11 05:24:52	05:24:47:4e:15:bd	\N	40 MHz	160 MHz
aa:ab:f2:0d:82:78	hasnahsall843@unifi	eero-Max-7	Amazon Technologies Inc.	Amazon	STA	Access Point	5 GHz	192.168.0.96	SeriMawar_2.4G	SeriMawar_5G	\N	44	2x2	2x2	11ax	11ax	-47	933	733	2026-10-10 15:55:52	05:24:47:4e:15:bd	\N	40 MHz	160 MHz
95:96:7d:38:8e:42	hasnahsall843@unifi	Hue-Bulb	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.87	SeriMawar_2.4G	\N	1	\N	1x1	1x1	11n	\N	-45	118	138	2026-10-09 15:52:52	05:24:47:4e:15:bd	\N	20 MHz	\N
e9:b3:56:33:96:fd	chongkahfa740@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	TamanAman_2.4G	TamanAman_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
42:5b:e4:83:d6:b9	chongkahfa740@unifi	iPad-Air	Apple, Inc.	Apple	STA	Client	2.4 GHz	192.168.0.109	TamanAman_2.4G	TamanAman_5G	1	\N	2x2	3x3	11n	11n	-86	175	351	2026-10-09 23:05:52	e9:b3:56:33:96:fd	Linux	40 MHz	160 MHz
fd:03:1b:ac:78:dc	chongkahfa740@unifi	TP-Link-Repeater	TP-Link Technologies Co., Ltd.	TP-Link	STA	Client	2.4 GHz	192.168.0.127	TamanAman_2.4G	TamanAman_5G	11	\N	4x4	3x3	11n	11n	-90	533	827	2026-10-09 08:51:52	e9:b3:56:33:96:fd	\N	40 MHz	80 MHz
d3:8a:3b:7a:af:d3	chongkahfa740@unifi	V2029	vivo Mobile Communication Co., Ltd.	Vivo	STA	Gateway	5 GHz	192.168.0.60	TamanAman_2.4G	TamanAman_5G	\N	44	3x3	4x4	11ac	11ac	-41	1111	437	2026-10-07 14:48:52	e9:b3:56:33:96:fd	SKYWORTH	20 MHz	160 MHz
f0:f3:a9:66:6e:7f	chongkahfa740@unifi	iPad-Air	Apple, Inc.	Apple	STA	Repeater	2.4 GHz	192.168.0.209	TamanAman_2.4G	TamanAman_5G	11	\N	4x4	2x2	11n	11n	-68	713	380	2026-10-11 04:55:52	e9:b3:56:33:96:fd	SKYWORTH	20 MHz	80 MHz
51:a3:3d:1a:57:11	chongkahfa740@unifi	WNC-Client	WNC Corporation	Wnc	STA	Repeater	5 GHz	192.168.0.32	TamanAman_2.4G	TamanAman_5G	\N	161	1x1	3x3	11n	11n	-89	172	438	2026-10-11 04:14:52	e9:b3:56:33:96:fd	\N	20 MHz	160 MHz
b2:7e:1b:04:ef:b0	chongkahfa740@unifi	MacBook-Pro	Apple, Inc.	Apple	STA	Client	2.4 GHz	192.168.0.44	TamanAman_2.4G	TamanAman_5G	6	\N	3x3	4x4	11ac	11ac	-70	956	769	2026-10-10 19:25:52	e9:b3:56:33:96:fd	Windows	40 MHz	80 MHz
3e:c8:3f:14:dc:02	chongkahfa740@unifi	Hue-Strip	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.3	TamanAman_2.4G	\N	1	\N	1x1	1x1	11n	\N	-56	70	145	2026-10-05 18:07:52	e9:b3:56:33:96:fd	\N	20 MHz	\N
87:5e:72:b4:f7:18	chongkahfa740@unifi	Shelly-1	Allterco Robotics EOOD	Shelly	STA	IoT	2.4 GHz	192.168.0.175	TamanAman_2.4G	\N	6	\N	1x1	1x1	11n	\N	-67	44	52	2026-10-05 23:34:52	e9:b3:56:33:96:fd	\N	20 MHz	\N
a1:c9:00:d2:be:7c	arunkrishn780@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	ArandaHome_2.4G	ArandaHome_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
a6:21:b8:0f:69:8b	arunkrishn780@unifi	SKYWORTH-STB	Shenzhen Skyworth Digital Technology CO.	Skyworth	STA	Gateway	5 GHz	192.168.0.28	ArandaHome_2.4G	ArandaHome_5G	\N	48	2x2	2x2	11ax	11ax	-89	939	1134	2026-10-10 01:49:52	a1:c9:00:d2:be:7c	Windows	40 MHz	80 MHz
e5:ea:09:70:a9:58	arunkrishn780@unifi	Galaxy-A54	Samsung Electronics Co., Ltd.	Samsung	STA	Gateway	5 GHz	192.168.0.130	ArandaHome_2.4G	ArandaHome_5G	\N	48	1x1	4x4	11ax	11ax	-33	231	709	2026-10-09 20:44:52	a1:c9:00:d2:be:7c	Linux	20 MHz	80 MHz
a7:e6:d2:e4:8a:4c	arunkrishn780@unifi	SKYWORTH-STB	Shenzhen Skyworth Digital Technology CO.	Skyworth	STA	Repeater	5 GHz	192.168.0.37	ArandaHome_2.4G	ArandaHome_5G	\N	149	2x2	4x4	11n	11n	-56	648	935	2026-10-09 21:19:52	a1:c9:00:d2:be:7c	Android	20 MHz	160 MHz
d4:c8:44:04:51:91	arunkrishn780@unifi	Pixel-7	Google LLC	Google	STA	Client	2.4 GHz	192.168.0.115	ArandaHome_2.4G	ArandaHome_5G	11	\N	1x1	3x3	11ax	11ax	-87	1102	846	2026-10-08 06:56:52	a1:c9:00:d2:be:7c	\N	20 MHz	160 MHz
e4:11:b5:86:74:eb	arunkrishn780@unifi	POCO-M5	Xiaomi Communications Co., Ltd.	Xiaomi	STA	Repeater	5 GHz	192.168.0.27	ArandaHome_2.4G	ArandaHome_5G	\N	161	4x4	1x1	11ac	11ac	-81	127	1162	2026-10-07 15:30:52	a1:c9:00:d2:be:7c	Linux	20 MHz	160 MHz
b3:d0:60:fb:be:96	zainalabid371@unifi	Root	ZTE Corporation	ZTE	Root	Access Point	Ethernet	192.168.0.1	ArandaHome_2.4G	ArandaHome_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	ZTE	40 MHz	160 MHz
8c:c2:58:fd:c8:11	zainalabid371@unifi	OnePlus-11	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Client	2.4 GHz	192.168.0.39	ArandaHome_2.4G	ArandaHome_5G	6	\N	4x4	3x3	11n	11n	-56	73	638	2026-10-11 01:28:52	b3:d0:60:fb:be:96	iOS	20 MHz	160 MHz
4b:eb:47:90:26:e8	zainalabid371@unifi	TP-Link-Repeater	TP-Link Technologies Co., Ltd.	TP-Link	STA	Repeater	5 GHz	192.168.0.73	ArandaHome_2.4G	ArandaHome_5G	\N	48	2x2	4x4	11ax	11ax	-55	994	1131	2026-10-07 15:47:52	b3:d0:60:fb:be:96	Windows	40 MHz	160 MHz
07:15:73:a4:48:13	zainalabid371@unifi	Galaxy-M14	Samsung Electronics Co., Ltd.	Samsung	STA	Client	2.4 GHz	192.168.0.121	ArandaHome_2.4G	ArandaHome_5G	11	\N	3x3	4x4	11ac	11ac	-71	132	831	2026-10-09 18:13:52	b3:d0:60:fb:be:96	Windows	20 MHz	160 MHz
90:87:5a:ef:69:09	zainalabid371@unifi	Pixel-7	Google LLC	Google	STA	Repeater	5 GHz	192.168.0.228	ArandaHome_2.4G	ArandaHome_5G	\N	153	1x1	1x1	11ac	11ac	-82	802	906	2026-10-10 05:50:52	b3:d0:60:fb:be:96	\N	40 MHz	80 MHz
69:7e:04:5f:c0:1c	divyarajen754@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	VillaSri_2.4G	VillaSri_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
e1:e8:47:cb:b4:92	divyarajen754@unifi	WNC-AP	WNC Corporation	Wnc	STA	Gateway	2.4 GHz	192.168.0.228	VillaSri_2.4G	VillaSri_5G	1	\N	1x1	3x3	11n	11n	-71	389	728	2026-10-09 12:41:52	69:7e:04:5f:c0:1c	Android	20 MHz	80 MHz
5e:3a:bf:1e:ce:fa	leechinhua468@unifi	Shelly-1	Allterco Robotics EOOD	Shelly	STA	IoT	2.4 GHz	192.168.0.32	VillaSri_2.4G	\N	1	\N	1x1	1x1	11n	\N	-58	75	64	2026-10-08 13:25:52	6e:36:ff:e3:f2:8a	\N	20 MHz	\N
4a:95:83:e2:f6:74	divyarajen754@unifi	iPad-Air	Apple, Inc.	Apple	STA	Gateway	5 GHz	192.168.0.226	VillaSri_2.4G	VillaSri_5G	\N	153	1x1	2x2	11n	11n	-33	739	847	2026-10-07 14:56:52	69:7e:04:5f:c0:1c	Linux	20 MHz	80 MHz
8f:86:4c:df:9d:21	divyarajen754@unifi	OnePlus-11	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Repeater	5 GHz	192.168.0.159	VillaSri_2.4G	VillaSri_5G	\N	40	1x1	3x3	11n	11n	-31	489	187	2026-10-08 09:08:52	69:7e:04:5f:c0:1c	Android	20 MHz	80 MHz
23:93:e2:59:c0:c3	divyarajen754@unifi	eero-Max-7	Amazon Technologies Inc.	Amazon	STA	Access Point	2.4 GHz	192.168.0.125	VillaSri_2.4G	VillaSri_5G	6	\N	2x2	2x2	11ax	11ax	-40	986	783	2026-10-12 03:17:52	69:7e:04:5f:c0:1c	\N	40 MHz	160 MHz
16:92:e5:84:e2:39	divyarajen754@unifi	Tuya-SmartPlug	Tuya Smart Inc.	Tuya	STA	IoT	2.4 GHz	192.168.0.29	VillaSri_2.4G	\N	1	\N	1x1	1x1	11n	\N	-73	150	103	2026-10-11 16:10:52	69:7e:04:5f:c0:1c	\N	20 MHz	\N
48:2b:25:4e:39:a2	divyarajen754@unifi	Tuya-Bulb	Tuya Smart Inc.	Tuya	STA	IoT	2.4 GHz	192.168.0.116	VillaSri_2.4G	\N	6	\N	1x1	1x1	11n	\N	-60	62	46	2026-10-07 22:55:52	69:7e:04:5f:c0:1c	\N	20 MHz	\N
38:bd:5e:56:4a:7e	divyarajen754@unifi	Sonoff-POW	ITEAD Intelligent Systems Co., Ltd.	Sonoff	STA	IoT	2.4 GHz	192.168.0.141	VillaSri_2.4G	\N	1	\N	1x1	1x1	11n	\N	-66	29	134	2026-10-05 10:53:52	69:7e:04:5f:c0:1c	\N	20 MHz	\N
4d:4c:81:6c:4b:16	divyarajen754@unifi	Tuya-Bulb	Tuya Smart Inc.	Tuya	STA	IoT	2.4 GHz	192.168.0.230	VillaSri_2.4G	\N	6	\N	1x1	1x1	11n	\N	-64	139	11	2026-10-12 06:10:52	69:7e:04:5f:c0:1c	\N	20 MHz	\N
75:ea:65:1f:2f:02	mohdrizalo944@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	DamaiResidensi_2.4G	DamaiResidensi_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
cd:44:b7:7b:33:3d	mohdrizalo944@unifi	Redmi-13C-5G	Xiaomi Communications Co., Ltd.	Xiaomi	STA	Gateway	2.4 GHz	192.168.0.129	DamaiResidensi_2.4G	DamaiResidensi_5G	6	\N	1x1	3x3	11ac	11ac	-51	926	698	2026-10-09 18:04:52	75:ea:65:1f:2f:02	SKYWORTH	20 MHz	80 MHz
22:64:ac:30:0a:9b	mohdrizalo944@unifi	Galaxy-A54	Samsung Electronics Co., Ltd.	Samsung	STA	Gateway	5 GHz	192.168.0.26	DamaiResidensi_2.4G	DamaiResidensi_5G	\N	149	2x2	1x1	11n	11n	-74	1182	1006	2026-10-11 09:13:52	75:ea:65:1f:2f:02	Windows	40 MHz	160 MHz
3c:ff:3d:a0:f9:d2	mohdrizalo944@unifi	Orbi-RBS350	Netgear Inc.	Netgear	STA	Access Point	Ethernet	192.168.0.214	DamaiResidensi_2.4G	DamaiResidensi_5G	\N	\N	2x2	4x4	11ax	11ax	\N	\N	\N	2026-10-11 21:20:52	75:ea:65:1f:2f:02	\N	\N	\N
81:77:1c:df:e1:ea	mohdrizalo944@unifi	Hue-Bulb	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.9	DamaiResidensi_2.4G	\N	6	\N	1x1	1x1	11n	\N	-61	41	144	2026-10-06 12:07:52	75:ea:65:1f:2f:02	\N	20 MHz	\N
7c:18:5f:a9:72:c7	mohdrizalo944@unifi	Sonoff-Basic	ITEAD Intelligent Systems Co., Ltd.	Sonoff	STA	IoT	2.4 GHz	192.168.0.61	DamaiResidensi_2.4G	\N	11	\N	1x1	1x1	11n	\N	-73	100	120	2026-10-11 14:05:52	75:ea:65:1f:2f:02	\N	20 MHz	\N
d3:9b:26:4f:73:09	mohdrizalo944@unifi	Tuya-Wall-Switch	Tuya Smart Inc.	Tuya	STA	IoT	2.4 GHz	192.168.0.7	DamaiResidensi_2.4G	\N	1	\N	1x1	1x1	11n	\N	-51	31	32	2026-10-10 01:17:52	75:ea:65:1f:2f:02	\N	20 MHz	\N
a9:8b:e5:c7:df:5d	mohdrizalo944@unifi	Hue-Strip	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.54	DamaiResidensi_2.4G	\N	11	\N	1x1	1x1	11n	\N	-71	12	54	2026-10-11 02:18:52	75:ea:65:1f:2f:02	\N	20 MHz	\N
b3:0d:bd:fc:6a:40	leechinhua764@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	VillaSri_2.4G	VillaSri_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
29:fc:5b:15:9a:bb	leechinhua764@unifi	realme-11-Pro	Realme Chongqing Mobile Telecommunications Corp.	Realme	STA	Repeater	2.4 GHz	192.168.0.144	VillaSri_2.4G	VillaSri_5G	6	\N	2x2	2x2	11ac	11ac	-66	813	567	2026-10-11 13:47:52	b3:0d:bd:fc:6a:40	SKYWORTH	20 MHz	160 MHz
c0:a0:59:f4:be:e4	leechinhua764@unifi	c0:a0:59:f4:be:e4	Xiaomi Communications Co., Ltd.	Xiaomi	STA	Gateway	2.4 GHz	192.168.0.59	VillaSri_2.4G	VillaSri_5G	11	\N	3x3	4x4	11ac	11ac	-84	511	1068	2026-10-07 11:35:52	b3:0d:bd:fc:6a:40	Windows	20 MHz	80 MHz
a7:52:7f:ca:84:ff	leechinhua764@unifi	OnePlus-11	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Client	2.4 GHz	192.168.0.72	VillaSri_2.4G	VillaSri_5G	1	\N	2x2	4x4	11n	11n	-61	419	463	2026-10-11 12:33:52	b3:0d:bd:fc:6a:40	Windows	20 MHz	160 MHz
2c:e4:af:ef:23:5b	leechinhua764@unifi	Echo-Dot	Amazon Technologies Inc.	Amazon	STA	Repeater	2.4 GHz	192.168.0.71	VillaSri_2.4G	VillaSri_5G	6	\N	4x4	4x4	11n	11n	-67	505	37	2026-10-11 02:49:52	b3:0d:bd:fc:6a:40	Windows	20 MHz	80 MHz
e4:ee:5f:62:44:88	leechinhua764@unifi	e4:ee:5f:62:44:88	Shenzhen Skyworth Digital Technology CO.	Skyworth	STA	Repeater	2.4 GHz	192.168.0.156	VillaSri_2.4G	VillaSri_5G	1	\N	4x4	3x3	11ac	11ac	-79	612	661	2026-10-10 20:42:52	b3:0d:bd:fc:6a:40	Linux	20 MHz	160 MHz
9f:37:5e:0b:82:e4	leechinhua764@unifi	V2029	vivo Mobile Communication Co., Ltd.	Vivo	STA	Repeater	2.4 GHz	192.168.0.175	VillaSri_2.4G	VillaSri_5G	6	\N	2x2	2x2	11ax	11ax	-86	1050	1126	2026-10-09 17:09:52	b3:0d:bd:fc:6a:40	Linux	20 MHz	80 MHz
6a:88:c6:50:2e:03	leechinhua764@unifi	Tuya-Bulb	Tuya Smart Inc.	Tuya	STA	IoT	2.4 GHz	192.168.0.92	VillaSri_2.4G	\N	6	\N	1x1	1x1	11n	\N	-61	9	92	2026-10-06 02:43:52	b3:0d:bd:fc:6a:40	\N	20 MHz	\N
84:55:21:07:3e:31	leechinhua764@unifi	Tuya-Wall-Switch	Tuya Smart Inc.	Tuya	STA	IoT	2.4 GHz	192.168.0.13	VillaSri_2.4G	\N	1	\N	1x1	1x1	11n	\N	-72	56	27	2026-10-05 18:15:52	b3:0d:bd:fc:6a:40	\N	20 MHz	\N
0e:d0:f6:06:93:e7	leechinhua764@unifi	Tuya-Wall-Switch	Tuya Smart Inc.	Tuya	STA	IoT	2.4 GHz	192.168.0.213	VillaSri_2.4G	\N	6	\N	1x1	1x1	11n	\N	-76	20	26	2026-10-10 20:29:52	b3:0d:bd:fc:6a:40	\N	20 MHz	\N
5c:f9:ee:d6:e3:70	leechinhua764@unifi	Tuya-Wall-Switch	Tuya Smart Inc.	Tuya	STA	IoT	2.4 GHz	192.168.0.251	VillaSri_2.4G	\N	11	\N	1x1	1x1	11n	\N	-43	133	90	2026-10-11 04:50:52	b3:0d:bd:fc:6a:40	\N	20 MHz	\N
40:12:f8:df:f6:fc	limweiming953@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	TamanAman_2.4G	TamanAman_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
be:f7:10:2f:54:6f	limweiming953@unifi	Galaxy-S23	Samsung Electronics Co., Ltd.	Samsung	STA	Gateway	2.4 GHz	192.168.0.244	TamanAman_2.4G	TamanAman_5G	6	\N	3x3	4x4	11n	11n	-78	449	60	2026-10-12 06:03:52	40:12:f8:df:f6:fc	Android	40 MHz	80 MHz
30:26:91:25:24:81	limweiming953@unifi	30:26:91:25:24:81	TP-Link Technologies Co., Ltd.	TP-Link	STA	Client	5 GHz	192.168.0.98	TamanAman_2.4G	TamanAman_5G	\N	157	4x4	1x1	11ax	11ax	-66	684	199	2026-10-11 21:26:52	40:12:f8:df:f6:fc	Windows	40 MHz	80 MHz
a1:9b:b0:cd:c5:c9	limweiming953@unifi	Fire-TV-Stick	Amazon Technologies Inc.	Amazon	STA	Repeater	2.4 GHz	192.168.0.171	TamanAman_2.4G	TamanAman_5G	6	\N	3x3	4x4	11n	11n	-76	307	711	2026-10-08 21:52:52	40:12:f8:df:f6:fc	\N	40 MHz	80 MHz
2e:5c:98:fd:fd:2b	limweiming953@unifi	OnePlus-Nord	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Repeater	2.4 GHz	192.168.0.144	TamanAman_2.4G	TamanAman_5G	6	\N	3x3	2x2	11n	11n	-73	1105	377	2026-10-09 02:24:52	40:12:f8:df:f6:fc	Android	20 MHz	160 MHz
98:5d:4a:fb:cb:1c	gohsoonhua435@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	VillaSri_2.4G	VillaSri_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
e5:4f:d3:0a:83:89	gohsoonhua435@unifi	SKYWORTH-STB	Shenzhen Skyworth Digital Technology CO.	Skyworth	STA	Repeater	2.4 GHz	192.168.0.18	VillaSri_2.4G	VillaSri_5G	1	\N	3x3	4x4	11ax	11ax	-64	927	767	2026-10-09 15:53:52	98:5d:4a:fb:cb:1c	SKYWORTH	20 MHz	80 MHz
f4:18:eb:50:57:59	gohsoonhua435@unifi	SKYWORTH-STB	Shenzhen Skyworth Digital Technology CO.	Skyworth	STA	Client	2.4 GHz	192.168.0.173	VillaSri_2.4G	VillaSri_5G	6	\N	3x3	1x1	11ac	11ac	-44	287	967	2026-10-08 08:57:52	98:5d:4a:fb:cb:1c	SKYWORTH	20 MHz	160 MHz
bf:b0:96:a7:3a:73	gohsoonhua435@unifi	TP-Link-Repeater	TP-Link Technologies Co., Ltd.	TP-Link	STA	Client	2.4 GHz	192.168.0.222	VillaSri_2.4G	VillaSri_5G	6	\N	1x1	1x1	11ac	11ac	-47	649	694	2026-10-08 23:06:52	98:5d:4a:fb:cb:1c	Android	20 MHz	80 MHz
c1:d0:9a:b2:c3:0c	gohsoonhua435@unifi	WNC-AP	WNC Corporation	Wnc	STA	Repeater	2.4 GHz	192.168.0.56	VillaSri_2.4G	VillaSri_5G	6	\N	3x3	1x1	11ac	11ac	-38	901	991	2026-10-07 19:23:52	98:5d:4a:fb:cb:1c	iOS	40 MHz	160 MHz
23:fb:bd:8d:d6:f1	gohsoonhua435@unifi	23:fb:bd:8d:d6:f1	vivo Mobile Communication Co., Ltd.	Vivo	STA	Client	5 GHz	192.168.0.180	VillaSri_2.4G	VillaSri_5G	\N	40	2x2	2x2	11n	11n	-63	235	56	2026-10-07 13:23:52	98:5d:4a:fb:cb:1c	\N	40 MHz	80 MHz
a2:0b:3b:31:0b:72	gohsoonhua435@unifi	AX201-Client	Intel Corporate	Intel	STA	Gateway	5 GHz	192.168.0.110	VillaSri_2.4G	VillaSri_5G	\N	40	2x2	4x4	11ac	11ac	-70	1143	299	2026-10-11 12:50:52	98:5d:4a:fb:cb:1c	Linux	20 MHz	160 MHz
dc:ee:36:b6:cb:2c	norhayatio609@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	DamaiResidensi_2.4G	DamaiResidensi_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
c6:e1:fb:c5:80:ad	norhayatio609@unifi	c6:e1:fb:c5:80:ad	Espressif Inc.	Espressif	STA	Client	2.4 GHz	192.168.0.77	DamaiResidensi_2.4G	DamaiResidensi_5G	11	\N	1x1	2x2	11ac	11ac	-54	1081	575	2026-10-11 11:00:52	dc:ee:36:b6:cb:2c	SKYWORTH	20 MHz	80 MHz
fd:39:e2:7f:6d:4f	norhayatio609@unifi	Galaxy-S23	Samsung Electronics Co., Ltd.	Samsung	STA	Gateway	5 GHz	192.168.0.58	DamaiResidensi_2.4G	DamaiResidensi_5G	\N	40	2x2	2x2	11ax	11ax	-59	1082	691	2026-10-08 23:10:52	dc:ee:36:b6:cb:2c	Linux	20 MHz	80 MHz
b0:7b:ac:c0:6e:0b	norhayatio609@unifi	Nest-Hub	Google LLC	Google	STA	Gateway	5 GHz	192.168.0.251	DamaiResidensi_2.4G	DamaiResidensi_5G	\N	40	3x3	2x2	11ac	11ac	-54	1030	1119	2026-10-10 06:43:52	dc:ee:36:b6:cb:2c	SKYWORTH	20 MHz	160 MHz
8d:cf:04:e9:0e:e7	norhayatio609@unifi	8d:cf:04:e9:0e:e7	Realme Chongqing Mobile Telecommunications Corp.	Realme	STA	Client	2.4 GHz	192.168.0.251	DamaiResidensi_2.4G	DamaiResidensi_5G	1	\N	3x3	3x3	11ac	11ac	-39	634	1147	2026-10-09 12:03:52	dc:ee:36:b6:cb:2c	Linux	20 MHz	160 MHz
3d:23:62:56:fa:a3	norhayatio609@unifi	Fire-TV-Stick	Amazon Technologies Inc.	Amazon	STA	Client	2.4 GHz	192.168.0.106	DamaiResidensi_2.4G	DamaiResidensi_5G	1	\N	1x1	3x3	11n	11n	-33	791	922	2026-10-08 14:02:52	dc:ee:36:b6:cb:2c	\N	20 MHz	80 MHz
d5:8c:90:b6:71:1c	norhayatio609@unifi	V2029	vivo Mobile Communication Co., Ltd.	Vivo	STA	Client	5 GHz	192.168.0.3	DamaiResidensi_2.4G	DamaiResidensi_5G	\N	153	2x2	4x4	11ac	11ac	-44	981	422	2026-10-11 14:09:52	dc:ee:36:b6:cb:2c	SKYWORTH	40 MHz	160 MHz
2e:69:31:2f:2b:57	leechinhua381@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	ArandaHome_2.4G	ArandaHome_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
72:7e:ed:9e:18:d2	leechinhua381@unifi	72:7e:ed:9e:18:d2	Espressif Inc.	Espressif	STA	Gateway	2.4 GHz	192.168.0.187	ArandaHome_2.4G	ArandaHome_5G	11	\N	3x3	1x1	11n	11n	-66	938	1170	2026-10-10 13:37:52	2e:69:31:2f:2b:57	Windows	20 MHz	80 MHz
64:be:c5:8f:bf:45	leechinhua381@unifi	V2207	vivo Mobile Communication Co., Ltd.	Vivo	STA	Repeater	5 GHz	192.168.0.43	ArandaHome_2.4G	ArandaHome_5G	\N	153	4x4	4x4	11ax	11ax	-75	843	118	2026-10-11 09:57:52	2e:69:31:2f:2b:57	\N	40 MHz	160 MHz
9b:cd:ab:10:50:c7	leechinhua381@unifi	Pixel-7	Google LLC	Google	STA	Client	2.4 GHz	192.168.0.123	ArandaHome_2.4G	ArandaHome_5G	1	\N	3x3	2x2	11n	11n	-46	1160	705	2026-10-09 22:26:52	2e:69:31:2f:2b:57	Linux	40 MHz	160 MHz
dc:62:09:03:b6:d8	leechinhua381@unifi	Galaxy-M14	Samsung Electronics Co., Ltd.	Samsung	STA	Client	2.4 GHz	192.168.0.176	ArandaHome_2.4G	ArandaHome_5G	6	\N	1x1	4x4	11n	11n	-69	944	383	2026-10-10 08:34:52	2e:69:31:2f:2b:57	Android	40 MHz	160 MHz
07:b3:56:86:ec:1c	leechinhua381@unifi	Intel-WiFi	Intel Corporate	Intel	STA	Repeater	5 GHz	192.168.0.155	ArandaHome_2.4G	ArandaHome_5G	\N	40	1x1	4x4	11n	11n	-43	817	9	2026-10-07 15:10:52	2e:69:31:2f:2b:57	\N	20 MHz	80 MHz
99:a3:b2:5d:86:1c	gohsoonhua109@unifi	Root	ZTE Corporation	ZTE	Root	Access Point	Ethernet	192.168.0.1	HarmoniVilla_2.4G	HarmoniVilla_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	ZTE	40 MHz	160 MHz
36:7f:44:6d:a3:1a	gohsoonhua109@unifi	WNC-AP	WNC Corporation	Wnc	STA	Gateway	5 GHz	192.168.0.43	HarmoniVilla_2.4G	HarmoniVilla_5G	\N	153	1x1	2x2	11ax	11ax	-56	524	547	2026-10-09 16:17:52	99:a3:b2:5d:86:1c	Windows	20 MHz	160 MHz
ed:88:25:1b:a5:e3	gohsoonhua109@unifi	Fire-TV-Stick	Amazon Technologies Inc.	Amazon	STA	Repeater	2.4 GHz	192.168.0.230	HarmoniVilla_2.4G	HarmoniVilla_5G	1	\N	4x4	3x3	11ac	11ac	-74	1127	924	2026-10-09 23:32:52	99:a3:b2:5d:86:1c	Android	20 MHz	80 MHz
49:79:a9:88:8f:60	gohsoonhua109@unifi	49:79:a9:88:8f:60	WNC Corporation	Wnc	STA	Gateway	2.4 GHz	192.168.0.127	HarmoniVilla_2.4G	HarmoniVilla_5G	11	\N	4x4	1x1	11ax	11ax	-48	790	899	2026-10-09 04:13:52	99:a3:b2:5d:86:1c	\N	20 MHz	80 MHz
0b:11:4d:e7:a1:dd	gohsoonhua109@unifi	eero-Pro-6E	Amazon Technologies Inc.	Amazon	STA	Access Point	5 GHz	192.168.0.152	HarmoniVilla_2.4G	HarmoniVilla_5G	\N	153	2x2	2x2	11ax	11ax	-43	471	478	2026-10-12 08:08:52	99:a3:b2:5d:86:1c	\N	40 MHz	160 MHz
92:9f:2e:94:2f:8c	gohsoonhua109@unifi	Orbi-RBR750	Netgear Inc.	Netgear	STA	Access Point	2.4 GHz	192.168.0.173	HarmoniVilla_2.4G	HarmoniVilla_5G	11	\N	2x2	2x2	11ax	11ax	-53	744	1157	2026-10-11 07:36:52	99:a3:b2:5d:86:1c	\N	40 MHz	160 MHz
25:28:53:7d:fc:f0	divyarajen16@unifi	Root	ZTE Corporation	ZTE	Root	Access Point	Ethernet	192.168.0.1	SeriMawar_2.4G	SeriMawar_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	ZTE	40 MHz	160 MHz
52:0f:07:e1:0d:0f	divyarajen16@unifi	OnePlus-11	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Repeater	5 GHz	192.168.0.74	SeriMawar_2.4G	SeriMawar_5G	\N	161	1x1	4x4	11ax	11ax	-31	443	177	2026-10-09 14:17:52	25:28:53:7d:fc:f0	Android	40 MHz	160 MHz
09:25:5d:8b:1b:ea	divyarajen16@unifi	WNC-Client	WNC Corporation	Wnc	STA	Client	2.4 GHz	192.168.0.62	SeriMawar_2.4G	SeriMawar_5G	6	\N	4x4	1x1	11ac	11ac	-43	860	742	2026-10-10 04:31:52	25:28:53:7d:fc:f0	Linux	20 MHz	160 MHz
b5:1e:81:0a:27:1b	divyarajen16@unifi	Nest-Wifi-Router	Google LLC	Google	STA	Access Point	5 GHz	192.168.0.86	SeriMawar_2.4G	SeriMawar_5G	\N	40	2x2	2x2	11ax	11ax	-70	490	1167	2026-10-12 05:28:52	25:28:53:7d:fc:f0	\N	40 MHz	160 MHz
b6:97:64:19:ab:2a	divyarajen16@unifi	decoMeshBE65	TP-Link Systems Inc.	Tp Link	STA	Access Point	Ethernet	192.168.0.95	SeriMawar_2.4G	SeriMawar_5G	\N	\N	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-10 22:24:52	25:28:53:7d:fc:f0	\N	\N	\N
e4:bd:db:1c:76:6a	divyarajen16@unifi	eero-6	Amazon Technologies Inc.	Amazon	STA	Access Point	Ethernet	192.168.0.209	SeriMawar_2.4G	SeriMawar_5G	\N	\N	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-10 20:30:52	25:28:53:7d:fc:f0	\N	\N	\N
f7:70:d4:dd:6f:57	vigneshsub201@unifi	Root	ZTE Corporation	ZTE	Root	Access Point	Ethernet	192.168.0.1	VillaSri_2.4G	VillaSri_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	ZTE	40 MHz	160 MHz
7b:70:87:31:91:fe	vigneshsub201@unifi	ESP32-Node	Espressif Inc.	Espressif	STA	Repeater	2.4 GHz	192.168.0.70	VillaSri_2.4G	VillaSri_5G	11	\N	2x2	4x4	11ax	11ax	-83	142	684	2026-10-12 06:37:52	f7:70:d4:dd:6f:57	\N	20 MHz	80 MHz
23:e9:4f:f2:d6:87	vigneshsub201@unifi	OPPO-A57	BBK Electronics Corp., Ltd.	Oppo	STA	Gateway	5 GHz	192.168.0.58	VillaSri_2.4G	VillaSri_5G	\N	48	1x1	4x4	11n	11n	-90	1024	1057	2026-10-09 14:12:52	f7:70:d4:dd:6f:57	Windows	40 MHz	80 MHz
e5:01:33:6e:d7:d4	vigneshsub201@unifi	Echo-Dot	Amazon Technologies Inc.	Amazon	STA	Gateway	5 GHz	192.168.0.78	VillaSri_2.4G	VillaSri_5G	\N	40	1x1	4x4	11ax	11ax	-67	1044	636	2026-10-09 22:24:52	f7:70:d4:dd:6f:57	Windows	20 MHz	160 MHz
72:53:f4:b0:17:46	vigneshsub201@unifi	Mi-11X	Xiaomi Communications Co., Ltd.	Xiaomi	STA	Gateway	5 GHz	192.168.0.93	VillaSri_2.4G	VillaSri_5G	\N	149	1x1	4x4	11ax	11ax	-56	685	481	2026-10-07 18:19:52	f7:70:d4:dd:6f:57	\N	20 MHz	160 MHz
42:28:b1:5d:52:eb	vigneshsub201@unifi	42:28:b1:5d:52:eb	Intel Corporate	Intel	STA	Gateway	2.4 GHz	192.168.0.129	VillaSri_2.4G	VillaSri_5G	6	\N	2x2	2x2	11ac	11ac	-42	69	645	2026-10-10 05:30:52	f7:70:d4:dd:6f:57	\N	40 MHz	160 MHz
62:f6:18:11:c5:bb	divyarajen359@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	DamaiResidensi_2.4G	DamaiResidensi_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
69:27:6d:ce:bc:50	divyarajen359@unifi	OnePlus-11	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Repeater	2.4 GHz	192.168.0.79	DamaiResidensi_2.4G	DamaiResidensi_5G	6	\N	3x3	1x1	11ac	11ac	-63	606	990	2026-10-07 14:25:52	62:f6:18:11:c5:bb	\N	20 MHz	160 MHz
7c:25:2a:39:37:ca	divyarajen359@unifi	V2148	vivo Mobile Communication Co., Ltd.	Vivo	STA	Gateway	2.4 GHz	192.168.0.29	DamaiResidensi_2.4G	DamaiResidensi_5G	11	\N	1x1	2x2	11ac	11ac	-86	977	540	2026-10-07 15:57:52	62:f6:18:11:c5:bb	iOS	20 MHz	80 MHz
df:c9:fc:5f:44:dd	divyarajen359@unifi	Nest-Wifi-Router	Google LLC	Google	STA	Access Point	Ethernet	192.168.0.165	DamaiResidensi_2.4G	DamaiResidensi_5G	\N	\N	2x2	4x4	11ax	11ax	\N	\N	\N	2026-10-10 19:01:52	62:f6:18:11:c5:bb	\N	\N	\N
2b:d7:de:a9:27:03	divyarajen359@unifi	Nest-Wifi-Pro	Google LLC	Google	STA	Access Point	2.4 GHz	192.168.0.225	DamaiResidensi_2.4G	DamaiResidensi_5G	11	\N	2x2	2x2	11ax	11ax	-61	807	1190	2026-10-12 07:45:52	62:f6:18:11:c5:bb	\N	40 MHz	160 MHz
e6:01:59:64:23:c1	divyarajen359@unifi	Sonoff-POW	ITEAD Intelligent Systems Co., Ltd.	Sonoff	STA	IoT	2.4 GHz	192.168.0.6	DamaiResidensi_2.4G	\N	11	\N	1x1	1x1	11n	\N	-77	51	114	2026-10-05 18:44:52	62:f6:18:11:c5:bb	\N	20 MHz	\N
90:a6:00:5b:dc:12	divyarajen359@unifi	ESP32-CAM	Espressif Inc.	Espressif	STA	IoT	2.4 GHz	192.168.0.45	DamaiResidensi_2.4G	\N	6	\N	1x1	1x1	11n	\N	-65	65	43	2026-10-05 12:20:52	62:f6:18:11:c5:bb	\N	20 MHz	\N
62:ee:21:12:ef:d5	divyarajen359@unifi	Sonoff-Basic	ITEAD Intelligent Systems Co., Ltd.	Sonoff	STA	IoT	2.4 GHz	192.168.0.177	DamaiResidensi_2.4G	\N	6	\N	1x1	1x1	11n	\N	-59	30	65	2026-10-05 19:13:52	62:f6:18:11:c5:bb	\N	20 MHz	\N
95:3a:a9:37:91:5c	divyarajen359@unifi	Sonoff-TH16	ITEAD Intelligent Systems Co., Ltd.	Sonoff	STA	IoT	2.4 GHz	192.168.0.50	DamaiResidensi_2.4G	\N	1	\N	1x1	1x1	11n	\N	-65	61	132	2026-10-07 15:23:52	62:f6:18:11:c5:bb	\N	20 MHz	\N
64:5c:bb:57:c7:db	wongmeilin430@unifi	Root	Fiberhome Telecommunication Technologies Co., Ltd.	FiberHome	Root	Access Point	Ethernet	192.168.0.1	BayuHome_2.4G	BayuHome_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	FIBERHOME	40 MHz	160 MHz
79:1b:5b:9b:a7:42	wongmeilin430@unifi	Pixel-7	Google LLC	Google	STA	Repeater	5 GHz	192.168.0.111	BayuHome_2.4G	BayuHome_5G	\N	153	4x4	1x1	11n	11n	-50	401	252	2026-10-10 00:03:52	64:5c:bb:57:c7:db	\N	20 MHz	80 MHz
ad:d8:3d:f4:e9:5d	wongmeilin430@unifi	OPPO-F19	BBK Electronics Corp., Ltd.	Oppo	STA	Client	5 GHz	192.168.0.67	BayuHome_2.4G	BayuHome_5G	\N	36	2x2	4x4	11n	11n	-52	788	165	2026-10-09 02:29:52	64:5c:bb:57:c7:db	SKYWORTH	20 MHz	160 MHz
d5:dd:6c:84:91:c8	wongmeilin430@unifi	Galaxy-M14	Samsung Electronics Co., Ltd.	Samsung	STA	Repeater	2.4 GHz	192.168.0.148	BayuHome_2.4G	BayuHome_5G	11	\N	3x3	1x1	11ax	11ax	-65	69	340	2026-10-09 22:11:52	64:5c:bb:57:c7:db	Linux	40 MHz	160 MHz
79:a0:a0:8c:28:0b	wongmeilin430@unifi	Nest-Wifi-Pro	Google LLC	Google	STA	Access Point	Ethernet	192.168.0.162	BayuHome_2.4G	BayuHome_5G	\N	\N	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-10 19:11:52	64:5c:bb:57:c7:db	\N	\N	\N
52:9a:33:9c:4a:54	wongmeilin430@unifi	Hue-Strip	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.40	BayuHome_2.4G	\N	11	\N	1x1	1x1	11n	\N	-40	17	55	2026-10-08 23:04:52	64:5c:bb:57:c7:db	\N	20 MHz	\N
b9:31:d0:8a:1f:b1	chongkahfa258@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	ChandranVilla_2.4G	ChandranVilla_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
21:b5:b3:c7:73:f5	chongkahfa258@unifi	Fire-TV-Stick	Amazon Technologies Inc.	Amazon	STA	Client	2.4 GHz	192.168.0.116	ChandranVilla_2.4G	ChandranVilla_5G	11	\N	4x4	2x2	11n	11n	-47	1193	609	2026-10-10 08:00:52	b9:31:d0:8a:1f:b1	\N	40 MHz	80 MHz
17:5e:bf:d4:ff:5d	chongkahfa258@unifi	Redmi-13C-5G	Xiaomi Communications Co., Ltd.	Xiaomi	STA	Gateway	2.4 GHz	192.168.0.166	ChandranVilla_2.4G	ChandranVilla_5G	6	\N	1x1	3x3	11n	11n	-89	1088	120	2026-10-09 23:49:52	b9:31:d0:8a:1f:b1	SKYWORTH	40 MHz	160 MHz
d4:32:0b:17:89:85	chongkahfa258@unifi	TP-Link-Repeater	TP-Link Technologies Co., Ltd.	TP-Link	STA	Client	2.4 GHz	192.168.0.111	ChandranVilla_2.4G	ChandranVilla_5G	6	\N	4x4	4x4	11ac	11ac	-60	1099	971	2026-10-11 04:23:52	b9:31:d0:8a:1f:b1	\N	40 MHz	80 MHz
41:ad:dd:87:28:17	chongkahfa258@unifi	OnePlus-Nord	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Repeater	2.4 GHz	192.168.0.166	ChandranVilla_2.4G	ChandranVilla_5G	1	\N	4x4	2x2	11n	11n	-85	748	749	2026-10-09 12:57:52	b9:31:d0:8a:1f:b1	iOS	20 MHz	80 MHz
05:20:a0:a0:83:7d	chongkahfa258@unifi	SKYWORTH-STB	Shenzhen Skyworth Digital Technology CO.	Skyworth	STA	Repeater	2.4 GHz	192.168.0.199	ChandranVilla_2.4G	ChandranVilla_5G	1	\N	1x1	2x2	11ax	11ax	-40	500	1045	2026-10-09 06:43:52	b9:31:d0:8a:1f:b1	Windows	20 MHz	80 MHz
bb:10:1d:2d:41:5b	chongkahfa258@unifi	decoMeshX60	TP-Link Systems Inc.	Tp Link	STA	Access Point	Ethernet	192.168.0.86	ChandranVilla_2.4G	ChandranVilla_5G	\N	\N	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-11 17:55:52	b9:31:d0:8a:1f:b1	\N	\N	\N
ae:8f:bc:a5:ff:a0	chongkahfa258@unifi	decoMeshX60	TP-Link Systems Inc.	Tp Link	STA	Access Point	2.4 GHz	192.168.0.34	ChandranVilla_2.4G	ChandranVilla_5G	11	\N	2x2	4x4	11ax	11ax	-43	808	342	2026-10-12 04:42:52	b9:31:d0:8a:1f:b1	\N	40 MHz	160 MHz
06:ae:dc:dc:94:38	chongkahfa258@unifi	Hue-Strip	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.143	ChandranVilla_2.4G	\N	11	\N	1x1	1x1	11n	\N	-46	90	14	2026-10-11 13:35:52	b9:31:d0:8a:1f:b1	\N	20 MHz	\N
db:f9:51:e1:c4:81	chongkahfa258@unifi	Sonoff-TH16	ITEAD Intelligent Systems Co., Ltd.	Sonoff	STA	IoT	2.4 GHz	192.168.0.93	ChandranVilla_2.4G	\N	6	\N	1x1	1x1	11n	\N	-42	127	37	2026-10-06 23:51:52	b9:31:d0:8a:1f:b1	\N	20 MHz	\N
ed:6d:61:d9:8d:ac	chongkahfa258@unifi	Hue-Bridge	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.205	ChandranVilla_2.4G	\N	6	\N	1x1	1x1	11n	\N	-76	91	15	2026-10-11 21:50:52	b9:31:d0:8a:1f:b1	\N	20 MHz	\N
90:c4:5e:3a:83:e2	nuraisyahh315@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	ArandaHome_2.4G	ArandaHome_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
63:3c:13:ed:85:3c	nuraisyahh315@unifi	Chromecast	Google LLC	Google	STA	Client	5 GHz	192.168.0.178	ArandaHome_2.4G	ArandaHome_5G	\N	44	2x2	1x1	11ax	11ax	-71	979	857	2026-10-08 02:51:52	90:c4:5e:3a:83:e2	\N	20 MHz	160 MHz
89:a6:15:a0:57:02	nuraisyahh315@unifi	Chromecast	Google LLC	Google	STA	Gateway	2.4 GHz	192.168.0.120	ArandaHome_2.4G	ArandaHome_5G	6	\N	1x1	1x1	11ax	11ax	-84	954	161	2026-10-08 12:23:52	90:c4:5e:3a:83:e2	Linux	40 MHz	80 MHz
89:bf:0f:00:41:c8	nuraisyahh315@unifi	Galaxy-S23	Samsung Electronics Co., Ltd.	Samsung	STA	Client	5 GHz	192.168.0.114	ArandaHome_2.4G	ArandaHome_5G	\N	48	2x2	2x2	11ac	11ac	-79	433	351	2026-10-09 03:14:52	90:c4:5e:3a:83:e2	Android	40 MHz	160 MHz
e4:d8:bf:3a:f5:bf	nuraisyahh315@unifi	Galaxy-S23	Samsung Electronics Co., Ltd.	Samsung	STA	Client	5 GHz	192.168.0.164	ArandaHome_2.4G	ArandaHome_5G	\N	153	3x3	3x3	11ac	11ac	-89	566	32	2026-10-10 16:56:52	90:c4:5e:3a:83:e2	Windows	40 MHz	80 MHz
8b:d9:b6:63:53:d7	nuraisyahh315@unifi	V2332	vivo Mobile Communication Co., Ltd.	Vivo	STA	Gateway	5 GHz	192.168.0.49	ArandaHome_2.4G	ArandaHome_5G	\N	153	1x1	1x1	11n	11n	-42	838	900	2026-10-08 17:18:52	90:c4:5e:3a:83:e2	Linux	20 MHz	160 MHz
a7:6e:5f:87:0c:5e	gohsoonhua794@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	TamanAman_2.4G	TamanAman_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
58:82:b9:7b:a5:52	gohsoonhua794@unifi	realme-11-Pro	Realme Chongqing Mobile Telecommunications Corp.	Realme	STA	Client	5 GHz	192.168.0.177	TamanAman_2.4G	TamanAman_5G	\N	157	2x2	4x4	11ac	11ac	-79	672	77	2026-10-10 14:31:52	a7:6e:5f:87:0c:5e	iOS	40 MHz	160 MHz
ce:26:dc:d4:34:c3	gohsoonhua794@unifi	Nest-Hub	Google LLC	Google	STA	Gateway	5 GHz	192.168.0.92	TamanAman_2.4G	TamanAman_5G	\N	153	2x2	4x4	11n	11n	-53	478	375	2026-10-08 01:50:52	a7:6e:5f:87:0c:5e	\N	20 MHz	80 MHz
5b:0c:58:5f:f9:a0	gohsoonhua794@unifi	OnePlus-Nord	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Client	5 GHz	192.168.0.86	TamanAman_2.4G	TamanAman_5G	\N	36	1x1	2x2	11n	11n	-69	464	1063	2026-10-10 22:49:52	a7:6e:5f:87:0c:5e	Windows	20 MHz	160 MHz
f0:fb:b3:20:03:30	gohsoonhua794@unifi	WNC-AP	WNC Corporation	Wnc	STA	Client	2.4 GHz	192.168.0.59	TamanAman_2.4G	TamanAman_5G	11	\N	4x4	2x2	11ax	11ax	-39	460	980	2026-10-08 04:13:52	a7:6e:5f:87:0c:5e	Linux	20 MHz	160 MHz
96:d7:87:6e:1f:90	gohsoonhua794@unifi	AX201-Client	Intel Corporate	Intel	STA	Repeater	5 GHz	192.168.0.200	TamanAman_2.4G	TamanAman_5G	\N	44	3x3	4x4	11n	11n	-53	845	1076	2026-10-10 19:26:52	a7:6e:5f:87:0c:5e	\N	20 MHz	160 MHz
b4:3f:71:bc:28:78	gohsoonhua794@unifi	Nest-Wifi-Router	Google LLC	Google	STA	Access Point	2.4 GHz	192.168.0.129	TamanAman_2.4G	TamanAman_5G	1	\N	2x2	4x4	11ax	11ax	-42	338	429	2026-10-10 20:14:52	a7:6e:5f:87:0c:5e	\N	40 MHz	160 MHz
09:2c:c6:69:50:77	zainalabid756@unifi	Root	ZTE Corporation	ZTE	Root	Access Point	Ethernet	192.168.0.1	ArandaHome_2.4G	ArandaHome_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	ZTE	40 MHz	160 MHz
f7:63:9a:b2:3a:4d	zainalabid756@unifi	WNC-Client	WNC Corporation	Wnc	STA	Client	2.4 GHz	192.168.0.110	ArandaHome_2.4G	ArandaHome_5G	11	\N	1x1	2x2	11ac	11ac	-65	242	208	2026-10-12 08:06:52	09:2c:c6:69:50:77	SKYWORTH	40 MHz	160 MHz
9f:e9:81:e2:f6:c6	zainalabid756@unifi	V2332	vivo Mobile Communication Co., Ltd.	Vivo	STA	Gateway	2.4 GHz	192.168.0.51	ArandaHome_2.4G	ArandaHome_5G	11	\N	1x1	1x1	11ac	11ac	-44	435	305	2026-10-11 22:52:52	09:2c:c6:69:50:77	Linux	20 MHz	80 MHz
66:5b:4b:21:15:71	zainalabid756@unifi	Intel-WiFi	Intel Corporate	Intel	STA	Repeater	2.4 GHz	192.168.0.218	ArandaHome_2.4G	ArandaHome_5G	11	\N	2x2	2x2	11ac	11ac	-66	821	156	2026-10-11 07:00:52	09:2c:c6:69:50:77	SKYWORTH	20 MHz	80 MHz
46:e3:09:37:a6:57	zainalabid756@unifi	46:e3:09:37:a6:57	Shenzhen Skyworth Digital Technology CO.	Skyworth	STA	Client	5 GHz	192.168.0.87	ArandaHome_2.4G	ArandaHome_5G	\N	36	3x3	1x1	11ac	11ac	-88	157	622	2026-10-08 02:58:52	09:2c:c6:69:50:77	Linux	20 MHz	80 MHz
ab:21:80:02:f3:a1	zainalabid756@unifi	SKYWORTH-STB	Shenzhen Skyworth Digital Technology CO.	Skyworth	STA	Client	5 GHz	192.168.0.31	ArandaHome_2.4G	ArandaHome_5G	\N	44	4x4	3x3	11ax	11ax	-74	450	134	2026-10-09 23:13:52	09:2c:c6:69:50:77	iOS	20 MHz	160 MHz
b7:c2:31:80:59:96	teohbeecho755@unifi	Root	Fiberhome Telecommunication Technologies Co., Ltd.	FiberHome	Root	Access Point	Ethernet	192.168.0.1	VillaSri_2.4G	VillaSri_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	FIBERHOME	40 MHz	160 MHz
50:26:c7:66:ae:79	teohbeecho755@unifi	TP-Link-Repeater	TP-Link Technologies Co., Ltd.	TP-Link	STA	Repeater	2.4 GHz	192.168.0.235	VillaSri_2.4G	VillaSri_5G	11	\N	1x1	3x3	11ax	11ax	-68	283	524	2026-10-09 01:28:52	b7:c2:31:80:59:96	Windows	40 MHz	80 MHz
ac:01:28:86:65:b5	teohbeecho755@unifi	V2207	vivo Mobile Communication Co., Ltd.	Vivo	STA	Repeater	5 GHz	192.168.0.63	VillaSri_2.4G	VillaSri_5G	\N	153	1x1	3x3	11ax	11ax	-90	1151	1112	2026-10-08 12:12:52	b7:c2:31:80:59:96	Android	20 MHz	160 MHz
4e:8f:b0:76:91:04	teohbeecho755@unifi	realme-C55	Realme Chongqing Mobile Telecommunications Corp.	Realme	STA	Gateway	2.4 GHz	192.168.0.184	VillaSri_2.4G	VillaSri_5G	1	\N	4x4	2x2	11ac	11ac	-33	307	1136	2026-10-07 19:17:52	b7:c2:31:80:59:96	Windows	20 MHz	80 MHz
61:5a:87:02:45:2c	teohbeecho755@unifi	Redmi-13C-5G	Xiaomi Communications Co., Ltd.	Xiaomi	STA	Gateway	5 GHz	192.168.0.48	VillaSri_2.4G	VillaSri_5G	\N	36	2x2	3x3	11ac	11ac	-87	732	1036	2026-10-11 14:41:52	b7:c2:31:80:59:96	iOS	40 MHz	80 MHz
73:b7:a6:64:25:f1	teohbeecho755@unifi	Galaxy-M14	Samsung Electronics Co., Ltd.	Samsung	STA	Repeater	5 GHz	192.168.0.83	VillaSri_2.4G	VillaSri_5G	\N	48	4x4	3x3	11ac	11ac	-80	1194	1015	2026-10-09 17:23:52	b7:c2:31:80:59:96	iOS	40 MHz	80 MHz
24:8e:6c:4b:16:d5	teohbeecho755@unifi	V2148	vivo Mobile Communication Co., Ltd.	Vivo	STA	Gateway	5 GHz	192.168.0.83	VillaSri_2.4G	VillaSri_5G	\N	36	2x2	4x4	11n	11n	-86	410	776	2026-10-07 20:32:52	b7:c2:31:80:59:96	Windows	20 MHz	160 MHz
60:21:ea:65:45:55	teohbeecho755@unifi	eero-Max-7	Amazon Technologies Inc.	Amazon	STA	Access Point	Ethernet	192.168.0.186	VillaSri_2.4G	VillaSri_5G	\N	\N	2x2	4x4	11ax	11ax	\N	\N	\N	2026-10-10 13:10:52	b7:c2:31:80:59:96	\N	\N	\N
75:86:ab:76:22:8c	teohbeecho755@unifi	decoMeshX50	TP-Link Systems Inc.	Tp Link	STA	Access Point	Ethernet	192.168.0.115	VillaSri_2.4G	VillaSri_5G	\N	\N	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-11 17:35:52	b7:c2:31:80:59:96	\N	\N	\N
4d:c5:19:a4:08:c8	teohbeecho755@unifi	eero-Pro-6E	Amazon Technologies Inc.	Amazon	STA	Access Point	Ethernet	192.168.0.119	VillaSri_2.4G	VillaSri_5G	\N	\N	2x2	4x4	11ax	11ax	\N	\N	\N	2026-10-11 11:58:52	b7:c2:31:80:59:96	\N	\N	\N
65:eb:6f:37:b9:00	teohbeecho755@unifi	Sonoff-Basic	ITEAD Intelligent Systems Co., Ltd.	Sonoff	STA	IoT	2.4 GHz	192.168.0.74	VillaSri_2.4G	\N	6	\N	1x1	1x1	11n	\N	-77	87	40	2026-10-06 15:46:52	b7:c2:31:80:59:96	\N	20 MHz	\N
38:3f:28:f5:c3:7f	teohbeecho755@unifi	Sonoff-POW	ITEAD Intelligent Systems Co., Ltd.	Sonoff	STA	IoT	2.4 GHz	192.168.0.229	VillaSri_2.4G	\N	6	\N	1x1	1x1	11n	\N	-70	88	109	2026-10-08 12:54:52	b7:c2:31:80:59:96	\N	20 MHz	\N
2f:2e:69:fb:1b:c3	teohbeecho755@unifi	Sonoff-POW	ITEAD Intelligent Systems Co., Ltd.	Sonoff	STA	IoT	2.4 GHz	192.168.0.100	VillaSri_2.4G	\N	6	\N	1x1	1x1	11n	\N	-64	57	137	2026-10-08 23:48:52	b7:c2:31:80:59:96	\N	20 MHz	\N
89:b2:71:7a:d7:ff	teohbeecho755@unifi	Hue-Bulb	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.245	VillaSri_2.4G	\N	11	\N	1x1	1x1	11n	\N	-70	88	136	2026-10-05 17:51:52	b7:c2:31:80:59:96	\N	20 MHz	\N
77:3f:93:3e:ba:95	kennethloh149@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	DamaiResidensi_2.4G	DamaiResidensi_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
ba:be:2c:7f:e0:87	kennethloh149@unifi	ba:be:2c:7f:e0:87	Google LLC	Google	STA	Gateway	2.4 GHz	192.168.0.221	DamaiResidensi_2.4G	DamaiResidensi_5G	6	\N	4x4	4x4	11ac	11ac	-84	737	900	2026-10-11 06:29:52	77:3f:93:3e:ba:95	Windows	20 MHz	80 MHz
c6:ce:e8:7b:0c:e0	kennethloh149@unifi	OPPO-A57	BBK Electronics Corp., Ltd.	Oppo	STA	Client	5 GHz	192.168.0.47	DamaiResidensi_2.4G	DamaiResidensi_5G	\N	44	1x1	3x3	11ax	11ax	-77	199	81	2026-10-10 11:59:52	77:3f:93:3e:ba:95	\N	20 MHz	80 MHz
b8:e8:d3:ea:c5:01	kennethloh149@unifi	realme-C55	Realme Chongqing Mobile Telecommunications Corp.	Realme	STA	Repeater	5 GHz	192.168.0.89	DamaiResidensi_2.4G	DamaiResidensi_5G	\N	48	4x4	2x2	11ac	11ac	-88	94	141	2026-10-10 10:01:52	77:3f:93:3e:ba:95	\N	20 MHz	80 MHz
05:97:a4:fb:86:8b	kennethloh149@unifi	Echo-Dot	Amazon Technologies Inc.	Amazon	STA	Gateway	2.4 GHz	192.168.0.49	DamaiResidensi_2.4G	DamaiResidensi_5G	1	\N	2x2	1x1	11ax	11ax	-81	848	271	2026-10-07 14:34:52	77:3f:93:3e:ba:95	\N	40 MHz	80 MHz
df:6e:c3:30:d6:03	kennethloh149@unifi	Orbi-RBR750	Netgear Inc.	Netgear	STA	Access Point	2.4 GHz	192.168.0.34	DamaiResidensi_2.4G	DamaiResidensi_5G	1	\N	2x2	2x2	11ax	11ax	-62	381	979	2026-10-11 09:30:52	77:3f:93:3e:ba:95	\N	40 MHz	160 MHz
a2:f7:44:cc:49:35	kennethloh149@unifi	decoMeshX50	TP-Link Systems Inc.	Tp Link	STA	Access Point	Ethernet	192.168.0.151	DamaiResidensi_2.4G	DamaiResidensi_5G	\N	\N	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-11 02:53:52	77:3f:93:3e:ba:95	\N	\N	\N
b3:f1:63:c1:e2:bc	kennethloh149@unifi	Sonoff-Basic	ITEAD Intelligent Systems Co., Ltd.	Sonoff	STA	IoT	2.4 GHz	192.168.0.44	DamaiResidensi_2.4G	\N	11	\N	1x1	1x1	11n	\N	-54	70	14	2026-10-10 06:06:52	77:3f:93:3e:ba:95	\N	20 MHz	\N
09:24:9e:08:1c:55	kennethloh149@unifi	Hue-Bridge	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.100	DamaiResidensi_2.4G	\N	6	\N	1x1	1x1	11n	\N	-59	143	123	2026-10-10 08:48:52	77:3f:93:3e:ba:95	\N	20 MHz	\N
27:9d:78:fe:8a:49	kennethloh149@unifi	ESP32-Switch	Espressif Inc.	Espressif	STA	IoT	2.4 GHz	192.168.0.58	DamaiResidensi_2.4G	\N	11	\N	1x1	1x1	11n	\N	-52	12	47	2026-10-07 22:02:52	77:3f:93:3e:ba:95	\N	20 MHz	\N
d5:08:69:3c:17:75	kennethloh149@unifi	Tuya-Bulb	Tuya Smart Inc.	Tuya	STA	IoT	2.4 GHz	192.168.0.56	DamaiResidensi_2.4G	\N	6	\N	1x1	1x1	11n	\N	-78	88	53	2026-10-11 11:37:52	77:3f:93:3e:ba:95	\N	20 MHz	\N
f1:06:f1:a2:5a:28	divyarajen791@unifi	Root	Fiberhome Telecommunication Technologies Co., Ltd.	FiberHome	Root	Access Point	Ethernet	192.168.0.1	TamanAman_2.4G	TamanAman_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	FIBERHOME	40 MHz	160 MHz
f5:63:1c:ae:43:d9	divyarajen791@unifi	f5:63:1c:ae:43:d9	Intel Corporate	Intel	STA	Repeater	5 GHz	192.168.0.242	TamanAman_2.4G	TamanAman_5G	\N	40	1x1	1x1	11ax	11ax	-69	330	867	2026-10-11 11:01:52	f1:06:f1:a2:5a:28	Linux	20 MHz	160 MHz
41:04:4a:a2:9f:2b	divyarajen791@unifi	iPhone-15	Apple, Inc.	Apple	STA	Gateway	5 GHz	192.168.0.253	TamanAman_2.4G	TamanAman_5G	\N	161	3x3	3x3	11ax	11ax	-45	645	588	2026-10-11 08:02:52	f1:06:f1:a2:5a:28	\N	20 MHz	160 MHz
10:8a:f3:a6:5f:36	divyarajen791@unifi	Intel-WiFi	Intel Corporate	Intel	STA	Repeater	2.4 GHz	192.168.0.238	TamanAman_2.4G	TamanAman_5G	6	\N	3x3	3x3	11ax	11ax	-37	639	172	2026-10-10 03:21:52	f1:06:f1:a2:5a:28	SKYWORTH	20 MHz	160 MHz
6f:2d:e4:7f:8f:be	divyarajen791@unifi	Fire-TV-Stick	Amazon Technologies Inc.	Amazon	STA	Gateway	5 GHz	192.168.0.166	TamanAman_2.4G	TamanAman_5G	\N	48	1x1	2x2	11n	11n	-37	954	956	2026-10-08 03:32:52	f1:06:f1:a2:5a:28	Linux	40 MHz	160 MHz
13:22:3e:34:6c:c2	divyarajen791@unifi	13:22:3e:34:6c:c2	Xiaomi Communications Co., Ltd.	Xiaomi	STA	Repeater	2.4 GHz	192.168.0.43	TamanAman_2.4G	TamanAman_5G	11	\N	2x2	1x1	11ax	11ax	-45	139	348	2026-10-07 22:22:52	f1:06:f1:a2:5a:28	Linux	20 MHz	80 MHz
c3:47:4b:b5:37:7b	divyarajen791@unifi	realme-11-Pro	Realme Chongqing Mobile Telecommunications Corp.	Realme	STA	Repeater	2.4 GHz	192.168.0.177	TamanAman_2.4G	TamanAman_5G	11	\N	3x3	2x2	11n	11n	-66	452	8	2026-10-08 06:51:52	f1:06:f1:a2:5a:28	SKYWORTH	40 MHz	160 MHz
7a:ba:ff:73:d2:ea	divyarajen791@unifi	decoMeshX50	TP-Link Systems Inc.	Tp Link	STA	Access Point	Ethernet	192.168.0.26	TamanAman_2.4G	TamanAman_5G	\N	\N	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-11 09:49:52	f1:06:f1:a2:5a:28	\N	\N	\N
7f:46:76:66:a8:78	yapkeansen529@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	VillaSri_2.4G	VillaSri_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
8b:b1:46:7d:e1:72	yapkeansen529@unifi	OnePlus-Nord	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Repeater	2.4 GHz	192.168.0.149	VillaSri_2.4G	VillaSri_5G	6	\N	3x3	1x1	11ac	11ac	-70	574	384	2026-10-10 19:14:52	7f:46:76:66:a8:78	Android	20 MHz	160 MHz
bb:1a:eb:48:88:56	yapkeansen529@unifi	OPPO-A78	BBK Electronics Corp., Ltd.	Oppo	STA	Gateway	5 GHz	192.168.0.114	VillaSri_2.4G	VillaSri_5G	\N	161	4x4	3x3	11ac	11ac	-83	1160	1112	2026-10-10 07:04:52	7f:46:76:66:a8:78	\N	20 MHz	80 MHz
b1:76:33:93:5f:36	yapkeansen529@unifi	Galaxy-S23	Samsung Electronics Co., Ltd.	Samsung	STA	Repeater	2.4 GHz	192.168.0.163	VillaSri_2.4G	VillaSri_5G	11	\N	4x4	1x1	11n	11n	-51	668	285	2026-10-09 17:48:52	7f:46:76:66:a8:78	Windows	40 MHz	160 MHz
85:31:ab:3d:13:cc	yapkeansen529@unifi	Fire-TV-Stick	Amazon Technologies Inc.	Amazon	STA	Gateway	5 GHz	192.168.0.150	VillaSri_2.4G	VillaSri_5G	\N	157	2x2	4x4	11ax	11ax	-65	1190	765	2026-10-12 02:17:52	7f:46:76:66:a8:78	\N	40 MHz	80 MHz
7b:ca:2a:18:97:e3	yapkeansen529@unifi	V2029	vivo Mobile Communication Co., Ltd.	Vivo	STA	Client	5 GHz	192.168.0.99	VillaSri_2.4G	VillaSri_5G	\N	48	2x2	4x4	11ax	11ax	-56	89	809	2026-10-10 12:37:52	7f:46:76:66:a8:78	\N	40 MHz	160 MHz
cc:a8:ec:d9:3e:47	yapkeansen529@unifi	SKYWORTH-STB	Shenzhen Skyworth Digital Technology CO.	Skyworth	STA	Gateway	5 GHz	192.168.0.230	VillaSri_2.4G	VillaSri_5G	\N	157	3x3	4x4	11ac	11ac	-57	758	698	2026-10-08 10:26:52	7f:46:76:66:a8:78	Windows	40 MHz	80 MHz
9f:dd:ef:30:53:b3	yapkeansen529@unifi	Tuya-Wall-Switch	Tuya Smart Inc.	Tuya	STA	IoT	2.4 GHz	192.168.0.118	VillaSri_2.4G	\N	1	\N	1x1	1x1	11n	\N	-54	61	109	2026-10-06 20:27:52	7f:46:76:66:a8:78	\N	20 MHz	\N
70:b2:1a:1b:f5:3b	yapkeansen529@unifi	Hue-Strip	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.55	VillaSri_2.4G	\N	6	\N	1x1	1x1	11n	\N	-71	149	54	2026-10-10 13:18:52	7f:46:76:66:a8:78	\N	20 MHz	\N
83:53:73:a2:c9:87	arunkrishn436@unifi	Root	Fiberhome Telecommunication Technologies Co., Ltd.	FiberHome	Root	Access Point	Ethernet	192.168.0.1	TamanAman_2.4G	TamanAman_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	FIBERHOME	40 MHz	160 MHz
ea:80:db:95:f0:90	arunkrishn436@unifi	Nest-Hub	Google LLC	Google	STA	Repeater	2.4 GHz	192.168.0.49	TamanAman_2.4G	TamanAman_5G	6	\N	1x1	2x2	11n	11n	-75	479	627	2026-10-07 16:20:52	83:53:73:a2:c9:87	\N	20 MHz	80 MHz
9c:b6:2f:dd:f4:8f	arunkrishn436@unifi	Redmi-Note-12	Xiaomi Communications Co., Ltd.	Xiaomi	STA	Repeater	2.4 GHz	192.168.0.51	TamanAman_2.4G	TamanAman_5G	11	\N	1x1	4x4	11ax	11ax	-47	639	993	2026-10-07 16:32:52	83:53:73:a2:c9:87	iOS	40 MHz	160 MHz
b8:e0:f6:71:3f:3d	arunkrishn436@unifi	WNC-Client	WNC Corporation	Wnc	STA	Repeater	5 GHz	192.168.0.42	TamanAman_2.4G	TamanAman_5G	\N	157	1x1	2x2	11ax	11ax	-63	621	19	2026-10-11 14:04:52	83:53:73:a2:c9:87	\N	40 MHz	80 MHz
07:5b:b6:03:1d:ff	arunkrishn436@unifi	07:5b:b6:03:1d:ff	TP-Link Technologies Co., Ltd.	TP-Link	STA	Client	2.4 GHz	192.168.0.30	TamanAman_2.4G	TamanAman_5G	1	\N	1x1	1x1	11n	11n	-75	831	1007	2026-10-10 11:37:52	83:53:73:a2:c9:87	Windows	40 MHz	160 MHz
36:4a:33:1a:f3:85	arunkrishn436@unifi	Galaxy-S23	Samsung Electronics Co., Ltd.	Samsung	STA	Gateway	2.4 GHz	192.168.0.96	TamanAman_2.4G	TamanAman_5G	1	\N	2x2	1x1	11ax	11ax	-46	140	150	2026-10-12 00:47:52	83:53:73:a2:c9:87	Android	40 MHz	160 MHz
e5:64:7c:3b:71:0c	arunkrishn436@unifi	e5:64:7c:3b:71:0c	TP-Link Technologies Co., Ltd.	TP-Link	STA	Client	2.4 GHz	192.168.0.198	TamanAman_2.4G	TamanAman_5G	6	\N	3x3	3x3	11ax	11ax	-35	1017	677	2026-10-10 22:39:52	83:53:73:a2:c9:87	Linux	20 MHz	160 MHz
e0:93:31:e9:bd:7e	arunkrishn436@unifi	Orbi-RBS350	Netgear Inc.	Netgear	STA	Access Point	Ethernet	192.168.0.24	TamanAman_2.4G	TamanAman_5G	\N	\N	2x2	4x4	11ax	11ax	\N	\N	\N	2026-10-11 22:28:52	83:53:73:a2:c9:87	\N	\N	\N
35:10:9b:87:01:78	arunkrishn436@unifi	Nest-Wifi-Router	Google LLC	Google	STA	Access Point	5 GHz	192.168.0.152	TamanAman_2.4G	TamanAman_5G	\N	48	2x2	4x4	11ax	11ax	-47	992	819	2026-10-10 16:11:52	83:53:73:a2:c9:87	\N	40 MHz	160 MHz
a3:e8:5a:44:55:8e	arunkrishn436@unifi	eero-Pro-6E	Amazon Technologies Inc.	Amazon	STA	Access Point	Ethernet	192.168.0.10	TamanAman_2.4G	TamanAman_5G	\N	\N	2x2	4x4	11ax	11ax	\N	\N	\N	2026-10-12 03:06:52	83:53:73:a2:c9:87	\N	\N	\N
36:99:24:e2:46:a2	arunkrishn436@unifi	Hue-Bulb	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.151	TamanAman_2.4G	\N	1	\N	1x1	1x1	11n	\N	-80	110	41	2026-10-06 01:08:52	83:53:73:a2:c9:87	\N	20 MHz	\N
f0:30:cb:73:d3:ec	azlinamohd728@unifi	Root	Fiberhome Telecommunication Technologies Co., Ltd.	FiberHome	Root	Access Point	Ethernet	192.168.0.1	ArandaHome_2.4G	ArandaHome_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	FIBERHOME	40 MHz	160 MHz
80:48:fc:a6:9f:fb	azlinamohd728@unifi	Galaxy-A54	Samsung Electronics Co., Ltd.	Samsung	STA	Gateway	5 GHz	192.168.0.166	ArandaHome_2.4G	ArandaHome_5G	\N	161	3x3	1x1	11n	11n	-51	735	1160	2026-10-11 15:01:52	f0:30:cb:73:d3:ec	Windows	20 MHz	80 MHz
dc:3d:73:ae:39:8e	azlinamohd728@unifi	ESP8266-Sensor	Espressif Inc.	Espressif	STA	Client	2.4 GHz	192.168.0.22	ArandaHome_2.4G	ArandaHome_5G	6	\N	3x3	3x3	11n	11n	-42	937	122	2026-10-11 09:58:52	f0:30:cb:73:d3:ec	Android	40 MHz	160 MHz
08:7f:da:ed:be:83	azlinamohd728@unifi	08:7f:da:ed:be:83	Amazon Technologies Inc.	Amazon	STA	Client	5 GHz	192.168.0.19	ArandaHome_2.4G	ArandaHome_5G	\N	44	1x1	4x4	11n	11n	-39	161	565	2026-10-08 02:05:52	f0:30:cb:73:d3:ec	\N	40 MHz	160 MHz
7e:ec:9a:6e:43:66	azlinamohd728@unifi	eero-6	Amazon Technologies Inc.	Amazon	STA	Access Point	Ethernet	192.168.0.63	ArandaHome_2.4G	ArandaHome_5G	\N	\N	2x2	4x4	11ax	11ax	\N	\N	\N	2026-10-11 14:55:52	f0:30:cb:73:d3:ec	\N	\N	\N
5d:0d:b5:32:60:c3	azlinamohd728@unifi	Orbi-RBS350	Netgear Inc.	Netgear	STA	Access Point	Ethernet	192.168.0.2	ArandaHome_2.4G	ArandaHome_5G	\N	\N	2x2	4x4	11ax	11ax	\N	\N	\N	2026-10-11 23:38:52	f0:30:cb:73:d3:ec	\N	\N	\N
e3:3e:0a:14:1b:19	azlinamohd728@unifi	Nest-Wifi-Router	Google LLC	Google	STA	Access Point	2.4 GHz	192.168.0.107	ArandaHome_2.4G	ArandaHome_5G	1	\N	2x2	2x2	11ax	11ax	-59	1106	475	2026-10-11 08:03:52	f0:30:cb:73:d3:ec	\N	40 MHz	160 MHz
b8:1f:c4:78:c1:25	azlinamohd728@unifi	Shelly-Plus-1PM	Allterco Robotics EOOD	Shelly	STA	IoT	2.4 GHz	192.168.0.177	ArandaHome_2.4G	\N	6	\N	1x1	1x1	11n	\N	-55	45	49	2026-10-07 16:11:52	f0:30:cb:73:d3:ec	\N	20 MHz	\N
17:89:66:50:45:e7	azlinamohd728@unifi	Tuya-Wall-Switch	Tuya Smart Inc.	Tuya	STA	IoT	2.4 GHz	192.168.0.35	ArandaHome_2.4G	\N	11	\N	1x1	1x1	11n	\N	-69	66	114	2026-10-11 14:51:52	f0:30:cb:73:d3:ec	\N	20 MHz	\N
43:23:8a:35:0c:c3	azlinamohd728@unifi	Tuya-Wall-Switch	Tuya Smart Inc.	Tuya	STA	IoT	2.4 GHz	192.168.0.18	ArandaHome_2.4G	\N	6	\N	1x1	1x1	11n	\N	-49	39	12	2026-10-09 00:53:52	f0:30:cb:73:d3:ec	\N	20 MHz	\N
fc:8d:c0:83:11:af	azlinamohd728@unifi	Shelly-Plus-1PM	Allterco Robotics EOOD	Shelly	STA	IoT	2.4 GHz	192.168.0.120	ArandaHome_2.4G	\N	11	\N	1x1	1x1	11n	\N	-49	49	113	2026-10-07 07:02:52	f0:30:cb:73:d3:ec	\N	20 MHz	\N
b4:cb:68:9a:a8:b7	rajeshmuru987@unifi	Root	Fiberhome Telecommunication Technologies Co., Ltd.	FiberHome	Root	Access Point	Ethernet	192.168.0.1	DamaiResidensi_2.4G	DamaiResidensi_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	FIBERHOME	40 MHz	160 MHz
7a:fd:e6:5f:36:64	rajeshmuru987@unifi	7a:fd:e6:5f:36:64	Amazon Technologies Inc.	Amazon	STA	Repeater	2.4 GHz	192.168.0.18	DamaiResidensi_2.4G	DamaiResidensi_5G	11	\N	2x2	4x4	11n	11n	-59	218	991	2026-10-11 19:55:52	b4:cb:68:9a:a8:b7	\N	40 MHz	80 MHz
40:19:01:9d:81:42	rajeshmuru987@unifi	Galaxy-S23	Samsung Electronics Co., Ltd.	Samsung	STA	Gateway	5 GHz	192.168.0.91	DamaiResidensi_2.4G	DamaiResidensi_5G	\N	44	2x2	1x1	11ax	11ax	-90	922	977	2026-10-08 05:32:52	b4:cb:68:9a:a8:b7	\N	40 MHz	160 MHz
5c:fe:9c:5c:58:ad	rajeshmuru987@unifi	Echo-Dot	Amazon Technologies Inc.	Amazon	STA	Gateway	2.4 GHz	192.168.0.251	DamaiResidensi_2.4G	DamaiResidensi_5G	1	\N	1x1	2x2	11ac	11ac	-42	1077	557	2026-10-10 05:44:52	b4:cb:68:9a:a8:b7	iOS	40 MHz	160 MHz
2c:fd:15:d2:7d:49	rajeshmuru987@unifi	MacBook-Pro	Apple, Inc.	Apple	STA	Gateway	2.4 GHz	192.168.0.47	DamaiResidensi_2.4G	DamaiResidensi_5G	1	\N	3x3	3x3	11ac	11ac	-58	420	1001	2026-10-10 21:26:52	b4:cb:68:9a:a8:b7	\N	20 MHz	160 MHz
09:1d:ba:21:c2:5d	rajeshmuru987@unifi	09:1d:ba:21:c2:5d	Amazon Technologies Inc.	Amazon	STA	Gateway	5 GHz	192.168.0.186	DamaiResidensi_2.4G	DamaiResidensi_5G	\N	157	2x2	4x4	11ax	11ax	-33	999	491	2026-10-10 16:14:52	b4:cb:68:9a:a8:b7	iOS	20 MHz	80 MHz
2a:89:e0:6a:b5:00	rajeshmuru987@unifi	eero-Max-7	Amazon Technologies Inc.	Amazon	STA	Access Point	Ethernet	192.168.0.46	DamaiResidensi_2.4G	DamaiResidensi_5G	\N	\N	2x2	4x4	11ax	11ax	\N	\N	\N	2026-10-11 21:52:52	b4:cb:68:9a:a8:b7	\N	\N	\N
86:98:e5:57:cb:57	rajeshmuru987@unifi	eero-Max-7	Amazon Technologies Inc.	Amazon	STA	Access Point	Ethernet	192.168.0.94	DamaiResidensi_2.4G	DamaiResidensi_5G	\N	\N	2x2	4x4	11ax	11ax	\N	\N	\N	2026-10-12 00:17:52	b4:cb:68:9a:a8:b7	\N	\N	\N
a3:36:ce:fe:7b:9b	rajeshmuru987@unifi	Sonoff-Basic	ITEAD Intelligent Systems Co., Ltd.	Sonoff	STA	IoT	2.4 GHz	192.168.0.42	DamaiResidensi_2.4G	\N	6	\N	1x1	1x1	11n	\N	-59	123	36	2026-10-10 06:11:52	b4:cb:68:9a:a8:b7	\N	20 MHz	\N
4f:37:59:28:39:37	rajeshmuru987@unifi	Sonoff-Basic	ITEAD Intelligent Systems Co., Ltd.	Sonoff	STA	IoT	2.4 GHz	192.168.0.97	DamaiResidensi_2.4G	\N	11	\N	1x1	1x1	11n	\N	-59	29	112	2026-10-10 15:56:52	b4:cb:68:9a:a8:b7	\N	20 MHz	\N
24:bb:c4:bb:96:04	rajeshmuru987@unifi	Tuya-SmartPlug	Tuya Smart Inc.	Tuya	STA	IoT	2.4 GHz	192.168.0.140	DamaiResidensi_2.4G	\N	11	\N	1x1	1x1	11n	\N	-75	114	144	2026-10-09 23:15:52	b4:cb:68:9a:a8:b7	\N	20 MHz	\N
37:15:e6:93:c5:17	kennethloh57@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	ChandranVilla_2.4G	ChandranVilla_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
22:63:4c:6d:c2:dc	kennethloh57@unifi	realme-11-Pro	Realme Chongqing Mobile Telecommunications Corp.	Realme	STA	Repeater	2.4 GHz	192.168.0.247	ChandranVilla_2.4G	ChandranVilla_5G	1	\N	4x4	2x2	11ax	11ax	-30	1040	137	2026-10-10 18:07:52	37:15:e6:93:c5:17	\N	20 MHz	160 MHz
fd:a3:3c:22:83:9c	kennethloh57@unifi	Nest-Hub	Google LLC	Google	STA	Gateway	2.4 GHz	192.168.0.147	ChandranVilla_2.4G	ChandranVilla_5G	6	\N	4x4	3x3	11ac	11ac	-34	665	65	2026-10-10 12:38:52	37:15:e6:93:c5:17	Windows	20 MHz	160 MHz
b3:da:1d:86:a5:00	kennethloh57@unifi	realme-C55	Realme Chongqing Mobile Telecommunications Corp.	Realme	STA	Client	2.4 GHz	192.168.0.119	ChandranVilla_2.4G	ChandranVilla_5G	11	\N	3x3	2x2	11n	11n	-74	398	991	2026-10-08 04:14:52	37:15:e6:93:c5:17	Windows	40 MHz	160 MHz
8e:98:ec:77:57:88	kennethloh57@unifi	SKYWORTH-STB	Shenzhen Skyworth Digital Technology CO.	Skyworth	STA	Gateway	2.4 GHz	192.168.0.251	ChandranVilla_2.4G	ChandranVilla_5G	6	\N	1x1	1x1	11n	11n	-31	619	704	2026-10-11 17:49:52	37:15:e6:93:c5:17	Android	40 MHz	160 MHz
9e:d8:25:1c:7f:57	kennethloh57@unifi	eero-Max-7	Amazon Technologies Inc.	Amazon	STA	Access Point	Ethernet	192.168.0.98	ChandranVilla_2.4G	ChandranVilla_5G	\N	\N	2x2	4x4	11ax	11ax	\N	\N	\N	2026-10-11 07:08:52	37:15:e6:93:c5:17	\N	\N	\N
9e:51:34:d4:8c:6b	rajeshmuru498@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	ArandaHome_2.4G	ArandaHome_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
34:52:d6:e6:c4:36	rajeshmuru498@unifi	Intel-WiFi	Intel Corporate	Intel	STA	Gateway	2.4 GHz	192.168.0.119	ArandaHome_2.4G	ArandaHome_5G	1	\N	3x3	1x1	11ac	11ac	-72	868	232	2026-10-09 10:21:52	9e:51:34:d4:8c:6b	\N	40 MHz	80 MHz
85:56:49:a0:96:4c	rajeshmuru498@unifi	Galaxy-M14	Samsung Electronics Co., Ltd.	Samsung	STA	Repeater	2.4 GHz	192.168.0.144	ArandaHome_2.4G	ArandaHome_5G	1	\N	1x1	3x3	11ac	11ac	-48	104	24	2026-10-08 09:19:52	9e:51:34:d4:8c:6b	\N	40 MHz	160 MHz
1e:09:70:4b:14:bf	rajeshmuru498@unifi	AX201-Client	Intel Corporate	Intel	STA	Gateway	5 GHz	192.168.0.132	ArandaHome_2.4G	ArandaHome_5G	\N	36	3x3	2x2	11ax	11ax	-32	659	153	2026-10-11 19:10:52	9e:51:34:d4:8c:6b	Android	20 MHz	160 MHz
76:ec:27:a7:a1:f9	rajeshmuru498@unifi	Echo-Dot	Amazon Technologies Inc.	Amazon	STA	Repeater	2.4 GHz	192.168.0.156	ArandaHome_2.4G	ArandaHome_5G	6	\N	4x4	3x3	11ac	11ac	-39	694	106	2026-10-11 02:15:52	9e:51:34:d4:8c:6b	\N	20 MHz	80 MHz
80:d9:93:87:2c:73	rajeshmuru498@unifi	80:d9:93:87:2c:73	Amazon Technologies Inc.	Amazon	STA	Repeater	2.4 GHz	192.168.0.57	ArandaHome_2.4G	ArandaHome_5G	1	\N	2x2	4x4	11ac	11ac	-35	239	809	2026-10-10 11:11:52	9e:51:34:d4:8c:6b	\N	40 MHz	160 MHz
ba:9d:b3:b8:a6:2e	rajeshmuru498@unifi	decoMeshX50	TP-Link Systems Inc.	Tp Link	STA	Access Point	Ethernet	192.168.0.7	ArandaHome_2.4G	ArandaHome_5G	\N	\N	2x2	4x4	11ax	11ax	\N	\N	\N	2026-10-10 10:28:52	9e:51:34:d4:8c:6b	\N	\N	\N
b9:4e:29:a4:5c:12	rajeshmuru498@unifi	decoMeshX50	TP-Link Systems Inc.	Tp Link	STA	Access Point	Ethernet	192.168.0.65	ArandaHome_2.4G	ArandaHome_5G	\N	\N	2x2	4x4	11ax	11ax	\N	\N	\N	2026-10-12 02:30:52	9e:51:34:d4:8c:6b	\N	\N	\N
64:3d:6f:d2:f7:7e	rajeshmuru498@unifi	Orbi-RBK852	Netgear Inc.	Netgear	STA	Access Point	2.4 GHz	192.168.0.175	ArandaHome_2.4G	ArandaHome_5G	6	\N	2x2	4x4	11ax	11ax	-55	823	683	2026-10-10 13:39:52	9e:51:34:d4:8c:6b	\N	40 MHz	160 MHz
65:ff:bd:62:ec:8a	sitizaleha592@unifi	Root	ZTE Corporation	ZTE	Root	Access Point	Ethernet	192.168.0.1	HarmoniVilla_2.4G	HarmoniVilla_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	ZTE	40 MHz	160 MHz
ec:5a:d3:dd:b7:c1	sitizaleha592@unifi	Chromecast	Google LLC	Google	STA	Client	5 GHz	192.168.0.228	HarmoniVilla_2.4G	HarmoniVilla_5G	\N	157	3x3	1x1	11ac	11ac	-59	883	1069	2026-10-12 09:33:52	65:ff:bd:62:ec:8a	Windows	40 MHz	160 MHz
fc:ab:41:16:30:18	sitizaleha592@unifi	TP-Link-Repeater	TP-Link Technologies Co., Ltd.	TP-Link	STA	Gateway	2.4 GHz	192.168.0.4	HarmoniVilla_2.4G	HarmoniVilla_5G	6	\N	1x1	3x3	11ax	11ax	-54	103	928	2026-10-08 02:48:52	65:ff:bd:62:ec:8a	Windows	40 MHz	80 MHz
d3:56:7e:49:c6:d5	sitizaleha592@unifi	iPhone-15	Apple, Inc.	Apple	STA	Client	5 GHz	192.168.0.44	HarmoniVilla_2.4G	HarmoniVilla_5G	\N	149	1x1	3x3	11ax	11ax	-44	618	899	2026-10-11 15:25:52	65:ff:bd:62:ec:8a	\N	20 MHz	160 MHz
1b:1e:12:ae:eb:4a	sitizaleha592@unifi	POCO-M5	Xiaomi Communications Co., Ltd.	Xiaomi	STA	Repeater	5 GHz	192.168.0.115	HarmoniVilla_2.4G	HarmoniVilla_5G	\N	161	4x4	4x4	11n	11n	-57	650	38	2026-10-08 06:25:52	65:ff:bd:62:ec:8a	Android	40 MHz	80 MHz
98:ad:b6:ff:fa:f0	sitizaleha592@unifi	Echo-Dot	Amazon Technologies Inc.	Amazon	STA	Gateway	2.4 GHz	192.168.0.7	HarmoniVilla_2.4G	HarmoniVilla_5G	6	\N	3x3	1x1	11ax	11ax	-86	53	970	2026-10-10 03:54:52	65:ff:bd:62:ec:8a	Windows	40 MHz	80 MHz
7b:0f:8d:5f:a1:53	sitizaleha592@unifi	Fire-TV-Stick	Amazon Technologies Inc.	Amazon	STA	Client	2.4 GHz	192.168.0.2	HarmoniVilla_2.4G	HarmoniVilla_5G	6	\N	3x3	1x1	11n	11n	-73	301	53	2026-10-08 00:47:52	65:ff:bd:62:ec:8a	Linux	20 MHz	80 MHz
f9:32:dd:95:d9:2e	sitizaleha592@unifi	eero-6	Amazon Technologies Inc.	Amazon	STA	Access Point	Ethernet	192.168.0.33	HarmoniVilla_2.4G	HarmoniVilla_5G	\N	\N	2x2	4x4	11ax	11ax	\N	\N	\N	2026-10-12 08:48:52	65:ff:bd:62:ec:8a	\N	\N	\N
84:d9:98:53:cb:35	sitizaleha592@unifi	eero-Max-7	Amazon Technologies Inc.	Amazon	STA	Access Point	Ethernet	192.168.0.54	HarmoniVilla_2.4G	HarmoniVilla_5G	\N	\N	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-10 21:47:52	65:ff:bd:62:ec:8a	\N	\N	\N
de:e7:c9:55:17:00	sitizaleha592@unifi	Hue-Bulb	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.69	HarmoniVilla_2.4G	\N	11	\N	1x1	1x1	11n	\N	-47	138	130	2026-10-11 05:17:52	65:ff:bd:62:ec:8a	\N	20 MHz	\N
6e:36:ff:e3:f2:8a	leechinhua468@unifi	Root	ZTE Corporation	ZTE	Root	Access Point	Ethernet	192.168.0.1	VillaSri_2.4G	VillaSri_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	ZTE	40 MHz	160 MHz
51:dd:1c:6a:24:3b	leechinhua468@unifi	51:dd:1c:6a:24:3b	Google LLC	Google	STA	Repeater	2.4 GHz	192.168.0.208	VillaSri_2.4G	VillaSri_5G	6	\N	4x4	3x3	11ac	11ac	-51	722	1172	2026-10-08 12:24:52	6e:36:ff:e3:f2:8a	Linux	20 MHz	80 MHz
af:f4:9d:bc:2f:de	leechinhua468@unifi	AX201-Client	Intel Corporate	Intel	STA	Repeater	5 GHz	192.168.0.225	VillaSri_2.4G	VillaSri_5G	\N	153	4x4	1x1	11ax	11ax	-80	1025	1175	2026-10-11 16:04:52	6e:36:ff:e3:f2:8a	SKYWORTH	40 MHz	160 MHz
03:cc:8f:fd:44:58	leechinhua468@unifi	ESP32-Node	Espressif Inc.	Espressif	STA	Client	2.4 GHz	192.168.0.210	VillaSri_2.4G	VillaSri_5G	11	\N	4x4	1x1	11ax	11ax	-49	39	202	2026-10-11 20:03:52	6e:36:ff:e3:f2:8a	SKYWORTH	40 MHz	160 MHz
45:38:f0:00:68:f2	leechinhua468@unifi	ESP8266-Sensor	Espressif Inc.	Espressif	STA	IoT	2.4 GHz	192.168.0.174	VillaSri_2.4G	\N	6	\N	1x1	1x1	11n	\N	-75	147	149	2026-10-09 17:12:52	6e:36:ff:e3:f2:8a	\N	20 MHz	\N
08:98:d7:a1:0b:ed	leechinhua468@unifi	Hue-Strip	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.3	VillaSri_2.4G	\N	6	\N	1x1	1x1	11n	\N	-73	18	68	2026-10-11 16:19:52	6e:36:ff:e3:f2:8a	\N	20 MHz	\N
37:5e:5f:e7:86:68	leechinhua468@unifi	Sonoff-POW	ITEAD Intelligent Systems Co., Ltd.	Sonoff	STA	IoT	2.4 GHz	192.168.0.125	VillaSri_2.4G	\N	6	\N	1x1	1x1	11n	\N	-66	131	70	2026-10-11 04:24:52	6e:36:ff:e3:f2:8a	\N	20 MHz	\N
cd:57:2a:88:cc:6d	arunkrishn822@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	HarmoniVilla_2.4G	HarmoniVilla_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
fe:23:24:e9:bf:05	arunkrishn822@unifi	fe:23:24:e9:bf:05	TP-Link Technologies Co., Ltd.	TP-Link	STA	Gateway	2.4 GHz	192.168.0.131	HarmoniVilla_2.4G	HarmoniVilla_5G	11	\N	3x3	4x4	11n	11n	-39	916	1094	2026-10-10 20:23:52	cd:57:2a:88:cc:6d	SKYWORTH	40 MHz	160 MHz
53:49:fe:0c:47:38	arunkrishn822@unifi	Echo-Dot	Amazon Technologies Inc.	Amazon	STA	Repeater	5 GHz	192.168.0.214	HarmoniVilla_2.4G	HarmoniVilla_5G	\N	161	2x2	1x1	11n	11n	-31	240	1155	2026-10-07 14:33:52	cd:57:2a:88:cc:6d	\N	20 MHz	80 MHz
8d:4f:fe:38:12:55	arunkrishn822@unifi	POCO-M5	Xiaomi Communications Co., Ltd.	Xiaomi	STA	Client	5 GHz	192.168.0.150	HarmoniVilla_2.4G	HarmoniVilla_5G	\N	153	2x2	1x1	11ac	11ac	-46	625	886	2026-10-07 22:01:52	cd:57:2a:88:cc:6d	\N	20 MHz	160 MHz
f9:77:89:21:c8:11	arunkrishn822@unifi	WNC-AP	WNC Corporation	Wnc	STA	Repeater	5 GHz	192.168.0.99	HarmoniVilla_2.4G	HarmoniVilla_5G	\N	157	1x1	2x2	11ac	11ac	-46	209	351	2026-10-10 16:11:52	cd:57:2a:88:cc:6d	\N	40 MHz	80 MHz
bd:d8:b0:68:d5:c0	arunkrishn822@unifi	OPPO-Reno8	BBK Electronics Corp., Ltd.	Oppo	STA	Repeater	5 GHz	192.168.0.125	HarmoniVilla_2.4G	HarmoniVilla_5G	\N	161	3x3	3x3	11ac	11ac	-79	1122	954	2026-10-10 01:50:52	cd:57:2a:88:cc:6d	iOS	40 MHz	80 MHz
4e:0d:cf:58:c7:c7	arunkrishn822@unifi	decoMeshM4	TP-Link Systems Inc.	Tp Link	STA	Access Point	5 GHz	192.168.0.69	HarmoniVilla_2.4G	HarmoniVilla_5G	\N	157	2x2	2x2	11ax	11ax	-68	1075	241	2026-10-10 10:14:52	cd:57:2a:88:cc:6d	\N	40 MHz	160 MHz
d2:cf:ae:51:d3:d7	arunkrishn822@unifi	decoMeshX60	TP-Link Systems Inc.	Tp Link	STA	Access Point	5 GHz	192.168.0.240	HarmoniVilla_2.4G	HarmoniVilla_5G	\N	44	2x2	2x2	11ax	11ax	-63	924	970	2026-10-10 16:24:52	cd:57:2a:88:cc:6d	\N	40 MHz	160 MHz
38:24:81:68:5c:63	arunkrishn822@unifi	Sonoff-POW	ITEAD Intelligent Systems Co., Ltd.	Sonoff	STA	IoT	2.4 GHz	192.168.0.152	HarmoniVilla_2.4G	\N	11	\N	1x1	1x1	11n	\N	-49	107	118	2026-10-06 06:47:52	cd:57:2a:88:cc:6d	\N	20 MHz	\N
10:fd:8d:e3:db:d9	arunkrishn822@unifi	Shelly-EM	Allterco Robotics EOOD	Shelly	STA	IoT	2.4 GHz	192.168.0.158	HarmoniVilla_2.4G	\N	6	\N	1x1	1x1	11n	\N	-67	145	104	2026-10-08 16:21:52	cd:57:2a:88:cc:6d	\N	20 MHz	\N
bd:1a:22:e6:0e:83	teohbeecho43@unifi	Root	ZTE Corporation	ZTE	Root	Access Point	Ethernet	192.168.0.1	VillaSri_2.4G	VillaSri_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	ZTE	40 MHz	160 MHz
63:6f:18:8d:04:52	teohbeecho43@unifi	WNC-AP	WNC Corporation	Wnc	STA	Repeater	2.4 GHz	192.168.0.74	VillaSri_2.4G	VillaSri_5G	11	\N	2x2	4x4	11ax	11ax	-32	959	893	2026-10-11 17:36:52	bd:1a:22:e6:0e:83	iOS	40 MHz	160 MHz
57:b3:cc:a0:79:e4	teohbeecho43@unifi	TP-Link-Repeater	TP-Link Technologies Co., Ltd.	TP-Link	STA	Repeater	5 GHz	192.168.0.42	VillaSri_2.4G	VillaSri_5G	\N	149	3x3	3x3	11n	11n	-51	670	552	2026-10-12 00:35:52	bd:1a:22:e6:0e:83	\N	40 MHz	160 MHz
ca:c2:cb:cf:4b:0c	teohbeecho43@unifi	AX201-Client	Intel Corporate	Intel	STA	Client	5 GHz	192.168.0.64	VillaSri_2.4G	VillaSri_5G	\N	157	1x1	1x1	11ac	11ac	-37	453	15	2026-10-11 22:03:52	bd:1a:22:e6:0e:83	SKYWORTH	40 MHz	160 MHz
c5:a8:1e:fc:0d:5c	teohbeecho43@unifi	SKYWORTH-STB	Shenzhen Skyworth Digital Technology CO.	Skyworth	STA	Repeater	2.4 GHz	192.168.0.149	VillaSri_2.4G	VillaSri_5G	11	\N	2x2	4x4	11ax	11ax	-82	1087	563	2026-10-08 02:57:52	bd:1a:22:e6:0e:83	\N	40 MHz	160 MHz
0d:cf:7e:3c:cd:a0	teohbeecho43@unifi	Chromecast	Google LLC	Google	STA	Client	5 GHz	192.168.0.127	VillaSri_2.4G	VillaSri_5G	\N	48	2x2	4x4	11ax	11ax	-90	685	856	2026-10-08 20:57:52	bd:1a:22:e6:0e:83	Linux	40 MHz	80 MHz
fb:f5:26:c3:27:9e	teohbeecho43@unifi	iPhone-15	Apple, Inc.	Apple	STA	Gateway	2.4 GHz	192.168.0.253	VillaSri_2.4G	VillaSri_5G	6	\N	4x4	2x2	11n	11n	-79	410	569	2026-10-08 14:44:52	bd:1a:22:e6:0e:83	Android	20 MHz	160 MHz
e6:5f:0c:ea:91:34	teohbeecho43@unifi	espressif	Espressif Inc.	Espressif	STA	IoT	2.4 GHz	192.168.0.75	VillaSri_2.4G	\N	11	\N	1x1	1x1	11n	\N	-60	37	131	2026-10-09 04:08:52	bd:1a:22:e6:0e:83	\N	20 MHz	\N
c0:54:57:3a:95:3d	teohbeecho43@unifi	Hue-Bridge	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.109	VillaSri_2.4G	\N	6	\N	1x1	1x1	11n	\N	-40	33	99	2026-10-05 19:52:52	bd:1a:22:e6:0e:83	\N	20 MHz	\N
36:7a:d5:bd:1d:5b	teohbeecho43@unifi	Hue-Bridge	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.5	VillaSri_2.4G	\N	1	\N	1x1	1x1	11n	\N	-60	27	140	2026-10-07 02:07:52	bd:1a:22:e6:0e:83	\N	20 MHz	\N
a6:7d:e9:8a:c7:85	mohamadhaf651@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	HarmoniVilla_2.4G	HarmoniVilla_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
f2:f9:bc:28:e7:be	mohamadhaf651@unifi	Intel-WiFi	Intel Corporate	Intel	STA	Client	2.4 GHz	192.168.0.42	HarmoniVilla_2.4G	HarmoniVilla_5G	1	\N	2x2	4x4	11ax	11ax	-32	572	781	2026-10-08 17:15:52	a6:7d:e9:8a:c7:85	Windows	20 MHz	80 MHz
19:ee:36:98:69:6b	mohamadhaf651@unifi	Intel-WiFi	Intel Corporate	Intel	STA	Gateway	2.4 GHz	192.168.0.245	HarmoniVilla_2.4G	HarmoniVilla_5G	6	\N	3x3	2x2	11n	11n	-73	440	867	2026-10-10 11:11:52	a6:7d:e9:8a:c7:85	\N	20 MHz	160 MHz
c8:05:0b:b4:46:94	muhammadda162@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	ChandranVilla_2.4G	ChandranVilla_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
7e:52:10:8b:1e:06	muhammadda162@unifi	OnePlus-Nord	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Gateway	2.4 GHz	192.168.0.126	ChandranVilla_2.4G	ChandranVilla_5G	11	\N	1x1	1x1	11ac	11ac	-66	244	982	2026-10-07 10:19:52	c8:05:0b:b4:46:94	Android	40 MHz	160 MHz
8f:bd:9c:53:0a:fe	muhammadda162@unifi	Chromecast	Google LLC	Google	STA	Gateway	5 GHz	192.168.0.94	ChandranVilla_2.4G	ChandranVilla_5G	\N	36	2x2	3x3	11n	11n	-42	550	908	2026-10-11 08:25:52	c8:05:0b:b4:46:94	Android	20 MHz	80 MHz
40:57:22:b5:91:ac	muhammadda162@unifi	SKYWORTH-STB	Shenzhen Skyworth Digital Technology CO.	Skyworth	STA	Client	2.4 GHz	192.168.0.15	ChandranVilla_2.4G	ChandranVilla_5G	11	\N	3x3	4x4	11ax	11ax	-38	1064	222	2026-10-07 16:06:52	c8:05:0b:b4:46:94	Windows	20 MHz	80 MHz
df:49:50:3b:a4:57	muhammadda162@unifi	ESP32-Node	Espressif Inc.	Espressif	STA	Client	5 GHz	192.168.0.17	ChandranVilla_2.4G	ChandranVilla_5G	\N	40	3x3	1x1	11n	11n	-30	328	701	2026-10-10 07:50:52	c8:05:0b:b4:46:94	\N	40 MHz	80 MHz
d7:b8:d8:aa:cd:a2	muhammadda162@unifi	d7:b8:d8:aa:cd:a2	Espressif Inc.	Espressif	STA	Repeater	2.4 GHz	192.168.0.134	ChandranVilla_2.4G	ChandranVilla_5G	11	\N	3x3	2x2	11n	11n	-71	929	1191	2026-10-10 03:35:52	c8:05:0b:b4:46:94	\N	40 MHz	80 MHz
44:e7:79:d6:54:b4	muhammadda162@unifi	44:e7:79:d6:54:b4	Amazon Technologies Inc.	Amazon	STA	Gateway	2.4 GHz	192.168.0.251	ChandranVilla_2.4G	ChandranVilla_5G	6	\N	3x3	3x3	11ax	11ax	-64	1091	1059	2026-10-08 13:29:52	c8:05:0b:b4:46:94	Android	20 MHz	160 MHz
05:47:1f:3c:71:e2	muhammadda162@unifi	ESP32-CAM	Espressif Inc.	Espressif	STA	IoT	2.4 GHz	192.168.0.39	ChandranVilla_2.4G	\N	11	\N	1x1	1x1	11n	\N	-44	40	116	2026-10-09 05:49:52	c8:05:0b:b4:46:94	\N	20 MHz	\N
5a:95:55:a9:34:15	muhammadda162@unifi	Tuya-Wall-Switch	Tuya Smart Inc.	Tuya	STA	IoT	2.4 GHz	192.168.0.140	ChandranVilla_2.4G	\N	1	\N	1x1	1x1	11n	\N	-78	85	148	2026-10-12 08:33:52	c8:05:0b:b4:46:94	\N	20 MHz	\N
98:8b:9d:ae:c9:22	rosliahmad669@unifi	Root	ZTE Corporation	ZTE	Root	Access Point	Ethernet	192.168.0.1	VillaSri_2.4G	VillaSri_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	ZTE	40 MHz	160 MHz
95:d1:74:2b:9e:79	rosliahmad669@unifi	realme-Note-50	Realme Chongqing Mobile Telecommunications Corp.	Realme	STA	Client	5 GHz	192.168.0.138	VillaSri_2.4G	VillaSri_5G	\N	40	2x2	2x2	11ax	11ax	-74	567	407	2026-10-10 18:44:52	98:8b:9d:ae:c9:22	\N	40 MHz	80 MHz
db:06:97:e7:af:6b	rosliahmad669@unifi	SKYWORTH-STB	Shenzhen Skyworth Digital Technology CO.	Skyworth	STA	Repeater	5 GHz	192.168.0.193	VillaSri_2.4G	VillaSri_5G	\N	157	2x2	4x4	11ax	11ax	-37	335	702	2026-10-09 08:42:52	98:8b:9d:ae:c9:22	Linux	20 MHz	160 MHz
32:9d:6e:a6:f8:a5	rosliahmad669@unifi	TP-Link-Repeater	TP-Link Technologies Co., Ltd.	TP-Link	STA	Repeater	2.4 GHz	192.168.0.119	VillaSri_2.4G	VillaSri_5G	1	\N	1x1	4x4	11ax	11ax	-57	359	872	2026-10-09 14:18:52	98:8b:9d:ae:c9:22	\N	40 MHz	160 MHz
0f:2e:6e:9d:91:63	rosliahmad669@unifi	Intel-WiFi	Intel Corporate	Intel	STA	Gateway	5 GHz	192.168.0.155	VillaSri_2.4G	VillaSri_5G	\N	153	1x1	2x2	11ac	11ac	-41	636	1167	2026-10-10 07:07:52	98:8b:9d:ae:c9:22	\N	20 MHz	80 MHz
0b:43:a0:ad:bc:79	mohamadhaf31@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	ArandaHome_2.4G	ArandaHome_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
d2:73:80:29:c8:5d	mohamadhaf31@unifi	OnePlus-11	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Gateway	5 GHz	192.168.0.108	ArandaHome_2.4G	ArandaHome_5G	\N	48	3x3	4x4	11ac	11ac	-57	426	922	2026-10-09 05:08:52	0b:43:a0:ad:bc:79	\N	40 MHz	80 MHz
f6:91:e5:45:a1:d4	mohamadhaf31@unifi	OnePlus-Nord	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Gateway	2.4 GHz	192.168.0.9	ArandaHome_2.4G	ArandaHome_5G	1	\N	2x2	1x1	11ax	11ax	-78	1027	91	2026-10-11 13:43:52	0b:43:a0:ad:bc:79	\N	20 MHz	160 MHz
0f:3c:5a:99:a1:4f	mohamadhaf31@unifi	TP-Link-Repeater	TP-Link Technologies Co., Ltd.	TP-Link	STA	Gateway	5 GHz	192.168.0.241	ArandaHome_2.4G	ArandaHome_5G	\N	149	1x1	1x1	11ax	11ax	-74	516	308	2026-10-11 05:48:52	0b:43:a0:ad:bc:79	iOS	40 MHz	80 MHz
fd:48:a0:05:f4:35	mohamadhaf31@unifi	OPPO-F19	BBK Electronics Corp., Ltd.	Oppo	STA	Repeater	2.4 GHz	192.168.0.196	ArandaHome_2.4G	ArandaHome_5G	1	\N	3x3	2x2	11ac	11ac	-75	70	103	2026-10-07 18:41:52	0b:43:a0:ad:bc:79	\N	40 MHz	160 MHz
04:16:f7:25:35:46	tanchweeme791@unifi	Root	Fiberhome Telecommunication Technologies Co., Ltd.	FiberHome	Root	Access Point	Ethernet	192.168.0.1	TamanAman_2.4G	TamanAman_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	FIBERHOME	40 MHz	160 MHz
d4:bd:c0:f3:c5:ca	tanchweeme791@unifi	Galaxy-M14	Samsung Electronics Co., Ltd.	Samsung	STA	Repeater	5 GHz	192.168.0.83	TamanAman_2.4G	TamanAman_5G	\N	157	2x2	2x2	11n	11n	-58	711	1176	2026-10-09 00:44:52	04:16:f7:25:35:46	Windows	20 MHz	80 MHz
c6:fe:5a:61:1f:e2	tanchweeme791@unifi	iPad-Air	Apple, Inc.	Apple	STA	Gateway	2.4 GHz	192.168.0.37	TamanAman_2.4G	TamanAman_5G	6	\N	3x3	4x4	11n	11n	-34	226	233	2026-10-09 02:52:52	04:16:f7:25:35:46	SKYWORTH	20 MHz	160 MHz
97:f9:5a:96:a3:7d	tanchweeme791@unifi	V2029	vivo Mobile Communication Co., Ltd.	Vivo	STA	Client	5 GHz	192.168.0.14	TamanAman_2.4G	TamanAman_5G	\N	153	3x3	4x4	11ax	11ax	-53	394	328	2026-10-10 01:38:52	04:16:f7:25:35:46	Windows	40 MHz	80 MHz
0a:c1:eb:38:aa:e1	tanchweeme791@unifi	iPhone-13	Apple, Inc.	Apple	STA	Gateway	5 GHz	192.168.0.216	TamanAman_2.4G	TamanAman_5G	\N	153	2x2	1x1	11ax	11ax	-84	214	124	2026-10-10 16:42:52	04:16:f7:25:35:46	iOS	40 MHz	160 MHz
3b:e6:13:26:fa:e5	tanchweeme791@unifi	Orbi-RBS350	Netgear Inc.	Netgear	STA	Access Point	2.4 GHz	192.168.0.29	TamanAman_2.4G	TamanAman_5G	11	\N	2x2	2x2	11ax	11ax	-70	235	211	2026-10-10 19:41:52	04:16:f7:25:35:46	\N	40 MHz	160 MHz
85:34:87:b2:a5:da	tanchweeme791@unifi	Orbi-RBR750	Netgear Inc.	Netgear	STA	Access Point	2.4 GHz	192.168.0.98	TamanAman_2.4G	TamanAman_5G	11	\N	2x2	2x2	11ax	11ax	-62	1003	200	2026-10-10 20:07:52	04:16:f7:25:35:46	\N	40 MHz	160 MHz
85:b4:ce:aa:ec:1c	tanchweeme791@unifi	eero-6	Amazon Technologies Inc.	Amazon	STA	Access Point	Ethernet	192.168.0.173	TamanAman_2.4G	TamanAman_5G	\N	\N	2x2	4x4	11ax	11ax	\N	\N	\N	2026-10-11 19:04:52	04:16:f7:25:35:46	\N	\N	\N
1c:60:b4:86:ab:66	tanchweeme791@unifi	ESP32-CAM	Espressif Inc.	Espressif	STA	IoT	2.4 GHz	192.168.0.217	TamanAman_2.4G	\N	11	\N	1x1	1x1	11n	\N	-75	89	139	2026-10-10 09:37:52	04:16:f7:25:35:46	\N	20 MHz	\N
21:54:ed:bc:da:39	tanchweeme791@unifi	Shelly-Plus-1PM	Allterco Robotics EOOD	Shelly	STA	IoT	2.4 GHz	192.168.0.165	TamanAman_2.4G	\N	1	\N	1x1	1x1	11n	\N	-55	77	30	2026-10-10 01:55:52	04:16:f7:25:35:46	\N	20 MHz	\N
f9:2b:df:58:1d:d0	tanchweeme791@unifi	espressif	Espressif Inc.	Espressif	STA	IoT	2.4 GHz	192.168.0.190	TamanAman_2.4G	\N	11	\N	1x1	1x1	11n	\N	-60	43	132	2026-10-08 07:09:52	04:16:f7:25:35:46	\N	20 MHz	\N
71:79:7f:33:ce:cd	gohsoonhua194@unifi	Root	Fiberhome Telecommunication Technologies Co., Ltd.	FiberHome	Root	Access Point	Ethernet	192.168.0.1	HarmoniVilla_2.4G	HarmoniVilla_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	FIBERHOME	40 MHz	160 MHz
59:d7:89:e7:41:dd	gohsoonhua194@unifi	Galaxy-A54	Samsung Electronics Co., Ltd.	Samsung	STA	Gateway	5 GHz	192.168.0.177	HarmoniVilla_2.4G	HarmoniVilla_5G	\N	149	2x2	1x1	11ax	11ax	-43	657	523	2026-10-10 15:40:52	71:79:7f:33:ce:cd	SKYWORTH	40 MHz	80 MHz
6f:2e:eb:a1:5b:92	gohsoonhua194@unifi	OnePlus-11	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Repeater	2.4 GHz	192.168.0.82	HarmoniVilla_2.4G	HarmoniVilla_5G	6	\N	2x2	4x4	11ac	11ac	-35	1122	748	2026-10-11 13:32:52	71:79:7f:33:ce:cd	\N	20 MHz	80 MHz
4a:f0:d7:9e:c6:38	tanchweeme843@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	TamanAman_2.4G	TamanAman_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
0b:48:e7:b2:22:b8	tanchweeme843@unifi	Intel-WiFi	Intel Corporate	Intel	STA	Client	5 GHz	192.168.0.220	TamanAman_2.4G	TamanAman_5G	\N	36	3x3	4x4	11n	11n	-53	1040	665	2026-10-09 02:33:52	4a:f0:d7:9e:c6:38	Windows	40 MHz	80 MHz
35:6e:2b:df:55:0d	tanchweeme843@unifi	realme-C55	Realme Chongqing Mobile Telecommunications Corp.	Realme	STA	Gateway	5 GHz	192.168.0.4	TamanAman_2.4G	TamanAman_5G	\N	149	2x2	1x1	11n	11n	-60	178	850	2026-10-11 12:07:52	4a:f0:d7:9e:c6:38	Windows	20 MHz	160 MHz
06:4c:5e:7f:53:16	tanchweeme843@unifi	Galaxy-M14	Samsung Electronics Co., Ltd.	Samsung	STA	Gateway	2.4 GHz	192.168.0.9	TamanAman_2.4G	TamanAman_5G	6	\N	4x4	1x1	11ax	11ax	-65	765	330	2026-10-10 03:52:52	4a:f0:d7:9e:c6:38	Windows	40 MHz	80 MHz
43:f3:57:56:a1:ea	tanchweeme843@unifi	43:f3:57:56:a1:ea	Amazon Technologies Inc.	Amazon	STA	Repeater	2.4 GHz	192.168.0.136	TamanAman_2.4G	TamanAman_5G	1	\N	4x4	4x4	11ax	11ax	-85	1031	423	2026-10-09 03:18:52	4a:f0:d7:9e:c6:38	Android	20 MHz	160 MHz
ac:b1:e7:a1:d7:29	tanchweeme843@unifi	Echo-Dot	Amazon Technologies Inc.	Amazon	STA	Repeater	2.4 GHz	192.168.0.200	TamanAman_2.4G	TamanAman_5G	6	\N	4x4	1x1	11n	11n	-66	111	669	2026-10-08 04:04:52	4a:f0:d7:9e:c6:38	\N	20 MHz	160 MHz
a7:fb:56:1a:e9:f8	tanchweeme843@unifi	V2029	vivo Mobile Communication Co., Ltd.	Vivo	STA	Gateway	5 GHz	192.168.0.40	TamanAman_2.4G	TamanAman_5G	\N	36	1x1	1x1	11n	11n	-31	604	57	2026-10-08 21:37:52	4a:f0:d7:9e:c6:38	\N	20 MHz	80 MHz
e7:98:9f:9b:da:3f	tanchweeme843@unifi	Hue-Strip	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.242	TamanAman_2.4G	\N	1	\N	1x1	1x1	11n	\N	-52	96	122	2026-10-11 02:18:52	4a:f0:d7:9e:c6:38	\N	20 MHz	\N
75:5c:f3:86:b5:92	rajeshmuru682@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	BayuHome_2.4G	BayuHome_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
fc:ba:bd:5e:a1:bb	rajeshmuru682@unifi	OPPO-A78	BBK Electronics Corp., Ltd.	Oppo	STA	Repeater	2.4 GHz	192.168.0.216	BayuHome_2.4G	BayuHome_5G	6	\N	2x2	4x4	11ax	11ax	-52	260	1063	2026-10-10 15:21:52	75:5c:f3:86:b5:92	iOS	40 MHz	160 MHz
cb:ce:d5:9d:28:53	rajeshmuru682@unifi	iPhone-15	Apple, Inc.	Apple	STA	Client	2.4 GHz	192.168.0.193	BayuHome_2.4G	BayuHome_5G	11	\N	1x1	2x2	11ac	11ac	-87	432	194	2026-10-10 21:53:52	75:5c:f3:86:b5:92	\N	40 MHz	80 MHz
b7:c9:a5:3c:39:68	rajeshmuru682@unifi	Fire-TV-Stick	Amazon Technologies Inc.	Amazon	STA	Repeater	2.4 GHz	192.168.0.143	BayuHome_2.4G	BayuHome_5G	11	\N	1x1	1x1	11n	11n	-37	552	890	2026-10-07 14:44:52	75:5c:f3:86:b5:92	iOS	40 MHz	160 MHz
2d:ff:d3:48:1d:18	rajeshmuru682@unifi	decoMeshX50	TP-Link Systems Inc.	Tp Link	STA	Access Point	5 GHz	192.168.0.117	BayuHome_2.4G	BayuHome_5G	\N	44	2x2	4x4	11ax	11ax	-54	470	869	2026-10-10 14:32:52	75:5c:f3:86:b5:92	\N	40 MHz	160 MHz
19:5a:7c:39:0a:c5	rajeshmuru682@unifi	Nest-Wifi-Pro	Google LLC	Google	STA	Access Point	Ethernet	192.168.0.229	BayuHome_2.4G	BayuHome_5G	\N	\N	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-11 16:11:52	75:5c:f3:86:b5:92	\N	\N	\N
2b:16:e7:55:45:42	rajeshmuru682@unifi	Tuya-Bulb	Tuya Smart Inc.	Tuya	STA	IoT	2.4 GHz	192.168.0.244	BayuHome_2.4G	\N	11	\N	1x1	1x1	11n	\N	-52	93	33	2026-10-09 19:02:52	75:5c:f3:86:b5:92	\N	20 MHz	\N
44:ae:86:72:3d:c7	priyasamy35@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	SeriMawar_2.4G	SeriMawar_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
3a:c2:98:d0:e2:b7	priyasamy35@unifi	SKYWORTH-STB	Shenzhen Skyworth Digital Technology CO.	Skyworth	STA	Repeater	5 GHz	192.168.0.232	SeriMawar_2.4G	SeriMawar_5G	\N	36	1x1	1x1	11ac	11ac	-30	488	1085	2026-10-10 13:18:52	44:ae:86:72:3d:c7	iOS	40 MHz	160 MHz
ef:9d:b5:55:d2:58	priyasamy35@unifi	iPhone-15	Apple, Inc.	Apple	STA	Client	2.4 GHz	192.168.0.59	SeriMawar_2.4G	SeriMawar_5G	11	\N	3x3	1x1	11ax	11ax	-85	227	1059	2026-10-09 14:16:52	44:ae:86:72:3d:c7	\N	20 MHz	80 MHz
12:6d:4e:f8:18:28	priyasamy35@unifi	OnePlus-Nord	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Repeater	5 GHz	192.168.0.41	SeriMawar_2.4G	SeriMawar_5G	\N	153	2x2	2x2	11ax	11ax	-37	502	120	2026-10-09 20:07:52	44:ae:86:72:3d:c7	iOS	20 MHz	80 MHz
ab:d6:61:d6:3b:62	priyasamy35@unifi	Nest-Wifi-Router	Google LLC	Google	STA	Access Point	Ethernet	192.168.0.63	SeriMawar_2.4G	SeriMawar_5G	\N	\N	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 02:29:52	44:ae:86:72:3d:c7	\N	\N	\N
50:33:6d:1e:9f:bf	priyasamy35@unifi	Nest-Wifi-Router	Google LLC	Google	STA	Access Point	Ethernet	192.168.0.245	SeriMawar_2.4G	SeriMawar_5G	\N	\N	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-10 21:21:52	44:ae:86:72:3d:c7	\N	\N	\N
0c:d9:ec:b1:a7:50	priyasamy35@unifi	Orbi-RBR750	Netgear Inc.	Netgear	STA	Access Point	5 GHz	192.168.0.229	SeriMawar_2.4G	SeriMawar_5G	\N	161	2x2	4x4	11ax	11ax	-62	229	905	2026-10-11 22:37:52	44:ae:86:72:3d:c7	\N	40 MHz	160 MHz
a4:e9:d5:f4:a9:44	priyasamy35@unifi	Shelly-Plus-1PM	Allterco Robotics EOOD	Shelly	STA	IoT	2.4 GHz	192.168.0.161	SeriMawar_2.4G	\N	6	\N	1x1	1x1	11n	\N	-46	84	84	2026-10-08 03:14:52	44:ae:86:72:3d:c7	\N	20 MHz	\N
76:fb:74:aa:d0:39	saifulazma630@unifi	Root	ZTE Corporation	ZTE	Root	Access Point	Ethernet	192.168.0.1	BayuHome_2.4G	BayuHome_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	ZTE	40 MHz	160 MHz
a6:2d:1f:1d:b1:84	saifulazma630@unifi	realme-Note-50	Realme Chongqing Mobile Telecommunications Corp.	Realme	STA	Client	5 GHz	192.168.0.86	BayuHome_2.4G	BayuHome_5G	\N	161	3x3	3x3	11n	11n	-41	854	1120	2026-10-10 19:27:52	76:fb:74:aa:d0:39	iOS	40 MHz	80 MHz
42:ac:97:fa:2e:66	saifulazma630@unifi	Echo-Dot	Amazon Technologies Inc.	Amazon	STA	Gateway	5 GHz	192.168.0.65	BayuHome_2.4G	BayuHome_5G	\N	157	4x4	2x2	11n	11n	-57	72	245	2026-10-09 16:25:52	76:fb:74:aa:d0:39	Windows	40 MHz	160 MHz
d8:57:0d:d8:fc:31	saifulazma630@unifi	d8:57:0d:d8:fc:31	BBK Electronics Corp., Ltd.	Oppo	STA	Repeater	5 GHz	192.168.0.10	BayuHome_2.4G	BayuHome_5G	\N	40	2x2	4x4	11ac	11ac	-45	917	1164	2026-10-09 20:04:52	76:fb:74:aa:d0:39	Linux	20 MHz	80 MHz
dd:bf:22:70:7c:c0	saifulazma630@unifi	OnePlus-11	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Repeater	5 GHz	192.168.0.34	BayuHome_2.4G	BayuHome_5G	\N	161	4x4	1x1	11ax	11ax	-62	285	92	2026-10-08 11:36:52	76:fb:74:aa:d0:39	Linux	20 MHz	160 MHz
01:d9:78:7f:ea:e4	saifulazma630@unifi	OPPO-A78	BBK Electronics Corp., Ltd.	Oppo	STA	Repeater	2.4 GHz	192.168.0.164	BayuHome_2.4G	BayuHome_5G	6	\N	2x2	3x3	11ac	11ac	-76	1008	738	2026-10-07 16:58:52	76:fb:74:aa:d0:39	Windows	20 MHz	80 MHz
e1:f7:73:a0:f5:ad	saifulazma630@unifi	eero-6	Amazon Technologies Inc.	Amazon	STA	Access Point	Ethernet	192.168.0.186	BayuHome_2.4G	BayuHome_5G	\N	\N	2x2	4x4	11ax	11ax	\N	\N	\N	2026-10-10 13:10:52	76:fb:74:aa:d0:39	\N	\N	\N
66:8c:75:77:07:94	saifulazma630@unifi	Orbi-RBR750	Netgear Inc.	Netgear	STA	Access Point	Ethernet	192.168.0.78	BayuHome_2.4G	BayuHome_5G	\N	\N	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 01:29:52	76:fb:74:aa:d0:39	\N	\N	\N
48:24:e5:fa:3e:c6	saifulazma901@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	DamaiResidensi_2.4G	DamaiResidensi_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
8c:a2:0c:96:7c:2c	saifulazma901@unifi	8c:a2:0c:96:7c:2c	TP-Link Technologies Co., Ltd.	TP-Link	STA	Gateway	2.4 GHz	192.168.0.152	DamaiResidensi_2.4G	DamaiResidensi_5G	6	\N	3x3	1x1	11ac	11ac	-60	149	1172	2026-10-11 07:29:52	48:24:e5:fa:3e:c6	\N	20 MHz	80 MHz
4c:a0:c7:db:06:7b	saifulazma901@unifi	WNC-Client	WNC Corporation	Wnc	STA	Repeater	2.4 GHz	192.168.0.137	DamaiResidensi_2.4G	DamaiResidensi_5G	11	\N	1x1	3x3	11ac	11ac	-43	467	1015	2026-10-09 00:27:52	48:24:e5:fa:3e:c6	\N	20 MHz	80 MHz
fc:e9:35:5a:1b:44	saifulazma901@unifi	OnePlus-Nord	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Gateway	2.4 GHz	192.168.0.21	DamaiResidensi_2.4G	DamaiResidensi_5G	6	\N	2x2	4x4	11ax	11ax	-73	847	932	2026-10-07 13:03:52	48:24:e5:fa:3e:c6	Windows	40 MHz	80 MHz
22:fd:b7:52:57:76	saifulazma901@unifi	iPad-Air	Apple, Inc.	Apple	STA	Repeater	5 GHz	192.168.0.202	DamaiResidensi_2.4G	DamaiResidensi_5G	\N	149	2x2	4x4	11ac	11ac	-72	125	502	2026-10-08 09:03:52	48:24:e5:fa:3e:c6	SKYWORTH	20 MHz	160 MHz
c3:96:ca:bc:b6:d9	saifulazma901@unifi	Nest-Wifi-Pro	Google LLC	Google	STA	Access Point	Ethernet	192.168.0.106	DamaiResidensi_2.4G	DamaiResidensi_5G	\N	\N	2x2	4x4	11ax	11ax	\N	\N	\N	2026-10-12 04:51:52	48:24:e5:fa:3e:c6	\N	\N	\N
32:41:f2:12:14:00	saifulazma901@unifi	Nest-Wifi-Pro	Google LLC	Google	STA	Access Point	5 GHz	192.168.0.53	DamaiResidensi_2.4G	DamaiResidensi_5G	\N	44	2x2	2x2	11ax	11ax	-50	1105	1172	2026-10-11 10:43:52	48:24:e5:fa:3e:c6	\N	40 MHz	160 MHz
a9:29:d5:09:ac:e5	saifulazma901@unifi	Orbi-RBK852	Netgear Inc.	Netgear	STA	Access Point	Ethernet	192.168.0.185	DamaiResidensi_2.4G	DamaiResidensi_5G	\N	\N	2x2	4x4	11ax	11ax	\N	\N	\N	2026-10-11 20:39:52	48:24:e5:fa:3e:c6	\N	\N	\N
c8:0c:5d:d9:57:3f	rosliahmad948@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	HarmoniVilla_2.4G	HarmoniVilla_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
e7:be:f6:5e:d2:c3	rosliahmad948@unifi	POCO-M5	Xiaomi Communications Co., Ltd.	Xiaomi	STA	Repeater	2.4 GHz	192.168.0.164	HarmoniVilla_2.4G	HarmoniVilla_5G	1	\N	1x1	4x4	11ac	11ac	-65	1103	539	2026-10-10 00:05:52	c8:0c:5d:d9:57:3f	Windows	40 MHz	80 MHz
3e:4f:88:e2:3a:76	rosliahmad948@unifi	Chromecast	Google LLC	Google	STA	Gateway	2.4 GHz	192.168.0.107	HarmoniVilla_2.4G	HarmoniVilla_5G	6	\N	2x2	3x3	11n	11n	-34	27	904	2026-10-10 17:52:52	c8:0c:5d:d9:57:3f	\N	20 MHz	160 MHz
16:07:f4:7f:47:ed	rosliahmad948@unifi	Hue-Strip	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.90	HarmoniVilla_2.4G	\N	1	\N	1x1	1x1	11n	\N	-45	148	118	2026-10-11 16:00:52	c8:0c:5d:d9:57:3f	\N	20 MHz	\N
92:7f:fd:f0:a9:da	zainalabid85@unifi	Root	Fiberhome Telecommunication Technologies Co., Ltd.	FiberHome	Root	Access Point	Ethernet	192.168.0.1	ChandranVilla_2.4G	ChandranVilla_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	FIBERHOME	40 MHz	160 MHz
0f:02:d1:6b:81:8a	zainalabid85@unifi	Intel-WiFi	Intel Corporate	Intel	STA	Repeater	5 GHz	192.168.0.96	ChandranVilla_2.4G	ChandranVilla_5G	\N	40	3x3	4x4	11ac	11ac	-51	684	984	2026-10-09 18:47:52	92:7f:fd:f0:a9:da	Linux	20 MHz	80 MHz
3c:0d:6a:e6:f9:81	zainalabid85@unifi	OPPO-Reno8	BBK Electronics Corp., Ltd.	Oppo	STA	Repeater	5 GHz	192.168.0.214	ChandranVilla_2.4G	ChandranVilla_5G	\N	161	2x2	3x3	11ac	11ac	-47	46	819	2026-10-09 19:01:52	92:7f:fd:f0:a9:da	Windows	40 MHz	80 MHz
32:ec:ac:51:1f:98	zainalabid85@unifi	ESP8266-Sensor	Espressif Inc.	Espressif	STA	Client	5 GHz	192.168.0.131	ChandranVilla_2.4G	ChandranVilla_5G	\N	157	4x4	4x4	11ac	11ac	-81	475	29	2026-10-11 02:46:52	92:7f:fd:f0:a9:da	Linux	40 MHz	80 MHz
ca:13:da:6a:1d:16	zainalabid85@unifi	Mi-11X	Xiaomi Communications Co., Ltd.	Xiaomi	STA	Repeater	2.4 GHz	192.168.0.49	ChandranVilla_2.4G	ChandranVilla_5G	11	\N	1x1	1x1	11n	11n	-52	30	305	2026-10-09 11:57:52	92:7f:fd:f0:a9:da	\N	40 MHz	80 MHz
66:24:4b:ed:b2:17	zainalabid85@unifi	SKYWORTH-STB	Shenzhen Skyworth Digital Technology CO.	Skyworth	STA	Gateway	5 GHz	192.168.0.93	ChandranVilla_2.4G	ChandranVilla_5G	\N	36	4x4	1x1	11n	11n	-37	563	966	2026-10-07 18:15:52	92:7f:fd:f0:a9:da	\N	20 MHz	80 MHz
66:00:52:7b:01:62	tanticksew84@unifi	Root	Fiberhome Telecommunication Technologies Co., Ltd.	FiberHome	Root	Access Point	Ethernet	192.168.0.1	SeriMawar_2.4G	SeriMawar_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	FIBERHOME	40 MHz	160 MHz
1f:7d:ad:9a:96:92	tanticksew84@unifi	ESP8266-Sensor	Espressif Inc.	Espressif	STA	Client	2.4 GHz	192.168.0.222	SeriMawar_2.4G	SeriMawar_5G	11	\N	4x4	1x1	11n	11n	-62	912	1147	2026-10-09 11:21:52	66:00:52:7b:01:62	Linux	20 MHz	80 MHz
b2:d4:27:42:60:40	tanticksew84@unifi	OnePlus-11	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Gateway	2.4 GHz	192.168.0.24	SeriMawar_2.4G	SeriMawar_5G	1	\N	4x4	1x1	11ax	11ax	-34	738	1089	2026-10-08 22:43:52	66:00:52:7b:01:62	Android	20 MHz	160 MHz
a2:ad:a3:2b:0a:7b	tanticksew84@unifi	a2:ad:a3:2b:0a:7b	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Repeater	2.4 GHz	192.168.0.212	SeriMawar_2.4G	SeriMawar_5G	1	\N	1x1	1x1	11ac	11ac	-37	653	1155	2026-10-11 00:46:52	66:00:52:7b:01:62	iOS	20 MHz	80 MHz
d4:46:20:70:78:71	tanticksew84@unifi	realme-11-Pro	Realme Chongqing Mobile Telecommunications Corp.	Realme	STA	Gateway	5 GHz	192.168.0.58	SeriMawar_2.4G	SeriMawar_5G	\N	44	1x1	1x1	11ac	11ac	-51	779	613	2026-10-08 03:33:52	66:00:52:7b:01:62	Linux	20 MHz	160 MHz
46:fc:ba:16:73:61	tanticksew84@unifi	SKYWORTH-STB	Shenzhen Skyworth Digital Technology CO.	Skyworth	STA	Repeater	5 GHz	192.168.0.23	SeriMawar_2.4G	SeriMawar_5G	\N	157	1x1	1x1	11n	11n	-60	81	821	2026-10-12 04:06:52	66:00:52:7b:01:62	\N	20 MHz	160 MHz
97:37:35:fb:1f:5e	tanticksew84@unifi	V2207	vivo Mobile Communication Co., Ltd.	Vivo	STA	Repeater	2.4 GHz	192.168.0.67	SeriMawar_2.4G	SeriMawar_5G	6	\N	4x4	3x3	11ax	11ax	-48	127	1007	2026-10-09 02:33:52	66:00:52:7b:01:62	\N	40 MHz	80 MHz
53:dc:dd:d4:0c:dc	tanticksew84@unifi	espressif	Espressif Inc.	Espressif	STA	IoT	2.4 GHz	192.168.0.118	SeriMawar_2.4G	\N	1	\N	1x1	1x1	11n	\N	-50	55	40	2026-10-08 22:16:52	66:00:52:7b:01:62	\N	20 MHz	\N
21:fe:3e:13:41:a0	tanticksew84@unifi	ESP32-CAM	Espressif Inc.	Espressif	STA	IoT	2.4 GHz	192.168.0.51	SeriMawar_2.4G	\N	6	\N	1x1	1x1	11n	\N	-51	73	122	2026-10-06 16:29:52	66:00:52:7b:01:62	\N	20 MHz	\N
92:29:6c:3a:f7:11	wongmeilin187@unifi	Root	ZTE Corporation	ZTE	Root	Access Point	Ethernet	192.168.0.1	HarmoniVilla_2.4G	HarmoniVilla_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	ZTE	40 MHz	160 MHz
5d:12:5f:5c:27:d8	wongmeilin187@unifi	iPhone-15	Apple, Inc.	Apple	STA	Gateway	2.4 GHz	192.168.0.190	HarmoniVilla_2.4G	HarmoniVilla_5G	1	\N	1x1	4x4	11ac	11ac	-33	1122	778	2026-10-09 06:47:52	92:29:6c:3a:f7:11	iOS	40 MHz	160 MHz
03:e8:eb:43:c0:3b	wongmeilin187@unifi	V2332	vivo Mobile Communication Co., Ltd.	Vivo	STA	Repeater	5 GHz	192.168.0.51	HarmoniVilla_2.4G	HarmoniVilla_5G	\N	157	4x4	1x1	11ac	11ac	-76	578	1050	2026-10-09 11:25:52	92:29:6c:3a:f7:11	Linux	40 MHz	80 MHz
30:56:48:16:2a:3c	wongmeilin187@unifi	Redmi-Note-12	Xiaomi Communications Co., Ltd.	Xiaomi	STA	Client	2.4 GHz	192.168.0.132	HarmoniVilla_2.4G	HarmoniVilla_5G	1	\N	4x4	2x2	11ax	11ax	-42	422	406	2026-10-09 23:30:52	92:29:6c:3a:f7:11	\N	20 MHz	160 MHz
04:a8:4b:d9:3d:22	wongmeilin187@unifi	SKYWORTH-STB	Shenzhen Skyworth Digital Technology CO.	Skyworth	STA	Repeater	5 GHz	192.168.0.236	HarmoniVilla_2.4G	HarmoniVilla_5G	\N	157	1x1	2x2	11ac	11ac	-70	588	990	2026-10-10 18:37:52	92:29:6c:3a:f7:11	Linux	20 MHz	80 MHz
65:d0:bc:74:b0:84	rosliahmad846@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	VillaSri_2.4G	VillaSri_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
62:05:01:a3:39:a0	rosliahmad846@unifi	MacBook-Pro	Apple, Inc.	Apple	STA	Repeater	2.4 GHz	192.168.0.136	VillaSri_2.4G	VillaSri_5G	1	\N	1x1	3x3	11n	11n	-61	1060	1092	2026-10-11 21:28:52	65:d0:bc:74:b0:84	Linux	40 MHz	160 MHz
ca:17:e1:2c:ec:32	rosliahmad846@unifi	Mi-11X	Xiaomi Communications Co., Ltd.	Xiaomi	STA	Client	5 GHz	192.168.0.246	VillaSri_2.4G	VillaSri_5G	\N	40	3x3	2x2	11n	11n	-63	971	1118	2026-10-12 06:43:52	65:d0:bc:74:b0:84	Android	40 MHz	160 MHz
52:c3:fa:ac:57:47	rosliahmad846@unifi	SKYWORTH-STB	Shenzhen Skyworth Digital Technology CO.	Skyworth	STA	Gateway	2.4 GHz	192.168.0.41	VillaSri_2.4G	VillaSri_5G	6	\N	1x1	4x4	11ac	11ac	-33	1188	568	2026-10-09 02:01:52	65:d0:bc:74:b0:84	\N	20 MHz	160 MHz
4e:e4:f6:75:6f:20	rosliahmad846@unifi	iPhone-15	Apple, Inc.	Apple	STA	Client	5 GHz	192.168.0.88	VillaSri_2.4G	VillaSri_5G	\N	36	3x3	2x2	11ax	11ax	-75	501	251	2026-10-08 15:38:52	65:d0:bc:74:b0:84	\N	40 MHz	160 MHz
f2:37:dd:e5:f3:5d	rosliahmad846@unifi	V2148	vivo Mobile Communication Co., Ltd.	Vivo	STA	Client	2.4 GHz	192.168.0.24	VillaSri_2.4G	VillaSri_5G	11	\N	1x1	2x2	11ac	11ac	-62	1129	392	2026-10-10 19:24:52	65:d0:bc:74:b0:84	Linux	40 MHz	160 MHz
27:ff:18:9f:85:56	rosliahmad846@unifi	ESP32-Switch	Espressif Inc.	Espressif	STA	IoT	2.4 GHz	192.168.0.134	VillaSri_2.4G	\N	1	\N	1x1	1x1	11n	\N	-54	45	147	2026-10-09 13:43:52	65:d0:bc:74:b0:84	\N	20 MHz	\N
68:ed:c6:68:ab:9b	rosliahmad846@unifi	Hue-Strip	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.156	VillaSri_2.4G	\N	1	\N	1x1	1x1	11n	\N	-61	44	54	2026-10-09 14:37:52	65:d0:bc:74:b0:84	\N	20 MHz	\N
3e:dd:a3:51:76:08	cheahsweel70@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	HarmoniVilla_2.4G	HarmoniVilla_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
11:4c:f1:5e:bb:98	cheahsweel70@unifi	OnePlus-11	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Gateway	2.4 GHz	192.168.0.132	HarmoniVilla_2.4G	HarmoniVilla_5G	1	\N	1x1	4x4	11ac	11ac	-71	789	705	2026-10-07 14:32:52	3e:dd:a3:51:76:08	SKYWORTH	40 MHz	160 MHz
ca:31:f9:f5:1e:be	cheahsweel70@unifi	ca:31:f9:f5:1e:be	TP-Link Technologies Co., Ltd.	TP-Link	STA	Client	2.4 GHz	192.168.0.112	HarmoniVilla_2.4G	HarmoniVilla_5G	11	\N	3x3	2x2	11ac	11ac	-32	140	490	2026-10-11 10:05:52	3e:dd:a3:51:76:08	\N	20 MHz	160 MHz
fa:cc:f8:0d:9f:82	cheahsweel70@unifi	fa:cc:f8:0d:9f:82	Xiaomi Communications Co., Ltd.	Xiaomi	STA	Gateway	2.4 GHz	192.168.0.252	HarmoniVilla_2.4G	HarmoniVilla_5G	6	\N	2x2	4x4	11ax	11ax	-42	757	650	2026-10-10 19:07:52	3e:dd:a3:51:76:08	Android	40 MHz	160 MHz
4a:a4:67:8b:0d:92	cheahsweel70@unifi	Galaxy-A54	Samsung Electronics Co., Ltd.	Samsung	STA	Client	2.4 GHz	192.168.0.48	HarmoniVilla_2.4G	HarmoniVilla_5G	6	\N	2x2	3x3	11ax	11ax	-64	1192	1006	2026-10-10 05:54:52	3e:dd:a3:51:76:08	\N	20 MHz	160 MHz
4b:b3:ed:d5:2e:62	cheahsweel70@unifi	WNC-AP	WNC Corporation	Wnc	STA	Client	5 GHz	192.168.0.74	HarmoniVilla_2.4G	HarmoniVilla_5G	\N	153	3x3	2x2	11n	11n	-41	174	1141	2026-10-11 17:40:52	3e:dd:a3:51:76:08	\N	40 MHz	80 MHz
fb:8f:ca:9c:6a:d2	cheahsweel70@unifi	Fire-TV-Stick	Amazon Technologies Inc.	Amazon	STA	Client	2.4 GHz	192.168.0.228	HarmoniVilla_2.4G	HarmoniVilla_5G	6	\N	2x2	4x4	11n	11n	-82	1194	388	2026-10-11 18:13:52	3e:dd:a3:51:76:08	Windows	40 MHz	160 MHz
66:29:82:5a:3e:7f	cheahsweel70@unifi	Hue-Bridge	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.117	HarmoniVilla_2.4G	\N	6	\N	1x1	1x1	11n	\N	-53	94	124	2026-10-12 01:44:52	3e:dd:a3:51:76:08	\N	20 MHz	\N
b2:cd:4d:fd:93:c3	cheahsweel70@unifi	Hue-Strip	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.178	HarmoniVilla_2.4G	\N	1	\N	1x1	1x1	11n	\N	-48	52	12	2026-10-10 06:44:52	3e:dd:a3:51:76:08	\N	20 MHz	\N
cf:13:e3:14:73:aa	cheahsweel70@unifi	Hue-Strip	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.205	HarmoniVilla_2.4G	\N	11	\N	1x1	1x1	11n	\N	-78	126	26	2026-10-11 21:22:52	3e:dd:a3:51:76:08	\N	20 MHz	\N
59:44:f7:ce:11:b9	arunkrishn86@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	ChandranVilla_2.4G	ChandranVilla_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
20:88:5b:dc:8a:04	arunkrishn86@unifi	SKYWORTH-STB	Shenzhen Skyworth Digital Technology CO.	Skyworth	STA	Repeater	2.4 GHz	192.168.0.194	ChandranVilla_2.4G	ChandranVilla_5G	11	\N	1x1	4x4	11ac	11ac	-63	594	533	2026-10-09 10:42:52	59:44:f7:ce:11:b9	\N	40 MHz	80 MHz
55:bd:77:07:c7:d6	arunkrishn86@unifi	55:bd:77:07:c7:d6	Amazon Technologies Inc.	Amazon	STA	Repeater	2.4 GHz	192.168.0.27	ChandranVilla_2.4G	ChandranVilla_5G	1	\N	3x3	1x1	11ac	11ac	-81	1173	598	2026-10-11 08:38:52	59:44:f7:ce:11:b9	SKYWORTH	40 MHz	80 MHz
ad:13:82:b6:89:0c	arunkrishn86@unifi	TP-Link-Repeater	TP-Link Technologies Co., Ltd.	TP-Link	STA	Gateway	5 GHz	192.168.0.31	ChandranVilla_2.4G	ChandranVilla_5G	\N	40	3x3	4x4	11ax	11ax	-86	1073	568	2026-10-08 21:16:52	59:44:f7:ce:11:b9	\N	20 MHz	80 MHz
9c:6a:06:54:c1:7d	arunkrishn86@unifi	ESP32-Node	Espressif Inc.	Espressif	STA	Repeater	5 GHz	192.168.0.163	ChandranVilla_2.4G	ChandranVilla_5G	\N	149	2x2	4x4	11n	11n	-85	152	566	2026-10-08 03:08:52	59:44:f7:ce:11:b9	\N	40 MHz	160 MHz
41:a4:6c:62:58:b9	arunkrishn86@unifi	Echo-Dot	Amazon Technologies Inc.	Amazon	STA	Gateway	5 GHz	192.168.0.208	ChandranVilla_2.4G	ChandranVilla_5G	\N	153	1x1	4x4	11ax	11ax	-64	97	763	2026-10-07 21:58:52	59:44:f7:ce:11:b9	Android	40 MHz	160 MHz
c8:cf:56:57:13:7f	arunkrishn86@unifi	c8:cf:56:57:13:7f	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Gateway	2.4 GHz	192.168.0.179	ChandranVilla_2.4G	ChandranVilla_5G	11	\N	4x4	1x1	11ax	11ax	-82	897	385	2026-10-11 23:11:52	59:44:f7:ce:11:b9	\N	20 MHz	80 MHz
2b:01:d1:26:4d:fe	farahnabil856@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	VillaSri_2.4G	VillaSri_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
75:b7:03:62:56:b5	farahnabil856@unifi	75:b7:03:62:56:b5	Amazon Technologies Inc.	Amazon	STA	Client	5 GHz	192.168.0.121	VillaSri_2.4G	VillaSri_5G	\N	48	3x3	4x4	11ax	11ax	-75	288	142	2026-10-07 19:38:52	2b:01:d1:26:4d:fe	\N	20 MHz	80 MHz
48:49:db:05:da:3d	farahnabil856@unifi	realme-Note-50	Realme Chongqing Mobile Telecommunications Corp.	Realme	STA	Client	2.4 GHz	192.168.0.186	VillaSri_2.4G	VillaSri_5G	1	\N	1x1	4x4	11ax	11ax	-35	284	482	2026-10-09 05:54:52	2b:01:d1:26:4d:fe	Android	40 MHz	80 MHz
9c:d5:8d:18:ef:87	farahnabil856@unifi	Nest-Hub	Google LLC	Google	STA	Gateway	5 GHz	192.168.0.139	VillaSri_2.4G	VillaSri_5G	\N	48	4x4	4x4	11n	11n	-70	1190	211	2026-10-09 07:09:52	2b:01:d1:26:4d:fe	Android	40 MHz	160 MHz
15:42:e8:ae:6a:10	farahnabil856@unifi	OnePlus-11	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Repeater	2.4 GHz	192.168.0.213	VillaSri_2.4G	VillaSri_5G	11	\N	4x4	2x2	11n	11n	-31	11	685	2026-10-09 08:49:52	2b:01:d1:26:4d:fe	Linux	20 MHz	160 MHz
c0:1f:c7:41:a6:6c	farahnabil856@unifi	c0:1f:c7:41:a6:6c	Google LLC	Google	STA	Repeater	5 GHz	192.168.0.16	VillaSri_2.4G	VillaSri_5G	\N	36	1x1	3x3	11ax	11ax	-52	279	768	2026-10-09 14:59:52	2b:01:d1:26:4d:fe	Windows	20 MHz	160 MHz
48:ab:31:d1:08:f9	farahnabil856@unifi	realme-Note-50	Realme Chongqing Mobile Telecommunications Corp.	Realme	STA	Client	2.4 GHz	192.168.0.176	VillaSri_2.4G	VillaSri_5G	1	\N	2x2	1x1	11ac	11ac	-83	629	189	2026-10-10 06:36:52	2b:01:d1:26:4d:fe	Android	20 MHz	80 MHz
f4:cc:8e:14:07:a9	farahnabil856@unifi	Shelly-Plus-1PM	Allterco Robotics EOOD	Shelly	STA	IoT	2.4 GHz	192.168.0.158	VillaSri_2.4G	\N	11	\N	1x1	1x1	11n	\N	-40	67	107	2026-10-06 02:07:52	2b:01:d1:26:4d:fe	\N	20 MHz	\N
bf:65:77:cb:f4:b6	farahnabil856@unifi	Hue-Strip	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.217	VillaSri_2.4G	\N	1	\N	1x1	1x1	11n	\N	-52	54	95	2026-10-07 05:08:52	2b:01:d1:26:4d:fe	\N	20 MHz	\N
50:e9:13:4e:58:89	chongkahfa371@unifi	Root	Fiberhome Telecommunication Technologies Co., Ltd.	FiberHome	Root	Access Point	Ethernet	192.168.0.1	HarmoniVilla_2.4G	HarmoniVilla_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	FIBERHOME	40 MHz	160 MHz
82:20:80:ed:57:67	chongkahfa371@unifi	Mi-11X	Xiaomi Communications Co., Ltd.	Xiaomi	STA	Repeater	5 GHz	192.168.0.189	HarmoniVilla_2.4G	HarmoniVilla_5G	\N	44	3x3	3x3	11ax	11ax	-36	119	473	2026-10-10 15:14:52	50:e9:13:4e:58:89	\N	40 MHz	160 MHz
57:0e:6f:24:1d:df	chongkahfa371@unifi	Intel-WiFi	Intel Corporate	Intel	STA	Client	5 GHz	192.168.0.244	HarmoniVilla_2.4G	HarmoniVilla_5G	\N	161	2x2	4x4	11ac	11ac	-53	735	182	2026-10-07 18:31:52	50:e9:13:4e:58:89	\N	40 MHz	160 MHz
49:5e:f1:e0:0b:20	chongkahfa371@unifi	Nest-Hub	Google LLC	Google	STA	Client	2.4 GHz	192.168.0.135	HarmoniVilla_2.4G	HarmoniVilla_5G	6	\N	3x3	4x4	11ac	11ac	-82	120	467	2026-10-08 13:00:52	50:e9:13:4e:58:89	\N	20 MHz	160 MHz
8d:50:e0:45:c4:69	chongkahfa371@unifi	TL-WA854RE	TP-Link Technologies Co., Ltd.	TP-Link	STA	Gateway	5 GHz	192.168.0.18	HarmoniVilla_2.4G	HarmoniVilla_5G	\N	161	3x3	2x2	11n	11n	-44	740	262	2026-10-09 09:59:52	50:e9:13:4e:58:89	iOS	20 MHz	80 MHz
32:d0:1b:1a:80:23	chongkahfa371@unifi	WNC-AP	WNC Corporation	Wnc	STA	Repeater	2.4 GHz	192.168.0.134	HarmoniVilla_2.4G	HarmoniVilla_5G	1	\N	1x1	2x2	11ax	11ax	-37	898	55	2026-10-08 13:04:52	50:e9:13:4e:58:89	Linux	20 MHz	160 MHz
b3:0e:a0:cc:23:67	chongkahfa371@unifi	Orbi-RBS350	Netgear Inc.	Netgear	STA	Access Point	5 GHz	192.168.0.164	HarmoniVilla_2.4G	HarmoniVilla_5G	\N	161	2x2	4x4	11ax	11ax	-49	730	982	2026-10-11 08:50:52	50:e9:13:4e:58:89	\N	40 MHz	160 MHz
0c:9c:2d:cf:8f:5d	kennethloh698@unifi	Root	ZTE Corporation	ZTE	Root	Access Point	Ethernet	192.168.0.1	ArandaHome_2.4G	ArandaHome_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	ZTE	40 MHz	160 MHz
37:f2:b4:83:c1:ce	kennethloh698@unifi	37:f2:b4:83:c1:ce	Intel Corporate	Intel	STA	Gateway	5 GHz	192.168.0.140	ArandaHome_2.4G	ArandaHome_5G	\N	157	2x2	4x4	11ax	11ax	-34	1060	15	2026-10-11 13:02:52	0c:9c:2d:cf:8f:5d	Android	20 MHz	160 MHz
fd:dd:3b:58:c9:a3	kennethloh698@unifi	OnePlus-Nord	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Gateway	2.4 GHz	192.168.0.74	ArandaHome_2.4G	ArandaHome_5G	1	\N	4x4	2x2	11ac	11ac	-39	897	1007	2026-10-08 07:53:52	0c:9c:2d:cf:8f:5d	\N	20 MHz	80 MHz
9b:1a:1f:6f:69:c7	kennethloh698@unifi	realme-Note-50	Realme Chongqing Mobile Telecommunications Corp.	Realme	STA	Repeater	5 GHz	192.168.0.89	ArandaHome_2.4G	ArandaHome_5G	\N	44	3x3	1x1	11n	11n	-63	1088	431	2026-10-10 15:01:52	0c:9c:2d:cf:8f:5d	Android	20 MHz	80 MHz
97:94:89:d0:ac:a0	kennethloh698@unifi	iPhone-13	Apple, Inc.	Apple	STA	Client	2.4 GHz	192.168.0.110	ArandaHome_2.4G	ArandaHome_5G	11	\N	2x2	4x4	11ac	11ac	-56	413	893	2026-10-09 04:13:52	0c:9c:2d:cf:8f:5d	SKYWORTH	40 MHz	80 MHz
50:1a:6a:e9:96:23	kennethloh698@unifi	SKYWORTH-STB	Shenzhen Skyworth Digital Technology CO.	Skyworth	STA	Gateway	5 GHz	192.168.0.216	ArandaHome_2.4G	ArandaHome_5G	\N	157	3x3	2x2	11ax	11ax	-30	552	992	2026-10-09 13:43:52	0c:9c:2d:cf:8f:5d	Windows	40 MHz	80 MHz
30:dc:a1:71:38:a7	kennethloh698@unifi	Nest-Wifi-Router	Google LLC	Google	STA	Access Point	Ethernet	192.168.0.196	ArandaHome_2.4G	ArandaHome_5G	\N	\N	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 06:29:52	0c:9c:2d:cf:8f:5d	\N	\N	\N
06:38:5d:2e:e7:41	kennethloh698@unifi	decoMeshX60	TP-Link Systems Inc.	Tp Link	STA	Access Point	Ethernet	192.168.0.52	ArandaHome_2.4G	ArandaHome_5G	\N	\N	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-11 19:42:52	0c:9c:2d:cf:8f:5d	\N	\N	\N
cf:73:6d:7e:e4:82	arunkrishn716@unifi	Root	Fiberhome Telecommunication Technologies Co., Ltd.	FiberHome	Root	Access Point	Ethernet	192.168.0.1	BayuHome_2.4G	BayuHome_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	FIBERHOME	40 MHz	160 MHz
9e:ae:88:39:a5:e1	arunkrishn716@unifi	WNC-AP	WNC Corporation	Wnc	STA	Gateway	2.4 GHz	192.168.0.91	BayuHome_2.4G	BayuHome_5G	6	\N	1x1	2x2	11n	11n	-62	855	452	2026-10-11 20:29:52	cf:73:6d:7e:e4:82	iOS	40 MHz	160 MHz
3b:d7:ea:15:2b:2e	arunkrishn716@unifi	ESP32-Node	Espressif Inc.	Espressif	STA	Repeater	2.4 GHz	192.168.0.197	BayuHome_2.4G	BayuHome_5G	11	\N	3x3	2x2	11ax	11ax	-33	267	680	2026-10-11 13:27:52	cf:73:6d:7e:e4:82	iOS	40 MHz	80 MHz
7b:c0:85:6c:62:23	arunkrishn716@unifi	OnePlus-Nord	OnePlus Technology (Shenzhen) Co., Ltd.	OnePlus	STA	Repeater	2.4 GHz	192.168.0.87	BayuHome_2.4G	BayuHome_5G	1	\N	2x2	4x4	11ax	11ax	-80	780	1008	2026-10-08 05:46:52	cf:73:6d:7e:e4:82	\N	20 MHz	80 MHz
12:96:a8:cd:7d:9d	arunkrishn716@unifi	Galaxy-A54	Samsung Electronics Co., Ltd.	Samsung	STA	Gateway	5 GHz	192.168.0.104	BayuHome_2.4G	BayuHome_5G	\N	36	1x1	2x2	11ac	11ac	-39	297	417	2026-10-08 09:14:52	cf:73:6d:7e:e4:82	\N	20 MHz	160 MHz
fb:54:f3:80:f2:53	arunkrishn716@unifi	Orbi-RBK852	Netgear Inc.	Netgear	STA	Access Point	5 GHz	192.168.0.38	BayuHome_2.4G	BayuHome_5G	\N	149	2x2	2x2	11ax	11ax	-52	236	640	2026-10-11 04:06:52	cf:73:6d:7e:e4:82	\N	40 MHz	160 MHz
6a:78:f0:19:ff:fc	arunkrishn716@unifi	ESP32-CAM	Espressif Inc.	Espressif	STA	IoT	2.4 GHz	192.168.0.97	BayuHome_2.4G	\N	11	\N	1x1	1x1	11n	\N	-80	83	27	2026-10-06 00:29:52	cf:73:6d:7e:e4:82	\N	20 MHz	\N
a3:8a:15:4d:37:41	arunkrishn716@unifi	Hue-Bulb	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.32	BayuHome_2.4G	\N	11	\N	1x1	1x1	11n	\N	-43	84	40	2026-10-10 10:02:52	cf:73:6d:7e:e4:82	\N	20 MHz	\N
a8:94:67:09:ae:5e	arunkrishn716@unifi	espressif	Espressif Inc.	Espressif	STA	IoT	2.4 GHz	192.168.0.45	BayuHome_2.4G	\N	11	\N	1x1	1x1	11n	\N	-60	36	16	2026-10-11 06:20:52	cf:73:6d:7e:e4:82	\N	20 MHz	\N
97:19:16:1b:fc:73	gohsoonhua731@unifi	Root	ZTE Corporation	ZTE	Root	Access Point	Ethernet	192.168.0.1	BayuHome_2.4G	BayuHome_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	ZTE	40 MHz	160 MHz
1c:1b:0e:39:56:26	gohsoonhua731@unifi	Fire-TV-Stick	Amazon Technologies Inc.	Amazon	STA	Repeater	2.4 GHz	192.168.0.149	BayuHome_2.4G	BayuHome_5G	6	\N	1x1	4x4	11ax	11ax	-56	1129	465	2026-10-11 13:03:52	97:19:16:1b:fc:73	\N	20 MHz	80 MHz
53:46:4a:49:de:a2	gohsoonhua731@unifi	WNC-AP	WNC Corporation	Wnc	STA	Client	2.4 GHz	192.168.0.23	BayuHome_2.4G	BayuHome_5G	11	\N	1x1	3x3	11n	11n	-49	148	752	2026-10-08 11:41:52	97:19:16:1b:fc:73	Linux	40 MHz	80 MHz
56:f3:c4:ab:8b:71	gohsoonhua731@unifi	ESP32-Node	Espressif Inc.	Espressif	STA	Repeater	5 GHz	192.168.0.75	BayuHome_2.4G	BayuHome_5G	\N	149	2x2	1x1	11ax	11ax	-52	1123	904	2026-10-07 22:36:52	97:19:16:1b:fc:73	Windows	20 MHz	160 MHz
3e:7b:25:7a:80:fb	gohsoonhua731@unifi	iPhone-13	Apple, Inc.	Apple	STA	Client	5 GHz	192.168.0.192	BayuHome_2.4G	BayuHome_5G	\N	161	3x3	4x4	11ac	11ac	-72	630	689	2026-10-11 22:42:52	97:19:16:1b:fc:73	\N	40 MHz	80 MHz
2d:0d:4a:8b:fd:87	gohsoonhua731@unifi	OPPO-Reno8	BBK Electronics Corp., Ltd.	Oppo	STA	Client	5 GHz	192.168.0.76	BayuHome_2.4G	BayuHome_5G	\N	48	2x2	2x2	11ax	11ax	-79	398	277	2026-10-11 16:08:52	97:19:16:1b:fc:73	SKYWORTH	40 MHz	80 MHz
54:0a:69:f5:51:0c	gohsoonhua731@unifi	iPad-Air	Apple, Inc.	Apple	STA	Repeater	5 GHz	192.168.0.19	BayuHome_2.4G	BayuHome_5G	\N	48	1x1	3x3	11n	11n	-85	222	307	2026-10-11 21:56:52	97:19:16:1b:fc:73	SKYWORTH	20 MHz	160 MHz
1a:dd:91:62:d6:3c	chongkahfa498@unifi	Root	ZTE Corporation	ZTE	Root	Access Point	Ethernet	192.168.0.1	TamanAman_2.4G	TamanAman_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	ZTE	40 MHz	160 MHz
b8:7c:68:3f:b3:bf	chongkahfa498@unifi	WNC-Client	WNC Corporation	Wnc	STA	Repeater	5 GHz	192.168.0.102	TamanAman_2.4G	TamanAman_5G	\N	36	4x4	2x2	11ax	11ax	-36	969	272	2026-10-10 03:10:52	1a:dd:91:62:d6:3c	Windows	40 MHz	160 MHz
0a:9e:02:69:06:41	chongkahfa498@unifi	TL-WA854RE	TP-Link Technologies Co., Ltd.	TP-Link	STA	Gateway	5 GHz	192.168.0.98	TamanAman_2.4G	TamanAman_5G	\N	36	2x2	1x1	11n	11n	-79	1144	306	2026-10-10 21:35:52	1a:dd:91:62:d6:3c	Windows	40 MHz	80 MHz
55:76:60:9c:db:f6	chongkahfa498@unifi	55:76:60:9c:db:f6	Apple, Inc.	Apple	STA	Gateway	5 GHz	192.168.0.190	TamanAman_2.4G	TamanAman_5G	\N	48	4x4	1x1	11n	11n	-34	125	978	2026-10-09 14:22:52	1a:dd:91:62:d6:3c	\N	20 MHz	80 MHz
5b:06:9a:34:11:71	kumaransiv303@unifi	Root	Fiberhome Telecommunication Technologies Co., Ltd.	FiberHome	Root	Access Point	Ethernet	192.168.0.1	TamanAman_2.4G	TamanAman_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	FIBERHOME	40 MHz	160 MHz
b2:5c:22:3e:e5:ef	kumaransiv303@unifi	Pixel-7	Google LLC	Google	STA	Repeater	2.4 GHz	192.168.0.119	TamanAman_2.4G	TamanAman_5G	11	\N	1x1	4x4	11ax	11ax	-72	511	14	2026-10-09 02:10:52	5b:06:9a:34:11:71	\N	40 MHz	160 MHz
e2:40:e8:a7:f0:a0	kumaransiv303@unifi	SKYWORTH-STB	Shenzhen Skyworth Digital Technology CO.	Skyworth	STA	Gateway	5 GHz	192.168.0.148	TamanAman_2.4G	TamanAman_5G	\N	161	4x4	2x2	11ax	11ax	-30	1153	1194	2026-10-08 01:19:52	5b:06:9a:34:11:71	iOS	20 MHz	160 MHz
c8:b4:fc:01:c3:ef	kumaransiv303@unifi	iPad-Air	Apple, Inc.	Apple	STA	Gateway	5 GHz	192.168.0.189	TamanAman_2.4G	TamanAman_5G	\N	153	1x1	4x4	11ac	11ac	-37	395	639	2026-10-11 05:56:52	5b:06:9a:34:11:71	iOS	20 MHz	160 MHz
5a:c3:74:8e:5b:60	kumaransiv303@unifi	ESP32-CAM	Espressif Inc.	Espressif	STA	IoT	2.4 GHz	192.168.0.223	TamanAman_2.4G	\N	11	\N	1x1	1x1	11n	\N	-73	12	51	2026-10-10 22:48:52	5b:06:9a:34:11:71	\N	20 MHz	\N
ca:d6:46:bf:ac:2c	kumaransiv303@unifi	Hue-Strip	Signify Netherlands B.V.	Philips	STA	IoT	2.4 GHz	192.168.0.178	TamanAman_2.4G	\N	11	\N	1x1	1x1	11n	\N	-43	23	12	2026-10-06 15:33:52	5b:06:9a:34:11:71	\N	20 MHz	\N
26:d5:b0:d1:26:ef	kumaransiv303@unifi	Shelly-Plus-1PM	Allterco Robotics EOOD	Shelly	STA	IoT	2.4 GHz	192.168.0.59	TamanAman_2.4G	\N	1	\N	1x1	1x1	11n	\N	-79	10	71	2026-10-09 17:03:52	5b:06:9a:34:11:71	\N	20 MHz	\N
54:a0:c1:30:35:43	rajeshmuru762@unifi	Root	ZTE Corporation	ZTE	Root	Access Point	Ethernet	192.168.0.1	HarmoniVilla_2.4G	HarmoniVilla_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	ZTE	40 MHz	160 MHz
9d:3c:22:25:6e:49	rajeshmuru762@unifi	ESP32-Node	Espressif Inc.	Espressif	STA	Gateway	2.4 GHz	192.168.0.248	HarmoniVilla_2.4G	HarmoniVilla_5G	11	\N	4x4	3x3	11ac	11ac	-31	861	206	2026-10-08 09:08:52	54:a0:c1:30:35:43	Linux	40 MHz	160 MHz
d6:5d:32:07:11:6f	rajeshmuru762@unifi	iPhone-15	Apple, Inc.	Apple	STA	Gateway	5 GHz	192.168.0.39	HarmoniVilla_2.4G	HarmoniVilla_5G	\N	153	2x2	1x1	11ac	11ac	-60	288	905	2026-10-11 04:11:52	54:a0:c1:30:35:43	\N	40 MHz	160 MHz
71:45:a7:3d:b3:b8	rajeshmuru762@unifi	ESP8266-Sensor	Espressif Inc.	Espressif	STA	IoT	2.4 GHz	192.168.0.143	HarmoniVilla_2.4G	\N	6	\N	1x1	1x1	11n	\N	-45	85	24	2026-10-10 01:32:52	54:a0:c1:30:35:43	\N	20 MHz	\N
cf:b8:e6:ea:d6:76	rajeshmuru762@unifi	Shelly-Plus-1PM	Allterco Robotics EOOD	Shelly	STA	IoT	2.4 GHz	192.168.0.216	HarmoniVilla_2.4G	\N	11	\N	1x1	1x1	11n	\N	-70	132	136	2026-10-08 01:41:52	54:a0:c1:30:35:43	\N	20 MHz	\N
ff:1b:60:8e:68:90	sitizaleha49@unifi	Root	ZTE Corporation	ZTE	Root	Access Point	Ethernet	192.168.0.1	ChandranVilla_2.4G	ChandranVilla_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	ZTE	40 MHz	160 MHz
7f:73:08:67:f3:31	sitizaleha49@unifi	7f:73:08:67:f3:31	Espressif Inc.	Espressif	STA	Repeater	5 GHz	192.168.0.56	ChandranVilla_2.4G	ChandranVilla_5G	\N	40	4x4	3x3	11ac	11ac	-57	604	950	2026-10-11 08:30:52	ff:1b:60:8e:68:90	iOS	20 MHz	160 MHz
21:3e:df:73:40:6b	sitizaleha49@unifi	ESP8266-Sensor	Espressif Inc.	Espressif	STA	Repeater	2.4 GHz	192.168.0.204	ChandranVilla_2.4G	ChandranVilla_5G	1	\N	3x3	2x2	11ax	11ax	-87	833	372	2026-10-08 02:13:52	ff:1b:60:8e:68:90	SKYWORTH	40 MHz	80 MHz
0f:b2:c0:5f:5c:e0	sitizaleha49@unifi	iPhone-13	Apple, Inc.	Apple	STA	Repeater	5 GHz	192.168.0.173	ChandranVilla_2.4G	ChandranVilla_5G	\N	161	1x1	1x1	11ax	11ax	-43	935	398	2026-10-09 14:52:52	ff:1b:60:8e:68:90	Windows	20 MHz	80 MHz
1f:a0:cd:38:8a:62	sitizaleha49@unifi	1f:a0:cd:38:8a:62	Shenzhen Skyworth Digital Technology CO.	Skyworth	STA	Repeater	2.4 GHz	192.168.0.25	ChandranVilla_2.4G	ChandranVilla_5G	6	\N	3x3	3x3	11ax	11ax	-76	728	782	2026-10-09 08:39:52	ff:1b:60:8e:68:90	iOS	40 MHz	80 MHz
64:4a:02:7f:39:6c	sitizaleha49@unifi	POCO-M5	Xiaomi Communications Co., Ltd.	Xiaomi	STA	Client	5 GHz	192.168.0.252	ChandranVilla_2.4G	ChandranVilla_5G	\N	40	4x4	3x3	11ac	11ac	-35	1104	679	2026-10-11 16:06:52	ff:1b:60:8e:68:90	SKYWORTH	40 MHz	160 MHz
21:72:bb:bb:e7:cb	kumaransiv245@unifi	Root	Fiberhome Telecommunication Technologies Co., Ltd.	FiberHome	Root	Access Point	Ethernet	192.168.0.1	SeriMawar_2.4G	SeriMawar_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	FIBERHOME	40 MHz	160 MHz
16:c0:8b:2a:38:39	kumaransiv245@unifi	OPPO-A78	BBK Electronics Corp., Ltd.	Oppo	STA	Repeater	2.4 GHz	192.168.0.159	SeriMawar_2.4G	SeriMawar_5G	1	\N	2x2	2x2	11n	11n	-52	91	1008	2026-10-10 07:34:52	21:72:bb:bb:e7:cb	Linux	40 MHz	80 MHz
f6:da:30:e1:e9:24	kumaransiv245@unifi	Fire-TV-Stick	Amazon Technologies Inc.	Amazon	STA	Gateway	2.4 GHz	192.168.0.155	SeriMawar_2.4G	SeriMawar_5G	6	\N	2x2	4x4	11n	11n	-31	430	1030	2026-10-07 11:17:52	21:72:bb:bb:e7:cb	iOS	20 MHz	160 MHz
4f:08:eb:b6:7d:ef	kumaransiv245@unifi	Nest-Wifi-Pro	Google LLC	Google	STA	Access Point	Ethernet	192.168.0.195	SeriMawar_2.4G	SeriMawar_5G	\N	\N	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-11 17:04:52	21:72:bb:bb:e7:cb	\N	\N	\N
71:c1:85:61:da:27	cheahsweel339@unifi	Root	ZTE Corporation	ZTE	Root	Access Point	Ethernet	192.168.0.1	BayuHome_2.4G	BayuHome_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	ZTE	40 MHz	160 MHz
70:3e:22:75:41:be	cheahsweel339@unifi	70:3e:22:75:41:be	vivo Mobile Communication Co., Ltd.	Vivo	STA	Client	5 GHz	192.168.0.111	BayuHome_2.4G	BayuHome_5G	\N	149	2x2	1x1	11ax	11ax	-73	1030	1071	2026-10-08 02:38:52	71:c1:85:61:da:27	\N	40 MHz	160 MHz
20:6a:57:d9:6f:7a	cheahsweel339@unifi	Chromecast	Google LLC	Google	STA	Repeater	5 GHz	192.168.0.246	BayuHome_2.4G	BayuHome_5G	\N	40	3x3	3x3	11ac	11ac	-43	141	181	2026-10-09 19:17:52	71:c1:85:61:da:27	Linux	20 MHz	80 MHz
90:00:8a:80:17:da	arunkrishn480@unifi	Root	Shenzhen Skyworth Digital Technology CO.	Skyworth	Root	Access Point	Ethernet	192.168.0.1	DamaiResidensi_2.4G	DamaiResidensi_5G	11	44	2x2	2x2	11ax	11ax	\N	\N	\N	2026-10-12 09:51:52	ff:ff:ff:ff:ff:ff	SKYWORTH	40 MHz	160 MHz
78:8c:74:a6:2f:aa	arunkrishn480@unifi	78:8c:74:a6:2f:aa	Intel Corporate	Intel	STA	Client	5 GHz	192.168.0.13	DamaiResidensi_2.4G	DamaiResidensi_5G	\N	44	2x2	3x3	11ax	11ax	-61	1197	816	2026-10-08 17:54:52	90:00:8a:80:17:da	Linux	40 MHz	160 MHz
5f:bb:6a:a3:10:94	arunkrishn480@unifi	realme-Note-50	Realme Chongqing Mobile Telecommunications Corp.	Realme	STA	Repeater	5 GHz	192.168.0.192	DamaiResidensi_2.4G	DamaiResidensi_5G	\N	161	3x3	2x2	11ac	11ac	-85	1061	904	2026-10-10 22:11:52	90:00:8a:80:17:da	\N	20 MHz	80 MHz
\.


--
-- Data for Name: routers; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.routers (serial_number, login_id, manufacturer, model, cpu_usage_pct, cpu_temperature_c, memory_usage_pct, monthly_usage_gb, rx_power_dbm) FROM stdin;
CWTCB90BE9D3	ticksew19@unifi	SKYWORTH	AX3000	44	45	56	312.4	-22.6
CWTA03606DE5	azlinamohd444@unifi	SKYWORTH	AX3000	48	44	24	700.6	-18.3
CWT29E25B43E	muhammadda300@unifi	FIBERHOME	AX3000	49	42	24	1384.4	-30.2
CWT4348594C0	tanticksew53@unifi	FIBERHOME	AX3000	88	55	31	531.9	-18.2
CWTB9FEB3102	kennethloh334@unifi	FIBERHOME	AX3000	37	35	60	1158.9	-19.9
CWT0AE37744D	hasnahsall843@unifi	SKYWORTH	AX3000	40	50	47	1030.6	-28.6
CWT3A6ECCF07	chongkahfa740@unifi	SKYWORTH	AX1800	88	48	76	1800.9	-22.8
CWT8F88F572A	arunkrishn780@unifi	SKYWORTH	AX3000	35	42	37	404.2	-32.8
CWTB432A8C55	zainalabid371@unifi	ZTE	AX3000	35	35	55	1465.6	-22.4
CWT8541C145E	divyarajen754@unifi	SKYWORTH	AX3000	32	36	41	1177.8	-21.1
CWT993C798D6	mohdrizalo944@unifi	SKYWORTH	AX3000	30	52	76	1773.1	-16.2
CWTE290C56CD	leechinhua764@unifi	SKYWORTH	AX1800	34	39	42	606.0	-18.8
CWTDCE816A17	limweiming953@unifi	SKYWORTH	AX3000	29	46	67	178.4	-20.5
CWT6C4BE5762	gohsoonhua435@unifi	SKYWORTH	AX3000	88	35	29	1445.3	-19.1
CWTA40752BC1	norhayatio609@unifi	SKYWORTH	AX1800	44	53	74	1591.2	-21.9
CWT3585E7356	leechinhua381@unifi	SKYWORTH	AX1800	37	53	69	971.9	-19.4
CWT43A38330F	gohsoonhua109@unifi	ZTE	AX1800	31	53	21	1306.6	-22.6
CWTD733CB990	divyarajen16@unifi	ZTE	AX3000	44	74	31	698.1	-21.1
CWTE10FCD0D2	vigneshsub201@unifi	ZTE	AX3000	27	39	41	1060.1	-22.3
CWTB6E0E76FF	divyarajen359@unifi	SKYWORTH	AX1800	41	38	32	449.0	-17.5
CWTB5D251056	wongmeilin430@unifi	FIBERHOME	AX3000	79	43	62	1883.1	-29.5
CWTF9A36FE0F	chongkahfa258@unifi	SKYWORTH	AX3000	45	42	81	1608.9	-20.3
CWTBDBB566C4	nuraisyahh315@unifi	SKYWORTH	AX3000	28	50	79	1577.6	-22.2
CWTDF681C53D	gohsoonhua794@unifi	SKYWORTH	AX3000	35	43	38	867.1	-18.6
CWT97C5E6290	zainalabid756@unifi	ZTE	AX1800	37	47	44	1841.6	-17.9
CWTFAA399675	teohbeecho755@unifi	FIBERHOME	AX3000	51	79	77	720.4	-21.2
CWT43870DA79	kennethloh149@unifi	SKYWORTH	AX3000	38	43	81	1388.3	-21.2
CWT6F4DE8A37	divyarajen791@unifi	FIBERHOME	AX3000	49	55	54	1432.2	-17.7
CWT357740FA7	yapkeansen529@unifi	SKYWORTH	AX3000	81	40	21	939.7	-31.2
CWTD80C09598	arunkrishn436@unifi	FIBERHOME	AX3000	36	48	28	534.1	-18.2
CWT974CB9E25	azlinamohd728@unifi	FIBERHOME	AX1800	30	45	31	1082.5	-28.7
CWT075A05301	rajeshmuru987@unifi	FIBERHOME	AX1800	68	54	62	1686.0	-18.1
CWTEB26BD614	kennethloh57@unifi	SKYWORTH	AX1800	73	55	32	1470.4	-22.9
CWTC1F84060E	rajeshmuru498@unifi	SKYWORTH	AX3000	32	66	33	1201.3	-18.4
CWTDD17C3056	sitizaleha592@unifi	ZTE	AX3000	68	46	41	1769.0	-21.9
CWTF59E0A3CD	leechinhua468@unifi	ZTE	AX3000	35	53	81	1118.8	-18.5
CWTF2D5B464D	arunkrishn822@unifi	SKYWORTH	AX1800	31	41	39	1363.0	-19.5
CWT456F01D70	teohbeecho43@unifi	ZTE	AX3000	40	53	34	309.9	-18.4
CWT0A8DCD069	mohamadhaf651@unifi	SKYWORTH	AX3000	29	48	45	407.3	-21.6
CWT335A5CE32	muhammadda162@unifi	SKYWORTH	AX1800	50	49	88	895.8	-30.3
CWTDE1199FAC	rosliahmad669@unifi	ZTE	AX3000	27	42	67	1736.4	-20.5
CWT1CE019935	mohamadhaf31@unifi	SKYWORTH	AX3000	46	43	83	1994.8	-22.3
CWT6BC106633	tanchweeme791@unifi	FIBERHOME	AX3000	39	47	38	667.6	-22.4
CWTDA8E1982F	gohsoonhua194@unifi	FIBERHOME	AX3000	43	52	36	306.7	-16.8
CWTA9E91839B	tanchweeme843@unifi	SKYWORTH	AX3000	36	33	42	1409.9	-32.2
CWT1007E603F	rajeshmuru682@unifi	SKYWORTH	AX3000	94	37	85	1646.0	-21.5
CWT382A333A8	priyasamy35@unifi	SKYWORTH	AX3000	75	36	30	891.6	-29.7
CWTDFF7886B9	saifulazma630@unifi	ZTE	AX1800	88	40	31	244.3	-20.0
CWT408871878	saifulazma901@unifi	SKYWORTH	AX3000	38	79	33	1915.4	-17.6
CWT612B82134	rosliahmad948@unifi	SKYWORTH	AX3000	69	34	69	54.9	-21.4
CWT5829ADB15	zainalabid85@unifi	FIBERHOME	AX3000	48	35	31	1266.3	-16.3
CWT04D004E8E	tanticksew84@unifi	FIBERHOME	AX3000	41	74	45	729.2	-16.1
CWT9D137F64E	wongmeilin187@unifi	ZTE	AX3000	39	43	29	889.0	-18.2
CWT309895BDA	rosliahmad846@unifi	SKYWORTH	AX3000	42	45	24	483.2	-19.5
CWT27181B83B	cheahsweel70@unifi	SKYWORTH	AX3000	54	31	26	861.6	-19.7
CWT62C8D9EAC	arunkrishn86@unifi	SKYWORTH	AX3000	50	37	83	1824.8	-21.7
CWT6C1EFC676	farahnabil856@unifi	SKYWORTH	AX1800	41	31	57	147.4	-22.8
CWT9B7309A39	chongkahfa371@unifi	FIBERHOME	AX3000	66	39	21	1124.5	-17.8
CWT755F39EAD	kennethloh698@unifi	ZTE	AX3000	46	66	63	33.9	-17.4
CWT0848AF101	arunkrishn716@unifi	FIBERHOME	AX1800	74	67	48	1128.7	-22.6
CWTD8DD845ED	gohsoonhua731@unifi	ZTE	AX3000	44	50	36	1422.5	-19.2
CWT858162DA1	chongkahfa498@unifi	ZTE	AX3000	28	39	50	803.5	-21.4
CWT23168C023	kumaransiv303@unifi	FIBERHOME	AX1800	51	78	73	1650.6	-19.6
CWTDBF4223BF	rajeshmuru762@unifi	ZTE	AX3000	48	53	34	866.0	-18.2
CWT3DE926853	sitizaleha49@unifi	ZTE	AX1800	36	36	80	1013.7	-18.6
CWT7693F0353	kumaransiv245@unifi	FIBERHOME	AX3000	31	46	44	741.1	-16.4
CWTEF23DF890	cheahsweel339@unifi	ZTE	AX3000	70	39	38	1295.5	-34.0
CWT748F2086D	arunkrishn480@unifi	SKYWORTH	AX3000	42	42	65	1107.6	-18.4
\.


--
-- Name: customer_summaries customer_summaries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_summaries
    ADD CONSTRAINT customer_summaries_pkey PRIMARY KEY (login_id);


--
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (login_id);


--
-- Name: devices devices_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_pkey PRIMARY KEY (mac_address);


--
-- Name: routers routers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.routers
    ADD CONSTRAINT routers_pkey PRIMARY KEY (serial_number);


--
-- Name: idx_devices_login_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_devices_login_id ON public.devices USING btree (login_id);


--
-- Name: idx_routers_login_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_routers_login_id ON public.routers USING btree (login_id);


--
-- Name: customer_summaries customer_summaries_login_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_summaries
    ADD CONSTRAINT customer_summaries_login_id_fkey FOREIGN KEY (login_id) REFERENCES public.customers(login_id) ON DELETE CASCADE;


--
-- Name: devices devices_login_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_login_id_fkey FOREIGN KEY (login_id) REFERENCES public.customers(login_id) ON DELETE CASCADE;


--
-- Name: routers routers_login_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.routers
    ADD CONSTRAINT routers_login_id_fkey FOREIGN KEY (login_id) REFERENCES public.customers(login_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict kCX6EWnmISkzZtUpIW9H63wOvn0sDcoZBdyx3QaOmv3dK2cZ71sZqwiLRo4lNCN

