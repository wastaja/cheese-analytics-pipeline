select
    trim(cheese_name) as cheese_name
    , trim(cheese_url) as cheese_url
    , nullif(trim(tasting_notes), '') as tasting_notes

    , nullif(trim(age), '') as age
    , nullif(trim(country_of_origin), '') as country_of_origin
    , nullif(trim(milk_type), '') as milk_type

    , organic
    , pasteurisation

    , nullif(trim(region), '') as region
    , nullif(trim(strength_of_cheese), '') as strength_of_cheese
    , nullif(trim(style_of_cheese), '') as style_of_cheese

from cheese_details_raw