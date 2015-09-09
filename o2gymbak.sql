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
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add recommend',7,'add_recommend'),(20,'Can change recommend',7,'change_recommend'),(21,'Can delete recommend',7,'delete_recommend'),(22,'Can add user',8,'add_user'),(23,'Can change user',8,'change_user'),(24,'Can delete user',8,'delete_user'),(25,'Can add time line',9,'add_timeline'),(26,'Can change time line',9,'change_timeline'),(27,'Can delete time line',9,'delete_timeline'),(28,'Can add working days',10,'add_workingdays'),(29,'Can change working days',10,'change_workingdays'),(30,'Can delete working days',10,'delete_workingdays'),(31,'Can add weibo',11,'add_weibo'),(32,'Can change weibo',11,'change_weibo'),(33,'Can delete weibo',11,'delete_weibo'),(34,'Can add long weibo',12,'add_longweibo'),(35,'Can change long weibo',12,'change_longweibo'),(36,'Can delete long weibo',12,'delete_longweibo'),(37,'Can add images',13,'add_images'),(38,'Can change images',13,'change_images'),(39,'Can delete images',13,'delete_images'),(40,'Can add order',14,'add_order'),(41,'Can change order',14,'change_order'),(42,'Can delete order',14,'delete_order'),(43,'Can add product',15,'add_product'),(44,'Can change product',15,'change_product'),(45,'Can delete product',15,'delete_product'),(46,'Can add course',16,'add_course'),(47,'Can change course',16,'change_course'),(48,'Can delete course',16,'delete_course'),(49,'Can add gym',17,'add_gym'),(50,'Can change gym',17,'change_gym'),(51,'Can delete gym',17,'delete_gym'),(52,'Can add schedule',18,'add_schedule'),(53,'Can change schedule',18,'change_schedule'),(54,'Can delete schedule',18,'delete_schedule');
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$20000$YaqEzoAYu9wH$8OzrmcuwJvbSd9WOQO6HuuVhDw69o/d1IU8X507E4S8=',NULL,0,'alex','','','',0,1,'2015-09-04 10:39:58'),(2,'pbkdf2_sha256$20000$qttSFSe3PKPt$fGQ3+Ph4DKtSKcRPcogSX7CQfdeZiesHfdGZtfW/INs=',NULL,0,'royn','','','',0,1,'2015-09-04 10:39:58');
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `business_gym`
--

LOCK TABLES `business_gym` WRITE;
/*!40000 ALTER TABLE `business_gym` DISABLE KEYS */;
INSERT INTO `business_gym` VALUES (1,'西山华府','健身房','[\"http://viet.nam.travel/wp-content/uploads/2014/09/gyms-in-vietnam.jpg\"]',NULL,'海淀区 马连洼 西山华府');
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `business_gym_coaches`
--

LOCK TABLES `business_gym_coaches` WRITE;
/*!40000 ALTER TABLE `business_gym_coaches` DISABLE KEYS */;
INSERT INTO `business_gym_coaches` VALUES (3,1,1),(4,1,3);
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
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `business_schedule`
--

LOCK TABLES `business_schedule` WRITE;
/*!40000 ALTER TABLE `business_schedule` DISABLE KEYS */;
INSERT INTO `business_schedule` VALUES (35,'2015-09-01',0,'','',1,1,2,'2015-09-06 05:23:44',0,0,35),(39,'2015-09-02',20,'','',1,1,2,'2015-09-06 05:24:02',0,0,40),(40,'2015-09-03',2,'','',1,1,2,'2015-09-06 05:24:09',0,0,35),(44,'2015-09-09',0,'','',13,1,2,'2015-09-08 08:10:28',0,0,NULL),(45,'2015-09-09',10,'','',14,1,2,'2015-09-08 08:38:32',0,0,NULL),(46,'2015-09-10',0,'','',15,1,2,'2015-09-08 10:17:39',0,0,NULL),(47,'2015-09-11',2,'','',15,1,2,'2015-09-08 10:17:39',0,0,NULL),(48,'2015-09-09',2,'','',16,1,2,'2015-09-08 15:28:22',0,0,NULL),(49,'2015-09-10',8,'','',17,1,1,'2015-09-08 16:09:31',0,0,NULL),(50,'2015-09-23',11,'','',17,1,1,'2015-09-08 16:09:31',0,0,NULL),(51,'2015-09-24',13,'','',17,1,1,'2015-09-08 16:09:31',0,0,NULL);
/*!40000 ALTER TABLE `business_schedule` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(16,'business','course'),(17,'business','gym'),(18,'business','schedule'),(5,'contenttypes','contenttype'),(14,'order','order'),(15,'order','product'),(7,'recommend','recommend'),(6,'sessions','session'),(9,'usr','timeline'),(8,'usr','user'),(10,'usr','workingdays'),(13,'weibo','images'),(12,'weibo','longweibo'),(11,'weibo','weibo');
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2015-09-04 10:37:46'),(2,'auth','0001_initial','2015-09-04 10:37:46'),(3,'admin','0001_initial','2015-09-04 10:37:46'),(4,'contenttypes','0002_remove_content_type_name','2015-09-04 10:37:47'),(5,'auth','0002_alter_permission_name_max_length','2015-09-04 10:37:47'),(6,'auth','0003_alter_user_email_max_length','2015-09-04 10:37:47'),(7,'auth','0004_alter_user_username_opts','2015-09-04 10:37:47'),(8,'auth','0005_alter_user_last_login_null','2015-09-04 10:37:47'),(9,'auth','0006_require_contenttypes_0002','2015-09-04 10:37:47'),(10,'sessions','0001_initial','2015-09-04 10:37:47');
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
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_order`
--

LOCK TABLES `order_order` WRITE;
/*!40000 ALTER TABLE `order_order` DISABLE KEYS */;
INSERT INTO `order_order` VALUES (1,'2015-09-06 05:24:09',NULL,'alex','royn',144136344022,NULL,'done',NULL,1,0),(13,'2015-09-08 08:37:43',NULL,'alex','royn',144169982721,NULL,'paid',NULL,2,100),(14,'2015-09-08 08:38:32',NULL,'alex','royn',144170151221,NULL,'unpaid',NULL,2,100),(15,'2015-09-08 10:17:39',NULL,'alex','royn',144170745921,NULL,'unpaid',NULL,1,100),(16,'2015-09-08 15:28:22',NULL,'alex','royn',144172610121,NULL,'unpaid',NULL,2,2000),(17,'2015-09-08 16:09:31',NULL,'royn','royn',144172857011,NULL,'inprogress',NULL,1,500);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_product`
--

LOCK TABLES `order_product` WRITE;
/*!40000 ALTER TABLE `order_product` DISABLE KEYS */;
INSERT INTO `order_product` VALUES (1,'royn','','3节体验课',3,500,200),(2,'royn','','10节优惠装',10,2000,1800);
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usr_timeline`
--

