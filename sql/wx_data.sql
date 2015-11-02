--
-- PostgreSQL database dump
--

-- Dumped from database version 9.1.9
-- Dumped by pg_dump version 9.2.2
-- Started on 2013-06-13 17:57:26 CDT

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 179 (class 3079 OID 11677)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2999 (class 0 OID 0)
-- Dependencies: 179
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- TOC entry 178 (class 3079 OID 18721)
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- TOC entry 3000 (class 0 OID 0)
-- Dependencies: 178
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


--
-- TOC entry 181 (class 3079 OID 17537)
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- TOC entry 3001 (class 0 OID 0)
-- Dependencies: 181
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


--
-- TOC entry 180 (class 3079 OID 18710)
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- TOC entry 3002 (class 0 OID 0)
-- Dependencies: 180
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 163 (class 1259 OID 16386)
-- Name: airports; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE airports (
    airport_id character(16) NOT NULL,
    name character varying(128),
    elevation real,
    continent character(2),
    region character(8),
    country character(2),
    location geography(Point,4326) NOT NULL
);


ALTER TABLE public.airports OWNER TO postgres;

--
-- TOC entry 177 (class 1259 OID 18680)
-- Name: events; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE events (
    event_id uuid NOT NULL,
    "time" timestamp without time zone NOT NULL,
    location geography NOT NULL,
    raw_text text NOT NULL,
    airport_id character(4),
    location_hash character(32)
);


ALTER TABLE public.events OWNER TO postgres;

--
-- TOC entry 2984 (class 2606 OID 16396)
-- Name: airport_id; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY airports
    ADD CONSTRAINT airport_id PRIMARY KEY (airport_id);


--
-- TOC entry 2989 (class 2606 OID 19243)
-- Name: unique_event; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY events
    ADD CONSTRAINT unique_event UNIQUE ("time", location_hash, raw_text);


--
-- TOC entry 2991 (class 2606 OID 18687)
-- Name: uuid_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY events
    ADD CONSTRAINT uuid_pkey PRIMARY KEY (event_id);


--
-- TOC entry 2985 (class 1259 OID 18671)
-- Name: airport_location_index; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX airport_location_index ON airports USING gist (location);


--
-- TOC entry 2986 (class 1259 OID 18688)
-- Name: event_location_index; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX event_location_index ON events USING gist (location);


--
-- TOC entry 2987 (class 1259 OID 18689)
-- Name: event_time; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX event_time ON events USING btree ("time");


--
-- TOC entry 2978 (class 2618 OID 18194)
-- Name: geometry_columns_delete; Type: RULE; Schema: public; Owner: postgres
--

CREATE RULE geometry_columns_delete AS ON DELETE TO geometry_columns DO INSTEAD NOTHING;


--
-- TOC entry 2976 (class 2618 OID 18192)
-- Name: geometry_columns_insert; Type: RULE; Schema: public; Owner: postgres
--

CREATE RULE geometry_columns_insert AS ON INSERT TO geometry_columns DO INSTEAD NOTHING;


--
-- TOC entry 2977 (class 2618 OID 18193)
-- Name: geometry_columns_update; Type: RULE; Schema: public; Owner: postgres
--

CREATE RULE geometry_columns_update AS ON UPDATE TO geometry_columns DO INSTEAD NOTHING;


--
-- TOC entry 2998 (class 0 OID 0)
-- Dependencies: 5
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- TOC entry 3003 (class 0 OID 0)
-- Dependencies: 163
-- Name: airports; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE airports FROM PUBLIC;
REVOKE ALL ON TABLE airports FROM postgres;
GRANT ALL ON TABLE airports TO postgres;
GRANT ALL ON TABLE airports TO wx_admins;


--
-- TOC entry 3004 (class 0 OID 0)
-- Dependencies: 177
-- Name: events; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE events FROM PUBLIC;
REVOKE ALL ON TABLE events FROM postgres;
GRANT ALL ON TABLE events TO postgres;
GRANT ALL ON TABLE events TO wx_admins;


-- Completed on 2013-06-13 17:57:26 CDT

--
-- PostgreSQL database dump complete
--

