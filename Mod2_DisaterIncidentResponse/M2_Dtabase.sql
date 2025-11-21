CREATE TABLE IF NOT EXISTS incidents (
    id VARCHAR(36) NOT NULL PRIMARY KEY,   -- UUID for each incident
    type ENUM('earthquake','flood','typhoon','fire','landslide') NOT NULL,  -- Disaster type
    phase ENUM('incoming','occurring','past') DEFAULT 'incoming',           -- Disaster phase
    severity ENUM('low','medium','high','critical') NOT NULL,               -- Danger level
    description TEXT NOT NULL,              -- Details about the disaster
    affected_area VARCHAR(255) NOT NULL,    -- Location affected
    affected_families INT DEFAULT 0,        -- Number of families affected
    relief_distributed INT DEFAULT 0,       -- Number of families who received aid
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,    -- When incident was reported
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  -- Last update
);
