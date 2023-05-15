CREATE DATABASE  IF NOT EXISTS `projectio` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `projectio`;
-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: projectio
-- ------------------------------------------------------
-- Server version	8.0.33

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('bc64203c73f5');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course` (
  `course_id` int NOT NULL AUTO_INCREMENT,
  `course_name` varchar(100) NOT NULL,
  `syllabus` varchar(200) NOT NULL,
  `university_id` int NOT NULL,
  `degree` varchar(100) NOT NULL,
  `cycle` varchar(100) NOT NULL,
  PRIMARY KEY (`course_id`),
  KEY `university_id` (`university_id`),
  CONSTRAINT `course_ibfk_1` FOREIGN KEY (`university_id`) REFERENCES `university` (`university_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES (1,'Aministracja','https://rekrutacja.ukw.edu.pl/oferta/studia-pierwszego-stopnia/administracja#.ZFfbr3ZBw2w',1,'licencjat','I stopnia'),(2,'Biologia','https://rekrutacja.ukw.edu.pl/oferta/studia-pierwszego-stopnia/biologia-licencjackie#.ZFfcEHZBw2w',1,'licencjat','I stopnia'),(3,'Informatyka','https://sylabus.uj.edu.pl/pl/5/1/3/19/88?masterElement=19',2,'licencjat','I stopnia'),(4,'Edytorstwo','https://sylabus.uj.edu.pl/pl/5/1/3/21/92?masterElement=21',2,'licencjat','I stopnia'),(5,'Architektura','https://rekrutacja.p.lodz.pl/pl/architektura-i-stopnia-wydzial-budownictwa-architektury-i-inzynierii-srodowiska',3,'inżynier','I stopnia'),(6,'Budownictwo','https://rekrutacja.p.lodz.pl/pl/budownictwo-i-stopnia-wydzial-budownictwa-architektury-i-inzynierii-srodowiska',3,'inżynier','I stopnia');
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rating`
--

DROP TABLE IF EXISTS `rating`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rating` (
  `rating_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `university_id` int NOT NULL,
  `course_id` int NOT NULL,
  `rating_value` int NOT NULL,
  `rating_description` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`rating_id`),
  KEY `course_id` (`course_id`),
  KEY `university_id` (`university_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `rating_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`),
  CONSTRAINT `rating_ibfk_2` FOREIGN KEY (`university_id`) REFERENCES `university` (`university_id`),
  CONSTRAINT `rating_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rating`
--

