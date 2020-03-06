/*
 *  Create the config database for nopassword
 */

CREATE TABLE mailboxes
(
	name TEXT PRIMARY KEY,
	host TEXT,
	user_name TEXT
);

CREATE TABLE sites
(
	name TEXT PRIMARY KEY,
	endpoint TEXT,
	identifier TEXT
);
