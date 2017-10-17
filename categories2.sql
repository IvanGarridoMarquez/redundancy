select count(*) as i from category_link where cat=88 and entry in (select entry from category_link where cat=89)
