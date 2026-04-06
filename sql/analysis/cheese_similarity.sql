with all_chesses as (
    select *
    from mart_cheese_features
),

pairs as (
    select
        a.cheese_name as source_cheese
        , b.cheese_name as candidate_cheese

        , a.milk_type_group as source_milk_type_group
        , b.milk_type_group as candidate_milk_type_group

        , a.style_group as source_style_group
        , b.style_group as candidate_style_group

        , a.pasteurisation as source_pasteurisation
        , b.pasteurisation as candidate_pasteurisation

        , a.country_of_origin as source_country
        , b.country_of_origin as candidate_country

        , a.organic as source_organic
        , b.organic as candidate_organic

        , a.strength_score as source_strength_score
        , b.strength_score as candidate_strength_score

        , case when a.milk_type_group = b.milk_type_group then 3 else 0 end as milk_type_score
        , case when a.style_group = b.style_group then 3 else 0 end as style_score
        , case when a.pasteurisation = b.pasteurisation then 1 else 0 end as pasteurisation_score
        , case when a.country_of_origin = b.country_of_origin then 1 else 0 end as country_score
        , case when a.organic = b.organic then 1 else 0 end as organic_score

        , case
            when a.strength_score is null or b.strength_score is null then 0
            when abs(a.strength_score - b.strength_score) = 0 then 2
            when abs(a.strength_score - b.strength_score) = 1 then 1
            else 0
          end as strength_score_match

    from all_chesses a
    cross join all_chesses b
    where a.cheese_name != b.cheese_name
)

select
    source_cheese
    , candidate_cheese
    , milk_type_score
    , style_score
    , pasteurisation_score
    , country_score
    , organic_score
    , strength_score_match
    , milk_type_score
        + style_score
        + pasteurisation_score
        + country_score
        + organic_score
        + strength_score_match as similarity_score
from pairs
order by 1, similarity_score desc, candidate_cheese