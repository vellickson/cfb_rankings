create table teams
(
    team_id           serial not null
        constraint teams_pkey
            primary key,
    team_name         varchar,
    conference        varchar,
    cfbd_team_id      integer,
    mascot            varchar,
    division          varchar,
    team_abbr         varchar,
    cfbd_venue_id     integer,
    location_city     varchar,
    timezone          varchar,
    location_state    varchar,
    location_capacity integer,
    location_venue    varchar
);

alter table teams
    owner to postgres;

