create temp table if not exists combo_tmp(k text, r jsonb);
do $$ begin

end $$;
select json_agg(json_build_object('k', k, 'url', r->'body'->>'url', 'err', r->'body'->'err')) from combo_tmp;