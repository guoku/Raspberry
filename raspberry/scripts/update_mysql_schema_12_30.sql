ALTER TABLE base_entity ADD COLUMN `mark` int(11) DEFAULT 0;
ALTER TABLE base_entity ADD KEY `base_entity_mark` (`mark`);
