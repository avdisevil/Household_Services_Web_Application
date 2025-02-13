BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Customer_Table" (
	"customer_id"	INTEGER NOT NULL UNIQUE,
	"email_id"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"full_name"	TEXT NOT NULL,
	"address"	TEXT NOT NULL,
	"pin_code"	INTEGER NOT NULL,
	"Block"	INTEGER DEFAULT 0,
	PRIMARY KEY("customer_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Professional_Table" (
	"professional_id"	INTEGER NOT NULL UNIQUE,
	"email_id"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"full_name"	TEXT NOT NULL,
	"service_name"	TEXT NOT NULL,
	"experience"	INTEGER NOT NULL,
	"document"	BLOB NOT NULL,
	"address"	TEXT NOT NULL,
	"pin_code"	INTEGER NOT NULL,
	"Approve"	INTEGER DEFAULT 0,
	"description"	TEXT,
	"rating"	INTEGER DEFAULT 5,
	"Block"	INTEGER DEFAULT 0,
	PRIMARY KEY("professional_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Service_Table" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	"price"	INTEGER NOT NULL,
	"description"	TEXT,
	"time_required"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Base_Table" (
	"id"	INTEGER NOT NULL UNIQUE,
	"service_id"	INTEGER NOT NULL,
	"customer_id"	INTEGER NOT NULL,
	"professional_id"	INTEGER NOT NULL,
	"date_of_request"	DATE NOT NULL,
	"date_of_completion"	DATE,
	"service_status"	INTEGER NOT NULL,
	"remarks"	TEXT,
	"service_rating"	INTEGER,
	FOREIGN KEY("customer_id") REFERENCES "Customer_Table"("customer_id"),
	FOREIGN KEY("service_id") REFERENCES "Service_Table"("id"),
	FOREIGN KEY("professional_id") REFERENCES "Professional_Table"("professional_id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Admin_Table" (
	"admin_id"	INTEGER NOT NULL UNIQUE,
	"email_id"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("admin_id" AUTOINCREMENT)
);
COMMIT;
