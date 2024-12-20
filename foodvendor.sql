-- MySQL dump 10.13  Distrib 9.1.0, for Linux (x86_64)
--
-- Host: localhost    Database: foodvendor
-- ------------------------------------------------------
-- Server version	9.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Orders`
--

DROP TABLE IF EXISTS `Orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Orders` (
  `OrderID` int NOT NULL,
  `ItemID` int NOT NULL,
  `FoodName` varchar(384) NOT NULL,
  `Quantity` int NOT NULL,
  `TotalPrice` decimal(10,2) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`OrderID`,`ItemID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Orders`
--

LOCK TABLES `Orders` WRITE;
/*!40000 ALTER TABLE `Orders` DISABLE KEYS */;
INSERT INTO `Orders` VALUES (1,8,'Beef Roll',1,90.00,2),(1,47,'Egg Roll',1,60.00,2),(2,37,'Sandesh',1,50.00,2),(2,38,'Kheer',2,140.00,2),(2,39,'Chamcham',3,150.00,2),(3,10,'Chicken Biryani',1,300.00,3);
/*!40000 ALTER TABLE `Orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `OrdersStatus`
--

DROP TABLE IF EXISTS `OrdersStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `OrdersStatus` (
  `OrderID` int NOT NULL,
  `OrderStatus` varchar(256) NOT NULL,
  `PayablePrice` decimal(10,2) NOT NULL,
  PRIMARY KEY (`OrderID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `OrdersStatus`
--