LOCK TABLES `usr_timeline` WRITE;
/*!40000 ALTER TABLE `usr_timeline` DISABLE KEYS */;
INSERT INTO `usr_timeline` VALUES (2,'alex'),(1,'royn'),(3,'xudongbo');
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
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usr_timeline_feed`
--

LOCK TABLES `usr_timeline_feed` WRITE;
/*!40000 ALTER TABLE `usr_timeline_feed` DISABLE KEYS */;
INSERT INTO `usr_timeline_feed` VALUES (2,1,1),(4,1,2),(5,1,3),(7,1,4),(9,1,5),(11,1,6),(1,2,1),(3,2,2),(6,2,3),(8,2,4),(10,2,5),(12,2,6);
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usr_timeline_followedby`
--

LOCK TABLES `usr_timeline_followedby` WRITE;
/*!40000 ALTER TABLE `usr_timeline_followedby` DISABLE KEYS */;
INSERT INTO `usr_timeline_followedby` VALUES (1,1,1),(3,1,2),(2,2,2),(4,3,3);
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usr_timeline_refresh`
--

LOCK TABLES `usr_timeline_refresh` WRITE;
/*!40000 ALTER TABLE `usr_timeline_refresh` DISABLE KEYS */;
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `displayname` (`displayname`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usr_user`
--

LOCK TABLES `usr_user` WRITE;
/*!40000 ALTER TABLE `usr_user` DISABLE KEYS */;
INSERT INTO `usr_user` VALUES (1,'royn','教练',1,'2015-09-08 16:15:28','http://i.imgur.com/oI1bF48.jpg',0,NULL),(2,'alex','用户',0,'2015-09-04 10:41:58','http://7xiwfp.com1.z0.glb.clouddn.com/f7fbe62e2bcd11e5900a7831c1cd33b6?imageView2/1/w/200/h/200',0,0),(3,'xudongbo','徐东波',1,'2015-09-08 16:10:52','http://www.touxiang.cn/uploads/20131114/14-065802_226.jpg',1,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usr_workingdays`
--

LOCK TABLES `usr_workingdays` WRITE;
/*!40000 ALTER TABLE `usr_workingdays` DISABLE KEYS */;
INSERT INTO `usr_workingdays` VALUES (1,'royn','1','','','',''),(2,'alex','','','','',''),(3,'xudongbo','','','','','');
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weibo_images`
--

LOCK TABLES `weibo_images` WRITE;
/*!40000 ALTER TABLE `weibo_images` DISABLE KEYS */;
INSERT INTO `weibo_images` VALUES (1,'http://newslounge.net/wp-content/uploads/2013/12/0cbd1704f4340cc6484dbacde68bbe31.jpg',1,'2015-09-04 10:43:19'),(2,'http://stat.ameba.jp/user_images/20121204/20/grfft-sugaya/8c/a6/j/o0396052212316078702.jpg',1,'2015-09-04 10:43:19'),(3,'http://terracehouse-fujitv.net/wp-content/uploads/2013/12/55-1.png',1,'2015-09-07 10:43:42');
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weibo_weibo`
--

LOCK TABLES `weibo_weibo` WRITE;
/*!40000 ALTER TABLE `weibo_weibo` DISABLE KEYS */;
INSERT INTO `weibo_weibo` VALUES (1,'测试','','[\"http://newslounge.net/wp-content/uploads/2013/12/0cbd1704f4340cc6484dbacde68bbe31.jpg\",\"http://stat.ameba.jp/user_images/20121204/20/grfft-sugaya/8c/a6/j/o0396052212316078702.jpg\"]',0,'2015-09-04 10:43:19','royn',0,NULL,0,NULL,0,0,0,NULL,NULL),(2,'hahahah','','[\"http://terracehouse-fujitv.net/wp-content/uploads/2013/12/55-1.png\"]',0,'2015-09-07 10:43:42','royn',0,NULL,0,NULL,1,0,1,NULL,NULL),(3,'','','',0,'2015-09-07 14:39:51','royn',0,NULL,0,NULL,0,0,0,1,NULL),(4,'','','',0,'2015-09-07 14:40:08','royn',0,NULL,0,NULL,0,0,0,3,NULL),(5,'','','',0,'2015-09-08 16:10:55','royn',0,NULL,0,NULL,0,0,0,3,NULL),(6,'','','',0,'2015-09-08 16:15:28','royn',0,NULL,1,2,1,0,0,NULL,NULL);
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

-- Dump completed on 2015-09-10  0:31:45
