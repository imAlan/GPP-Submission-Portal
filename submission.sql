-- MySQL dump 10.13  Distrib 5.6.14, for Linux (x86_64)
--
-- Host: localhost    Database: submission
-- ------------------------------------------------------
-- Server version	5.6.14

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Document`
--

DROP TABLE IF EXISTS `Document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Document` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(500) NOT NULL,
  `description` varchar(500) NOT NULL,
  `datePublished` date DEFAULT NULL,
  `dateSubmitted` datetime NOT NULL,
  `dateCreated` date DEFAULT NULL,
  `dateRemoved` date DEFAULT NULL,
  `filename` varchar(255) DEFAULT NULL,
  `common_id` int(11) DEFAULT NULL,
  `section_id` int(11) DEFAULT NULL,
  `status` enum('published','removed','publishing','not_approved') NOT NULL,
  `request_deletion` enum('yes','no') DEFAULT NULL,
  `approved` enum('yes','no') DEFAULT NULL,
  `reason` varchar(500) DEFAULT NULL,
  `hardcopy` enum('yes','no') DEFAULT NULL,
  `doc_url` varchar(255) DEFAULT NULL,
  `path` varchar(300) DEFAULT NULL,
  `num_access` int(11) DEFAULT NULL,
  `agency` enum('Aging','Buildings','Campaign Finance','Childrens Services','City Council','City Clerk','City Planning','Citywide Admin Svcs','Civilian Complaint','Comm - Police Corr','Community Assistance','Comptroller','Conflicts of Interest','Consumer Affairs','Contracts','Correction','Criminal Justice Coordinator','Cultural Affairs','DOI - Investigation','Design/Construction','Disabilities','District Atty, NY County','Districting Commission','Domestic Violence','Economic Development','Education, Dept. of','Elections, Board of','Emergency Mgmt.','Employment','Empowerment Zone','Environmental - DEP','Environmental - OEC','Environmental - ECB','Equal Employment','Film/Theatre','Finance','Fire','FISA','Health and Mental Hyg.','HealthStat','Homeless Services','Hospitals - HHC','Housing - HPD','Human Rights','Human Rsrcs - HRA','Immigrant Affairs','Independent Budget','Info. Tech. and Telecom.','Intergovernmental','International Affairs','Judiciary Committee','Juvenile Justice','Labor Relations','Landmarks','Law Department','Library - Brooklyn','Library - New York','Library - Queens','Loft Board','Management and Budget','Mayor','Metropolitan Transportation Authority','NYCERS','Operations','Parks and Recreation','Payroll Administration','Police','Police Pension Fund','Probation','Public Advocate','Public Health','Public Housing-NYCHA','Records','Rent Guidelines','Sanitation','School Construction','Small Business Svcs','Sports Commission','Standards and Appeal','Tax Appeals Tribunal','Tax Commission','Taxi and Limousine','Transportation','Trials and Hearings','Veterans - Military','Volunteer Center','Voter Assistance','Youth & Community') NOT NULL,
  `category` enum('Business and Consumers','Cultural/Entertainment','Education','Environment','Finance and Budget','Government Policy','Health','Housing and Buildings','Human Services','Labor Relations','Public Safety','Recreation/Parks','Sanitation','Technology','Transportation') DEFAULT NULL,
  `type` enum('Annual Report','Audit Report','Bond Offering - Official Statements','Budget Report','Bulletins','Charts','Consultant Report','Diagrams','Directories','Guide - Manual','Handbooks','Hearing - Minutes','Legislative Document','Monthly ReportMemoranda - Directive','Orders','Plans','Press Release','Quarterly Report','Serial Publication','Staff Report','Studies','Report') NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Document`
--

