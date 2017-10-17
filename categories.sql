select category.categoryName,
count(*) as freq
from category_link
inner join category on category_link.cat=category.idcategory
where category.blog=4
group by category_link.cat