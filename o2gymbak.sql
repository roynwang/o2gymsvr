-- MySQL dump 10.13  Distrib 5.6.17, for osx10.7 (x86_64)
--
-- Host: localhost    Database: o2gym
-- ------------------------------------------------------
-- Server version	5.6.17

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permission_group_id_689710a9a73b7457_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `auth__content_type_id_508cf46651277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add recommend',7,'add_recommend'),(20,'Can change recommend',7,'change_recommend'),(21,'Can delete recommend',7,'delete_recommend'),(22,'Can add user',8,'add_user'),(23,'Can change user',8,'change_user'),(24,'Can delete user',8,'delete_user'),(25,'Can add time line',9,'add_timeline'),(26,'Can change time line',9,'change_timeline'),(27,'Can delete time line',9,'delete_timeline'),(28,'Can add working days',10,'add_workingdays'),(29,'Can change working days',10,'change_workingdays'),(30,'Can delete working days',10,'delete_workingdays'),(31,'Can add weibo',11,'add_weibo'),(32,'Can change weibo',11,'change_weibo'),(33,'Can delete weibo',11,'delete_weibo'),(34,'Can add long weibo',12,'add_longweibo'),(35,'Can change long weibo',12,'change_longweibo'),(36,'Can delete long weibo',12,'delete_longweibo'),(37,'Can add images',13,'add_images'),(38,'Can change images',13,'change_images'),(39,'Can delete images',13,'delete_images'),(40,'Can add order',14,'add_order'),(41,'Can change order',14,'change_order'),(42,'Can delete order',14,'delete_order'),(43,'Can add product',15,'add_product'),(44,'Can change product',15,'change_product'),(45,'Can delete product',15,'delete_product'),(46,'Can add course',16,'add_course'),(47,'Can change course',16,'change_course'),(48,'Can delete course',16,'delete_course'),(49,'Can add gym',17,'add_gym'),(50,'Can change gym',17,'change_gym'),(51,'Can delete gym',17,'delete_gym'),(52,'Can add schedule',18,'add_schedule'),(53,'Can change schedule',18,'change_schedule'),(54,'Can delete schedule',18,'delete_schedule'),(55,'Can add body eval',19,'add_bodyeval'),(56,'Can change body eval',19,'change_bodyeval'),(57,'Can delete body eval',19,'delete_bodyeval'),(58,'Can add body eval options',20,'add_bodyevaloptions'),(59,'Can change body eval options',20,'change_bodyevaloptions'),(60,'Can delete body eval options',20,'delete_bodyevaloptions'),(61,'Can add train',21,'add_train'),(62,'Can change train',21,'change_train'),(63,'Can delete train',21,'delete_train'),(64,'Can add sms',22,'add_sms'),(65,'Can change sms',22,'change_sms'),(66,'Can delete sms',22,'delete_sms');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$20000$YaqEzoAYu9wH$8OzrmcuwJvbSd9WOQO6HuuVhDw69o/d1IU8X507E4S8=',NULL,0,'alex','','','',0,1,'2015-09-04 10:39:58'),(2,'pbkdf2_sha256$20000$qttSFSe3PKPt$fGQ3+Ph4DKtSKcRPcogSX7CQfdeZiesHfdGZtfW/INs=',NULL,0,'royn','','','',0,1,'2015-09-04 10:39:58'),(9,'pbkdf2_sha256$20000$k1cCXVoMJY3q$1QmJLrIpTj2uHH98RmqeR0fT3LECQbMrEFxobrk1sZ0=',NULL,0,'18612261069','','','',0,1,'2015-09-18 10:12:06'),(10,'pbkdf2_sha256$20000$K39PhkEexqXx$A8Clb3Tg+/1IxZr8RThWCrNSfODhSzP/Zj/EhiVnITg=',NULL,0,'18311286007','','','',0,1,'2015-09-21 06:15:56');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_permissi_user_id_7f0938558328534a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `business_bodyeval`
--

DROP TABLE IF EXISTS `business_bodyeval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `business_bodyeval` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `date` date NOT NULL,
  `option` varchar(64) NOT NULL,
  `value` varchar(64) NOT NULL,
  `unit` varchar(64) NOT NULL,
  `group` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `business_bodyeval`
--

