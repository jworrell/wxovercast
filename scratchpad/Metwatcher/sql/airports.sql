CREATE TABLE airports (
	id 					INTEGER,
	ident 				TEXT,
	type 				TEXT,
	name 				TEXT,
	latitude_deg 		REAL,
	longitude_deg 		REAL,
	elevation_ft 		REAL,
	continent 			TEXT,
	iso_country 		TEXT,
	iso_region 			TEXT,
	municipality 		TEXT,
	scheduled_service 	TEXT,
	gps_code 			TEXT,
	iata_code 			TEXT,
	local_code 			TEXT,
	home_link 			TEXT,
	wikipedia_link 		TEXT,
	keywords 			TEXT
);

CREATE INDEX airport_by_ident ON airports (
	ident
);

CREATE INDEX airport_by_location ON airports (
	latitude_deg,
	longitude_deg
);