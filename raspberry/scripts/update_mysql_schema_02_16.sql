ALTER TABLE base_note_comment ADD COLUMN `entity_id` int(11) NOT NULL;
ALTER TABLE base_note_comment ADD KEY `base_note_entity_id` (`entity_id`);
UPDATE base_note_comment INNER JOIN base_note ON base_note_comment.note_id=base_note.id SET base_note_comment.entity_id=base_note.entity_id;
