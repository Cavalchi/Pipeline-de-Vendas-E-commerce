-- As queries abaixo foram construídas com base no dataset real da Olist
-- e têm como objetivo responder a perguntas de negócio exigidas no escopo.

-- 1. GMV por categoria
-- Mostra a receita total (Gross Merchandise Volume) gerada pelas 10 categorias mais rentáveis.
SELECT 
    p.product_category_name AS category, 
    SUM(oi.price) AS gmv
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY p.product_category_name
ORDER BY gmv DESC 
LIMIT 10;


-- 2. Atraso médio de entrega por estado
-- Cruza a tabela de pedidos com clientes para identificar a diferença 
-- (em dias) entre quando o produto era estimado para chegar e quando efetivamente chegou.
-- Usando a diferença de datas do PostgreSQL:
SELECT 
    c.customer_state AS state,
    AVG(DATE_PART('day', o.order_delivered_customer_date::timestamp - o.order_estimated_delivery_date::timestamp)) AS atraso_medio_dias
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered' 
  AND o.order_delivered_customer_date > o.order_estimated_delivery_date
GROUP BY c.customer_state
ORDER BY atraso_medio_dias DESC;


-- 3. Categoria com maior nota de satisfação (reviews)
-- Junta avaliações, itens do pedido e produtos para verificar quais 
-- categorias de produtos receberam as maiores notas médias de avaliação.
SELECT 
    p.product_category_name AS category,
    AVG(r.review_score) AS media_satisfacao,
    COUNT(r.review_id) AS total_avaliacoes
FROM order_reviews r
JOIN order_items oi ON r.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_category_name
HAVING COUNT(r.review_id) > 50  -- Filtra categorias com baixa amostragem
ORDER BY media_satisfacao DESC
LIMIT 10;
