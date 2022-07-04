create table season_opponents
(
    season_opponent_id serial  not null
        constraint season_opponents_id
            primary key,
    record_id          integer not null
        constraint season_opponents_records_id_fk
            references records,
    opponent_id        integer
        constraint season_opponents_teams_team_id_fk
            references teams
);

alter table season_opponents
    owner to postgres;


