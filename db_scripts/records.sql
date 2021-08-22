create table records
(
    team_id        integer
        constraint records_teams_team_id_fk
            references teams,
    home_wins      integer,
    home_losses    integer,
    road_wins      integer,
    road_losses    integer,
    neutral_wins   integer,
    neutral_losses integer,
    record_id      integer not null
        constraint records_pk
            primary key,
    point_diff     integer,
    season         integer,
    week           integer
);

alter table records
    owner to postgres;

create unique index records_record_id_uindex
    on records (record_id);

