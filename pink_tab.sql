-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 25, 2025 at 12:37 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pink_tab`
--

-- --------------------------------------------------------

--
-- Table structure for table `access_log`
--

CREATE TABLE `access_log` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `employee_id` varchar(9) NOT NULL,
  `access_timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `access_log`
--

INSERT INTO `access_log` (`id`, `employee_id`, `access_timestamp`) VALUES
(1, '202503002', '2025-03-25 12:58:57'),
(2, '202503001', '2025-03-25 16:36:40'),
(3, '202503002', '2025-03-25 16:59:53'),
(4, '1', '2025-03-25 17:01:10'),
(5, '1', '2025-03-25 17:03:19'),
(6, '202503001', '2025-03-25 17:03:33'),
(7, '202503001', '2025-03-25 17:09:18'),
(8, '1', '2025-03-25 17:09:24'),
(9, '1', '2025-03-25 17:30:58'),
(10, '202503001', '2025-03-25 17:34:09'),
(11, '202503002', '2025-03-25 17:37:26');

-- --------------------------------------------------------

--
-- Table structure for table `change_log`
--

CREATE TABLE `change_log` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `employee_id` varchar(9) DEFAULT NULL,
  `change_type` varchar(60) DEFAULT NULL,
  `change_timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `change_log`
--

INSERT INTO `change_log` (`id`, `employee_id`, `change_type`, `change_timestamp`) VALUES
(1, '202503002', 'ADDED INVENTORY BFORA - Berry Fun Orange', '2025-03-25 19:15:24'),
(2, '202503002', 'ADDED INVENTORY SCLEM - Super Citric Lemon', '2025-03-25 19:15:53'),
(3, '202503002', 'ADDED INVENTORY SCLEM - Piltover Special HexSoda', '2025-03-25 19:17:19'),
(4, '202503002', 'ADDED INVENTORY TESTS - test', '2025-03-25 19:20:29'),
(5, '202503002', 'DELETED INVENTORY TESTS - test', '2025-03-25 19:26:24'),
(6, '202503002', 'DELETED INVENTORY SCLEM - Super Citric Lemon', '2025-03-25 19:27:45'),
(7, '202503002', 'DELETED INVENTORY BFORA - Berry Fun Orange', '2025-03-25 19:33:51'),
(8, '202503002', 'ADDED INVENTORY PSHXS - Magnetic Magic Cherry', '2025-03-25 19:36:25'),
(9, '202503002', 'DELETED INVENTORY MMCHR - Magnetic Magic Cherry', '2025-03-25 19:36:40');

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE `employee` (
  `id` varchar(9) NOT NULL,
  `first_name` varchar(60) DEFAULT NULL,
  `last_name` varchar(60) DEFAULT NULL,
  `emp_pass` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`id`, `first_name`, `last_name`, `emp_pass`) VALUES
('1', 'Test', 'User', '123'),
('202503001', 'Jayce', 'Talis', 'Cr4nk17'),
('202503002', 'Viktor', 'Novak', 'inallpossibilities'),
('202503003', 'Caitlyn', 'Kiramman', '6olet');

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

CREATE TABLE `inventory` (
  `id` varchar(5) NOT NULL,
  `name` varchar(60) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `exp_date` date DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventory`
--

INSERT INTO `inventory` (`id`, `name`, `quantity`, `exp_date`, `price`) VALUES
('PSHXS', 'Piltover Special HexSoda', 50, '2025-09-30', 149.99);

-- --------------------------------------------------------

--
-- Table structure for table `test`
--

CREATE TABLE `test` (
  `testnum` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `test`
--

INSERT INTO `test` (`testnum`) VALUES
(2),
(3),
(4),
(5),
(5),
(5),
(515);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `access_log`
--
ALTER TABLE `access_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `employee_id` (`employee_id`);

--
-- Indexes for table `change_log`
--
ALTER TABLE `change_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `employee_id` (`employee_id`);

--
-- Indexes for table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Indexes for table `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `access_log`
--
ALTER TABLE `access_log`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `change_log`
--
ALTER TABLE `change_log`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `access_log`
--
ALTER TABLE `access_log`
  ADD CONSTRAINT `access_log_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`id`);

--
-- Constraints for table `change_log`
--
ALTER TABLE `change_log`
  ADD CONSTRAINT `change_log_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
