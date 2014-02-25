ALTER TABLE base_entity_tag ADD COLUMN `tag_hash` varchar(32) NOT NULL;
ALTER TABLE base_entity_tag ADD KEY `base_entity_tag_hash` (`tag_hash`);
UPDATE base_entity_tag INNER JOIN base_tag ON base_entity_tag.tag_id=base_tag.id SET base_entity_tag.tag_hash=base_tag.tag_hash;
