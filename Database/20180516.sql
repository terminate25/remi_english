-- MySQL dump 10.16  Distrib 10.1.26-MariaDB, for Win32 (AMD64)
--
-- Host: localhost    Database: remi_english
-- ------------------------------------------------------
-- Server version	10.1.26-MariaDB

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
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` int(11) DEFAULT NULL,
  `title` longtext NOT NULL,
  `account_class` int(11) NOT NULL,
  `tax_class` int(11) NOT NULL,
  `is_cash` int(11) DEFAULT NULL,
  `settlement_date_type` int(11) DEFAULT NULL,
  `created_datetime` datetime(6) DEFAULT NULL,
  `updated_datetime` datetime(6) DEFAULT NULL,
  `deleted_flag` int(11) NOT NULL,
  `account_code` int(11) NOT NULL,
  `account_name` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `answer`
--

DROP TABLE IF EXISTS `answer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `answer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) NOT NULL,
  `answer` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answer`
--

LOCK TABLES `answer` WRITE;
/*!40000 ALTER TABLE `answer` DISABLE KEYS */;
INSERT INTO `answer` VALUES (89,90,'1'),(90,90,'2'),(91,90,'3'),(92,90,'4'),(93,91,'1'),(94,91,'2'),(95,91,'3333'),(96,91,'33333333'),(97,110,'a'),(98,110,'aa'),(99,110,'aaaaa'),(100,110,'bbbb'),(101,111,'cho '),(102,111,'aa'),(103,111,'aaa'),(104,111,'aaa');
/*!40000 ALTER TABLE `answer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_restriction`
--

DROP TABLE IF EXISTS `api_restriction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_restriction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(1024) NOT NULL,
  `need_owner_flag` int(11) NOT NULL,
  `created_datetime` datetime(6) NOT NULL,
  `updated_datetime` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_restriction`
--

LOCK TABLES `api_restriction` WRITE;
/*!40000 ALTER TABLE `api_restriction` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_restriction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `async_transaction`
--

DROP TABLE IF EXISTS `async_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `async_transaction` (
  `transaction_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `client_order` bigint(20) DEFAULT NULL,
  `prev_client_order` bigint(20) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `accepted_datetime` datetime(6) DEFAULT NULL,
  `started_datetime` datetime(6) DEFAULT NULL,
  `finished_datetime` datetime(6) DEFAULT NULL,
  `status` int(11) NOT NULL,
  `reason` longtext,
  `method` longtext,
  `resource_name` longtext,
  `params` longtext,
  `request_data` longtext,
  `result` longtext,
  PRIMARY KEY (`transaction_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `async_transaction`
--

LOCK TABLES `async_transaction` WRITE;
/*!40000 ALTER TABLE `async_transaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `async_transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `base_user_course`
--

DROP TABLE IF EXISTS `base_user_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `base_user_course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `course_id` int(11) NOT NULL,
  `is_done` tinyint(2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `base_user_course_pk_idx` (`user_id`),
  KEY `base_couser_pk_idx` (`course_id`),
  CONSTRAINT `base_couser_pk` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `base_user_course_pk` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `base_user_course`
--

LOCK TABLES `base_user_course` WRITE;
/*!40000 ALTER TABLE `base_user_course` DISABLE KEYS */;
INSERT INTO `base_user_course` VALUES (1,1,1,NULL);
/*!40000 ALTER TABLE `base_user_course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `base_user_lesson`
--

DROP TABLE IF EXISTS `base_user_lesson`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `base_user_lesson` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `lesson_id` int(11) DEFAULT NULL,
  `is_done` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id_lesson_pk_idx` (`user_id`),
  KEY `lesson_id_pk_idx` (`lesson_id`),
  CONSTRAINT `lesson_id_pk` FOREIGN KEY (`lesson_id`) REFERENCES `lesson` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_id_lesson_pk` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `base_user_lesson`
--

LOCK TABLES `base_user_lesson` WRITE;
/*!40000 ALTER TABLE `base_user_lesson` DISABLE KEYS */;
INSERT INTO `base_user_lesson` VALUES (1,1,1,0);
/*!40000 ALTER TABLE `base_user_lesson` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `base_user_level`
--

DROP TABLE IF EXISTS `base_user_level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `base_user_level` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `level_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `is_done` tinyint(2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `base_user_level_pk_idx` (`user_id`),
  KEY `base_user_level_level_k_idx` (`level_id`),
  CONSTRAINT `base_user_level_level_k` FOREIGN KEY (`level_id`) REFERENCES `level` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `base_user_level_pk` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `base_user_level`
--

LOCK TABLES `base_user_level` WRITE;
/*!40000 ALTER TABLE `base_user_level` DISABLE KEYS */;
INSERT INTO `base_user_level` VALUES (1,1,1,0);
/*!40000 ALTER TABLE `base_user_level` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `base_user_part`
--

DROP TABLE IF EXISTS `base_user_part`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `base_user_part` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `part_id` int(11) NOT NULL,
  `is_done` tinyint(4) NOT NULL COMMENT 'Is done: \n 0 - Unlocked \n 1 - Passed : When all tests and video passed\n \n',
  `created_datetime` datetime DEFAULT NULL,
  `updated_datetime` datetime DEFAULT NULL,
  `video` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `student_part_pk_idx` (`user_id`),
  KEY `student_part_id_pk_idx` (`part_id`),
  CONSTRAINT `part_xxx_user_pk` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `part_xxxx_pk` FOREIGN KEY (`part_id`) REFERENCES `part` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `base_user_part`
--

LOCK TABLES `base_user_part` WRITE;
/*!40000 ALTER TABLE `base_user_part` DISABLE KEYS */;
INSERT INTO `base_user_part` VALUES (1,1,1,0,NULL,NULL,1);
/*!40000 ALTER TABLE `base_user_part` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `base_user_step`
--

DROP TABLE IF EXISTS `base_user_step`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `base_user_step` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `test_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `part_id` int(11) DEFAULT NULL,
  `right_percent` int(11) DEFAULT '0',
  `right_number_question` int(11) DEFAULT '0',
  `implement_date` datetime DEFAULT NULL,
  `is_done` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=536 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `base_user_step`
--

LOCK TABLES `base_user_step` WRITE;
/*!40000 ALTER TABLE `base_user_step` DISABLE KEYS */;
INSERT INTO `base_user_step` VALUES (483,80,1,22,100,4,NULL,1),(484,80,1,22,100,5,NULL,1),(485,76,1,22,0,0,NULL,0),(486,76,1,22,0,0,NULL,0),(487,76,1,22,66,4,NULL,1),(488,76,1,22,50,1,NULL,1),(489,76,1,22,16,1,NULL,1),(490,76,1,22,0,0,NULL,0),(491,76,1,22,0,0,NULL,0),(492,76,1,22,0,0,NULL,0),(493,76,1,22,0,0,NULL,0),(494,76,1,22,0,0,NULL,0),(495,76,1,22,0,0,NULL,0),(496,76,1,22,100,2,NULL,1),(497,76,1,22,0,0,NULL,0),(498,76,1,22,0,0,NULL,0),(499,76,1,22,0,0,NULL,0),(500,76,1,22,0,0,NULL,0),(501,76,1,22,0,0,NULL,0),(502,76,1,22,0,0,NULL,0),(503,76,1,22,0,0,NULL,0),(504,76,1,22,0,0,NULL,0),(505,76,1,22,0,0,NULL,0),(506,76,1,22,0,0,NULL,0),(507,76,1,22,0,0,NULL,0),(508,76,1,22,0,0,NULL,0),(509,77,1,22,0,0,NULL,0),(510,77,1,22,0,0,NULL,0),(511,77,1,22,0,0,NULL,0),(512,77,1,22,0,0,NULL,0),(513,77,1,22,0,0,NULL,0),(514,77,1,22,100,8,NULL,1),(515,78,1,22,0,0,NULL,0),(516,78,1,22,0,0,NULL,0),(517,78,1,22,100,1,NULL,1),(518,78,1,22,100,1,NULL,1),(519,78,1,22,100,4,NULL,1),(520,76,1,22,71,5,NULL,1),(521,77,1,22,100,8,NULL,1),(522,79,1,22,0,0,NULL,0),(523,79,1,22,0,0,NULL,0),(524,79,1,22,0,0,NULL,0),(525,79,1,22,0,0,NULL,0),(526,79,1,22,0,0,NULL,0),(527,79,1,22,0,0,NULL,0),(528,77,1,22,100,8,NULL,1),(529,79,1,22,0,0,NULL,0),(530,80,1,22,100,6,NULL,1),(531,76,1,22,0,0,NULL,0),(532,76,1,22,20,1,NULL,1),(533,77,1,22,100,8,NULL,1),(534,78,1,22,100,3,NULL,1),(535,80,1,22,86,13,NULL,1);
/*!40000 ALTER TABLE `base_user_step` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text,
  `created_datetime` datetime DEFAULT NULL,
  `updated_datetime` datetime DEFAULT NULL,
  `content` text,
  `order` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES (1,'Course 1','2018-05-16 00:58:13','2018-05-16 01:29:14',NULL,1),(2,'Course 2','2018-05-16 02:06:52','2018-05-16 11:29:33',NULL,2),(3,'Course 3','2018-05-16 12:40:02','2018-05-16 12:40:02',NULL,3);
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `default_user`
--

DROP TABLE IF EXISTS `default_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `default_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `default_user`
--

LOCK TABLES `default_user` WRITE;
/*!40000 ALTER TABLE `default_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `default_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (4,'auth','group'),(2,'auth','permission'),(3,'auth','user'),(5,'contenttypes','contenttype'),(11,'default','account'),(60,'default','answer'),(35,'default','apirestriction'),(21,'default','asynctransaction'),(15,'default','authgroup'),(41,'default','authgrouppermissions'),(31,'default','authmetainfo'),(42,'default','authmetatype'),(20,'default','authpermission'),(48,'default','authuser'),(24,'default','authusergroups'),(22,'default','authuseruserpermissions'),(34,'default','basedataauthmetarel'),(29,'default','basedatametarel'),(56,'default','basestudentlesson'),(61,'default','basetestuser'),(9,'default','billdef'),(53,'default','bizbudget'),(7,'default','bizprospect'),(28,'default','bphistory'),(6,'default','bphistoryitem'),(30,'default','budget'),(13,'default','budgetinfo'),(39,'default','budgetplan'),(17,'default','cockpitrole'),(44,'default','currentcashbalance'),(23,'default','defaultuser'),(38,'default','demodefaultbudget'),(52,'default','djangoadminlog'),(51,'default','djangocontenttype'),(47,'default','djangomigrations'),(36,'default','djangosession'),(16,'default','fiscalperiod'),(46,'default','fiscalterm'),(14,'default','importhistory'),(32,'default','journalvoucher'),(58,'default','lesson'),(26,'default','loandef'),(59,'default','master'),(43,'default','metainfo'),(10,'default','metatype'),(54,'default','operationlog'),(50,'default','portalmenu'),(19,'default','portalmenurequirerole'),(27,'default','product'),(57,'default','question'),(8,'default','repeatablescheduledjournaldef'),(18,'default','scheduledjournal'),(33,'default','singlescheduledjournaldef'),(40,'default','tabledefinition'),(45,'default','target'),(25,'default','targetproductrel'),(12,'default','taxrate'),(62,'default','test'),(1,'default','user'),(49,'default','userfilter'),(37,'default','userrole'),(55,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2017-09-09 04:13:08.088904'),(2,'contenttypes','0002_remove_content_type_name','2017-09-09 04:13:08.121460'),(3,'auth','0001_initial','2017-09-09 04:13:08.335549'),(4,'auth','0002_alter_permission_name_max_length','2017-09-09 04:13:08.359710'),(5,'auth','0003_alter_user_email_max_length','2017-09-09 04:13:08.383110'),(6,'auth','0004_alter_user_username_opts','2017-09-09 04:13:08.393696'),(7,'auth','0005_alter_user_last_login_null','2017-09-09 04:13:08.415488'),(8,'auth','0006_require_contenttypes_0002','2017-09-09 04:13:08.417402'),(9,'auth','0007_alter_validators_add_error_messages','2017-09-09 04:13:08.427357'),(10,'auth','0008_alter_user_username_max_length','2017-09-09 04:13:08.451163'),(11,'default','0001_initial','2017-09-09 04:13:08.465945'),(12,'default','0002_auto_20170909_0336','2017-09-09 04:13:13.848431'),(13,'sessions','0001_initial','2017-09-09 04:13:13.851202'),(14,'default','0003_auto_20170927_1324','2017-09-27 13:24:37.139153'),(15,'default','0004_account_answer_apirestriction_asynctransaction_authgroup_authgrouppermissions_authpermission_authuse','2017-10-01 09:32:57.568038'),(16,'default','0005_basetestuser','2017-10-04 02:17:49.807020'),(17,'default','0006_test','2017-10-04 03:55:17.445686'),(18,'default','0002_auto_20171025_0523','2017-10-25 05:23:59.763484');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lesson`
--

DROP TABLE IF EXISTS `lesson`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lesson` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `level_id` int(11) DEFAULT NULL,
  `name` text,
  `created_datetime` datetime DEFAULT NULL,
  `updated_datetime` datetime DEFAULT NULL,
  `content` text,
  `order` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_idx` (`level_id`),
  KEY `id_idx_level_id` (`level_id`),
  CONSTRAINT `lesson_level_pk` FOREIGN KEY (`level_id`) REFERENCES `level` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lesson`
--

LOCK TABLES `lesson` WRITE;
/*!40000 ALTER TABLE `lesson` DISABLE KEYS */;
INSERT INTO `lesson` VALUES (1,1,'Lesson 1 Level 1 Course 1','2018-05-16 00:59:07','2018-05-16 00:59:07',NULL,1),(2,4,'Course 2 Level 2 Lesson 1','2018-05-16 12:53:22','2018-05-16 12:53:22',NULL,1);
/*!40000 ALTER TABLE `lesson` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `level`
--

DROP TABLE IF EXISTS `level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `level` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_id` int(11) NOT NULL,
  `name` text,
  `created_datetime` datetime DEFAULT NULL,
  `updated_datetime` datetime DEFAULT NULL,
  `order` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `level_course_pk_idx` (`course_id`),
  CONSTRAINT `level_course_pk` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `level`
--

LOCK TABLES `level` WRITE;
/*!40000 ALTER TABLE `level` DISABLE KEYS */;
INSERT INTO `level` VALUES (1,1,'Level 1 Course 1','2018-05-16 00:58:41','2018-05-16 00:58:41',1),(2,1,'Level 2 Course 1','2018-05-16 01:29:41','2018-05-16 01:29:41',2),(3,2,'Level 1 Course 2','2018-05-16 11:29:44','2018-05-16 11:29:44',1),(4,2,'Level 2 Course 2','2018-05-16 12:53:02','2018-05-16 12:53:02',2);
/*!40000 ALTER TABLE `level` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master`
--

DROP TABLE IF EXISTS `master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `master` (
  `master_id` int(11) NOT NULL,
  `mastertype` int(11) NOT NULL,
  `name` varchar(400) NOT NULL,
  `created_datetime` datetime DEFAULT NULL,
  `updated_datetime` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master`
--

LOCK TABLES `master` WRITE;
/*!40000 ALTER TABLE `master` DISABLE KEYS */;
INSERT INTO `master` VALUES (1,1,'Master',NULL,NULL,1),(3,1,'Question Type',NULL,NULL,3),(4,1,'Gender',NULL,NULL,4),(1,3,'Type 1 :  Question : Audio -  Answer: Image',NULL,NULL,9),(2,3,'Type 2 : Question : Image -  Answer: Audio',NULL,NULL,10),(3,3,'Type 3: Question : Image and Audio -  Answer: Audio',NULL,NULL,11),(4,3,'Type 4: Question : Image -  Answer: Audio',NULL,NULL,12),(5,3,'Type 5: Question: Audio - Answer: Text',NULL,NULL,13),(1,4,'Male',NULL,'2017-10-27 07:18:14',14),(4,4,'Female',NULL,'2017-10-25 14:21:33',15),(5,1,'roles',NULL,NULL,17),(1,5,'Admin',NULL,NULL,18),(2,5,'Student',NULL,NULL,19),(3,5,'Teacher',NULL,NULL,20),(4,5,'Manager',NULL,NULL,21),(7,4,'Others','2017-10-27 07:18:24','2017-10-27 07:18:24',32),(6,3,'Type 6:  Question : Image, Audio and Image hint -  Answer: Speak',NULL,NULL,33),(7,3,'Type 7:  Question : Video and Image hint -  Answer: Speak',NULL,NULL,34),(8,3,'Type 8:  Question : Video -  Answer: Audio',NULL,NULL,35),(5,5,'SuperAdmin',NULL,NULL,36);
/*!40000 ALTER TABLE `master` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `part`
--

DROP TABLE IF EXISTS `part`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `part` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lesson_id` int(11) NOT NULL,
  `name` text,
  `created_datetime` datetime DEFAULT NULL,
  `updated_datetime` datetime DEFAULT NULL,
  `content` text,
  `type` int(11) DEFAULT NULL,
  `summary` text,
  `order` int(11) DEFAULT NULL,
  `video` text,
  PRIMARY KEY (`id`),
  KEY `part_lesson_pk_idx` (`lesson_id`),
  CONSTRAINT `part_lesson_pk` FOREIGN KEY (`lesson_id`) REFERENCES `lesson` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `part`
--

LOCK TABLES `part` WRITE;
/*!40000 ALTER TABLE `part` DISABLE KEYS */;
INSERT INTO `part` VALUES (1,2,'Lesson 1 Level 1 Course 1',NULL,'2018-05-16 12:54:34','Lesson 1 Level 1 Course 1',NULL,'vnindex-2017-12-27-21_15_11.625742.csv',1,'Beautiful World - Wild Animals (Petar Milinković - Ashes Of Stars) [Short Film].mp4');
/*!40000 ALTER TABLE `part` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question`
--

DROP TABLE IF EXISTS `question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `part_id` int(11) NOT NULL,
  `name` text,
  `question` text,
  `answer` text,
  `created_datetime` datetime DEFAULT NULL,
  `updated_datetime` datetime DEFAULT NULL,
  `test_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `test_id_pk_idx` (`test_id`),
  CONSTRAINT `test_id_pk` FOREIGN KEY (`test_id`) REFERENCES `test` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question`
--

LOCK TABLES `question` WRITE;
/*!40000 ALTER TABLE `question` DISABLE KEYS */;
INSERT INTO `question` VALUES (1,1,NULL,'Beautiful World - Wild Animals (Petar Milinković - Ashes Of Stars) [Short Film].mp4','Screenshot (2).png',NULL,NULL,1);
/*!40000 ALTER TABLE `question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test`
--

DROP TABLE IF EXISTS `test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `part_id` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `question_number_goal` int(11) DEFAULT NULL,
  `question_percent_goal` int(11) DEFAULT NULL,
  `name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `test_part_id_pk_idx` (`part_id`),
  CONSTRAINT `test_part_id_pk` FOREIGN KEY (`part_id`) REFERENCES `part` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test`
--

LOCK TABLES `test` WRITE;
/*!40000 ALTER TABLE `test` DISABLE KEYS */;
INSERT INTO `test` VALUES (1,1,1,20,20,'Test 1');
/*!40000 ALTER TABLE `test` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login_name` varchar(64) NOT NULL,
  `password` blob,
  `user_name` varchar(64) DEFAULT NULL,
  `address` varchar(64) DEFAULT NULL,
  `phone` varchar(64) DEFAULT NULL,
  `email` varchar(64) DEFAULT NULL,
  `gender` int(11) NOT NULL,
  `created_datetime` datetime DEFAULT NULL,
  `updated_datetime` datetime DEFAULT NULL,
  `roles` int(3) DEFAULT NULL,
  `teacher_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `login_name` (`login_name`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','$2b$14$JY/y60siksuhcVA675RB9eFxzWdJP21QdWgh5Pd7o1M77u8YX//CK','admin','asdfasdfasf','2332423423','adfadsfasd',1,NULL,'2018-05-16 01:16:06',1,NULL),(65,'teacher 1','$2b$14$aTMeuLLxXsGWVbL8YX0giu10FTLqUOeVYnA2zYBXHWt3qHlJa1RP6','teacher 1','aaaa','aaaaa','aaaaaa',1,NULL,NULL,1,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-05-16 13:06:24
