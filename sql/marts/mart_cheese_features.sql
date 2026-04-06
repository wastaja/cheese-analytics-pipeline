with deduplicated as (
    select distinct
        cheese_name
        , cheese_url
        , country_of_origin
        , milk_type
        , organic
        , pasteurisation
        , region
        , strength_of_cheese
        , style_of_cheese
        , age
    from stg_cheese_details
)

select
    cheese_name
    , cheese_url
    , country_of_origin
    , milk_type
    , organic
    , pasteurisation
    , region
    , strength_of_cheese
    , style_of_cheese
    , age

    , case
        when lower(milk_type) = 'cows' then 'cow'
        when lower(milk_type) = 'goats' then 'goat'
        when lower(milk_type) = 'ewes' then 'ewe'
        when lower(milk_type) = 'buffalo' then 'buffalo'
        when lower(milk_type) = 'mixed milk' then 'mixed'
        else 'other'
      end as milk_type_group

    , case
        when lower(style_of_cheese) like '%blue%' then 'blue'
        when lower(style_of_cheese) like '%hard%' then 'hard'
        when lower(style_of_cheese) like '%soft%' then 'soft'
        when lower(style_of_cheese) like '%bloomy%' then 'bloomy'
        when lower(style_of_cheese) like '%creamy%' then 'creamy'
        else 'other'
      end as style_group

    , case
        when lower(strength_of_cheese) like '%mild%' and lower(strength_of_cheese) not like '%strong%' then 1
        when lower(strength_of_cheese) like '%medium%' and lower(strength_of_cheese) not like '%strong%' then 2
        when lower(strength_of_cheese) like '%strong%' then 3
        else null
      end as strength_score

from deduplicated