LOCK TABLES `Document` WRITE;
/*!40000 ALTER TABLE `Document` DISABLE KEYS */;
INSERT INTO `Document` VALUES (1,'Test Document','Morbi leo risus, porta ac consectetur ac, vestibulum at eros. Donec sed odio dui. Aenean lacinia bibendum nulla sed consectetur. Nullam id dolor id nibh ultricies vehicula ut id elit. Integer posuere erat a ante venenatis dapibus posuere velit aliquet. Nullam quis risus eget urna mollis ornare vel eu leo. Vivamus sagittis lacus vel augue laoreet rutrum faucibus dolor auctor.',NULL,'2014-09-26 11:16:08','2010-07-07',NULL,'1_Test Document',NULL,NULL,'published','yes','yes','Wrong Link','no','https://bitcoin.org/bitcoin.pdf',NULL,0,'Records','Education','Plans');
/*!40000 ALTER TABLE `Document` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Section`
--

DROP TABLE IF EXISTS `Section`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Section` (
  `did` int(11) NOT NULL,
  `section` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`did`),
  CONSTRAINT `Section_ibfk_1` FOREIGN KEY (`did`) REFERENCES `Document` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Section`
--

LOCK TABLES `Section` WRITE;
/*!40000 ALTER TABLE `Section` DISABLE KEYS */;
/*!40000 ALTER TABLE `Section` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Submit`
--

DROP TABLE IF EXISTS `Submit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Submit` (
  `uid` int(11) NOT NULL,
  `did` int(11) NOT NULL,
  PRIMARY KEY (`uid`,`did`),
  KEY `did` (`did`),
  CONSTRAINT `Submit_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `User` (`id`),
  CONSTRAINT `Submit_ibfk_2` FOREIGN KEY (`did`) REFERENCES `Document` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Submit`
--

LOCK TABLES `Submit` WRITE;
/*!40000 ALTER TABLE `Submit` DISABLE KEYS */;
INSERT INTO `Submit` VALUES (1,1);
/*!40000 ALTER TABLE `Submit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `User` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `first` varchar(255) NOT NULL,
  `last` varchar(255) NOT NULL,
  `role` enum('User','Admin','Agency_Admin') DEFAULT NULL,
  `agency` enum('Aging','Buildings','Campaign Finance','Childrens Services','City Council','City Clerk','City Planning','Citywide Admin Svcs','Civilian Complaint','Comm - Police Corr','Community Assistance','Comptroller','Conflicts of Interest','Consumer Affairs','Contracts','Correction','Criminal Justice Coordinator','Cultural Affairs','DOI - Investigation','Design/Construction','Disabilities','District Atty, NY County','Districting Commission','Domestic Violence','Economic Development','Education, Dept. of','Elections, Board of','Emergency Mgmt.','Employment','Empowerment Zone','Environmental - DEP','Environmental - OEC','Environmental - ECB','Equal Employment','Film/Theatre','Finance','Fire','FISA','Health and Mental Hyg.','HealthStat','Homeless Services','Hospitals - HHC','Housing - HPD','Human Rights','Human Rsrcs - HRA','Immigrant Affairs','Independent Budget','Info. Tech. and Telecom.','Intergovernmental','International Affairs','Judiciary Committee','Juvenile Justice','Labor Relations','Landmarks','Law Department','Library - Brooklyn','Library - New York','Library - Queens','Loft Board','Management and Budget','Mayor','Metropolitan Transportation Authority','NYCERS','Operations','Parks and Recreation','Payroll Administration','Police','Police Pension Fund','Probation','Public Advocate','Public Health','Public Housing-NYCHA','Records','Rent Guidelines','Sanitation','School Construction','Small Business Svcs','Sports Commission','Standards and Appeal','Tax Appeals Tribunal','Tax Commission','Taxi and Limousine','Transportation','Trials and Hearings','Veterans - Military','Volunteer Center','Voter Assistance','Youth & Community') NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `date_joined` datetime DEFAULT NULL,
  `last_visited` date DEFAULT NULL,
  `visits` int(11) DEFAULT NULL,
  `remove` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES (1,'achen','pbkdf2:sha1:1000$bzv8DEKt$6da18a3a69b8bdd915795b2ce88a4291f3d0cec9','Alan','Chen','Admin','Records','achen@records.nyc.gov','123-123-1234','2014-09-06 00:00:00','2014-10-24',10,0),(2,'kcobb','pbkdf2:sha1:1000$zgC8pHW5$8da5fdb2e35a057f38502b1640765e9aa1c1f4a5','Ken','Cobb','Admin','Records','kcobb@records.nyc.gov','123-123-1234','2014-08-27 00:00:00','2014-08-27',0,1),(3,'rjoe','pbkdf2:sha1:1000$sJotivzr$7c1b9a8c3d6772573a9924411ed0e4a91bf6c299','Richard','Joe','Admin','Records','rjoe@records.nyc.gov','123-123-1232','2014-08-27 00:00:00','2014-08-27',0,0),(4,'cbruzzese','pbkdf2:sha1:1000$yAfl8tPg$4fe07e3bb53382f48b26de1d76284c5691e05c7c','Christine','Bruzzese','Admin','Records','cbruzzese@records.nyc.gov','345-345-5678','2014-08-27 00:00:00','2014-08-28',4,0),(5,'user','pbkdf2:sha1:1000$8bBLUK0A$0e9ba4b28c31403d1cd3730985fcb5c165abdfec','Joel','Castillo','User','Records','jcastillo@records.nyc.gov','123-123-1234','2014-08-27 00:00:00','2014-09-26',5,0),(6,'agency_admin','pbkdf2:sha1:1000$0OXqiyek$738f9ab7f29fc060bd9420e03ae2a74502345c71','Joel','Castillo','Agency_Admin','Records','jcastillo@nyu.edu','234-234-2365','2014-08-27 00:00:00','2014-09-26',6,0),(7,'admin','pbkdf2:sha1:1000$QhSoStkb$6c5c85f48b96150cf0361b78c94857c928e292ad','Joel','Castillo','Admin','Records','jcastillo@records.edu','345-475-2362','2014-08-27 00:00:00','2014-09-12',5,0),(8,'jrobbins','pbkdf2:sha1:1000$vaS6bSkj$14379cb29c06e6ae7748d6039010cc5b57c9ab3e','Julia','Robbins','User','Records','jrobbins@records.nyc.gov','212-788-8590','2014-08-28 00:00:00','2014-08-28',0,0),(9,'alvi','pbkdf2:sha1:1000$OAPNLPAH$3b2553084061b7ff28b4b3464b06c82d825254a0','Alvi','Kabir','User','Aging','alvi@nyu.edu','123-123-1233','2014-09-03 00:00:00','2014-09-03',0,0);
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-11-07 11:20:23
