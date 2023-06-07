/*
 Navicat Premium Data Transfer

 Source Server         : Mysql
 Source Server Type    : MySQL
 Source Server Version : 80032 (8.0.32)
 Source Host           : 127.0.0.1:3306
 Source Schema         : DB_Draft

 Target Server Type    : MySQL
 Target Server Version : 80032 (8.0.32)
 File Encoding         : 65001

 Date: 07/06/2023 20:15:23
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for content
-- ----------------------------
DROP TABLE IF EXISTS `content`;
CREATE TABLE `content` (
  `docname` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `content` text COLLATE utf8mb4_general_ci NOT NULL,
  `format` text COLLATE utf8mb4_general_ci NOT NULL,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`docname`,`username`) USING BTREE,
  KEY `content_ibfk_2` (`username`),
  CONSTRAINT `content_ibfk_1` FOREIGN KEY (`docname`) REFERENCES `document` (`docname`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `content_ibfk_2` FOREIGN KEY (`username`) REFERENCES `document` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for document
-- ----------------------------
DROP TABLE IF EXISTS `document`;
CREATE TABLE `document` (
  `docname` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `createtime` datetime NOT NULL,
  `updatetime` datetime NOT NULL,
  `size` int NOT NULL,
  `username` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`docname`,`username`) USING BTREE,
  KEY `username` (`username`),
  KEY `docname` (`docname`),
  CONSTRAINT `document_ibfk_1` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for history
-- ----------------------------
DROP TABLE IF EXISTS `history`;
CREATE TABLE `history` (
  `docname` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `modtime` datetime NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `size` int NOT NULL,
  PRIMARY KEY (`docname`,`username`,`modtime`) USING BTREE,
  KEY `username` (`username`),
  CONSTRAINT `history_ibfk_1` FOREIGN KEY (`docname`) REFERENCES `document` (`docname`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `history_ibfk_2` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for permission
-- ----------------------------
DROP TABLE IF EXISTS `permission`;
CREATE TABLE `permission` (
  `username` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `docname` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `shareable` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0',
  `sharee` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `writable` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0',
  PRIMARY KEY (`username`,`docname`),
  KEY `docname` (`docname`),
  KEY `sharee` (`sharee`),
  CONSTRAINT `permission_ibfk_1` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `permission_ibfk_2` FOREIGN KEY (`docname`) REFERENCES `document` (`docname`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `username` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- View structure for user_documents
-- ----------------------------
DROP VIEW IF EXISTS `user_documents`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `user_documents` AS select `u`.`username` AS `username`,`d`.`docname` AS `docname`,`d`.`createtime` AS `createtime`,`d`.`updatetime` AS `updatetime`,`d`.`size` AS `size`,`p`.`shareable` AS `shareable`,`p`.`sharee` AS `sharee`,`p`.`writable` AS `writable` from ((`user` `u` join `document` `d` on((`u`.`username` = `d`.`username`))) left join `permission` `p` on(((`d`.`docname` = `p`.`docname`) and (`u`.`username` = `p`.`username`))));

SET FOREIGN_KEY_CHECKS = 1;
