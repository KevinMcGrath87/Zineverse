-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: zineverse
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `collections`
--

DROP TABLE IF EXISTS `collections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `collections` (
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `zine_id` int NOT NULL,
  `user_id` int NOT NULL,
  KEY `fk_collections_zines_idx` (`zine_id`),
  KEY `fk_collections_users1_idx` (`user_id`),
  CONSTRAINT `fk_collections_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `fk_collections_zines` FOREIGN KEY (`zine_id`) REFERENCES `zines` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `collections`
--

LOCK TABLES `collections` WRITE;
/*!40000 ALTER TABLE `collections` DISABLE KEYS */;
INSERT INTO `collections` VALUES ('2023-01-22 17:02:03','2023-01-22 17:02:03',18,4),('2023-01-23 14:18:55','2023-01-23 14:18:55',19,4),('2023-01-24 17:18:10','2023-01-24 17:18:10',20,7),('2023-01-24 18:56:29','2023-01-24 18:56:29',22,4),('2023-02-08 19:31:17','2023-02-08 19:31:17',23,4);
/*!40000 ALTER TABLE `collections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `comment` longtext NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL,
  `zine_id` int NOT NULL,
  `user_id1` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_comments_zines1_idx` (`zine_id`),
  KEY `fk_comments_users1_idx` (`user_id1`),
  CONSTRAINT `fk_comments_users1` FOREIGN KEY (`user_id1`) REFERENCES `users` (`id`),
  CONSTRAINT `fk_comments_zines1` FOREIGN KEY (`zine_id`) REFERENCES `zines` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `friends`
--

DROP TABLE IF EXISTS `friends`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `friends` (
  `user_id` int NOT NULL,
  `friend_id` int NOT NULL,
  KEY `fk_friends_users1_idx` (`user_id`),
  KEY `fk_friends_users2_idx` (`friend_id`),
  CONSTRAINT `fk_friends_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `fk_friends_users2` FOREIGN KEY (`friend_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `friends`
--

LOCK TABLES `friends` WRITE;
/*!40000 ALTER TABLE `friends` DISABLE KEYS */;
INSERT INTO `friends` VALUES (6,4),(4,5),(4,5),(8,4);
/*!40000 ALTER TABLE `friends` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (4,'Kevin','email@email.email','$2b$12$.Sj89qhZ0LGofOMuFk0ZbeLrBTLkp2TaKgZgIT.SrBw4qSqfP9Al6','2023-01-20 12:55:36',NULL),(5,'Adrian','adrian@gmail.com','$2b$12$AWfInyDYiDqGKZI5DIHZ7OFYIG8qd2zYHH6TfF/AYhgG4c6otg0Ua','2023-01-20 12:56:20',NULL),(6,'AdrianGarcia','adrian@yahoo.com','$2b$12$65i.Wy8JW4HD8lmubuH6FuKYfSrMUkc1.x1nKCyu7d0B9/A/j.AO2','2023-01-22 20:06:38',NULL),(7,'Allie','allie@gmail.com','$2b$12$lOAWl7etPz76ZXWzIt.kOexj6EpJOMslzpeBF1v676CM1Fu0wQFNe','2023-01-24 17:17:18',NULL),(8,'Test','test@test.com','$2b$12$o1d0xS.i4fmUG8Fg7o1wQu5XhgX9qcpCczZ24wHz2E00Lp7KfuO.q','2023-01-24 19:24:01',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zines`
--

DROP TABLE IF EXISTS `zines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `zines` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `path` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zines`
--

LOCK TABLES `zines` WRITE;
/*!40000 ALTER TABLE `zines` DISABLE KEYS */;
INSERT INTO `zines` VALUES (18,'Plastic','Kevin McGrath','A zine about the end of humanity.','G:\\codingdojo\\solo_project\\flask_app\\static\\zinelib\\Plastic','2023-01-22 17:02:03','2023-01-22 17:02:03'),(19,'Newer Zine','Kevin','A newer Zine','G:\\codingdojo\\solo_project\\flask_app\\static\\zinelib\\Newer Zine','2023-01-23 14:18:55','2023-01-23 14:18:55'),(20,'Whatever','Allie Reidy','Allie\'s Zine','G:\\codingdojo\\solo_project\\flask_app\\static\\zinelib\\Whatever','2023-01-24 17:18:10','2023-01-24 17:18:10'),(22,'NewZine2','Kevin','description','G:\\codingdojo\\solo_project\\flask_app\\static\\zinelib\\NewZine2','2023-01-24 18:56:28','2023-01-24 18:56:28'),(23,'NewNewZine','Keivn','A new zine','G:\\codingdojo\\solo_project\\flask_app\\static\\zinelib\\NewNewZine','2023-02-08 19:31:17','2023-02-08 19:31:17');
/*!40000 ALTER TABLE `zines` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-02-09 10:40:30
