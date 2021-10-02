create table records
(
    team_id        integer
        constraint records_teams_team_id_fk
            references teams,
    home_wins      integer default 0,
    home_losses    integer default 0,
    road_wins      integer default 0,
    road_losses    integer default 0,
    neutral_wins   integer default 0,
    neutral_losses integer default 0,
    record_id      serial not null
        constraint records_pk
            primary key,
    point_diff     integer default 0,
    season         integer,
    week           integer
);

alter table records
    owner to postgres;

create unique index records_record_id_uindex
    on records (record_id);