LOCK TABLES `business_bodyeval` WRITE;
/*!40000 ALTER TABLE `business_bodyeval` DISABLE KEYS */;
INSERT INTO `business_bodyeval` VALUES (2,'alex','2015-09-14','身高','185','cm','1.基础信息'),(3,'alex','2015-09-14','体重','192','kg','1.基础信息'),(4,'alex','2015-09-14','胸围','356','cm','1.基础信息'),(5,'alex','2015-09-14','身高','134','cm','1.基础信息'),(6,'alex','2015-09-14','体重','246','kg','1.基础信息'),(7,'alex','2015-09-14','胸围','789','cm','1.基础信息'),(8,'alex','2015-09-14','身高','190','cm','1.基础信息'),(9,'alex','2015-09-14','体重','190','kg','1.基础信息'),(10,'alex','2015-09-14','胸围','190','cm','1.基础信息'),(11,'royn','2015-09-16','身高','180','cm','1.基础信息'),(12,'royn','2015-09-16','体重','75','kg','1.基础信息'),(13,'royn','2015-09-16','胸围','100','cm','1.基础信息'),(14,'18612261069','2015-09-18','身高','180','cm','1.基础信息'),(15,'18612261069','2015-09-18','体重','20','kg','1.基础信息'),(16,'18612261069','2015-09-18','胸围','110','cm','1.基础信息');
/*!40000 ALTER TABLE `business_bodyeval` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `business_bodyevaloptions`
--

DROP TABLE IF EXISTS `business_bodyevaloptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `business_bodyevaloptions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `option` varchar(64) NOT NULL,
  `unit` varchar(64) NOT NULL,
  `group` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `business_bodyevaloptions`
--

LOCK TABLES `business_bodyevaloptions` WRITE;
/*!40000 ALTER TABLE `business_bodyevaloptions` DISABLE KEYS */;
INSERT INTO `business_bodyevaloptions` VALUES (1,'身高','cm','1.基础信息'),(2,'体重','kg','1.基础信息'),(3,'胸围','cm','1.基础信息');
/*!40000 ALTER TABLE `business_bodyevaloptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `business_course`
--

DROP TABLE IF EXISTS `business_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `business_course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(32) NOT NULL,
  `brief` varchar(1024) NOT NULL,
  `price` int(11) NOT NULL,
  `pic` varchar(256) NOT NULL,
  `gym_id` varchar(32) NOT NULL,
  `recommand_p` int(11) DEFAULT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `business_course_gym_id_6231e46bd5d73e27_fk_business_gym_name` (`gym_id`),
  CONSTRAINT `business_course_gym_id_6231e46bd5d73e27_fk_business_gym_name` FOREIGN KEY (`gym_id`) REFERENCES `business_gym` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `business_course`
--

LOCK TABLES `business_course` WRITE;
/*!40000 ALTER TABLE `business_course` DISABLE KEYS */;
/*!40000 ALTER TABLE `business_course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `business_course_coach`
--

DROP TABLE IF EXISTS `business_course_coach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `business_course_coach` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `course_id` (`course_id`,`user_id`),
  KEY `business_course_coach_user_id_7076384118dff645_fk_usr_user_id` (`user_id`),
  CONSTRAINT `business_course_coach_user_id_7076384118dff645_fk_usr_user_id` FOREIGN KEY (`user_id`) REFERENCES `usr_user` (`id`),
  CONSTRAINT `business_course_course_id_4e7cdd921cc7b687_fk_business_course_id` FOREIGN KEY (`course_id`) REFERENCES `business_course` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `business_course_coach`
--

LOCK TABLES `business_course_coach` WRITE;
/*!40000 ALTER TABLE `business_course_coach` DISABLE KEYS */;
/*!40000 ALTER TABLE `business_course_coach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `business_course_student`
--

DROP TABLE IF EXISTS `business_course_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `business_course_student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `course_id` (`course_id`,`user_id`),
  KEY `business_course_student_user_id_17e3eddcd0f75232_fk_usr_user_id` (`user_id`),
  CONSTRAINT `business_course_course_id_79a475568190c842_fk_business_course_id` FOREIGN KEY (`course_id`) REFERENCES `business_course` (`id`),
  CONSTRAINT `business_course_student_user_id_17e3eddcd0f75232_fk_usr_user_id` FOREIGN KEY (`user_id`) REFERENCES `usr_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `business_course_student`
--

LOCK TABLES `business_course_student` WRITE;
/*!40000 ALTER TABLE `business_course_student` DISABLE KEYS */;
/*!40000 ALTER TABLE `business_course_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `business_gym`
--

DROP TABLE IF EXISTS `business_gym`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `business_gym` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `introduction` varchar(1024) NOT NULL,
  `imgs` varchar(1024) NOT NULL,
  `recommand_p` int(11) DEFAULT NULL,
  `address` varchar(256) NOT NULL,
  `mapid` int(11) NOT NULL,
  `distance` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `business_gym`
--

LOCK TABLES `business_gym` WRITE;
/*!40000 ALTER TABLE `business_gym` DISABLE KEYS */;
INSERT INTO `business_gym` VALUES (1,'西山华府游泳健身会所','滋润不油腻的小蜜蜂日霜会员新低价','[\"http://viet.nam.travel/wp-content/uploads/2014/09/gyms-in-vietnam.jpg\"]',NULL,'海淀区 马连洼 西山华府',1,0);
/*!40000 ALTER TABLE `business_gym` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `business_gym_coaches`
--

DROP TABLE IF EXISTS `business_gym_coaches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `business_gym_coaches` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gym_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `gym_id` (`gym_id`,`user_id`),
  KEY `business_gym_coaches_user_id_72a6a6f0e91cbed2_fk_usr_user_id` (`user_id`),
  CONSTRAINT `business_gym_coaches_gym_id_60b407e2182c38fd_fk_business_gym_id` FOREIGN KEY (`gym_id`) REFERENCES `business_gym` (`id`),
  CONSTRAINT `business_gym_coaches_user_id_72a6a6f0e91cbed2_fk_usr_user_id` FOREIGN KEY (`user_id`) REFERENCES `usr_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `business_gym_coaches`
--

LOCK TABLES `business_gym_coaches` WRITE;
/*!40000 ALTER TABLE `business_gym_coaches` DISABLE KEYS */;
INSERT INTO `business_gym_coaches` VALUES (14,1,1),(13,1,8);
/*!40000 ALTER TABLE `business_gym_coaches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `business_schedule`
--

DROP TABLE IF EXISTS `business_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `business_schedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `hour` int(11) NOT NULL,
  `comment` varchar(1024) NOT NULL,
  `feedback` varchar(1024) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `coach_id` int(11) NOT NULL,
  `custom_id` int(11) NOT NULL,
  `created` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `done` tinyint(1) NOT NULL,
  `rate` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `business_schedule_order_id_1bf741cd6a5dc2a8_fk_order_order_id` (`order_id`),
  KEY `business_schedule_coach_id_1fb4f947da649052_fk_usr_user_id` (`coach_id`),
  KEY `business_schedule_custom_id_2c5d73d6ccce4c1a_fk_usr_user_id` (`custom_id`),
  CONSTRAINT `business_schedule_coach_id_1fb4f947da649052_fk_usr_user_id` FOREIGN KEY (`coach_id`) REFERENCES `usr_user` (`id`),
  CONSTRAINT `business_schedule_custom_id_2c5d73d6ccce4c1a_fk_usr_user_id` FOREIGN KEY (`custom_id`) REFERENCES `usr_user` (`id`),
  CONSTRAINT `business_schedule_order_id_1bf741cd6a5dc2a8_fk_order_order_id` FOREIGN KEY (`order_id`) REFERENCES `order_order` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `business_schedule`
--

LOCK TABLES `business_schedule` WRITE;
/*!40000 ALTER TABLE `business_schedule` DISABLE KEYS */;
INSERT INTO `business_schedule` VALUES (35,'2015-09-01',0,'很好的','',1,1,2,'2015-09-13 17:40:15',0,1,40),(39,'2015-09-02',20,'','',1,1,2,'2015-09-13 17:41:02',0,1,40),(40,'2015-09-03',2,'','',1,1,2,'2015-09-14 17:39:35',0,1,35),(44,'2015-09-09',0,'','',13,1,2,'2015-09-14 17:41:56',0,1,45),(46,'2015-09-10',0,'','',15,1,2,'2015-09-08 10:17:39',0,0,NULL),(47,'2015-09-11',2,'','',15,1,2,'2015-09-08 10:17:39',0,0,NULL),(48,'2015-09-09',2,'好评','',16,1,2,'2015-09-16 13:57:58',0,1,40),(49,'2015-09-10',8,'','',17,1,1,'2015-09-08 16:09:31',0,0,NULL),(50,'2015-09-23',11,'','',17,1,1,'2015-09-08 16:09:31',0,0,NULL),(51,'2015-09-24',13,'','',17,1,1,'2015-09-08 16:09:31',0,0,NULL),(53,'2015-09-24',18,'','',18,1,2,'2015-09-14 09:41:32',0,0,NULL),(54,'2015-09-25',7,'','',18,1,2,'2015-09-14 09:41:32',0,0,NULL),(55,'2015-09-30',2,'','',18,1,2,'2015-09-14 09:42:19',0,0,NULL),(56,'2015-09-17',3,'','',19,1,2,'2015-09-17 08:36:38',0,1,NULL),(57,'2015-09-22',2,'','',14,1,2,'2015-09-16 09:27:15',0,0,NULL),(58,'2015-09-17',12,'','',20,1,2,'2015-09-16 09:33:10',0,0,NULL),(60,'2015-09-23',8,'','',21,1,7,'2015-09-18 10:17:58',0,0,NULL),(64,'2015-09-20',6,'','',21,1,7,'2015-09-18 10:23:12',0,0,NULL),(67,'2015-09-24',8,'','',22,1,7,'2015-09-18 13:01:41',0,0,NULL),(68,'2015-09-23',17,'','',22,1,7,'2015-09-18 13:01:41',0,0,NULL),(69,'2015-09-19',8,'挺好','',23,1,7,'2015-09-26 13:55:16',0,1,35),(70,'2015-09-22',17,'','',23,1,7,'2015-09-18 13:12:16',0,0,NULL),(71,'2015-09-26',24,'','',23,1,7,'2015-09-18 13:12:16',0,0,NULL),(72,'2015-09-20',0,'','',24,1,7,'2015-09-19 12:54:04',0,0,NULL),(73,'2015-09-23',1,'','',25,1,7,'2015-09-19 18:28:01',0,0,NULL),(74,'2015-09-23',6,'','',26,1,7,'2015-09-19 18:29:14',0,0,NULL),(75,'2015-09-23',21,'','',28,1,7,'2015-09-19 18:32:19',0,0,NULL),(76,'2015-09-25',2,'','',29,1,7,'2015-09-19 18:39:27',0,0,NULL),(77,'2015-09-24',2,'','',30,1,7,'2015-09-19 18:42:12',0,0,NULL),(78,'2015-09-24',21,'','',31,1,7,'2015-09-19 18:48:24',0,0,NULL),(79,'2015-09-25',12,'','',32,1,7,'2015-09-19 18:49:56',0,0,NULL),(80,'2015-09-24',6,'','',33,1,7,'2015-09-19 18:54:03',0,0,NULL),(81,'2015-09-22',21,'','',34,1,7,'2015-09-20 03:30:09',0,0,NULL),(82,'2015-09-23',13,'','',35,1,7,'2015-09-20 03:41:52',0,0,NULL),(83,'2015-09-24',23,'','',36,1,7,'2015-09-20 03:42:24',0,0,NULL),(84,'2015-09-24',16,'','',37,1,7,'2015-09-20 03:45:17',0,0,NULL),(85,'2015-09-24',11,'','',37,1,7,'2015-09-20 03:46:02',0,0,NULL),(86,'2015-09-23',15,'','',38,1,8,'2015-09-21 06:16:46',0,0,NULL),(87,'2015-09-25',3,'','',39,8,7,'2015-09-21 07:17:30',0,0,NULL),(88,'2015-09-23',12,'','',40,8,7,'2015-09-26 14:38:14',0,1,NULL),(89,'2015-09-25',22,'','',41,1,7,'2015-09-23 08:36:51',0,0,NULL),(90,'2015-09-25',18,'','',42,1,7,'2015-09-23 08:37:25',0,0,NULL),(91,'2015-09-25',20,'','',21,1,7,'2015-09-23 09:23:11',0,0,NULL),(92,'2015-09-25',15,'','',22,1,7,'2015-09-23 09:25:40',0,0,NULL),(93,'2015-09-25',10,'','',43,1,7,'2015-09-24 08:58:05',0,0,NULL),(94,'2015-09-26',7,'','',43,1,7,'2015-09-24 08:58:05',0,0,NULL),(95,'2015-09-29',7,'','',43,1,7,'2015-09-24 08:58:05',0,0,NULL),(96,'2015-09-27',0,'','',45,8,7,'2015-09-26 14:39:47',0,0,NULL),(97,'2015-09-29',1,'','',45,8,7,'2015-09-26 14:39:47',0,0,NULL),(98,'2015-10-01',12,'','',45,8,7,'2015-09-26 14:39:47',0,0,NULL);
/*!40000 ALTER TABLE `business_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `business_train`
--

DROP TABLE IF EXISTS `business_train`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `business_train` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `weight` varchar(64) NOT NULL,
  `repeattimes` varchar(64) NOT NULL,
  `groupid` int(11) NOT NULL,
  `action_name` varchar(64) NOT NULL,
  `action_order` int(11) NOT NULL,
  `course_id` int(11) DEFAULT NULL,
  `date` date NOT NULL,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `business_train_course_id_46db80dd043c00_fk_business_schedule_id` (`course_id`),
  CONSTRAINT `business_train_course_id_46db80dd043c00_fk_business_schedule_id` FOREIGN KEY (`course_id`) REFERENCES `business_schedule` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `business_train`
--

LOCK TABLES `business_train` WRITE;
/*!40000 ALTER TABLE `business_train` DISABLE KEYS */;
INSERT INTO `business_train` VALUES (1,'1','2',0,'撒地方',1,40,'2015-09-15','alex'),(2,'10','10',0,'阿三地方',0,40,'2015-09-15','alex'),(3,'10','10',0,'阿萨德f',0,40,'2015-09-15','alex'),(4,'100','100',0,'双方深蹲',0,40,'2015-09-15','alex'),(5,'100','1',0,'撒地方',0,44,'2015-09-15','alex'),(6,'10','10',0,'我腿',0,NULL,'2015-09-16','royn'),(7,'20','20',1,'我腿',0,NULL,'2015-09-16','royn'),(8,'10','10',0,'三分',0,NULL,'2015-09-16','royn'),(9,'10','10',1,'name',1,NULL,'2015-09-16','alex'),(10,'10','10',0,'三分',0,NULL,'2015-09-16','royn'),(13,'10','10',0,'哈哈哈',0,NULL,'2015-09-16','royn'),(14,'10','10',0,'0916',0,48,'2015-09-16','alex'),(15,'10','10',0,'动作2',1,56,'2015-09-17','alex'),(16,'10','10',0,'好',0,56,'2015-09-17','alex'),(17,'10','10',0,'卧推',0,NULL,'2015-09-18','18612261069'),(18,'19','15',0,'给风格',0,NULL,'2015-09-24','18612261069'),(19,'10','10',0,'vvvshbs',1,88,'2015-09-26','18612261069'),(20,'10','10',0,'gavv',0,88,'2015-09-26','18612261069');
/*!40000 ALTER TABLE `business_train` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `djang_content_type_id_697914295151027a_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `djang_content_type_id_697914295151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
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
  UNIQUE KEY `django_content_type_app_label_45f3b1d93ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(19,'business','bodyeval'),(20,'business','bodyevaloptions'),(16,'business','course'),(17,'business','gym'),(18,'business','schedule'),(21,'business','train'),(5,'contenttypes','contenttype'),(14,'order','order'),(15,'order','product'),(7,'recommend','recommend'),(6,'sessions','session'),(22,'sms','sms'),(9,'usr','timeline'),(8,'usr','user'),(10,'usr','workingdays'),(13,'weibo','images'),(12,'weibo','longweibo'),(11,'weibo','weibo');
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
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2015-09-04 10:37:46'),(2,'auth','0001_initial','2015-09-04 10:37:46'),(3,'admin','0001_initial','2015-09-04 10:37:46'),(4,'contenttypes','0002_remove_content_type_name','2015-09-04 10:37:47'),(5,'auth','0002_alter_permission_name_max_length','2015-09-04 10:37:47'),(6,'auth','0003_alter_user_email_max_length','2015-09-04 10:37:47'),(7,'auth','0004_alter_user_username_opts','2015-09-04 10:37:47'),(8,'auth','0005_alter_user_last_login_null','2015-09-04 10:37:47'),(9,'auth','0006_require_contenttypes_0002','2015-09-04 10:37:47'),(10,'sessions','0001_initial','2015-09-04 10:37:47'),(11,'business','0001_initial','2015-09-13 16:16:07'),(12,'sms','0001_initial','2015-09-17 10:25:43');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_order`
--

DROP TABLE IF EXISTS `order_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `gym_id` varchar(32) DEFAULT NULL,
  `custom_id` varchar(64) DEFAULT NULL,
  `coach_id` varchar(64) DEFAULT NULL,
  `billid` bigint(20) NOT NULL,
  `paidtime` datetime DEFAULT NULL,
  `status` varchar(32) NOT NULL,
  `parentorder_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `amount` int(11) NOT NULL,
  `channel` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_order_gym_id_196cd238bd689be6_fk_business_gym_name` (`gym_id`),
  KEY `order_order_custom_id_185f27e9de4b2e63_fk_usr_user_name` (`custom_id`),
  KEY `order_order_coach_id_1b1c660112413849_fk_usr_user_name` (`coach_id`),
  KEY `order_order_parentorder_id_51a00572e948edb1_fk_order_order_id` (`parentorder_id`),
  KEY `order_order_product_id_c2415c8535d8fae_fk_order_product_id` (`product_id`),
  KEY `order_order_2b8e1a23` (`billid`),
  CONSTRAINT `order_order_coach_id_1b1c660112413849_fk_usr_user_name` FOREIGN KEY (`coach_id`) REFERENCES `usr_user` (`name`),
  CONSTRAINT `order_order_custom_id_185f27e9de4b2e63_fk_usr_user_name` FOREIGN KEY (`custom_id`) REFERENCES `usr_user` (`name`),
  CONSTRAINT `order_order_gym_id_196cd238bd689be6_fk_business_gym_name` FOREIGN KEY (`gym_id`) REFERENCES `business_gym` (`name`),
  CONSTRAINT `order_order_parentorder_id_51a00572e948edb1_fk_order_order_id` FOREIGN KEY (`parentorder_id`) REFERENCES `order_order` (`id`),
  CONSTRAINT `order_order_product_id_c2415c8535d8fae_fk_order_product_id` FOREIGN KEY (`product_id`) REFERENCES `order_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_order`
--

LOCK TABLES `order_order` WRITE;
/*!40000 ALTER TABLE `order_order` DISABLE KEYS */;
INSERT INTO `order_order` VALUES (1,'2015-09-14 17:39:35',NULL,'alex','royn',144136344022,NULL,'done',NULL,1,100,''),(13,'2015-09-08 08:37:43',NULL,'alex','royn',144169982721,NULL,'paid',NULL,2,100,''),(14,'2015-09-08 08:38:32',NULL,'alex','royn',144170151221,NULL,'unpaid',NULL,2,100,''),(15,'2015-09-08 10:17:39',NULL,'alex','royn',144170745921,NULL,'unpaid',NULL,1,100,''),(16,'2015-09-08 15:28:22',NULL,'alex','royn',144172610121,NULL,'unpaid',NULL,2,2000,''),(17,'2015-09-08 16:09:31',NULL,'royn','royn',144172857011,NULL,'inprogress',NULL,1,500,''),(18,'2015-09-14 09:42:19',NULL,'alex','royn',144222369121,NULL,'inprogress',NULL,1,500,''),(19,'2015-09-16 09:12:38',NULL,'alex','royn',144239475821,NULL,'unpaid',NULL,2,2000,''),(20,'2015-09-16 09:33:10',NULL,'alex','royn',144239598921,NULL,'unpaid',NULL,2,2000,''),(21,'2015-09-18 13:01:18',NULL,'18612261069','royn',144257147771,NULL,'inprogress',NULL,1,500,''),(22,'2015-09-18 13:01:41',NULL,'18612261069','royn',144258130071,NULL,'inprogress',NULL,1,500,''),(23,'2015-09-18 13:12:16',NULL,'18612261069','royn',144258193671,NULL,'unpaid',NULL,1,500,''),(24,'2015-09-19 12:53:59',NULL,'18612261069','royn',144266723971,NULL,'unpaid',NULL,1,500,''),(25,'2015-09-19 18:28:01',NULL,'18612261069','royn',144268728071,NULL,'unpaid',NULL,1,500,''),(26,'2015-09-19 18:29:14',NULL,'18612261069','royn',144268735371,NULL,'unpaid',NULL,1,500,''),(27,'2015-09-19 18:29:49',NULL,'18612261069','royn',144268738971,NULL,'unpaid',NULL,1,500,''),(28,'2015-09-19 18:32:13',NULL,'18612261069','royn',144268753271,NULL,'unpaid',NULL,1,500,''),(29,'2015-09-19 18:39:26',NULL,'18612261069','royn',144268796671,NULL,'unpaid',NULL,1,500,''),(30,'2015-09-19 18:42:10',NULL,'18612261069','royn',144268813071,NULL,'unpaid',NULL,1,500,''),(31,'2015-09-19 18:48:24',NULL,'18612261069','royn',144268850471,NULL,'unpaid',NULL,1,500,''),(32,'2015-09-19 18:49:56',NULL,'18612261069','royn',144268859671,NULL,'unpaid',NULL,1,500,''),(33,'2015-09-19 18:54:03',NULL,'18612261069','royn',144268884371,NULL,'unpaid',NULL,1,500,''),(34,'2015-09-20 03:30:09',NULL,'18612261069','royn',144271980871,NULL,'unpaid',NULL,1,500,''),(35,'2015-09-20 03:41:52',NULL,'18612261069','royn',144272051271,NULL,'unpaid',NULL,1,500,''),(36,'2015-09-20 03:42:24',NULL,'18612261069','royn',144272054371,NULL,'unpaid',NULL,1,500,''),(37,'2015-09-20 03:45:17',NULL,'18612261069','royn',144272071671,NULL,'unpaid',NULL,1,500,''),(38,'2015-09-21 06:16:46',NULL,'18311286007','royn',144281620681,NULL,'paid',NULL,1,500,''),(39,'2015-09-21 07:17:30',NULL,'18612261069','18311286007',144281985078,NULL,'unpaid',NULL,3,2000,''),(40,'2015-09-21 07:19:11',NULL,'18612261069','18311286007',144281995178,NULL,'unpaid',NULL,3,2000,''),(41,'2015-09-23 08:36:51',NULL,'18612261069','royn',144299741171,NULL,'unpaid',NULL,1,500,''),(42,'2015-09-23 08:37:25',NULL,'18612261069','royn',144299744471,NULL,'unpaid',NULL,1,500,''),(43,'2015-09-24 08:58:05',NULL,'18612261069','royn',144308508571,NULL,'unpaid',NULL,1,500,''),(44,'2015-09-24 12:39:10',NULL,'18612261069','royn',144309835071,NULL,'unpaid',NULL,2,2000,''),(45,'2015-09-26 14:39:47',NULL,'18612261069','18311286007',144327838678,NULL,'inprogress',NULL,4,1800,'');
/*!40000 ALTER TABLE `order_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_product`
--

DROP TABLE IF EXISTS `order_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `coach_id` varchar(64) DEFAULT NULL,
  `pic` varchar(256) NOT NULL,
  `introduction` longtext NOT NULL,
  `amount` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  `promotion` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_product_coach_id_127ed22bb9b06814_fk_usr_user_name` (`coach_id`),
  CONSTRAINT `order_product_coach_id_127ed22bb9b06814_fk_usr_user_name` FOREIGN KEY (`coach_id`) REFERENCES `usr_user` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_product`
--

LOCK TABLES `order_product` WRITE;
/*!40000 ALTER TABLE `order_product` DISABLE KEYS */;
INSERT INTO `order_product` VALUES (1,'royn','','3节体验课',3,500,200),(2,'royn','','10节优惠装',10,2000,1800),(3,'18311286007','','测试课程',10,2000,1800),(4,'18311286007','','描述啊好不好',3,1800,1500);
/*!40000 ALTER TABLE `order_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recommend_recommend`
--

DROP TABLE IF EXISTS `recommend_recommend`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recommend_recommend` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `recommend_type` varchar(16) NOT NULL,
  `article_id` int(11) DEFAULT NULL,
  `person_id` int(11) DEFAULT NULL,
  `gyms_id` int(11) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  `recommend_title` varchar(64) NOT NULL,
  `recommend_pic` varchar(512) NOT NULL,
  `recommend_subtitle` varchar(512) NOT NULL,
  `recommend_loc` varchar(64) NOT NULL,
  `recommend_price` varchar(64) NOT NULL,
  `corner` varchar(12) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `recommend_recommen_article_id_3e3f0da8a8f25bd3_fk_weibo_weibo_id` (`article_id`),
  KEY `recommend_recommend_person_id_58ad65600d5fd1ff_fk_usr_user_id` (`person_id`),
  KEY `recommend_recommend_gyms_id_258bd63f38337408_fk_business_gym_id` (`gyms_id`),
  KEY `recommend_recom_course_id_719e7c0af2e62d1f_fk_business_course_id` (`course_id`),
  CONSTRAINT `recommend_recommend_gyms_id_258bd63f38337408_fk_business_gym_id` FOREIGN KEY (`gyms_id`) REFERENCES `business_gym` (`id`),
  CONSTRAINT `recommend_recommend_person_id_58ad65600d5fd1ff_fk_usr_user_id` FOREIGN KEY (`person_id`) REFERENCES `usr_user` (`id`),
  CONSTRAINT `recommend_recommen_article_id_3e3f0da8a8f25bd3_fk_weibo_weibo_id` FOREIGN KEY (`article_id`) REFERENCES `weibo_weibo` (`id`),
  CONSTRAINT `recommend_recom_course_id_719e7c0af2e62d1f_fk_business_course_id` FOREIGN KEY (`course_id`) REFERENCES `business_course` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recommend_recommend`
--

LOCK TABLES `recommend_recommend` WRITE;
/*!40000 ALTER TABLE `recommend_recommend` DISABLE KEYS */;
INSERT INTO `recommend_recommend` VALUES (1,'2015-09-09 12:40:34','gym',NULL,NULL,1,NULL,'便宜带泳池的健身房','http://img1.wikia.nocookie.net/__cb20150426102309/logopedia/images/e/ee/LD_610x240_AboutUs.jpg','开业大促销','海淀区 马连洼北路 西山华府','1500','recommend'),(2,'2015-09-09 12:42:45','user',NULL,3,NULL,NULL,'明星教练: 徐东波','http://img3.wikia.nocookie.net/__cb20150110175953/logopedia/images/2/24/BOTR_610x240_Module1.jpg','TRX 壶铃 Crossfit','海淀区 马连洼北路 西山华府','','hot'),(3,'2015-09-09 15:53:07','user',NULL,1,NULL,NULL,'明星教练Royn','http://viet.nam.travel/wp-content/uploads/2014/09/gyms-in-vietnam.jpg','带你一点点了解Crossfit','西二旗 润桥健身','200','');
/*!40000 ALTER TABLE `recommend_recommend` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sms_sms`
--

DROP TABLE IF EXISTS `sms_sms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_sms` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `number` bigint(20) NOT NULL,
  `vcode` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `number` (`number`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sms_sms`
--

LOCK TABLES `sms_sms` WRITE;
/*!40000 ALTER TABLE `sms_sms` DISABLE KEYS */;
INSERT INTO `sms_sms` VALUES (7,18612261069,638419),(8,18311286007,207321);
/*!40000 ALTER TABLE `sms_sms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usr_timeline`
--

DROP TABLE IF EXISTS `usr_timeline`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usr_timeline` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_id` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_id` (`name_id`),
  CONSTRAINT `usr_timeline_name_id_2aa3e95a889da96f_fk_usr_user_name` FOREIGN KEY (`name_id`) REFERENCES `usr_user` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usr_timeline`
--

LOCK TABLES `usr_timeline` WRITE;
/*!40000 ALTER TABLE `usr_timeline` DISABLE KEYS */;
INSERT INTO `usr_timeline` VALUES (5,'18311286007'),(4,'18612261069'),(2,'alex'),(1,'royn'),(3,'xudongbo');
/*!40000 ALTER TABLE `usr_timeline` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usr_timeline_feed`
--

DROP TABLE IF EXISTS `usr_timeline_feed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usr_timeline_feed` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timeline_id` int(11) NOT NULL,
  `weibo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `timeline_id` (`timeline_id`,`weibo_id`),
  KEY `usr_timeline_feed_weibo_id_95b6e5b9e3d26b_fk_weibo_weibo_id` (`weibo_id`),
  CONSTRAINT `usr_timeline_feed_timeline_id_48a79b117394169_fk_usr_timeline_id` FOREIGN KEY (`timeline_id`) REFERENCES `usr_timeline` (`id`),
  CONSTRAINT `usr_timeline_feed_weibo_id_95b6e5b9e3d26b_fk_weibo_weibo_id` FOREIGN KEY (`weibo_id`) REFERENCES `weibo_weibo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usr_timeline_feed`
--

LOCK TABLES `usr_timeline_feed` WRITE;
/*!40000 ALTER TABLE `usr_timeline_feed` DISABLE KEYS */;
INSERT INTO `usr_timeline_feed` VALUES (2,1,1),(4,1,2),(5,1,3),(7,1,4),(9,1,5),(11,1,6),(13,1,7),(15,1,8),(1,2,1),(3,2,2),(6,2,3),(8,2,4),(10,2,5),(12,2,6),(14,2,7),(16,2,8),(17,4,9),(18,4,10),(19,4,11),(20,4,12),(21,4,13),(22,4,14),(23,4,15),(24,4,16),(25,4,17),(26,4,18),(27,4,19),(28,4,20),(29,4,21),(30,4,22),(31,4,23),(32,4,24);
/*!40000 ALTER TABLE `usr_timeline_feed` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usr_timeline_followedby`
--

DROP TABLE IF EXISTS `usr_timeline_followedby`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usr_timeline_followedby` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `from_timeline_id` int(11) NOT NULL,
  `to_timeline_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `from_timeline_id` (`from_timeline_id`,`to_timeline_id`),
  KEY `usr_timeline__to_timeline_id_5ac8ce23084dbe0b_fk_usr_timeline_id` (`to_timeline_id`),
  CONSTRAINT `usr_timeline__to_timeline_id_5ac8ce23084dbe0b_fk_usr_timeline_id` FOREIGN KEY (`to_timeline_id`) REFERENCES `usr_timeline` (`id`),
  CONSTRAINT `usr_timelin_from_timeline_id_5e93d7e27be6ab5e_fk_usr_timeline_id` FOREIGN KEY (`from_timeline_id`) REFERENCES `usr_timeline` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usr_timeline_followedby`
--

LOCK TABLES `usr_timeline_followedby` WRITE;
/*!40000 ALTER TABLE `usr_timeline_followedby` DISABLE KEYS */;
INSERT INTO `usr_timeline_followedby` VALUES (1,1,1),(3,1,2),(2,2,2),(4,3,3),(5,4,4),(6,5,5);
/*!40000 ALTER TABLE `usr_timeline_followedby` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usr_timeline_refresh`
--

DROP TABLE IF EXISTS `usr_timeline_refresh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usr_timeline_refresh` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timeline_id` int(11) NOT NULL,
  `weibo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `timeline_id` (`timeline_id`,`weibo_id`),
  KEY `usr_timeline_refresh_weibo_id_52b6874552e9095b_fk_weibo_weibo_id` (`weibo_id`),
  CONSTRAINT `usr_timeline_refresh_weibo_id_52b6874552e9095b_fk_weibo_weibo_id` FOREIGN KEY (`weibo_id`) REFERENCES `weibo_weibo` (`id`),
  CONSTRAINT `usr_timeline_ref_timeline_id_47e144be2975acd1_fk_usr_timeline_id` FOREIGN KEY (`timeline_id`) REFERENCES `usr_timeline` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usr_timeline_refresh`
--

LOCK TABLES `usr_timeline_refresh` WRITE;
/*!40000 ALTER TABLE `usr_timeline_refresh` DISABLE KEYS */;
INSERT INTO `usr_timeline_refresh` VALUES (1,4,9),(2,4,10),(3,4,11),(4,4,12),(5,4,13),(6,4,14),(7,4,15),(8,4,16),(9,4,17),(10,4,18),(11,4,19),(12,4,20),(13,4,21),(14,4,22),(15,4,23),(16,4,24);
/*!40000 ALTER TABLE `usr_timeline_refresh` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usr_user`
--

DROP TABLE IF EXISTS `usr_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usr_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `displayname` varchar(128) NOT NULL,
  `iscoach` tinyint(1) NOT NULL,
  `created` datetime NOT NULL,
  `avatar` varchar(256) NOT NULL,
  `upnum` int(11) NOT NULL,
  `recommand_p` int(11) DEFAULT NULL,
  `tags` varchar(64) DEFAULT '',
  `introduction` varchar(1024) DEFAULT '',
  `order_count` int(11) NOT NULL DEFAULT '0',
  `course_count` int(11) NOT NULL DEFAULT '0',
  `rate` bigint(20) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `displayname` (`displayname`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usr_user`
--

LOCK TABLES `usr_user` WRITE;
/*!40000 ALTER TABLE `usr_user` DISABLE KEYS */;
INSERT INTO `usr_user` VALUES (1,'royn','教练',1,'2015-09-26 13:55:16','http://7xiwfp.com1.z0.glb.clouddn.com/9b247ea15b9d11e596477831c1cd33b6.jpg',0,NULL,'啊哈哈 哈哈哈','hahahahahah',1,0,35),(2,'alex','用户',0,'2015-09-04 10:41:58','http://7xiwfp.com1.z0.glb.clouddn.com/f7fbe62e2bcd11e5900a7831c1cd33b6?imageView2/1/w/200/h/200',0,0,'','',0,0,0),(3,'xudongbo','徐东波',1,'2015-09-08 16:10:52','http://www.touxiang.cn/uploads/20131114/14-065802_226.jpg',1,NULL,'','',0,0,0),(7,'18612261069','18612261069',0,'2015-09-18 13:00:53','http://7xiwfp.com1.z0.glb.clouddn.com/4adfdc175e0511e595027831c1cd33b6.jpg',0,NULL,'','',0,0,0),(8,'18311286007','测试教练',1,'2015-09-21 06:18:15','http://7xiwfp.com1.z0.glb.clouddn.com/85b8e5cf602811e5b6097831c1cd33b6.jpg',0,NULL,'啊哈哈 哈哈哈','',0,0,0);
/*!40000 ALTER TABLE `usr_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usr_user_commented`
--

DROP TABLE IF EXISTS `usr_user_commented`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usr_user_commented` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `weibo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`weibo_id`),
  KEY `usr_user_commented_weibo_id_102b578a15e72514_fk_weibo_weibo_id` (`weibo_id`),
  CONSTRAINT `usr_user_commented_user_id_127e49120079223c_fk_usr_user_id` FOREIGN KEY (`user_id`) REFERENCES `usr_user` (`id`),
  CONSTRAINT `usr_user_commented_weibo_id_102b578a15e72514_fk_weibo_weibo_id` FOREIGN KEY (`weibo_id`) REFERENCES `weibo_weibo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usr_user_commented`
--

LOCK TABLES `usr_user_commented` WRITE;
/*!40000 ALTER TABLE `usr_user_commented` DISABLE KEYS */;
/*!40000 ALTER TABLE `usr_user_commented` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usr_user_fwded`
--

DROP TABLE IF EXISTS `usr_user_fwded`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usr_user_fwded` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `weibo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`weibo_id`),
  KEY `usr_user_fwded_weibo_id_2742f7912e5cba74_fk_weibo_weibo_id` (`weibo_id`),
  CONSTRAINT `usr_user_fwded_user_id_50ef2f0e5ab0959c_fk_usr_user_id` FOREIGN KEY (`user_id`) REFERENCES `usr_user` (`id`),
  CONSTRAINT `usr_user_fwded_weibo_id_2742f7912e5cba74_fk_weibo_weibo_id` FOREIGN KEY (`weibo_id`) REFERENCES `weibo_weibo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usr_user_fwded`
--

LOCK TABLES `usr_user_fwded` WRITE;
/*!40000 ALTER TABLE `usr_user_fwded` DISABLE KEYS */;
INSERT INTO `usr_user_fwded` VALUES (1,1,2);
/*!40000 ALTER TABLE `usr_user_fwded` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usr_user_upped`
--

DROP TABLE IF EXISTS `usr_user_upped`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usr_user_upped` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `weibo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`weibo_id`),
  KEY `usr_user_upped_weibo_id_484052496d2f0976_fk_weibo_weibo_id` (`weibo_id`),
  CONSTRAINT `usr_user_upped_user_id_58eadb14dd62f3b2_fk_usr_user_id` FOREIGN KEY (`user_id`) REFERENCES `usr_user` (`id`),
  CONSTRAINT `usr_user_upped_weibo_id_484052496d2f0976_fk_weibo_weibo_id` FOREIGN KEY (`weibo_id`) REFERENCES `weibo_weibo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usr_user_upped`
--

LOCK TABLES `usr_user_upped` WRITE;
/*!40000 ALTER TABLE `usr_user_upped` DISABLE KEYS */;
INSERT INTO `usr_user_upped` VALUES (2,1,2),(1,1,6);
/*!40000 ALTER TABLE `usr_user_upped` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usr_user_upped_person`
--

DROP TABLE IF EXISTS `usr_user_upped_person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usr_user_upped_person` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `from_user_id` int(11) NOT NULL,
  `to_user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `from_user_id` (`from_user_id`,`to_user_id`),
  KEY `usr_user_upped_person_to_user_id_43337bf0ae93a36_fk_usr_user_id` (`to_user_id`),
  CONSTRAINT `usr_user_upped_person_to_user_id_43337bf0ae93a36_fk_usr_user_id` FOREIGN KEY (`to_user_id`) REFERENCES `usr_user` (`id`),
  CONSTRAINT `usr_user_upped_pers_from_user_id_5cc298db0dbcc0e7_fk_usr_user_id` FOREIGN KEY (`from_user_id`) REFERENCES `usr_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usr_user_upped_person`
--

LOCK TABLES `usr_user_upped_person` WRITE;
/*!40000 ALTER TABLE `usr_user_upped_person` DISABLE KEYS */;
INSERT INTO `usr_user_upped_person` VALUES (1,1,3),(2,3,1);
/*!40000 ALTER TABLE `usr_user_upped_person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usr_workingdays`
--

DROP TABLE IF EXISTS `usr_workingdays`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usr_workingdays` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `weekrest` varchar(32) NOT NULL,
  `excep_rest` varchar(1024) NOT NULL,
  `excep_work` varchar(1024) NOT NULL,
  `out_hours` varchar(64) NOT NULL,
  `noon_hours` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usr_workingdays`
--

LOCK TABLES `usr_workingdays` WRITE;
/*!40000 ALTER TABLE `usr_workingdays` DISABLE KEYS */;
INSERT INTO `usr_workingdays` VALUES (1,'royn','1','','','',''),(2,'alex','','','','',''),(3,'xudongbo','','','','',''),(4,'18612261069','','','','',''),(5,'18311286007','','','','','');
/*!40000 ALTER TABLE `usr_workingdays` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `weibo_images`
--

DROP TABLE IF EXISTS `weibo_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `weibo_images` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(256) NOT NULL,
  `by_id` int(11) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `weibo_images_by_id_24d38e17d08dcf5a_fk_usr_user_id` (`by_id`),
  CONSTRAINT `weibo_images_by_id_24d38e17d08dcf5a_fk_usr_user_id` FOREIGN KEY (`by_id`) REFERENCES `usr_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weibo_images`
--

LOCK TABLES `weibo_images` WRITE;
/*!40000 ALTER TABLE `weibo_images` DISABLE KEYS */;
INSERT INTO `weibo_images` VALUES (1,'http://newslounge.net/wp-content/uploads/2013/12/0cbd1704f4340cc6484dbacde68bbe31.jpg',1,'2015-09-04 10:43:19'),(2,'http://stat.ameba.jp/user_images/20121204/20/grfft-sugaya/8c/a6/j/o0396052212316078702.jpg',1,'2015-09-04 10:43:19'),(3,'http://terracehouse-fujitv.net/wp-content/uploads/2013/12/55-1.png',1,'2015-09-07 10:43:42'),(4,'http://7xiwfp.com1.z0.glb.clouddn.com/d306865c5c4611e58d127831c1cd33b6.jpg',1,'2015-09-16 07:44:57'),(5,'http://7xiwfp.com1.z0.glb.clouddn.com/8bce44ab5c4911e59e927831c1cd33b6.jpg',1,'2015-09-16 08:04:26'),(6,'http://7xiwfp.com1.z0.glb.clouddn.com/eec391de5ded11e5bc5f7831c1cd33b6.jpg',7,'2015-09-18 10:13:40'),(7,'http://7xiwfp.com1.z0.glb.clouddn.com/f4d870265ded11e586a57831c1cd33b6.jpg',7,'2015-09-18 10:13:50'),(8,'http://7xiwfp.com1.z0.glb.clouddn.com/050937005dee11e5a69a7831c1cd33b6.jpg',7,'2015-09-18 10:14:18'),(9,'http://7xiwfp.com1.z0.glb.clouddn.com/0aa702ab5dee11e591957831c1cd33b6.jpg',7,'2015-09-18 10:14:27'),(10,'http://7xiwfp.com1.z0.glb.clouddn.com/0ebdc0995dee11e5a6237831c1cd33b6.jpg',7,'2015-09-18 10:14:34'),(11,'http://7xiwfp.com1.z0.glb.clouddn.com/1ac3aeae5dee11e585317831c1cd33b6.jpg',7,'2015-09-18 10:14:54'),(12,'http://7xiwfp.com1.z0.glb.clouddn.com/2265b2915dee11e5a8d67831c1cd33b6.jpg',7,'2015-09-18 10:15:07'),(13,'http://7xiwfp.com1.z0.glb.clouddn.com/27e482a35dee11e58fc87831c1cd33b6.jpg',7,'2015-09-18 10:15:16'),(14,'http://7xiwfp.com1.z0.glb.clouddn.com/2c219f425dee11e5b79f7831c1cd33b6.jpg',7,'2015-09-18 10:15:25'),(15,'http://7xiwfp.com1.z0.glb.clouddn.com/60c5d6d15dee11e5b24d7831c1cd33b6.jpg',7,'2015-09-18 10:16:51'),(16,'http://7xiwfp.com1.z0.glb.clouddn.com/e784377a5df711e59a4a7831c1cd33b6.jpg',7,'2015-09-18 11:25:03'),(17,'http://7xiwfp.com1.z0.glb.clouddn.com/d409ffee5df811e5abaa7831c1cd33b6.jpg',7,'2015-09-18 11:31:40'),(18,'http://7xiwfp.com1.z0.glb.clouddn.com/412a62ab61df11e58f8e7831c1cd33b6.jpg',7,'2015-09-23 10:38:41'),(19,'http://7xiwfp.com1.z0.glb.clouddn.com/41a8ae9961ed11e5bf317831c1cd33b6.jpg',7,'2015-09-23 12:18:55'),(20,'http://7xiwfp.com1.z0.glb.clouddn.com/4f2fb26661ed11e584af7831c1cd33b6.jpg',7,'2015-09-23 12:19:17'),(21,'http://7xiwfp.com1.z0.glb.clouddn.com/c044497d61f111e590d87831c1cd33b6.jpg',7,'2015-09-23 12:51:05');
/*!40000 ALTER TABLE `weibo_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `weibo_longweibo`
--

DROP TABLE IF EXISTS `weibo_longweibo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `weibo_longweibo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `weiboid_id` int(11) NOT NULL,
  `content` longtext NOT NULL,
  `by_id` int(11) DEFAULT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `weibo_longweibo_weiboid_id_45180e5244be3a52_fk_weibo_weibo_id` (`weiboid_id`),
  KEY `weibo_longweibo_by_id_174c58037071117f_fk_usr_user_id` (`by_id`),
  CONSTRAINT `weibo_longweibo_by_id_174c58037071117f_fk_usr_user_id` FOREIGN KEY (`by_id`) REFERENCES `usr_user` (`id`),
  CONSTRAINT `weibo_longweibo_weiboid_id_45180e5244be3a52_fk_weibo_weibo_id` FOREIGN KEY (`weiboid_id`) REFERENCES `weibo_weibo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weibo_longweibo`
--

LOCK TABLES `weibo_longweibo` WRITE;
/*!40000 ALTER TABLE `weibo_longweibo` DISABLE KEYS */;
/*!40000 ALTER TABLE `weibo_longweibo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `weibo_weibo`
--

DROP TABLE IF EXISTS `weibo_weibo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `weibo_weibo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(16) NOT NULL,
  `brief` varchar(128) NOT NULL,
  `imgs` varchar(1024) NOT NULL,
  `islong` tinyint(1) NOT NULL,
  `created` datetime NOT NULL,
  `by_id` varchar(64) DEFAULT NULL,
  `iscomments` tinyint(1) NOT NULL,
  `commentto_id` int(11) DEFAULT NULL,
  `isfwd` tinyint(1) NOT NULL,
  `fwdfrom_id` int(11) DEFAULT NULL,
  `upnum` int(11) NOT NULL,
  `commentnum` int(11) NOT NULL,
  `fwdnum` int(11) NOT NULL,
  `coach_id` int(11) DEFAULT NULL,
  `recommand_p` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `weibo_weibo_by_id_1ae292b9c356ad11_fk_usr_user_name` (`by_id`),
  KEY `weibo_weibo_commentto_id_b9c874c184928f5_fk_weibo_weibo_id` (`commentto_id`),
  KEY `weibo_weibo_fwdfrom_id_76da9dd05234cc74_fk_weibo_weibo_id` (`fwdfrom_id`),
  KEY `weibo_weibo_coach_id_9a9752595cb34cf_fk_usr_user_id` (`coach_id`),
  CONSTRAINT `weibo_weibo_by_id_1ae292b9c356ad11_fk_usr_user_name` FOREIGN KEY (`by_id`) REFERENCES `usr_user` (`name`),
  CONSTRAINT `weibo_weibo_coach_id_9a9752595cb34cf_fk_usr_user_id` FOREIGN KEY (`coach_id`) REFERENCES `usr_user` (`id`),
  CONSTRAINT `weibo_weibo_commentto_id_b9c874c184928f5_fk_weibo_weibo_id` FOREIGN KEY (`commentto_id`) REFERENCES `weibo_weibo` (`id`),
  CONSTRAINT `weibo_weibo_fwdfrom_id_76da9dd05234cc74_fk_weibo_weibo_id` FOREIGN KEY (`fwdfrom_id`) REFERENCES `weibo_weibo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weibo_weibo`
--

LOCK TABLES `weibo_weibo` WRITE;
/*!40000 ALTER TABLE `weibo_weibo` DISABLE KEYS */;
INSERT INTO `weibo_weibo` VALUES (1,'测试','','[\"http://newslounge.net/wp-content/uploads/2013/12/0cbd1704f4340cc6484dbacde68bbe31.jpg\",\"http://stat.ameba.jp/user_images/20121204/20/grfft-sugaya/8c/a6/j/o0396052212316078702.jpg\"]',0,'2015-09-04 10:43:19','royn',0,NULL,0,NULL,0,0,0,NULL,NULL),(2,'hahahah','','[\"http://terracehouse-fujitv.net/wp-content/uploads/2013/12/55-1.png\"]',0,'2015-09-07 10:43:42','royn',0,NULL,0,NULL,1,0,1,NULL,NULL),(3,'','','',0,'2015-09-07 14:39:51','royn',0,NULL,0,NULL,0,0,0,1,NULL),(4,'','','',0,'2015-09-07 14:40:08','royn',0,NULL,0,NULL,0,0,0,3,NULL),(5,'','','',0,'2015-09-08 16:10:55','royn',0,NULL,0,NULL,0,0,0,3,NULL),(6,'','','',0,'2015-09-08 16:15:28','royn',0,NULL,1,2,1,0,0,NULL,NULL),(7,'新照片','','[\"http://7xiwfp.com1.z0.glb.clouddn.com/d306865c5c4611e58d127831c1cd33b6.jpg\"]',0,'2015-09-16 07:44:57','royn',0,NULL,0,NULL,0,0,0,NULL,NULL),(8,'新照片','','[\"http://7xiwfp.com1.z0.glb.clouddn.com/8bce44ab5c4911e59e927831c1cd33b6.jpg\"]',0,'2015-09-16 08:04:26','royn',0,NULL,0,NULL,0,0,0,NULL,NULL),(9,'新照片','','[\"http://7xiwfp.com1.z0.glb.clouddn.com/eec391de5ded11e5bc5f7831c1cd33b6.jpg\"]',0,'2015-09-18 10:13:40','18612261069',0,NULL,0,NULL,0,0,0,NULL,NULL),(10,'新照片','','[\"http://7xiwfp.com1.z0.glb.clouddn.com/f4d870265ded11e586a57831c1cd33b6.jpg\"]',0,'2015-09-18 10:13:50','18612261069',0,NULL,0,NULL,0,0,0,NULL,NULL),(11,'新照片','','[\"http://7xiwfp.com1.z0.glb.clouddn.com/050937005dee11e5a69a7831c1cd33b6.jpg\"]',0,'2015-09-18 10:14:18','18612261069',0,NULL,0,NULL,0,0,0,NULL,NULL),(12,'新照片','','[\"http://7xiwfp.com1.z0.glb.clouddn.com/0aa702ab5dee11e591957831c1cd33b6.jpg\"]',0,'2015-09-18 10:14:27','18612261069',0,NULL,0,NULL,0,0,0,NULL,NULL),(13,'新照片','','[\"http://7xiwfp.com1.z0.glb.clouddn.com/0ebdc0995dee11e5a6237831c1cd33b6.jpg\"]',0,'2015-09-18 10:14:34','18612261069',0,NULL,0,NULL,0,0,0,NULL,NULL),(14,'新照片','','[\"http://7xiwfp.com1.z0.glb.clouddn.com/1ac3aeae5dee11e585317831c1cd33b6.jpg\"]',0,'2015-09-18 10:14:54','18612261069',0,NULL,0,NULL,0,0,0,NULL,NULL),(15,'新照片','','[\"http://7xiwfp.com1.z0.glb.clouddn.com/2265b2915dee11e5a8d67831c1cd33b6.jpg\"]',0,'2015-09-18 10:15:07','18612261069',0,NULL,0,NULL,0,0,0,NULL,NULL),(16,'新照片','','[\"http://7xiwfp.com1.z0.glb.clouddn.com/27e482a35dee11e58fc87831c1cd33b6.jpg\"]',0,'2015-09-18 10:15:16','18612261069',0,NULL,0,NULL,0,0,0,NULL,NULL),(17,'新照片','','[\"http://7xiwfp.com1.z0.glb.clouddn.com/2c219f425dee11e5b79f7831c1cd33b6.jpg\"]',0,'2015-09-18 10:15:25','18612261069',0,NULL,0,NULL,0,0,0,NULL,NULL),(18,'新照片','','[\"http://7xiwfp.com1.z0.glb.clouddn.com/60c5d6d15dee11e5b24d7831c1cd33b6.jpg\"]',0,'2015-09-18 10:16:51','18612261069',0,NULL,0,NULL,0,0,0,NULL,NULL),(19,'新照片','','[\"http://7xiwfp.com1.z0.glb.clouddn.com/e784377a5df711e59a4a7831c1cd33b6.jpg\"]',0,'2015-09-18 11:25:03','18612261069',0,NULL,0,NULL,0,0,0,NULL,NULL),(20,'新照片','','[\"http://7xiwfp.com1.z0.glb.clouddn.com/d409ffee5df811e5abaa7831c1cd33b6.jpg\"]',0,'2015-09-18 11:31:40','18612261069',0,NULL,0,NULL,0,0,0,NULL,NULL),(21,'新照片','','[\"http://7xiwfp.com1.z0.glb.clouddn.com/412a62ab61df11e58f8e7831c1cd33b6.jpg\"]',0,'2015-09-23 10:38:41','18612261069',0,NULL,0,NULL,0,0,0,NULL,NULL),(22,'新照片','','[\"http://7xiwfp.com1.z0.glb.clouddn.com/41a8ae9961ed11e5bf317831c1cd33b6.jpg\"]',0,'2015-09-23 12:18:55','18612261069',0,NULL,0,NULL,0,0,0,NULL,NULL),(23,'新照片','','[\"http://7xiwfp.com1.z0.glb.clouddn.com/4f2fb26661ed11e584af7831c1cd33b6.jpg\"]',0,'2015-09-23 12:19:17','18612261069',0,NULL,0,NULL,0,0,0,NULL,NULL),(24,'发布了照片','','[\"http://7xiwfp.com1.z0.glb.clouddn.com/c044497d61f111e590d87831c1cd33b6.jpg\"]',0,'2015-09-23 12:51:05','18612261069',0,NULL,0,NULL,0,0,0,NULL,NULL);
/*!40000 ALTER TABLE `weibo_weibo` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-09-26 22:50:35
