-- ========================================
-- ResiTrack Database Setup
-- ========================================

-- Create the database
-- creating a "folder" for your app's data
CREATE DATABASE IF NOT EXISTS resitrack;
USE resitrack;

-- Create the 'households' table
-- This table stores info about each household and their safety status
CREATE TABLE IF NOT EXISTS households (
    id VARCHAR(36) PRIMARY KEY, 

    name VARCHAR(255) NOT NULL, 

    address VARCHAR(255) NOT NULL, 
   
    latitude DECIMAL(10,6) NOT NULL, 

    longitude DECIMAL(10,6) NOT NULL, 

    contact VARCHAR(50), 

    special_needs VARCHAR(255), 

    status ENUM('safe', 'not_safe', 'unverified') DEFAULT 'unverified', 

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

);
