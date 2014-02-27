ALTER TABLE base_entity ADD COLUMN `rank_score` int(11) NOT NULL DEFAULT '0';
ALTER TABLE base_entity ADD KEY `base_entity_rank_score` (`rank_score`);
