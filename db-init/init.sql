CREATE DATABASE IF NOT EXISTS kandy_LMS;
USE kandy_LMS;

/*M!999999\- enable the sandbox mode */
-- MariaDB dump 10.19-11.4.3-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: kandy_LMS
-- ------------------------------------------------------
-- Server version	11.4.3-MariaDB-1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin` (
  `admin_id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_name` varchar(20) NOT NULL,
  `password` varchar(100) NOT NULL,
  `email` varchar(40) NOT NULL,
  PRIMARY KEY (`admin_id`),
  UNIQUE KEY `ix_admin_email` (`email`),
  UNIQUE KEY `ix_admin_admin_name` (`admin_name`),
  KEY `ix_admin_admin_id` (`admin_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES
(1,'thush','67215bebe2fe2737d90bb951347c6a0852a1f537','thushanmadhusanka3@gmail.com');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `branch`
--

DROP TABLE IF EXISTS `branch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `branch` (
  `branch_id` varchar(8) NOT NULL,
  `branch_name` varchar(20) NOT NULL,
  `address` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`address`)),
  `email` varchar(40) NOT NULL,
  `location` varchar(10) NOT NULL,
  `mobile` int(11) NOT NULL,
  `open_time` time NOT NULL,
  `close_time` time NOT NULL,
  `description` text DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `branch_manager_id` varchar(10) DEFAULT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`branch_id`),
  UNIQUE KEY `ix_branch_email` (`email`),
  UNIQUE KEY `ix_branch_branch_name` (`branch_name`),
  KEY `branch_manager_id` (`branch_manager_id`),
  KEY `ix_branch_mobile` (`mobile`),
  KEY `ix_branch_branch_id` (`branch_id`),
  CONSTRAINT `branch_ibfk_1` FOREIGN KEY (`branch_manager_id`) REFERENCES `branch_manager` (`manager_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `branch`
--

