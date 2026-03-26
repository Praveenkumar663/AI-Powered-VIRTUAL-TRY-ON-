-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 15, 2024 at 12:50 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `1virtualtryondb`
--

-- --------------------------------------------------------

--
-- Table structure for table `booktb`
--

CREATE TABLE `booktb` (
  `id` bigint(10) NOT NULL auto_increment,
  `UserName` varchar(250) NOT NULL,
  `Bookid` varchar(250) NOT NULL,
  `Qty` varchar(250) NOT NULL,
  `Amount` varchar(250) NOT NULL,
  `CardName` varchar(250) NOT NULL,
  `CardNo` varchar(250) NOT NULL,
  `CvNo` varchar(250) NOT NULL,
  `Date` date NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `booktb`
--


-- --------------------------------------------------------

--
-- Table structure for table `carttb`
--

CREATE TABLE `carttb` (
  `id` bigint(10) NOT NULL auto_increment,
  `UserName` varchar(250) NOT NULL,
  `ProductName` varchar(250) NOT NULL,
  `ProductType` varchar(250) NOT NULL,
  `Price` varchar(250) NOT NULL,
  `Qty` decimal(18,2) NOT NULL,
  `Tprice` decimal(28,2) NOT NULL,
  `Image` varchar(500) NOT NULL,
  `Date` date NOT NULL,
  `Status` varchar(250) NOT NULL,
  `Bookid` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `carttb`
--


-- --------------------------------------------------------

--
-- Table structure for table `protb`
--

CREATE TABLE `protb` (
  `id` bigint(10) NOT NULL auto_increment,
  `ProductName` varchar(250) NOT NULL,
  `ProductType` varchar(250) NOT NULL,
  `Size` varchar(10) NOT NULL,
  `Price` varchar(250) NOT NULL,
  `Qty` varchar(250) NOT NULL,
  `Info` varchar(500) NOT NULL,
  `Image` varchar(500) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `protb`
--

INSERT INTO `protb` (`id`, `ProductName`, `ProductType`, `Size`, `Price`, `Qty`, `Info`, `Image`) VALUES
(2, 'tshirt', 'Tshirt', 'S', '600', '50', 'green shirt', '1750.png'),
(3, 'sunglass007', 'Sunglasses', 'S', '800', '200', 'black shine', '7562.png'),
(4, 'Tshirt', 'Tshirt', 'S', '900', '4', 'blue Color', '9795.png');

-- --------------------------------------------------------

--
-- Table structure for table `regtb`
--

CREATE TABLE `regtb` (
  `Name` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Address` varchar(250) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `regtb`
--

INSERT INTO `regtb` (`Name`, `Email`, `Mobile`, `Address`, `UserName`, `Password`) VALUES
('sangeeth Kumar', 'sangeeth5535@gmail.com', '9486365535', 'No 16, Samnath Plaza, Madurai Main Road, Melapudhur', 'san', 'san'),
('sangeeth Kumar', 'sangeeth5535@gmail.com', '9486365535', 'No 16, Samnath Plaza, Madurai Main Road, Melapudhur', 'san56', 'san56'),
('jackson ', 'sangeeth5535@gmail.com', '9486365535', 'No 16, Samnath Plaza, Madurai Main Road, Melapudhur', 'jackson ', 'jackson ');
