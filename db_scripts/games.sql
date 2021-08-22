create table games
(
    game_id       serial
        constraint games_pk
            primary key,
    cfbd_game_id  integer,
    season        integer,
    game_type     varchar,
    game_date     date,
    neutral_site  boolean,
    cfbd_venue_id integer,
    home_team     integer
        constraint games_teams_team_id_fk
            references teams,
    away_team     integer
        constraint games_teams_team_id_fk_2
            references teams,
    home_points   integer,
    away_points   integer,
    overtime      boolean
);

alter table games
    owner to postgres;

