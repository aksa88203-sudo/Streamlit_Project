USE `inventory_db`;

INSERT INTO `products` (`id`, `name`, `sku`, `quantity`, `reorder_level`, `max_stock`, `price`, `category`)
VALUES
  (1, 'Laptop', 'LAP001', 45, 20, 50, 999.99, 'Electronics'),
  (2, 'Wireless Mouse', 'MOU001', 150, 30, 100, 29.99, 'Electronics'),
  (3, 'USB-C Cable', 'CAB001', 8, 50, 200, 12.99, 'Accessories'),
  (4, 'Monitor 27"', 'MON001', 25, 10, 40, 349.99, 'Electronics'),
  (5, 'Keyboard', 'KEY001', 180, 25, 80, 79.99, 'Electronics'),
  (6, 'Webcam HD', 'WEB001', 12, 15, 50, 89.99, 'Electronics'),
  (7, 'Desk Lamp', 'LAM001', 65, 20, 60, 34.99, 'Office'),
  (8, 'Notebook Pack', 'NOT001', 200, 50, 150, 9.99, 'Office')
ON DUPLICATE KEY UPDATE
  `name` = VALUES(`name`),
  `quantity` = VALUES(`quantity`),
  `reorder_level` = VALUES(`reorder_level`),
  `max_stock` = VALUES(`max_stock`),
  `price` = VALUES(`price`),
  `category` = VALUES(`category`);

INSERT INTO `sales` (`id`, `sale_date`, `product_id`, `product_name`, `quantity`, `total`)
VALUES
  (1, '2026-04-03', 2, 'Wireless Mouse', 3, 89.97),
  (2, '2026-04-05', 1, 'Laptop', 1, 999.99),
  (3, '2026-04-08', 3, 'USB-C Cable', 7, 90.93),
  (4, '2026-04-12', 4, 'Monitor 27"', 2, 699.98),
  (5, '2026-04-15', 5, 'Keyboard', 4, 319.96),
  (6, '2026-04-19', 7, 'Desk Lamp', 5, 174.95),
  (7, '2026-04-24', 6, 'Webcam HD', 2, 179.98),
  (8, '2026-04-28', 8, 'Notebook Pack', 10, 99.90),
  (9, '2026-05-02', 2, 'Wireless Mouse', 6, 179.94),
  (10, '2026-05-04', 5, 'Keyboard', 3, 239.97),
  (11, '2026-05-06', 1, 'Laptop', 1, 999.99),
  (12, '2026-05-08', 3, 'USB-C Cable', 9, 116.91),
  (13, '2026-05-08', 7, 'Desk Lamp', 4, 139.96),
  (14, '2026-05-08', 8, 'Notebook Pack', 12, 119.88);
