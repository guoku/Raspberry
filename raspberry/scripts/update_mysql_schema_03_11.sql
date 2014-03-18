ALTER TABLE base_guoku_plus ADD COLUMN `seller_remarks` varchar(100) NULL default '';
ALTER TABLE base_guoku_plus ADD COLUMN `editor_remarks` varchar(100) NULL default '';
ALTER TABLE base_guoku_plus ADD COLUMN `shop_nick` varchar(50);
ALTER TABLE base_guoku_plus ADD COLUMN `updated_time` datetime;
ALTER TABLE base_guoku_plus ADD COLUMN `end_time` datetime NULL;
