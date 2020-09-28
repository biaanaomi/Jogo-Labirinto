drop table if exists userinfo;
   CREATE TABLE `user_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(30),
  `tempo` varchar(30),
  PRIMARY KEY (`id`)
);