ALTER TABLE base_entity_tag add `tag_text` varchar(128) NOT NULL;
UPDATE base_entity_tag INNER JOIN base_tag ON base_entity_tag.tag_id=base_tag.id SET base_entity_tag.tag_text=base_tag.tag;
ALTER TABLE base_entity_tag ADD KEY `base_entity_tag_text` (`tag_text`);