LOCK TABLES `rating` WRITE;
/*!40000 ALTER TABLE `rating` DISABLE KEYS */;
/*!40000 ALTER TABLE `rating` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `university`
--

DROP TABLE IF EXISTS `university`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `university` (
  `university_id` int NOT NULL AUTO_INCREMENT,
  `university_name` varchar(100) NOT NULL,
  `location` varchar(50) NOT NULL,
  `website` varchar(100) NOT NULL,
  PRIMARY KEY (`university_id`)
) ENGINE=InnoDB AUTO_INCREMENT=154 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `university`
--

LOCK TABLES `university` WRITE;
/*!40000 ALTER TABLE `university` DISABLE KEYS */;
INSERT INTO `university` VALUES (1,'Uniwersytet Kazimierza Wielkiego w Bydgoszczy','Bydgoszcz','https://www.ukw.edu.pl'),(2,'Uniwersytet Jagielloński w Krakowie','Kraków','https://www.uj.edu.pl'),(3,'Politechnika Łódzka','Łódź','https://www.p.lodz.pl'),(4,'Akademia Pomorska w Słupsku','Słupsk','https://www.apsl.edu.pl'),(5,'Politechnika Lubelska','Lublin','https://www.pollub.pl'),(6,'Uniwersytet Marii Curie-Skłodowskiej w Lublinie','Lublin','https://www.umcs.pl/pl/kandydat.htm'),(7,'Uniwersytet im. Adama Mickiewicza w Poznaniu','Poznań','https://amu.edu.pl/kandydaci'),(8,'Uczelnia Techniczno-Handlowa im. Heleny Chodkowskiej w Warszawie','Warszawa','https://www.uth.edu.pl'),(9,'Uniwersytet Łódzki Wydział Zarządzania','Łódź','https://www.wz.uni.lodz.pl/'),(10,'Uniwersytet Ekonomiczny w Poznaniu','Poznań','https://www.ue.poznan.pl'),(11,'Górnośląska Wyższa Szkoła Przedsiębiorczości im. K.Goduli w Chorzowie','Chorzów','https://www.gwsp.edu.pl'),(12,'Krakowska Wyższa Szkoła Promocji Zdrowia','Kraków','https://www.kwspz.pl'),(13,'Uniwersytet Zielonogórski','Zielona Góra','http://www.rekrutacja.uz.zgora.pl'),(14,'Uniwersytet Gdański','Gdańsk','https://ug.edu.pl/'),(15,'Uniwersytet Medyczny w Łodzi','Łódź','https://umed.pl'),(16,'Akademia Ateneum w Gdańsku','Gdańsk','https://www.ateneum.edu.pl'),(17,'Akademia Zamojska','Zamość','https://www.akademiazamojska.edu.pl/'),(18,'Uczelnia Nauk Społecznych w Łodzi','Łódź','https://uns.lodz.pl/'),(19,'Szkoła Główna Gospodarstwa Wiejskiego w Warszawie','Warszawa','https://www.sggw.edu.pl/'),(20,'Uniwersytet Przyrodniczy w Lublinie','Lublin','https://www.up.lublin.pl'),(21,'Szkoła Wyższa Ekonomii i Zarządzania w Łodzi','Łódź','https://www.sweiz.pl'),(22,'Uniwersytet Papieski Jana Pawła II w Krakowie','Kraków','https://www.upjp2.edu.pl'),(23,'Akademia Pedagogiki Specjalnej im. Marii Grzegorzewskiej w Warszawie','Warszawa','http://www.aps.edu.pl'),(24,'Collegium Polonicum w Słubicach, UAM w Poznaniu','Słubice','https://www.cp.edu.pl'),(25,'Wyższa Szkoła Sztuki i Projektowania w Łodzi','Łódź','https://www.wssip.edu.pl'),(26,'Akademia Sztuki Wojennej w Warszawie ','Warszawa','https://www.wojsko-polskie.pl/aszwoj/'),(27,'Akademia Nauk Stosowanych im. J.A. Komeńskiego w Lesznie','Leszno','https://www.pwsz.edu.pl'),(28,'Wyższa Szkoła Turystyki i Ekologii w Suchej Beskidzkiej','Sucha Beskidzka','https://www.wste.edu.pl'),(29,'Politechnika Częstochowska','Częstochowa','https://www.pcz.pl'),(30,'Akademia Nauk Stosowanych im. prof. E. Lipińskiego w Kielcach','Kielce','https://www.wseip.edu.pl'),(31,'Uniwersytet Medyczny w Białymstoku','Białystok','https://www.umb.edu.pl'),(32,'Akademia Nauk Stosowanych im. Stanisława Staszica w Pile','Piła','https://ans.pila.pl/'),(33,'Politechnika Krakowska im. Tadeusza Kościuszki','Kraków','https://www.pk.edu.pl'),(34,'Wyższa Szkoła Biznesu i Nauk o Zdrowiu w Łodzi','Łódź','https://www.wsbinoz.edu.pl'),(35,'Wydział Prawa i Administracji Uniwersytetu Warszawskiego','Warszawa','https://www.wpia.uw.edu.pl'),(36,'Wyższa Szkoła Logistyki w Poznaniu','Poznań','http://www.wsl.com.pl'),(37,'Uniwersytet Ekonomiczny w Krakowie','Kraków','https://www.uek.krakow.pl'),(38,'Państwowa Uczelnia Zawodowa im. Ignacego Mościckiego w Ciechanowie','Ciechanów','https://puzim.edu.pl'),(39,'Szkoła Główna Służby Pożarniczej w Warszawie','Warszawa','https://www.sgsp.edu.pl'),(40,'Wyższa Szkoła Kształcenia Zawodowego ','Wrocław','https://www.studia-online.pl/src-OOU'),(41,'Uniwersytet Warmińsko-Mazurski w Olsztynie','Olsztyn','http://www.uwm.edu.pl'),(42,'Akademia Humanistyczno-Ekonomiczna w Łodzi','Łódź','https://www.ahe.lodz.pl'),(43,'Wyższa Szkoła Biznesu National-Louis University w Nowym Sączu','Nowy Sącz','https://www.wsb-nlu.edu.pl'),(44,'Wojskowa Akademia Techniczna im. J. Dąbrowskiego w Warszawie','Warszawa','https://www.wojsko-polskie.pl/wat/'),(45,'Akademia im. Aleksandra Gieysztora w Pułtusku','Pułtusk','https://pultusk.vistula.edu.pl/'),(46,'Wyższa Szkoła Zarządzania i Bankowości w Poznaniu','Poznań','https://www.wszib.poznan.pl'),(47,'Politechnika Opolska','Opole','https://www.po.opole.pl'),(48,'Europejska Wyższa Szkoła Prawa i Administracji w Warszawie','Warszawa','https://ewspa.edu.pl/'),(49,'Wyższa Szkoła Biznesu National-Louis University, Filia w Tarnowie','Tarnów','https://www.wsb-nlu.edu.pl/pl/studia-tarnow'),(50,'Warszawska Szkoła Zarządzania - Szkoła Wyższa','Warszawa','https://www.wsz-sw.edu.pl'),(51,'Akademia Ignatianum w Krakowie ','Kraków','https://www.ignatianum.edu.pl'),(52,'Pomorska Szkoła Wyższa w Starogardzie Gdańskim','Starogard Gdański','https://twojestudia.pl'),(53,'Akademia Finansów i Biznesu Vistula w Warszawie','Warszawa','https://www.vistula.edu.pl'),(54,'Akademia Mazowiecka w Płocku ','Płock','https://mazowiecka.edu.pl'),(55,'Warszawska Akademia Medyczna Nauk Stosowanych','Warszawa','https://wam.edu.pl/'),(56,'Lubelska Akademia WSEI','Lublin','https://www.wsei.lublin.pl'),(57,'Gdańska Szkoła Wyższa','Gdańsk','https://www.gsw.gda.pl'),(58,'Akademia Nauk Stosowanych w Wałczu','Gdańsk','https://www.pwsz.eu'),(59,'Akademia Nauk Stosowanych im. H. Cegielskiego w Gnieźnie, Uczelnia Państwowa','Gniezno','https://ans-gniezno.edu.pl'),(60,'Wydział Fizyki, Uniwersytet w Białymstoku','Białystok','https://fizyka.uwb.edu.pl/'),(61,'Uniwersytet Rolniczy im. Hugona Kołłątaja w Krakowie','Kraków','https://rekrutacja.urk.edu.pl'),(62,'Uniwersytet Wirtualnej Edukacji','Nowy Sącz','https://www.uwe.edu.pl'),(63,'Społeczna Akademia Nauk w Łodzi','Łódź','https://san.edu.pl'),(64,'Politechnika Rzeszowska im. Ignacego Łukasiewicza','Rzeszów','https://w.prz.edu.pl'),(65,'Uczelnia Jana Wyżykowskiego, Filia w Lubinie','Lubin','http://ujw.pl'),(66,'Wyższa Szkoła Przedsiębiorczości i Administracji w Lublinie','Lublin','https://www.wspa.pl'),(67,'Warszawska Uczelnia Medyczna im. Tadeusza Koźluka','Warszawa','https://www.wumed.edu.pl'),(68,'Akademia Medycznych i Społecznych Nauk Stosowanych w Elblągu','Elbląg','https://amisns.edu.pl/pl/'),(69,'Wyższa Szkoła Europejska im. ks. Józefa Tischnera w Krakowie','Kraków','https://www.wse.krakow.pl'),(70,'Uniwersytet Medyczny im. Piastów Śląskich we Wrocławiu','Wrocław','https://www.umw.edu.pl'),(71,'Uniwersytet WSB Merito w Łodzi','Łódź','https://www.merito.pl/lodz/'),(72,'Powiślańska Szkoła Wyższa','Kwidzyn','https://powislanska.edu.pl/'),(73,'Powiślańska Szkoła Wyższa Filia w Kościerzynie','Kościerzyna','https://powislanska.edu.pl/'),(74,'Polsko-Japońska Akademia Technik Komputerowych, Filia w Gdańsku','Gdańsk','https://gdansk.pja.edu.pl/pl/'),(75,'Akademia Marynarki Wojennej im. Bohaterów Westerplatte w Gdyni','Gdynia','https://amw.gdynia.pl'),(76,'Wyższa Szkoła Zarządzania i Bankowości w Krakowie','Kraków','https://www.wszib.edu.pl'),(77,'Uniwersytet Kardynała Stefana Wyszyńskiego w Warszawie','Warszawa','http://www.uksw.edu.pl'),(78,'Wyższa Szkoła Inżynierii i Zdrowia w Warszawie','Warszawa','https://www.wsiiz.pl'),(79,'Katolicki Uniwersytet Lubelski Jana Pawła II','Lublin','http://kul.pl'),(80,'Collegium Da Vinci w Poznaniu','Poznań','https://cdv.pl'),(81,'Państwowa Wyższa Szkoła Techniczno-Ekonomiczna im. ks. B. Markiewicza w Jarosławiu','Jarosław','https://www.pwste.edu.pl'),(82,'Akademia Nauk Stosowanych w Tarnowie','Tarnów','http://anstar.edu.pl'),(83,'Uniwersytet Przyrodniczy w Poznaniu','Poznań','http://www.up.poznan.pl'),(84,'Akademia Nauk Stosowanych w Raciborzu','Racibórz','https://akademiarac.edu.pl'),(85,'Sopocka Akademia Nauk Stosowanych, Wydział Międzyuczelniany w Gdańsku','Racibórz','https://sopocka.edu.pl/'),(86,'Uniwersytet Medyczny im. Karola Marcinkowskiego w Poznaniu','Poznań','https://www.ump.edu.pl'),(87,'Akademia Nauk Stosowanych w Nowym Sączu','Nowy Sącz','https://www.ans-ns.edu.pl/'),(88,'Polsko-Japońska Akademia Technik Komputerowych w Warszawie','Warszawa','https://www.pja.edu.pl'),(89,'Uczelnia Jana Wyżykowskiego w Polkowicach','Polkowice','http://ujw.pl'),(90,'Podhalańska Państwowa Uczelnia Zawodowa w Nowym Targu','Nowy Targ','http://www.ppuz.edu.pl'),(91,'Collegium Medicum im. L. Rydygiera w Bydgoszczy','Bydgoszcz','https://www.cm.umk.pl'),(92,'Polsko-Japońska Akademia Technik Komputerowych, Filia w Bytomiu','Bytom','https://pja.edu.pl/informatyka-bytom/'),(93,'Szkoła Wyższa Wymiaru Sprawiedliwości w Warszawie','Warszawa','https://swws.edu.pl/'),(94,'Uniwersytet WSB Merito we Wrocławiu','Wrocław','https://www.merito.pl/wroclaw/'),(95,'Collegium Civitas w Warszawie','Wrocław','https://www.civitas.edu.pl'),(96,'Politechnika Poznańska','Poznań','https://www.put.poznan.pl/pl/rekrutacja'),(97,'Gnieźnieńska Szkoła Wyższa Milenium','Gniezno','https://studia.milenium.edu.pl/'),(98,'Pedagogium Wyższa Szkoła Nauk Społecznych w Warszawie','Warszawa','https://www.pedagogium.pl'),(99,'Wyższa Szkoła Administracji i Biznesu im. E. Kwiatkowskiego w Gdyni','Gdynia','https://www.wsaib.pl'),(100,'VIAMODA Szkoła Wyższa w Warszawie','Warszawa','https://www.viamoda.edu.pl'),(101,'Sopocka Akademia Nauk Stosowanych','Sopot','https://sopocka.edu.pl/'),(102,'Uniwersytet Pedagogiczny im. Komisji Edukacji Narodowej w Krakowie','Kraków','https://www.up.krakow.pl'),(103,'Collegium Humanum w Warszawie','Warszawa','https://humanum.pl'),(104,'Uniwersytet WSB Merito w Gdańsku','Gdańsk','https://www.merito.pl/gdansk/'),(105,'Wrocławska Wyższa Szkoła Informatyki Stosowanej HORYZONT','Wrocław','https://www.horyzont.eu'),(106,'Szkoła Główna Turystyki i Hotelarstwa w Warszawie - grupa Vistula','Warszawa','https://www.vistulahospitality.edu.pl'),(107,'Uniwersytet SWPS Katowice','Katowice','https://www.swps.pl/katowice'),(108,'Zachodniopomorski Uniwersytet Technologiczny w Szczecinie','Szczecin','https://www.zut.edu.pl/index.php?id=15622'),(109,'Akademia Śląska w Katowicach','Katowice','https://www.wst.com.pl'),(110,'Collegium Humanum w Rzeszowie','Rzeszów','https://www.humanum.pl/studia-w-rzeszowie'),(111,'Collegium Humanum w Poznaniu','Poznań','https://www.humanum.pl/studia-w-poznaniu'),(112,'Lotnicza Akademia Wojskowa w Dęblinie ','Dęblin','https://www.wojsko-polskie.pl/law'),(113,'Menedżerska Akademia Nauk Stosowanych w Warszawie','Warszawa','https://mans.org.pl/'),(114,'Bydgoska Szkoła Wyższa','Bydgoszcz','https://www.bsw.edu.pl'),(115,'Państwowa Wyższa Szkoła Zawodowa w Głogowie','Głogów','https://pwsz.glogow.pl/'),(116,'WSHiU Akademia Nauk Stosowanych w Poznaniu','Poznań','https://wshiu.pl'),(117,'Uniwersytet WSB Merito w Opolu','Opole','https://www.merito.pl/opole/'),(118,'Uniwersytet WSB Merito w Toruniu','Toruń','https://www.merito.pl/torun/'),(119,'Uniwersytet Przyrodniczy we Wrocławiu','Wrocław','http://www.rekrutacja.upwr.edu.pl'),(120,'Wszechnica Polska Akademia Nauk Stosowanych w Warszawie','Warszawa','https://www.wszechnicapolska.edu.pl'),(121,'Wyższa Szkoła Prawa we Wrocławiu','Wrocław','https://www.prawowroclaw.edu.pl'),(122,'WIT Wyższa Szkoła Informatyki Stosowanej i Zarządzania w Warszawie','Warszawa','https://www.wit.edu.pl'),(123,'Uniwersytet Morski w Gdyni','Gdynia','https://www.umg.edu.pl'),(124,'Uczelnia Łazarskiego w Warszawie','Warszawa','https://rekrutacja.lazarski.pl'),(125,'Akademia Górnośląska im. Wojciecha Korfantego w Katowicach','Katowice','https://www.gwsh.pl'),(126,'Pomorski Uniwersytet Medyczny w Szczecinie','Szczecin','https://www.pum.edu.pl'),(127,'Politechnika Świętokrzyska w Kielcach','Kielce','https://www.tu.kielce.pl'),(128,'Uczelnia Społeczno - Medyczna w Warszawie','Warszawa','https://usmbm.edu.pl'),(129,'Wyższa Szkoła Zdrowia w Gdańsku','Gdańsk','https://www.wsz.pl'),(130,'Wydział Inżynierii Lądowej Politechnika Krakowska','Kraków','https://wil.pk.edu.pl/index.php?lang=pl-pl'),(131,'Wrocławska Akademia Biznesu w Naukach Stosowanych','Wrocław','https://wab.edu.pl/'),(132,'Akademia Nauk Stosowanych TWP w Szczecinie','Szczecin','https://akademiatwp.pl'),(133,'Społeczna Akademia Nauk w Warszawie','Warszawa','http://www.warszawa.san.edu.pl'),(134,'Powiślańska Szkoła Wyższa Filia w Gdańsku','Gdańsk','https://powislanska.edu.pl/'),(135,'Akademia Sztuk Pięknych im. E. Gepperta we Wrocławiu','Wrocław','https://www.asp.wroc.pl'),(136,'Uniwersytet WSB Merito w Poznaniu','Poznań','https://www.merito.pl/poznan/'),(137,'Uniwersytet Szczeciński','Szczecin','https://kandydaci.usz.edu.pl/'),(138,'Uniwersytet WSB Merito Bydgoszcz','Bydgoszcz','https://www.merito.pl/bydgoszcz/'),(139,'Wyższa Szkoła Turystyki i Języków Obcych w Warszawie','Warszawa','https://wstijo.edu.pl'),(140,'Wyższa Szkoła Biznesu i Nauk o Zdrowiu, Filia w Rybniku','Rybnik','http://www.rybnik.wsbinoz.pl'),(141,'Coventry University Wrocław','Wrocław','https://www.coventry.ac.uk/wroclaw/'),(142,'Wyższa Szkoła Ekologii i Zarządzania w Warszawie','Warszawa','https://www.wseiz.pl'),(143,'Uniwersytet WSB Merito w Chorzowie','Chorzów','https://www.merito.pl/chorzow/'),(144,'Uniwersytet Dolnośląski DSW we Wrocławiu','Wrocław','https://www.dsw.edu.pl'),(145,'Uniwersytet Humanistyczno-Przyrodniczy im. Jana Długosza w Częstochowie','Częstochowa','https://www.ujd.edu.pl'),(146,'Politechnika Morska w Szczecinie','Szczecin','https://www.pm.szczecin.pl/'),(147,'WSPiA Rzeszowska Szkoła Wyższa','Rzeszów','http://www.wspia.eu'),(148,'Uniwersytet WSB Merito w Gdyni','Gdynia','https://www.merito.pl/gdynia/'),(149,'Uczelnia WSB Merito w Warszawie','Warszawa','https://www.merito.pl/warszawa/'),(150,'Collegium Humanum we Wrocławiu','Wrocław','https://www.humanum.pl/studia-we-wroclawiu/'),(151,'Wyższa Szkoła Nauk o Zdrowiu w Bydgoszczy','Bydgoszcz','https://www.uczelniamedyczna.pl'),(152,'Uniwersytet WSB Merito w Szczecinie','Szczecin','https://www.merito.pl/szczecin/'),(153,'Powiślańska Szkoła Wyższa Filia w Toruniu','Toruń','https://powislanska.edu.pl/');
/*!40000 ALTER TABLE `university` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usos_login`
--

DROP TABLE IF EXISTS `usos_login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usos_login` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `access_token` varchar(100) NOT NULL,
  `refresh_token` varchar(100) NOT NULL,
  `expiration_time` datetime NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usos_login`
--

LOCK TABLES `usos_login` WRITE;
/*!40000 ALTER TABLE `usos_login` DISABLE KEYS */;
/*!40000 ALTER TABLE `usos_login` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-11 14:30:03
