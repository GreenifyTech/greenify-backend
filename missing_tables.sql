-- ─────────────────────────────────────────────────────
-- TABLE: cart_items
-- ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS cart_items (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    user_id    INT      NOT NULL,
    product_id INT      NOT NULL,
    quantity   INT      NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                         ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_cart_items_user_product (user_id, product_id),
    FOREIGN KEY (user_id)    REFERENCES users(id)    ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─────────────────────────────────────────────────────
-- TABLE: bouquet_items
-- ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS bouquet_items (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    bouquet_id INT           NOT NULL,
    flower_type VARCHAR(100) NOT NULL,
    color      VARCHAR(100)  NOT NULL,
    quantity   INT           NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    created_at DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_bouquet_item_unique (bouquet_id, flower_type, color),
    FOREIGN KEY (bouquet_id) REFERENCES bouquets(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─────────────────────────────────────────────────────
-- TABLE: payments
-- ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS payments (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    order_id         INT           NOT NULL UNIQUE,
    amount           DECIMAL(10,2) NOT NULL,
    method           ENUM('cash_on_delivery','online_payment') NOT NULL,
    status           ENUM('pending','paid','failed','refunded')
                     NOT NULL DEFAULT 'pending',
    transaction_ref  VARCHAR(255),
    created_at       DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
                                   ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─────────────────────────────────────────────────────
-- TABLE: ai_consultations
-- ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ai_consultations (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    user_id          INT      NOT NULL,
    symptoms         TEXT     NOT NULL,
    possible_disease TEXT     NOT NULL,
    cause            TEXT     NOT NULL,
    treatment        TEXT     NOT NULL,
    confidence       ENUM('high','medium','low') NOT NULL,
    disclaimer       TEXT     NOT NULL,
    created_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

