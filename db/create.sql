/*
 *  Create the config database for nopassword
 */

CREATE TABLE mailboxes
(
	name TEXT UNIQUE,
	host TEXT,
	user_name TEXT
);

CREATE TABLE sites
(
	name TEXT UNIQUE,
	endpoint TEXT,
	identifier TEXT
);
