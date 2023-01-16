create table urls(
    id bigint primary key generated always as identity,
    name VARCHAR(255) unique,
    created_at timestamp default now()
);

create table url_checks(
    id bigint primary key generated always as identity, 
    url_id bigint, 
    status_code int,
    h1 VARCHAR(512),
    title VARCHAR(512), 
    description VARCHAR(512), 
    created_at timestamp default now()
)
