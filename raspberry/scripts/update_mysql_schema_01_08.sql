update base_entity inner join (select distinct entity_id from base_note where selector_id is not null) as tn ON base_entity.id=tn.entity_id set base_entity.weight=1 where base_entity.weight <= 0;
