-- phpMyAdmin SQL Dump
-- version 3.2.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 02, 2023 at 08:50 PM
-- Server version: 5.1.41
-- PHP Version: 5.3.1

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `ricedetection`
--
CREATE DATABASE `ricedetection` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `ricedetection`;

-- --------------------------------------------------------

--
-- Table structure for table `personaldetails`
--

CREATE TABLE IF NOT EXISTS `personaldetails` (
  `PersonId` int(11) NOT NULL AUTO_INCREMENT,
  `Firstname` varchar(250) NOT NULL,
  `Lastname` varchar(250) NOT NULL,
  `Phoneno` bigint(250) NOT NULL,
  `Emailid` varchar(250) NOT NULL,
  `Address` varchar(250) NOT NULL,
  `Username` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  `Recorded_Date` date NOT NULL,
  PRIMARY KEY (`PersonId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=16 ;

--
-- Dumping data for table `personaldetails`
--

INSERT INTO `personaldetails` (`PersonId`, `Firstname`, `Lastname`, `Phoneno`, `Emailid`, `Address`, `Username`, `Password`, `Recorded_Date`) VALUES
(13, 'kiruba', 'v', 9043963074, 'kirubakarans2009@gmail.com', 'chennai', 'kiruba', 'kiruba', '2022-06-24'),
(14, 'hari', 's', 9043963074, 'kirubakarans2009@gmail.com', 'cddsasa', 'hari', 'hari', '2023-06-02'),
(15, 'hari', 's', 9043963074, 'kirubakarans2009@gmail.com', 'cddsasa', 'hari1', 'hari1', '2023-06-02');

-- --------------------------------------------------------

--
-- Table structure for table `uploaddetails`
--

CREATE TABLE IF NOT EXISTS `uploaddetails` (
  `UploadId` int(11) NOT NULL AUTO_INCREMENT,
  `PersonId` int(11) NOT NULL,
  `ImagePath` varchar(250) NOT NULL,
  `OPImagePath1` varchar(250) DEFAULT NULL,
  `OPImagePath2` varchar(250) DEFAULT NULL,
  `OPImagePath3` varchar(250) DEFAULT NULL,
  `Results` varchar(250) DEFAULT NULL,
  `Recorded_Date` datetime NOT NULL,
  PRIMARY KEY (`UploadId`),
  KEY `PersonId` (`PersonId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `uploaddetails`
--

INSERT INTO `uploaddetails` (`UploadId`, `PersonId`, `ImagePath`, `OPImagePath1`, `OPImagePath2`, `OPImagePath3`, `Results`, `Recorded_Date`) VALUES
(2, 15, 'oracle.png', 'cts.jpg', 'cts.jpg', 'cts.jpg', 'Test Output', '2023-06-02 00:00:00');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
