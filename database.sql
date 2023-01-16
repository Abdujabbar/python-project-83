create table urls(
    id bigint primary key generated always as identity,
    name VARCHAR(255) unique,
    created_at timestamp default now()
);

CREATE TABLE "url_checks" (
    id bigint primary key generated always as identity,
    "url_id" int8,
    "status_code" int4,
    "h1" varchar(512),
    "title" varchar(512),
    "description" varchar(512),
    "created_at" timestamp DEFAULT now(),
    CONSTRAINT "url_checks_url_id_fkey" FOREIGN KEY ("url_id") REFERENCES "urls"("id")
);