LOCK TABLES `OrdersStatus` WRITE;
/*!40000 ALTER TABLE `OrdersStatus` DISABLE KEYS */;
INSERT INTO `OrdersStatus` VALUES (1,'completed',150.00),(2,'in process',340.00),(3,'in process',300.00);
/*!40000 ALTER TABLE `OrdersStatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `foodItems`
--

DROP TABLE IF EXISTS `foodItems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `foodItems` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `FoodName` varchar(100) NOT NULL,
  `Category` varchar(50) NOT NULL,
  `Description` text,
  `Price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `foodItems`
--

LOCK TABLES `foodItems` WRITE;
/*!40000 ALTER TABLE `foodItems` DISABLE KEYS */;
INSERT INTO `foodItems` VALUES (1,'Samosa','Starter','Fried pastry stuffed with spiced potatoes and lentils.',20.00),(2,'Piyaji','Starter','Crispy deep-fried fritters made from lentils and onions.',15.00),(3,'Chotpoti','Starter','Spicy chickpea-based street food with potatoes, tamarind sauce, and eggs.',80.00),(4,'Beguni','Starter','Deep-fried eggplant slices coated with chickpea flour.',30.00),(5,'Chicken Pakora','Starter','Marinated chicken pieces deep-fried in gram flour batter.',100.00),(6,'Mughlai Paratha','Starter','Paratha stuffed with eggs and minced meat, fried until crispy.',120.00),(7,'Fuchka','Snack','Crispy shells filled with spicy, tangy chickpea and potato mixture.',50.00),(8,'Beef Roll','Snack','Paratha rolled with spiced beef, onions, and green chilies.',90.00),(9,'Kacchi Biryani','Main Course','Fragrant rice cooked with marinated mutton, potatoes, and aromatic spices.',350.00),(10,'Chicken Biryani','Main Course','Biryani cooked with marinated chicken and fragrant spices.',300.00),(11,'Tehari','Main Course','Rice cooked with spiced beef and potatoes.',250.00),(12,'Beef Bhuna','Main Course','Tender beef cooked with aromatic spices in a thick gravy.',280.00),(13,'Chicken Curry','Main Course','Classic chicken curry cooked with a blend of spices, tomatoes, and onions.',200.00),(14,'Beef Rezala','Main Course','Mildly spiced beef curry cooked with yogurt and milk.',350.00),(15,'Chingri Malai Curry','Main Course','Prawns cooked in a rich coconut milk gravy with aromatic spices.',400.00),(16,'Ilish Bhaja','Main Course','Fried Hilsa fish served with steamed rice.',450.00),(17,'Rui Maacher Kalia','Main Course','Rohu fish cooked in a thick and flavorful gravy.',300.00),(18,'Pabda Maacher Jhal','Main Course','Pabda fish cooked in a spicy tomato-based sauce.',320.00),(19,'Chicken Roast','Main Course','Slow-cooked chicken dish with aromatic spices.',220.00),(20,'Mutton Bhuna','Main Course','Mutton cooked with rich spices and served in a thick gravy.',450.00),(21,'Polao','Main Course','Aromatic rice cooked with ghee, bay leaves, and cardamom.',180.00),(22,'Bhuna Khichuri','Main Course','Savory rice and lentils cooked with spices, often served with meat or fish.',220.00),(23,'Aloo Bhorta','Vegetarian','Mashed potatoes mixed with mustard oil, green chilies, and onions.',50.00),(24,'Begun Bhaja','Vegetarian','Fried eggplant slices seasoned with turmeric and salt.',40.00),(25,'Chana Dal','Vegetarian','Split chickpea lentil curry cooked with onions, garlic, and spices.',80.00),(26,'Paneer Bharta','Vegetarian','Mashed cottage cheese cooked with spices, tomatoes, and onions.',150.00),(27,'Dhokar Dalna','Vegetarian','Lentil cakes cooked in a spicy tomato-based gravy.',120.00),(28,'Shak Bhaji','Vegetarian','Stir-fried leafy greens with garlic and green chilies.',60.00),(29,'Misti Kumra Bhaji','Vegetarian','Fried sweet pumpkin slices cooked with spices.',70.00),(30,'Paratha','Bread','Layered, flaky flatbread cooked on a griddle.',20.00),(31,'Naan','Bread','Soft, leavened flatbread baked in a tandoor oven.',30.00),(32,'Roti','Bread','Traditional flatbread made with wheat flour.',15.00),(33,'Luchi','Bread','Deep-fried flatbread, similar to puri.',10.00),(34,'Bakarkhani','Bread','Sweet, flaky bread perfect as a snack or side dish.',25.00),(35,'Mishti Doi','Dessert','Traditional sweetened yogurt.',60.00),(36,'Rasgulla','Dessert','Soft, spongy cheese balls soaked in sugar syrup.',40.00),(37,'Sandesh','Dessert','Sweet made from fresh paneer mixed with sugar.',50.00),(38,'Kheer','Dessert','Creamy rice pudding made with milk, sugar, and cardamom.',70.00),(39,'Chamcham','Dessert','A sweet made from curdled milk and soaked in sugar syrup.',50.00),(40,'Patishapta','Dessert','Sweet crepes filled with coconut and jaggery.',35.00),(41,'Jalebi','Dessert','Deep-fried spirals of batter soaked in sugar syrup.',30.00),(42,'Borhani','Beverage','Tangy yogurt-based drink flavored with spices.',40.00),(43,'Lassi','Beverage','Refreshing yogurt-based drink, can be sweet or salty.',50.00),(44,'Sarbat','Beverage','Sweet, refreshing drink made with lemon juice and sugar.',30.00),(45,'Chai','Beverage','Traditional tea made with milk and sugar.',20.00),(46,'Green Coconut Water','Beverage','Fresh coconut water, a natural hydrating drink.',60.00),(47,'Egg Roll','Snack','Paratha wrap filled with egg, vegetables, and sauce.',60.00),(48,'Beef Singara','Snack','Fried pastry filled with spiced minced beef.',35.00),(49,'Aloo Chop','Snack','Potato patty coated in batter and deep-fried.',25.00),(50,'Muri','Snack','Puffed rice mixed with mustard oil, onions, and green chilies.',10.00),(51,'Chingri Bhorta','Main Course','Mashed shrimp mixed with spices and mustard oil.',180.00),(52,'Haleem','Main Course','Slow-cooked lentils, meat, and spices.',250.00);
/*!40000 ALTER TABLE `foodItems` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sessions`
--

DROP TABLE IF EXISTS `sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sessions` (
  `session_id` varchar(384) NOT NULL,
  `user_id` int NOT NULL,
  `expires_at` datetime NOT NULL,
  PRIMARY KEY (`session_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessions`
--

LOCK TABLES `sessions` WRITE;
/*!40000 ALTER TABLE `sessions` DISABLE KEYS */;
INSERT INTO `sessions` VALUES ('2e31ecd3-fdad-48a5-8b98-f4a3886bb3a4',2,'2024-10-01 01:43:44'),('5c3fdf67-d3b1-4476-9116-e085bdfd4c75',2,'2024-10-03 01:44:01'),('67cbedaa-14b9-445a-913f-f076a20f7a62',2,'2024-10-29 09:43:19'),('987b44ee-40db-4b9f-a95e-33ff0fffda7b',3,'2024-10-01 02:45:13'),('b964a369-880c-4739-9927-ecc6ca01135b',4,'2024-10-29 10:16:30'),('d96ee6a4-c67e-4267-9bb9-00443023e525',3,'2024-10-03 02:03:30'),('df4853ce-a07d-4988-830d-d2e7cc4119fb',5,'2024-10-29 10:20:34'),('e3ffe97c-ffe8-4078-beed-5856e97191bc',7,'2024-10-29 10:28:44');
/*!40000 ALTER TABLE `sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(256) NOT NULL,
  `username` varchar(384) NOT NULL,
  `password` varchar(384) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`),
  CONSTRAINT `users_chk_1` CHECK ((char_length(`username`) > 1)),
  CONSTRAINT `users_chk_2` CHECK ((char_length(`password`) > 3))
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (2,'pr.javedjarif@gmail.com','javed jarif','1234'),(3,'dev.syfulislam@gmail.com','syful islam','1234'),(4,'Dummy1@gmail.com','Dummy1','12345'),(5,'Dummy2@gmail.com','Dummy2','12345'),(7,'Dummy3@gmail.com','Dummy3','12345');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-29  0:27:10
