create table season_opponents
(
    season_opponent_pk serial
        constraint season_opponents_pk
            primary key,
    record_id          integer not null
        constraint season_opponents_record_id__fk
            references records,
    opponent_id        integer not null
        constraint season_opponents_team_id__fk
            references teams
);

alter table season_opponents
    owner to postgres;

create unique index season_opponents_season_opponent_pk_uindex
    on season_opponents (season_opponent_pk);


