DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_product_supplies`(IN `var_product_id` INT)
select s.*, 
if(s.id in (select supply_id from product_supplies where product_id = var_product_id), 'checked', '') checked,
(select quantity from product_supplies where supply_id = s.id and product_id = var_product_id) quantity
from supply s$$
DELIMITER ;
