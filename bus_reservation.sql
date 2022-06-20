-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jun 20, 2022 at 07:26 AM
-- Server version: 5.7.26
-- PHP Version: 7.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bus_reservation`
--

-- --------------------------------------------------------

--
-- Table structure for table `booking`
--

DROP TABLE IF EXISTS `booking`;
CREATE TABLE IF NOT EXISTS `booking` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `payment` float NOT NULL,
  `booking_date` datetime NOT NULL,
  `status` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `fk_booking_user_id_users_id` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `booking_detail`
--

DROP TABLE IF EXISTS `booking_detail`;
CREATE TABLE IF NOT EXISTS `booking_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `booking_id` int(11) NOT NULL,
  `trip_id` int(11) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `qty` int(11) NOT NULL,
  `price` float NOT NULL,
  `total` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_booking_detail_booking_booking_id` (`booking_id`),
  KEY `fk_booking_detail_trip_trip_id` (`trip_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `bus`
--

DROP TABLE IF EXISTS `bus`;
CREATE TABLE IF NOT EXISTS `bus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_id` int(11) NOT NULL,
  `bus_name` varchar(255) NOT NULL,
  `bus_desc` varchar(255) DEFAULT NULL,
  `num_of_seat` int(11) DEFAULT '15',
  `price_per_seat` float DEFAULT '7',
  `created_date` datetime DEFAULT NULL,
  `status` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `fk_bus_bus_type_type_id` (`type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `bus`
--

INSERT INTO `bus` (`id`, `type_id`, `bus_name`, `bus_desc`, `num_of_seat`, `price_per_seat`, `created_date`, `status`) VALUES
(1, 1, 'PP-SR-Express', 'Morning', 15, 7, '2022-06-15 12:40:57', 1),
(2, 1, 'PP-SR-Express', 'Afternoon', 15, 7, '2022-06-15 12:41:14', 1),
(3, 2, 'PP-SR-VIP', 'Evening', 15, 10, '2022-06-15 12:42:05', 0),
(4, 1, 'PP-SHV-Express', 'Morning', 15, 7, '2022-06-15 12:42:46', 1),
(5, 1, 'PP-SHV-Express', 'Afternoon', 15, 7, '2022-06-15 12:42:54', 1),
(6, 2, 'PP-SHV-VIP', 'Evening', 15, 10, '2022-06-15 12:43:13', 0);

-- --------------------------------------------------------

--
-- Table structure for table `bus_type`
--

DROP TABLE IF EXISTS `bus_type`;
CREATE TABLE IF NOT EXISTS `bus_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_name` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `status` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `bus_type`
--

INSERT INTO `bus_type` (`id`, `type_name`, `created_at`, `status`) VALUES
(1, 'Express', '2022-06-14 22:43:19', 1),
(2, 'VIP', '2022-06-14 22:43:30', 1);

-- --------------------------------------------------------

--
-- Table structure for table `locations`
--

DROP TABLE IF EXISTS `locations`;
CREATE TABLE IF NOT EXISTS `locations` (
  `loc_id` int(11) NOT NULL AUTO_INCREMENT,
  `loc_name` varchar(255) DEFAULT NULL,
  `created_date` date DEFAULT NULL,
  `status` int(11) DEFAULT '1',
  PRIMARY KEY (`loc_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `locations`
--

INSERT INTO `locations` (`loc_id`, `loc_name`, `created_date`, `status`) VALUES
(1, 'Phnom Penh to Siem Reap', '2022-03-25', 1),
(2, 'Siem Reap to Phnom Penh', '2022-03-25', 1),
(3, 'Phnom Penh to Sihanoukville', '2022-03-25', 1),
(4, 'Sihanoukville to Phnom Penh', '2022-03-25', 1);

-- --------------------------------------------------------

--
-- Table structure for table `trip`
--

DROP TABLE IF EXISTS `trip`;
CREATE TABLE IF NOT EXISTS `trip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `loc_id` int(11) NOT NULL,
  `bus_id` int(11) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `seat` int(11) DEFAULT '15',
  `departure_date` date NOT NULL,
  `departure_time` time DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_trip_locations_loc_id` (`loc_id`),
  KEY `fk_trip_bus_id_bus_id` (`bus_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) DEFAULT NULL,
  `user_pass` varchar(255) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `user_desc` varchar(255) DEFAULT 'User',
  `phone` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `created_date` date DEFAULT NULL,
  `status` int(11) DEFAULT '1',
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `user_name`, `user_pass`, `first_name`, `last_name`, `date_of_birth`, `user_desc`, `phone`, `email`, `created_date`, `status`) VALUES
(1, 'socheapheaktra', 'pheaktra123', 'Doung', 'Socheapheaktra', '2001-01-23', 'User', '092605441', 'socheapheaktra@gmail.com', '2022-04-09', 1),
(2, 'socheapheaktra_test', 'pheaktra123', 'Socheapheaktra', 'Test', NULL, 'User', NULL, 'socheapheaktra_test@gmail.com', '2022-04-11', 1),
(7, 'test_user', '123456789', NULL, NULL, NULL, 'User', NULL, 'test_test@gmail.com', '2022-04-04', 1),
(4, 'admin', 'admin', NULL, NULL, NULL, 'Admin', NULL, 'socheapheaktra_admin@gmail.com', '2022-04-20', 1),
(6, 'socheapheaktra123', 'pheaktra123', NULL, NULL, NULL, 'User', NULL, 'socheapheaktra@gmail.com', '2022-04-25', 1),
(8, 'test', 'test', NULL, NULL, NULL, 'User', NULL, 'test@test.com', '2022-05-25', 1),
(9, 'asdfa', 'test', NULL, NULL, NULL, 'User', NULL, 'test@test.comasdfa', '2022-05-25', 1),
(10, 'asdfasdfa', 'asdfasdfa', NULL, NULL, NULL, 'User', NULL, 'asdfasdfasdfa', '2022-05-25', 1);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
