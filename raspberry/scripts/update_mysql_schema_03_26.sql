ALTER TABLE base_entity ADD COLUMN `novus_time` datetime DEFAULT NULL;
ALTER TABLE base_entity ADD KEY `base_entity_novus_time` (`novus_time`);
UPDATE base_entity SET novus_time=updated_time WHERE weight=0;
