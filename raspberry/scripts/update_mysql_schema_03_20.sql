update base_note inner join ( SELECT note_id, count(*) as tot from base_note_poke group by note_id) as tmpt on base_note.id=tmpt.note_id SET base_note.poke_count=tmpt.tot;

ALTER TABLE base_guoku_plus ADD COLUMN `end_time` datetime NULL;
ALTER TABLE base_guoku_plus_token ADD COLUMN `quantity` int(11) NULL;