LOCK TABLES `branch` WRITE;
/*!40000 ALTER TABLE `branch` DISABLE KEYS */;
INSERT INTO `branch` VALUES
('SofzrblP','mainbranch','{\"line 1\": \"123 Main St\", \"line2\": \"Springfield\"}','mainbranch@example.com','gampha',1234567890,'09:00:00','17:00:00','Main branch of the company',1,'RX_gINRzdY','2024-10-08 08:03:31');
/*!40000 ALTER TABLE `branch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `branch_halls`
--

DROP TABLE IF EXISTS `branch_halls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `branch_halls` (
  `row_id` int(11) NOT NULL AUTO_INCREMENT,
  `hall_name` varchar(10) NOT NULL,
  `branch_id` varchar(8) DEFAULT NULL,
  PRIMARY KEY (`row_id`),
  KEY `ix_branch_halls_branch_id` (`branch_id`),
  KEY `ix_branch_halls_hall_name` (`hall_name`),
  CONSTRAINT `branch_halls_ibfk_1` FOREIGN KEY (`branch_id`) REFERENCES `branch` (`branch_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `branch_halls`
--

LOCK TABLES `branch_halls` WRITE;
/*!40000 ALTER TABLE `branch_halls` DISABLE KEYS */;
INSERT INTO `branch_halls` VALUES
(1,'Hall A','SofzrblP'),
(2,'Hall B','SofzrblP');
/*!40000 ALTER TABLE `branch_halls` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `branch_images`
--

DROP TABLE IF EXISTS `branch_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `branch_images` (
  `image_id` int(11) NOT NULL AUTO_INCREMENT,
  `image_url` text NOT NULL,
  `branch_id` varchar(8) DEFAULT NULL,
  PRIMARY KEY (`image_id`),
  KEY `ix_branch_images_branch_id` (`branch_id`),
  CONSTRAINT `branch_images_ibfk_1` FOREIGN KEY (`branch_id`) REFERENCES `branch` (`branch_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `branch_images`
--

LOCK TABLES `branch_images` WRITE;
/*!40000 ALTER TABLE `branch_images` DISABLE KEYS */;
INSERT INTO `branch_images` VALUES
(1,'https://example.com/image1.jpg','SofzrblP'),
(2,'https://example.com/image2.jpg','SofzrblP');
/*!40000 ALTER TABLE `branch_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `branch_manager`
--

DROP TABLE IF EXISTS `branch_manager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `branch_manager` (
  `manager_id` varchar(10) NOT NULL,
  `manager_name` varchar(30) NOT NULL,
  `manager_email` varchar(40) NOT NULL,
  PRIMARY KEY (`manager_id`),
  UNIQUE KEY `ix_branch_manager_manager_email` (`manager_email`),
  UNIQUE KEY `ix_branch_manager_manager_name` (`manager_name`),
  KEY `ix_branch_manager_manager_id` (`manager_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `branch_manager`
--

LOCK TABLES `branch_manager` WRITE;
/*!40000 ALTER TABLE `branch_manager` DISABLE KEYS */;
INSERT INTO `branch_manager` VALUES
('0EQODC8tKy','kamal','kamal@gmail.com'),
('RX_gINRzdY','nimal','nimal@gmail.com');
/*!40000 ALTER TABLE `branch_manager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `certificate_images_student`
--

DROP TABLE IF EXISTS `certificate_images_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `certificate_images_student` (
  `certificate_image_id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` varchar(15) DEFAULT NULL,
  `certificate_image_url` text NOT NULL,
  PRIMARY KEY (`certificate_image_id`),
  KEY `ix_certificate_images_student_certificate_image_id` (`certificate_image_id`),
  KEY `ix_certificate_images_student_student_id` (`student_id`),
  CONSTRAINT `certificate_images_student_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `certificate_images_student`
--

LOCK TABLES `certificate_images_student` WRITE;
/*!40000 ALTER TABLE `certificate_images_student` DISABLE KEYS */;
INSERT INTO `certificate_images_student` VALUES
(1,'235424822752505','https://fastly.picsum.photos/id/235/200/200.jpg?hmac=YnNmt_uSm-7R-s3j5I_di0aCpJqnfzRzeAzZCV-SS4w'),
(2,'235424822752505','http://image.oi/sdfasdfsdf.png');
/*!40000 ALTER TABLE `certificate_images_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class_branch`
--

DROP TABLE IF EXISTS `class_branch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `class_branch` (
  `class_id` varchar(36) NOT NULL,
  `branch_id` varchar(8) NOT NULL,
  PRIMARY KEY (`class_id`,`branch_id`),
  KEY `branch_id` (`branch_id`),
  CONSTRAINT `class_branch_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`),
  CONSTRAINT `class_branch_ibfk_2` FOREIGN KEY (`branch_id`) REFERENCES `branch` (`branch_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_branch`
--

LOCK TABLES `class_branch` WRITE;
/*!40000 ALTER TABLE `class_branch` DISABLE KEYS */;
/*!40000 ALTER TABLE `class_branch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class_fees`
--

DROP TABLE IF EXISTS `class_fees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `class_fees` (
  `class_id` varchar(36) NOT NULL,
  `class_type_id` int(11) NOT NULL,
  `class_fee` float NOT NULL,
  PRIMARY KEY (`class_id`,`class_type_id`),
  KEY `class_type_id` (`class_type_id`),
  CONSTRAINT `class_fees_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`),
  CONSTRAINT `class_fees_ibfk_2` FOREIGN KEY (`class_type_id`) REFERENCES `class_type` (`class_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_fees`
--

LOCK TABLES `class_fees` WRITE;
/*!40000 ALTER TABLE `class_fees` DISABLE KEYS */;
/*!40000 ALTER TABLE `class_fees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class_images`
--

DROP TABLE IF EXISTS `class_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `class_images` (
  `row_id` int(11) NOT NULL AUTO_INCREMENT,
  `class_id` varchar(36) DEFAULT NULL,
  `url` text NOT NULL,
  PRIMARY KEY (`row_id`),
  KEY `ix_class_images_class_id` (`class_id`),
  CONSTRAINT `class_images_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_images`
--

LOCK TABLES `class_images` WRITE;
/*!40000 ALTER TABLE `class_images` DISABLE KEYS */;
/*!40000 ALTER TABLE `class_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class_type`
--

DROP TABLE IF EXISTS `class_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `class_type` (
  `class_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `class_type` varchar(15) NOT NULL,
  PRIMARY KEY (`class_type_id`),
  UNIQUE KEY `class_type` (`class_type`),
  KEY `ix_class_type_class_type_id` (`class_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_type`
--

LOCK TABLES `class_type` WRITE;
/*!40000 ALTER TABLE `class_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `class_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classes`
--

DROP TABLE IF EXISTS `classes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `classes` (
  `class_id` varchar(36) NOT NULL,
  `class_name` varchar(25) NOT NULL,
  `teacher_id` varchar(36) DEFAULT NULL,
  `education_level_id` varchar(36) DEFAULT NULL,
  `class_type_id` int(11) DEFAULT NULL,
  `about` text DEFAULT NULL,
  `class_active` tinyint(1) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`class_id`),
  UNIQUE KEY `ix_classes_class_name` (`class_name`),
  KEY `teacher_id` (`teacher_id`),
  KEY `ix_classes_class_id` (`class_id`),
  KEY `ix_classes_education_level_id` (`education_level_id`),
  KEY `ix_classes_class_type_id` (`class_type_id`),
  CONSTRAINT `classes_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`teacher_id`),
  CONSTRAINT `classes_ibfk_2` FOREIGN KEY (`education_level_id`) REFERENCES `education_level` (`education_level_id`),
  CONSTRAINT `classes_ibfk_3` FOREIGN KEY (`class_type_id`) REFERENCES `class_type` (`class_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classes`
--

LOCK TABLES `classes` WRITE;
/*!40000 ALTER TABLE `classes` DISABLE KEYS */;
/*!40000 ALTER TABLE `classes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `education_level`
--

DROP TABLE IF EXISTS `education_level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `education_level` (
  `education_level_id` varchar(36) NOT NULL,
  `education_level_name` varchar(15) NOT NULL,
  PRIMARY KEY (`education_level_id`),
  KEY `ix_education_level_education_level_id` (`education_level_id`),
  KEY `ix_education_level_education_level_name` (`education_level_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `education_level`
--

LOCK TABLES `education_level` WRITE;
/*!40000 ALTER TABLE `education_level` DISABLE KEYS */;
INSERT INTO `education_level` VALUES
('02d7c5e0-c504-48de-bc1f-7184eacd65b9','grade 1'),
('7cc26716-4e3a-46ab-b40d-5de6cafadb9c','grade 1'),
('94128ecb-5544-4567-8036-babf3e93f3db','grade 1'),
('d0d36ac0-bfea-41b0-986f-23ec9e8f1bcf','grade 1'),
('3a90276a-cba1-43c5-a657-da8e64f164c0','grade 10'),
('d6235d5a-ffe2-4299-8e53-1e5abebf2ee9','grade 11');
/*!40000 ALTER TABLE `education_level` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `officer`
--

DROP TABLE IF EXISTS `officer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `officer` (
  `officer_id` varchar(15) NOT NULL,
  `officer_username` varchar(20) NOT NULL,
  `officer_firstname` varchar(15) NOT NULL,
  `officer_lastname` varchar(15) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  `officer_address` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`officer_address`)),
  `province` varchar(10) DEFAULT NULL,
  `district` varchar(10) DEFAULT NULL,
  `home_town` varchar(10) DEFAULT NULL,
  `officer_email` varchar(40) NOT NULL,
  `officer_gender` tinyint(1) DEFAULT NULL,
  `officer_mobile` int(11) NOT NULL,
  `branch_id` varchar(8) DEFAULT NULL,
  `officer_NIC` varchar(15) DEFAULT NULL,
  `officer_school` text DEFAULT NULL,
  `education_level_id` varchar(36) DEFAULT NULL,
  `officer_active` tinyint(1) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`officer_id`),
  UNIQUE KEY `officer_mobile` (`officer_mobile`),
  UNIQUE KEY `ix_officer_officer_email` (`officer_email`),
  UNIQUE KEY `ix_officer_officer_username` (`officer_username`),
  KEY `branch_id` (`branch_id`),
  KEY `ix_officer_education_level_id` (`education_level_id`),
  KEY `ix_officer_officer_firstname` (`officer_firstname`),
  KEY `ix_officer_officer_lastname` (`officer_lastname`),
  KEY `ix_officer_officer_id` (`officer_id`),
  CONSTRAINT `officer_ibfk_1` FOREIGN KEY (`branch_id`) REFERENCES `branch` (`branch_id`),
  CONSTRAINT `officer_ibfk_2` FOREIGN KEY (`education_level_id`) REFERENCES `education_level` (`education_level_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `officer`
--

LOCK TABLES `officer` WRITE;
/*!40000 ALTER TABLE `officer` DISABLE KEYS */;
INSERT INTO `officer` VALUES
('NgB4QtHQrErgoYT','ruwan-437ju','ruwan','darshana','5efb22dcc36cb11a1bfd0148ee1615cb49e00a26','{\"lane1\": \"road1\", \"lane2\": \"gampaha\"}','western','gampaha','gampaha','thushanmadhusanka3@gmail.com',1,775651884,'SofzrblP','200236503381','bandaranayake colledge','3a90276a-cba1-43c5-a657-da8e64f164c0',1,'2024-10-25 20:48:45');
/*!40000 ALTER TABLE `officer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `officer_certificate_images`
--

DROP TABLE IF EXISTS `officer_certificate_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `officer_certificate_images` (
  `row_id` int(11) NOT NULL AUTO_INCREMENT,
  `officer_id` varchar(15) NOT NULL,
  `image_url` text NOT NULL,
  PRIMARY KEY (`row_id`),
  KEY `ix_officer_certificate_images_officer_id` (`officer_id`),
  CONSTRAINT `officer_certificate_images_ibfk_1` FOREIGN KEY (`officer_id`) REFERENCES `officer` (`officer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `officer_certificate_images`
--

LOCK TABLES `officer_certificate_images` WRITE;
/*!40000 ALTER TABLE `officer_certificate_images` DISABLE KEYS */;
INSERT INTO `officer_certificate_images` VALUES
(5,'NgB4QtHQrErgoYT','https://example.com/sfdgsdf'),
(6,'NgB4QtHQrErgoYT','https://example.com/argdzfgdf');
/*!40000 ALTER TABLE `officer_certificate_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profile_images`
--

DROP TABLE IF EXISTS `profile_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `profile_images` (
  `profile_image_id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` varchar(15) DEFAULT NULL,
  `profile_image_url` text NOT NULL,
  PRIMARY KEY (`profile_image_id`),
  KEY `ix_profile_images_profile_image_id` (`profile_image_id`),
  KEY `ix_profile_images_student_id` (`student_id`),
  CONSTRAINT `profile_images_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profile_images`
--

LOCK TABLES `profile_images` WRITE;
/*!40000 ALTER TABLE `profile_images` DISABLE KEYS */;
INSERT INTO `profile_images` VALUES
(1,'235424822752505','https://fastly.picsum.photos/id/235/200/200.jpg?hmac=YnNmt_uSm-7R-s3j5I_di0aCpJqnfzRzeAzZCV-SS4w');
/*!40000 ALTER TABLE `profile_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student` (
  `student_id` varchar(15) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(80) NOT NULL,
  `firstname` varchar(15) NOT NULL,
  `lastname` varchar(15) NOT NULL,
  `email` varchar(40) NOT NULL,
  `address` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`address`)),
  `gender` tinyint(1) NOT NULL,
  `admission_free_is_paid` tinyint(1) NOT NULL,
  `mother_tung` varchar(10) DEFAULT NULL,
  `NIC` varchar(14) DEFAULT NULL,
  `school` varchar(50) DEFAULT NULL,
  `mobile` int(11) DEFAULT NULL,
  `education_level_id` varchar(36) DEFAULT NULL,
  `branch_id` varchar(8) DEFAULT NULL,
  `created` datetime NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `mobile` (`mobile`),
  KEY `ix_student_student_id` (`student_id`),
  KEY `ix_student_education_level_id` (`education_level_id`),
  KEY `ix_student_branch_id` (`branch_id`),
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`education_level_id`) REFERENCES `education_level` (`education_level_id`),
  CONSTRAINT `student_ibfk_2` FOREIGN KEY (`branch_id`) REFERENCES `branch` (`branch_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES
('235424822752505','thush-90tfp','2e7d951fba17083b15037a9a77a7868382a8bcad','thush','madhu','thushanmadhusanka3@gmail.com','{\"line1\": \"udugampola\", \"line2\": \"udugampola\", \"city\": \"gampaha\"}',1,1,'sinhala','200126302298','senarath paranavithana collage',784514770,'3a90276a-cba1-43c5-a657-da8e64f164c0','sofzrblp','2024-10-26 07:10:20',1);
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_parents`
--

DROP TABLE IF EXISTS `student_parents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student_parents` (
  `row_id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` varchar(15) DEFAULT NULL,
  `father_name` varchar(25) DEFAULT NULL,
  `father_mobile` int(11) DEFAULT NULL,
  `father_email` varchar(40) DEFAULT NULL,
  `father_occupation` varchar(15) DEFAULT NULL,
  `father_address` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`father_address`)),
  `mother_name` varchar(25) DEFAULT NULL,
  `mother_mobile` int(11) DEFAULT NULL,
  `mother_email` varchar(40) DEFAULT NULL,
  `mother_occupation` varchar(15) DEFAULT NULL,
  `mother_address` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`mother_address`)),
  `info_send` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`row_id`),
  UNIQUE KEY `father_mobile` (`father_mobile`),
  UNIQUE KEY `father_email` (`father_email`),
  UNIQUE KEY `mother_mobile` (`mother_mobile`),
  UNIQUE KEY `mother_email` (`mother_email`),
  KEY `ix_student_parents_row_id` (`row_id`),
  KEY `ix_student_parents_student_id` (`student_id`),
  CONSTRAINT `student_parents_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_parents`
--

LOCK TABLES `student_parents` WRITE;
/*!40000 ALTER TABLE `student_parents` DISABLE KEYS */;
INSERT INTO `student_parents` VALUES
(1,'235424822752505','john sr',1234567891,'johnr@example.com','engineer','{\"street\": \"123 Main St\", \"city\": \"Springfield\", \"state\": \"IL\"}','jane ',1234567091,'jane@example.com','teacher','{\"street\": \"123 Main St\", \"city\": \"Springfield\", \"state\": \"IL\"}',1);
/*!40000 ALTER TABLE `student_parents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_siblings`
--

DROP TABLE IF EXISTS `student_siblings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student_siblings` (
  `row_id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` varchar(15) DEFAULT NULL,
  `name` varchar(40) NOT NULL,
  `DOB` date DEFAULT NULL,
  `gender` tinyint(1) NOT NULL,
  `mobile` int(11) DEFAULT NULL,
  PRIMARY KEY (`row_id`),
  KEY `ix_student_siblings_student_id` (`student_id`),
  KEY `ix_student_siblings_row_id` (`row_id`),
  CONSTRAINT `student_siblings_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_siblings`
--

LOCK TABLES `student_siblings` WRITE;
/*!40000 ALTER TABLE `student_siblings` DISABLE KEYS */;
INSERT INTO `student_siblings` VALUES
(1,'235424822752505','jane doe ','2005-05-15',0,1234567890);
/*!40000 ALTER TABLE `student_siblings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher`
--

DROP TABLE IF EXISTS `teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teacher` (
  `teacher_id` varchar(36) NOT NULL,
  `teacher_username` varchar(20) NOT NULL,
  `teacher_password` varchar(80) NOT NULL,
  `teacher_firstname` varchar(15) NOT NULL,
  `teacher_lastname` varchar(15) NOT NULL,
  `teacher_email` varchar(40) NOT NULL,
  `teacher_mobile` int(11) NOT NULL,
  `subject` varchar(15) NOT NULL,
  `branch_id` varchar(8) DEFAULT NULL,
  `education_level_id` varchar(36) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `teacher_address` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`teacher_address`)),
  `province` varchar(10) DEFAULT NULL,
  `district` varchar(10) DEFAULT NULL,
  `home_town` varchar(10) DEFAULT NULL,
  `teacher_gender` tinyint(1) DEFAULT NULL,
  `teacher_NIC` varchar(15) DEFAULT NULL,
  `teacher_school` varchar(50) DEFAULT NULL,
  `teacher_description` text DEFAULT NULL,
  `teacher_active` tinyint(1) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`teacher_id`),
  UNIQUE KEY `ix_teacher_teacher_username` (`teacher_username`),
  KEY `branch_id` (`branch_id`),
  KEY `ix_teacher_teacher_lastname` (`teacher_lastname`),
  KEY `ix_teacher_subject` (`subject`),
  KEY `ix_teacher_teacher_id` (`teacher_id`),
  KEY `ix_teacher_education_level_id` (`education_level_id`),
  KEY `ix_teacher_teacher_email` (`teacher_email`),
  KEY `ix_teacher_teacher_mobile` (`teacher_mobile`),
  KEY `ix_teacher_teacher_firstname` (`teacher_firstname`),
  CONSTRAINT `teacher_ibfk_1` FOREIGN KEY (`branch_id`) REFERENCES `branch` (`branch_id`),
  CONSTRAINT `teacher_ibfk_2` FOREIGN KEY (`education_level_id`) REFERENCES `education_level` (`education_level_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher`
--

LOCK TABLES `teacher` WRITE;
/*!40000 ALTER TABLE `teacher` DISABLE KEYS */;
INSERT INTO `teacher` VALUES
('7cbed3c2-cb9d-425a-bfe3-3284fdcc3df6','ruwan-u2qxb','1e344354aec431505a9c28cf5e8e4d2be9aff084','ruwan','darshana','ruwan@gmail.com',775651884,'combine maths','SofzrblP','3a90276a-cba1-43c5-a657-da8e64f164c0',NULL,'{\"lane1\": \"road1\", \"lane2\": \"gampaha\"}','western','gampaha','gampaha',1,'200236503381','bandaranayake colledge','combine maths is awsome',0,'2024-10-26 07:24:42');
/*!40000 ALTER TABLE `teacher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher_certificate_images`
--

DROP TABLE IF EXISTS `teacher_certificate_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teacher_certificate_images` (
  `row_id` int(11) NOT NULL AUTO_INCREMENT,
  `teacher_id` varchar(36) NOT NULL,
  `image_url` text NOT NULL,
  PRIMARY KEY (`row_id`),
  KEY `ix_teacher_certificate_images_teacher_id` (`teacher_id`),
  CONSTRAINT `teacher_certificate_images_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`teacher_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher_certificate_images`
--

LOCK TABLES `teacher_certificate_images` WRITE;
/*!40000 ALTER TABLE `teacher_certificate_images` DISABLE KEYS */;
INSERT INTO `teacher_certificate_images` VALUES
(1,'7cbed3c2-cb9d-425a-bfe3-3284fdcc3df6','https://example.com/sfdgsdf'),
(2,'7cbed3c2-cb9d-425a-bfe3-3284fdcc3df6','https://example.com/argdzfgdf');
/*!40000 ALTER TABLE `teacher_certificate_images` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2024-10-26  9:00:40
