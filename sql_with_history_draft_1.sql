CREATE SCHEMA "users";

CREATE SCHEMA "devices";

CREATE TYPE "users"."role" AS ENUM (
  'admin',
  'technician'
);

CREATE TYPE "devices"."status" AS ENUM (
  'installed',
  'broken',
  'sentforrepair',
  'sentforcalibraion',
  'missing'
);

CREATE TABLE "users" (
  "id" integer PRIMARY KEY,
  "role" enum
);

CREATE TABLE "global_metadatas" (
  "id" integer PRIMARY KEY,
  "start_date" date,
  "end_date" date,
  "title" string,
  "abstract" string,
  "keywords" array,
  "creator_name" string,
  "creator_contact" string,
  "license" string,
  "version" float64
);

CREATE TABLE "locations" (
  "id" integer PRIMARY KEY,
  "description" varchar,
  "abbreviated_description" varchar,
  "notes" string
);

CREATE TABLE "devices" (
  "id" integer PRIMARY KEY,
  "serial_number" uuid,
  "device_type_id" integer,
  "status" enum,
  "calibration_date" date,
  "calibration_due" date,
  "ship_to_calibration_by" date,
  "notes" string
);

CREATE TABLE "components" (
  "id" integer PRIMARY KEY,
  "serial_number" uuid,
  "device_id" integer,
  "calibration_date" date,
  "installation_date" date,
  "removal_date" date,
  "status" string,
  "component_type_id" integer
);

CREATE TABLE "installation_groups" (
  "id" integer PRIMARY KEY,
  "label" string,
  "created_at" date,
  "updated_at" date,
  "notes" string
);

CREATE TABLE "installations" (
  "id" integer PRIMARY KEY,
  "device_installations_id" integer,
  "installation_group_id" integer,
  "location_id" integer,
  "label" string,
  "abbreviated_label" string,
  "installed_date" date,
  "removal_date" date,
  "created_at" date,
  "updated_at" date
);

CREATE TABLE "device_installations" (
  "id" integer PRIMARY KEY,
  "device_id" integer,
  "installation_id" integer,
  "filename_prefix" string,
  "installed_date" date,
  "removal_date" date,
  "created_at" date,
  "updated_at" date
);

CREATE TABLE "device_types" (
  "id" integer PRIMARY KEY,
  "label" string,
  "alternative_label" string,
  "definition" string,
  "example_output" string,
  "file_header" string,
  "filename" string,
  "identifier" string,
  "instrument_type" enum,
  "manual_link" string,
  "calibration_file" string,
  "parser" string,
  "uri" jsonb,
  "permitted_parameters" jsonb
);

CREATE TABLE "component_types" (
  "id" integer PRIMARY KEY,
  "device_type_id" integer,
  "name" string
);

CREATE TABLE "device_type_measurements" (
  "id" integer PRIMARY KEY,
  "device_type_id" integer,
  "accuracy" string,
  "label" string,
  "alternative_label" string,
  "description" string,
  "header_label" string,
  "instrument_range" tuple,
  "resolution" float64,
  "type" enum,
  "units" string,
  "units_long" string,
  "uri" jsonb
);

ALTER TABLE "installation_groups" ADD FOREIGN KEY ("id") REFERENCES "installations" ("installation_group_id");

ALTER TABLE "installations" ADD FOREIGN KEY ("location_id") REFERENCES "locations" ("id");

ALTER TABLE "device_installations" ADD FOREIGN KEY ("device_id") REFERENCES "devices" ("id");

ALTER TABLE "device_installations" ADD FOREIGN KEY ("installation_id") REFERENCES "installations" ("id");

ALTER TABLE "devices" ADD FOREIGN KEY ("device_type_id") REFERENCES "device_types" ("id");

ALTER TABLE "device_type_measurements" ADD FOREIGN KEY ("device_type_id") REFERENCES "device_types" ("id");

ALTER TABLE "component_types" ADD FOREIGN KEY ("device_type_id") REFERENCES "device_types" ("id");

ALTER TABLE "component_types" ADD FOREIGN KEY ("id") REFERENCES "components" ("component_type_id");

ALTER TABLE "components" ADD FOREIGN KEY ("component_type_id") REFERENCES "devices" ("id");
