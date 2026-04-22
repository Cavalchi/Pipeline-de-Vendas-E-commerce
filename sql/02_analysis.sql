-- GMV por categoria
SELECT 
    p.product_category_name AS category, 
    ROUND(SUM(oi.price)::numeric, 2) AS gmv
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY p.product_category_name
ORDER BY gmv DESC 
LIMIT 10;


-- Atraso de dias por estado
SELECT 
    c.customer_state AS state,
    ROUND(AVG(DATE_PART('day', o.order_delivered_customer_date::timestamp - o.order_estimated_delivery_date::timestamp))::numeric, 1) AS atraso_medio_dias
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered' 
  AND o.order_delivered_customer_date > o.order_estimated_delivery_date
GROUP BY c.customer_state
ORDER BY atraso_medio_dias DESC;


-- top categorias no review
SELECT 
    p.product_category_name AS category,
    ROUND(AVG(r.review_score)::numeric, 2) AS media_satisfacao,
    COUNT(r.review_id) AS total_avaliacoes
FROM order_reviews r
JOIN order_items oi ON r.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_category_name
HAVING COUNT(r.review_id) > 50
ORDER BY media_satisfacao DESC
LIMIT 10;
