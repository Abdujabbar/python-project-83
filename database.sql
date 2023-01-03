create table urls(
    id bigint primary key generated always as identity,
    name VARCHAR(255) unique,
    created_at timestamp default now()
);