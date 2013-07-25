# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.5.27)
# Database: soya
# Generation Time: 2013-05-29 00:57:20 +0000
# Generation Time: 2013-05-29 00:57:20 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table admins
# ------------------------------------------------------------

DROP TABLE IF EXISTS `admins`;

CREATE TABLE `admins` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `encrypted_password` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `reset_password_token` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `reset_password_sent_at` datetime DEFAULT NULL,
  `remember_created_at` datetime DEFAULT NULL,
  `sign_in_count` int(11) DEFAULT '0',
  `current_sign_in_at` datetime DEFAULT NULL,
  `last_sign_in_at` datetime DEFAULT NULL,
  `current_sign_in_ip` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `last_sign_in_ip` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `confirmation_token` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `confirmed_at` datetime DEFAULT NULL,
  `confirmation_sent_at` datetime DEFAULT NULL,
  `unconfirmed_email` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `authentication_token` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_admins_on_email` (`email`),
  UNIQUE KEY `index_admins_on_reset_password_token` (`reset_password_token`),
  UNIQUE KEY `index_admins_on_confirmation_token` (`confirmation_token`),
  UNIQUE KEY `index_admins_on_authentication_token` (`authentication_token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



# Dump of table bbs_post_analysis_categorizeds
# ------------------------------------------------------------

DROP TABLE IF EXISTS `bbs_post_analysis_categorizeds`;

CREATE TABLE `bbs_post_analysis_categorizeds` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bbs_post_id` int(11) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `label_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_bbs_post_analysis_categorizeds_on_bbs_post_id` (`bbs_post_id`),
  KEY `index_bbs_post_analysis_categorizeds_on_category_id` (`category_id`),
  KEY `index_bbs_post_analysis_categorizeds_on_label_id` (`label_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



# Dump of table bbs_posts
# ------------------------------------------------------------

DROP TABLE IF EXISTS `bbs_posts`;

CREATE TABLE `bbs_posts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `info_source_id` int(11) DEFAULT NULL,
  `keyword_id` int(11) DEFAULT NULL,
  `urgency` int(11) DEFAULT NULL,
	`bbs_user_screen_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `url` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `title` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `content` text COLLATE utf8_unicode_ci,
  `read_count` int(11) DEFAULT NULL,
  `comment_count` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `index_bbs_posts_on_info_source_id` (`info_source_id`),
  KEY `index_bbs_posts_on_keyword_id` (`keyword_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



# Dump of table blog_post_analysis_categorizeds
# ------------------------------------------------------------

DROP TABLE IF EXISTS `blog_post_analysis_categorizeds`;

CREATE TABLE `blog_post_analysis_categorizeds` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `blog_post_id` int(11) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `label_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_blog_post_analysis_categorizeds_on_blog_post_id` (`blog_post_id`),
  KEY `index_blog_post_analysis_categorizeds_on_category_id` (`category_id`),
  KEY `index_blog_post_analysis_categorizeds_on_label_id` (`label_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



# Dump of table blog_posts
# ------------------------------------------------------------

DROP TABLE IF EXISTS `blog_posts`;

CREATE TABLE `blog_posts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `info_source_id` int(11) DEFAULT NULL,
  `keyword_id` int(11) DEFAULT NULL,
  `urgency` int(11) DEFAULT NULL,
  `url` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `blog_user_screen_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `title` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `content` text COLLATE utf8_unicode_ci,
  `read_count` int(11) DEFAULT NULL,
  `comment_count` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `index_blog_posts_on_info_source_id` (`info_source_id`),
  KEY `index_blog_posts_on_keyword_id` (`keyword_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



# Dump of table categories
# ------------------------------------------------------------

DROP TABLE IF EXISTS `categories`;

CREATE TABLE `categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `str` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `by_keyword` tinyint(1) DEFAULT '0',
  `str_en` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;

INSERT INTO `categories` (`id`, `str`, `by_keyword`, `str_en`)
VALUES
	(1,'情感',0,'sentiment'),
	(2,'关键词分类',1,'keywords'),
	(3,'语义分类',0,'semantic');

/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table delayed_jobs
# ------------------------------------------------------------

DROP TABLE IF EXISTS `delayed_jobs`;

CREATE TABLE `delayed_jobs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `priority` int(11) DEFAULT '0',
  `attempts` int(11) DEFAULT '0',
  `handler` text COLLATE utf8_unicode_ci,
  `last_error` text COLLATE utf8_unicode_ci,
  `run_at` datetime DEFAULT NULL,
  `locked_at` datetime DEFAULT NULL,
  `failed_at` datetime DEFAULT NULL,
  `locked_by` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `queue` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `delayed_jobs_priority` (`priority`,`run_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



# Dump of table info_source_types
# ------------------------------------------------------------

DROP TABLE IF EXISTS `info_source_types`;

CREATE TABLE `info_source_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `str` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `enstr` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

LOCK TABLES `info_source_types` WRITE;
/*!40000 ALTER TABLE `info_source_types` DISABLE KEYS */;

INSERT INTO `info_source_types` (`id`, `str`, `enstr`)
VALUES
	(1,'微博信息','weibo'),
	(2,'社区论坛','bbs'),
	(3,'新闻站点','news'),
	(4,'百科知道','wiki'),
	(5,'视频网站','video'),
	(6,'知名博客','blog');

/*!40000 ALTER TABLE `info_source_types` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table info_sources
# ------------------------------------------------------------

DROP TABLE IF EXISTS `info_sources`;

CREATE TABLE `info_sources` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `str` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `period` int(11) DEFAULT NULL,
  `info_source_type_id` int(11) DEFAULT NULL,
  `user_url` varchar(60) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

LOCK TABLES `info_sources` WRITE;
/*!40000 ALTER TABLE `info_sources` DISABLE KEYS */;

INSERT INTO `info_sources` (`id`, `str`, `period`, `info_source_type_id`, `user_url`)
VALUES
	(null,'凤凰山下论坛',120,2,'http://www.dz19.net/'),
	(null,'开县乡情论坛',120,2,'http://bbs.cqkx.com/forum.php'),
	(null,'人民网四川频道',120,3,'http://sc.people.com.cn/'),
	(null,'中国新闻网四川新闻',120,3,'http://www.sc.chinanews.com.cn/'),
	(null,'成都商报',120,3,'http://e.chengdu.cn/'),
	(null,'金融投资报',120,3,'http://www.stocknews.sc.cn/');
-- 	(1,'新浪微博',30,1,'http://weibo.com/u/'),
-- 	(2,'百度知道',720,4,''),
-- 	(3,'优酷视频',1440,5,''),
-- 	(4,'天涯论坛',720,2,''),
-- 	(5,'新浪微博-热门',30,1,''),
-- 	(6,'新浪微博-搜索',30,1,''),
-- 	(7,'腾讯微博',60,1,'http://t.qq.com/'),
-- 	(8,'网易微博',120,1,' http://t.163.com/'),
-- 	(9,'搜狐微博',120,1,' http://t.sohu.com/user/index_nologin.jsp?uid='),
-- 	(10,'百度新闻',720,3,''),
-- 	(11,'谷歌新闻',720,3,''),
-- 	(12,'百度贴吧',360,2,''),
-- 	(13,'搜搜问问',720,4,''),
-- 	(14,'新浪博客',360,6,''),
-- 	(15,'百度新闻-对手',720,3,''),
-- 	(16,'谷歌新闻-对手',720,3,'');

/*!40000 ALTER TABLE `info_sources` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table jobs
# ------------------------------------------------------------

DROP TABLE IF EXISTS `jobs`;

CREATE TABLE `jobs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `info_source_id` int(11) NOT NULL,
  `fetched_info_count` int(11) NOT NULL,
  `real_fetched_info_count` int(11) NOT NULL,
  `previous_executed` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  KEY `index_jobs_on_info_source_id` (`info_source_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

LOCK TABLES `jobs` WRITE;
/*!40000 ALTER TABLE `jobs` DISABLE KEYS */;

INSERT INTO `jobs` (`id`, `info_source_id`, `fetched_info_count`, `real_fetched_info_count`, `previous_executed`)
VALUES
	(1,1,0,0,'2013-04-01 00:00:00'),
	(2,1,50,50,'2013-05-22 00:14:31'),
	(3,2,38,35,'2013-05-28 18:04:34');

/*!40000 ALTER TABLE `jobs` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table keywords
# ------------------------------------------------------------

DROP TABLE IF EXISTS `keywords`;

CREATE TABLE `keywords` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `str` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

LOCK TABLES `keywords` WRITE;
/*!40000 ALTER TABLE `keywords` DISABLE KEYS */;

INSERT INTO `keywords` (`id`, `str`)
VALUES
	(1,'中国邮政储蓄银行四川省分行'),
	(2,'邮储银行'),
	(3,'邮储银行四川');

/*!40000 ALTER TABLE `keywords` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table label_keywords
# ------------------------------------------------------------

DROP TABLE IF EXISTS `label_keywords`;

CREATE TABLE `label_keywords` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `label_id` int(11) DEFAULT NULL,
  `str` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `index_label_keywords_on_label_id` (`label_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



# Dump of table labels
# ------------------------------------------------------------

DROP TABLE IF EXISTS `labels`;

CREATE TABLE `labels` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `str` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `str_en` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

LOCK TABLES `labels` WRITE;
/*!40000 ALTER TABLE `labels` DISABLE KEYS */;

INSERT INTO `labels` (`id`, `str`, `category_id`, `str_en`)
VALUES
	(1,'正面',0,'positive'),
	(2,'中性',0,'neutral'),
	(3,'负面',0,'negative'),
	(4,'集团领导',1,'jtld'),
	(5,'五星电器',1,'wxdq'),
	(6,'百思买',1,'bsm');

/*!40000 ALTER TABLE `labels` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table news
# ------------------------------------------------------------

DROP TABLE IF EXISTS `news`;

CREATE TABLE `news` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `info_source_id` int(11) DEFAULT NULL,
  `keyword_id` int(11) DEFAULT NULL,
  `source_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `urgency` int(11) DEFAULT NULL,
  `url` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `title` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `content` text COLLATE utf8_unicode_ci,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



# Dump of table operations
# ------------------------------------------------------------

DROP TABLE IF EXISTS `operations`;

CREATE TABLE `operations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `handled` tinyint(1) DEFAULT '0',
  `ignored` tinyint(1) DEFAULT '0',
  `handled_alert` tinyint(1) DEFAULT '0',
  `ignored_alert` tinyint(1) DEFAULT '0',
  `operatable_id` int(11) DEFAULT NULL,
  `operatable_type` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



# Dump of table schema_migrations
# ------------------------------------------------------------

DROP TABLE IF EXISTS `schema_migrations`;

CREATE TABLE `schema_migrations` (
  `version` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  UNIQUE KEY `unique_schema_migrations` (`version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

LOCK TABLES `schema_migrations` WRITE;
/*!40000 ALTER TABLE `schema_migrations` DISABLE KEYS */;

INSERT INTO `schema_migrations` (`version`)
VALUES
	('20130419134944'),
	('20130419135456'),
	('20130420063950'),
	('20130420070541'),
	('20130420071654'),
	('20130420090314'),
	('20130421103210'),
	('20130421103654'),
	('20130421105613'),
	('20130421110704'),
	('20130421111614'),
	('20130423020746'),
	('20130423081224'),
	('20130427074754'),
	('20130427075312'),
	('20130427075715'),
	('20130427075743'),
	('20130427080203'),
	('20130427080212'),
	('20130521152130'),
	('20130524151417'),
	('20130527101654'),
	('20130528124930');

/*!40000 ALTER TABLE `schema_migrations` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table video_post_analysis_categorizeds
# ------------------------------------------------------------

DROP TABLE IF EXISTS `video_post_analysis_categorizeds`;

CREATE TABLE `video_post_analysis_categorizeds` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `video_post_id` int(11) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `label_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_video_post_analysis_categorizeds_on_video_post_id` (`video_post_id`),
  KEY `index_video_post_analysis_categorizeds_on_category_id` (`category_id`),
  KEY `index_video_post_analysis_categorizeds_on_label_id` (`label_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



# Dump of table video_posts
# ------------------------------------------------------------

DROP TABLE IF EXISTS `video_posts`;

CREATE TABLE `video_posts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `info_source_id` int(11) DEFAULT NULL,
  `keyword_id` int(11) DEFAULT NULL,
  `urgency` int(11) DEFAULT NULL,
  `video_user_screen_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `title` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `watch_count` int(11) DEFAULT NULL,
  `comment_count` int(11) DEFAULT NULL,
  `up_count` int(11) DEFAULT NULL,
  `down_count` int(11) DEFAULT NULL,
  `repost_count` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `index_video_posts_on_info_source_id` (`info_source_id`),
  KEY `index_video_posts_on_keyword_id` (`keyword_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



# Dump of table weibo_status_analysis_categorizeds
# ------------------------------------------------------------

DROP TABLE IF EXISTS `weibo_status_analysis_categorizeds`;

CREATE TABLE `weibo_status_analysis_categorizeds` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `weibo_status_id` int(11) DEFAULT NULL,
  `label_id` int(11) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_weibo_status_analysis_categorizeds_on_weibo_status_id` (`weibo_status_id`),
  KEY `index_weibo_status_analysis_categorizeds_on_label_id` (`label_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



# Dump of table weibo_statuses
# ------------------------------------------------------------

DROP TABLE IF EXISTS `weibo_statuses`;

CREATE TABLE `weibo_statuses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `weibo_origin_id` int(11) NOT NULL,
  `weibo_user_id` int(11) DEFAULT NULL,
  `weibo_user_screen_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `info_source_id` int(11) DEFAULT NULL,
  `keyword_id` int(11) DEFAULT NULL,
  `repost_count` int(11) NOT NULL,
  `comment_count` int(11) NOT NULL,
  `retweeted` tinyint(1) DEFAULT '0',
  `retweeted_status_id` int(11) DEFAULT NULL,
  `with_picture` tinyint(1) DEFAULT '0',
  `pic_address` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `geo_info_city` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `geo_info_province` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `urgency` int(11) DEFAULT '0',
  `text` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

LOCK TABLES `weibo_statuses` WRITE;
/*!40000 ALTER TABLE `weibo_statuses` DISABLE KEYS */;

INSERT INTO `weibo_statuses` (`id`, `url`, `weibo_origin_id`, `weibo_user_id`, `weibo_user_screen_name`, `info_source_id`, `keyword_id`, `repost_count`, `comment_count`, `retweeted`, `retweeted_status_id`, `with_picture`, `pic_address`, `geo_info_city`, `geo_info_province`, `urgency`, `text`, `created_at`)
VALUES
	(1,'http://weibo.com/1696300250/zxLqWFntM',2147483647,1,'辉爷是总攻',1,1,0,2,0,NULL,NULL,NULL,'南京','江苏',0,'@南京五星电器 【投诉】315在新街口五星电器买了西门子一台冰箱一台洗衣机，当时发票上开的是常用名，跟身份证上名字不一样，当时询问销售员，销售员表示不妨碍拿节能补贴，现在去拿，说是名字不一样不能拿，之后就是一直拖着不解决，明显是想等5月结束节能补贴发放，求解决','2013-05-21 19:06:59'),
	(2,'http://weibo.com/2636968650/zxLqCj9cQ',2147483647,2,'OMG你是Q',1,1,0,0,0,NULL,NULL,'http://ww2.sinaimg.cn/thumbnail/9d2cf2cajw1e4w4koib26j20c70ejjsc.jpg','福州','福建',0,'【百思买任命周猛为中国区总裁兼五星电器CEO】五星电器今天宣布，将由周猛担任公司的首席执行官（CEO），周猛同时被任命为五星电器母公司百思买的中国区总裁。他将负责五星电器的零售连锁，其在线及数字业务，还包括百思买移动正在试验中的中国业务。','2013-05-21 19:06:10'),
	(3,'http://weibo.com/1725401854/zxKPh7224',2147483647,3,'flysky66',1,1,0,0,1,NULL,NULL,NULL,'南京','江苏',0,'不错 //@向恩永:[鼓掌] //@五星刘娣Eliane://@五星电器南京新街口旗舰店:五星电器电器新街口旗舰店视听部员工许奇辰精彩出演 #极品前任# 亲 你的前任也是极品嘛 五星人转起来~~@南京五星电器 @五星电器@天蝎1015V @张莲V @木木---Love @卞卞就是我 @糖糖姑姑2012 @五星刘娣Eliane @王军@','2013-05-21 17:34:12'),
	(4,'http://weibo.com/2258726652/zxKGApVjH',2147483647,4,'杭州五星电器',1,1,0,0,0,NULL,NULL,'http://ww3.sinaimg.cn/thumbnail/86a16efcjw1e4w1ao7vbrj20cn138q9d.jpg','杭州','浙江',0,'#五星电器 星推荐#抢节能补贴迎8周年庆典，5.24起钜献3天   载誉全城！存10得100，存30得300；满1000降200，满2000降400… 现小编给您推荐几款家底节能产品~~~~','2013-05-21 17:12:46'),
	(5,'http://weibo.com/1883869391/zxKrU36lR',2147483647,5,'南京五星电器',1,1,0,1,1,NULL,NULL,NULL,'南京','江苏',0,'[笑哈哈]五星人许奇辰的首次触影，大家有钱的捧个钱场没钱的捧个人场[笑哈哈]//@五星电器南京新街口旗舰店:五星电器电器新街口旗舰店视听部员工许奇辰精彩出演 #极品前任# ','2013-05-21 16:36:35'),
	(6,'http://weibo.com/1761874477/zxKoKpusp',2147483647,6,'五星刘娣Eliane',1,1,3,1,1,NULL,NULL,NULL,'南京','江苏',0,'//@五星电器南京新街口旗舰店:五星电器电器新街口旗舰店视听部员工许奇辰精彩出演 #极品前任# 亲 你的前任也是极品嘛 五星人转起来~~@南京五星电器 @五星电器@天蝎1015V @张莲V @木木---Love @卞卞就是我 @糖糖姑姑2012 @五星刘娣Eliane @王军@','2013-05-21 16:28:50'),
	(7,'http://weibo.com/1879439790/zxIXDjZtR',2147483647,7,'汪志晓',1,1,0,1,1,NULL,NULL,NULL,'无锡','江苏',0,'在五星电器这也设立一个吧//@21视点: 转发微博','2013-05-21 12:49:17'),
	(8,'http://weibo.com/1750024131/zxIESfuN4',2147483647,8,'奈何花落殇红颜',1,1,0,0,0,NULL,NULL,NULL,'南通','江苏',0,'囯家节能补贴5月31日结束，彩电要涨价!5月24-27日，五星电器联合TCL彩电举办员工及亲属超级福利内购会带您赶上节能补贴末班车。32寸蓝光LED补贴价仅需1390元；42寸3D网络电视补贴价2999元；48寸3D网络电视补贴价仅3999元；如有需求请至五星电器，错过了节能补贴将不会再有机会!','2013-05-21 12:03:05'),
	(9,'http://weibo.com/3179664973/zxIvGdPKS',2147483647,9,'环保华骄地板',1,1,0,0,0,NULL,NULL,NULL,'成都','四川',0,'【大卫地板溧阳金牌联盟建材工厂内供会销量喜人】大卫地板溧阳金牌联盟建材工厂内供会销量喜人 5月5日，溧阳市金牌联盟建材工厂内供会在新体育馆内盛大举行。大卫地板、友邦集成吊顶、大自然木门、杜菲尼卫浴、五星电器等...  --@大卫地板官方微博 的微刊《大卫地板新闻》 http://t.cn/zH2UsVL','2013-05-21 11:40:26'),
	(10,'http://weibo.com/3302477951/zxHSnAsA4',2147483647,10,'余洪飞3302477951',1,1,0,1,1,NULL,NULL,NULL,'','其它',0,'我在五星电器买家电呢！//@值-得://@河南五星电器:[鼓掌]','2013-05-21 10:03:37'),
	(11,'http://weibo.com/2367108870/zxHFWkUZ4',2147483647,11,'辛辛辛辛_小辛',1,1,1,1,0,NULL,NULL,NULL,'郑州','河南',0,'五一买的空调，本想着有优惠，却买了一肚子气，@五星电器  你们的奥克斯@奥克斯 专柜答应我十天后装机，然后我十五号左右去问告诉我在联系发货，买都买了我肯定等了，二十号去问，你们的郑州碧沙岗店铺装修，柜台都空了，然后告诉我没有货，你们早点不知道通知我没有货？难道冬天我才能用吗？真可恶！','2013-05-21 09:32:59'),
	(12,'http://weibo.com/2896573320/zxD1ntDah',2147483647,12,'南京花婆婆绘本馆',1,1,0,5,1,NULL,NULL,NULL,'南京','江苏',0,'您好，我们故事馆在龙江省妇幼对面，江东北路305号滨江广场2幢17楼下面有个大的五星电器。。。我们最小的孩子是2岁呢！！！欢迎您来看看哦~','2013-05-20 21:42:04'),
	(13,'http://weibo.com/1435830410/zxCLiv8aR',2147483647,13,'南京小蜗牛',1,1,0,0,1,NULL,NULL,NULL,'南京','江苏',0,'同问。应该可以通过发卡单位查到丢卡人联系电话。//@丰一源陈志清: 请教：市民卡是什么东西？良民证？呵呵//@张旭东南京: //@混搭Queen小新:好粗心的顾客啊！扩散！@南京小蜗牛 @张旭东南京 //@五星电器:扩散：有丢失市民卡的南京顾客请前往珠江路五星电器门店。//@直播南京官方版: 转发微博','2013-05-20 21:02:27'),
	(14,'http://weibo.com/1870578244/zxC5H8OFy',2147483647,14,'熊亚茹',1,1,0,0,0,NULL,NULL,'http://ww4.sinaimg.cn/thumbnail/6f7ec244jw1e4uzcnkckpj20dw1vfn2j.jpg','济宁','山东',0,'……这不就是多了个加密功能 没发现更智能在哪 小便又忽悠 // @五星电器: 高度改装后的这台机器能做的比一般Windows智能手机更多。它可以收发电子邮件，播放视频和音频，编纂Office文档，上网冲浪，以及同步日历、联系人和行程。最后，没错，它还可以打电话——无论是给加密或非 http://t.cn/zHw1JlI','2013-05-20 19:19:55'),
	(15,'http://weibo.com/3025322725/zxBHywwhk',2147483647,15,'MyLoft寡人',1,1,0,0,0,NULL,NULL,'http://ww1.sinaimg.cn/thumbnail/b452c2e5jw1e4uxmsbjeqj20c70ejjsc.jpg','黑河','黑龙江',0,'【百思买任命周猛为中国区总裁兼五星电器CEO】五星电器今天宣布，将由周猛担任公司的首席执行官（CEO），周猛同时被任命为五星电器母公司百思买的中国区总裁。他将负责五星电器的零售连锁，其在线及数字业务，还包括百思买移动正在试验中的中国业务。','2013-05-20 18:20:25'),
	(16,'http://weibo.com/2258726652/zxBDn4MEj',2147483647,4,'杭州五星电器',1,1,0,1,0,NULL,NULL,'http://ww2.sinaimg.cn/thumbnail/86a16efcjw1e4uxc1n9qpj20co0s3tc7.jpg','杭州','浙江',0,'#节能补贴倒计时11天#“快跑，节能补贴快结束了，来不及了！”“什么？节能补贴5月底就要结束了？靠，你怎么不早说！”“告诉我，哪里还能搭上最后节能补贴的末班车！”#小新偷偷告诉你：五星电器节能补贴末班车到站停靠啦，6月1日即将开往你看不到的远方#','2013-05-20 18:10:06'),
	(17,'http://weibo.com/2671717811/zxBaQeX6M',2147483647,16,'丰一源陈志清',1,1,1,0,1,NULL,NULL,NULL,'深圳','广东',0,'请教：市民卡是什么东西？良民证？呵呵//@张旭东南京: //@混搭Queen小新:好粗心的顾客啊！扩散！@南京小蜗牛 @张旭东南京 //@五星电器:扩散：有丢失市民卡的南京顾客请前往珠江路五星电器门店。//@直播南京官方版: 转发微博','2013-05-20 16:59:52'),
	(18,'http://weibo.com/2017927407/zxAYp2NWm',2147483647,17,'晗涵viola',1,1,0,2,0,NULL,NULL,NULL,'南京','江苏',0,'@西门子家电 【投诉】我家2012年9月在江苏省宿迁市泗洪县五星电器买的西门子的抽烟机和煤气灶。抽油烟机没有油壶。9个月过去了，还没有给装。煤气灶灶头也换了。打了2个月的电话让西门子泗洪维修部人来修。到现在也没有人来。现在完全不能用了。来个人维修下那么难吗？','2013-05-20 16:29:11'),
	(19,'http://weibo.com/2022372735/zxAYeFTvh',2147483647,18,'Belong_孙楠',1,1,0,0,1,NULL,NULL,NULL,'南京','江苏',0,'//@张旭东南京://@混搭Queen小新:好粗心的顾客啊！扩散！@南京小蜗牛 @张旭东南京 //@五星电器:扩散：有丢失市民卡的南京顾客请前往珠江路五星电器门店。//@直播南京官方版: 转发微博','2013-05-20 16:28:48'),
	(20,'http://weibo.com/1683205152/zxAVYAXDU',2147483647,19,'张旭东南京',1,1,3,5,1,NULL,NULL,NULL,'南京','江苏',0,'//@混搭Queen小新:好粗心的顾客啊！扩散！@南京小蜗牛 @张旭东南京 //@五星电器:扩散：有丢失市民卡的南京顾客请前往珠江路五星电器门店。//@直播南京官方版: 转发微博','2013-05-20 16:23:15'),
	(21,'http://weibo.com/2268832064/zxAqEkNII',2147483647,20,'常州五星电器',1,1,0,1,0,NULL,NULL,'http://ww3.sinaimg.cn/thumbnail/873ba140jw1e4us0invm9j20if03caak.jpg','常州','江苏',0,'#致我们即将逝去的节能补贴#没有什么能够阻挡，你对省钱的向往！经过五一黄金周，依然对价格彷徨！待你犹豫过五月，节能补贴已错过！千万不要等到逝去时，才追悔莫及！节能家电疯抢月与你不见不散！再美好的东西，都有失去的一天；再触底的价格，也有终止的一天！省钱就从常州五星电器节能家电疯抢走起','2013-05-20 15:06:03'),
	(22,'http://weibo.com/2668760014/zxzLbfzUe',2147483647,21,'一见钟芹相守一生',1,1,0,0,0,NULL,NULL,NULL,'盐城','江苏',0,'海信智能变频冰箱，凝聚专业力量，融粹独有科技，以智慧开启活水保鲜时代，为你奉上最水嫩新鲜的食物，让您轻松感受新鲜生活。节能补贴即将逝去之时，海信给予你品质与价格的双重享受，183升1299，对开门3999，210升1799，选择海信冰箱，活的不一样！5月24日到31日，疯狂8天！欢迎到五星电器选购！','2013-05-20 13:23:52'),
	(23,'http://weibo.com/1785493814/zxzaVrL5x',2147483647,22,'Cecilia晓小',1,1,24,10,0,NULL,NULL,NULL,'南京','江苏',0,'在五星买的家电…钱都付了…结果带我家电卖了…不愿意处理…就给你一句话…你愿意补差价…你就换？你原来那个没有了…没有想到那么大的五星电器就是这样处理事情…坐了一个小时一个领导都见不到…@南京零距离  我在这里:http://t.cn/zj58UR7','2013-05-20 11:54:35'),
	(24,'http://weibo.com/2911208041/zxz01F5RM',2147483647,23,'瑞祥商联卡-楽',1,1,0,0,0,NULL,NULL,NULL,'南京','江苏',0,'端午到，福利到，员工福利 商务馈赠 一卡百通 瑞祥商联卡！赶快购买吧，可在东方商城 金鹰仙林店 苏宁环球购物中心 奥特莱斯 五星电器 新世界百货 欧尚超市 望湘园 川味观 巴黎贝甜 常青藤 座上客等400家商户消费，消费还享受折扣哦！南京 镇江 盐城通用 购卡热线：18260028439 何经理 送卡上门服务','2013-05-20 11:27:44'),
	(25,'http://weibo.com/1939076760/zxyVe7eQu',2147483647,24,'四川五星电器',1,1,0,0,0,NULL,NULL,'http://ww3.sinaimg.cn/thumbnail/7393f698gw1e4ulczisizj20hs0d940n.jpg','成都','四川',0,'#节能补贴倒计时#世界上最远的距离不是你在办以旧换新，我在纠结农村户口，而是错过了五一促销，你却不知道节能补贴即将到期！截止日期：5月31号，观望等不来实惠！五星电器三重补贴助你抢搭节能家电末班车！','2013-05-20 11:15:54'),
	(26,'http://weibo.com/1750441861/zxySW0Xdb',2147483647,25,'银联商务江苏分公司',1,1,0,0,0,NULL,NULL,'http://ww2.sinaimg.cn/thumbnail/68559f85jw1e4ul75g7xyj20hs0d93zm.jpg','南京','江苏',0,'#持卡人慧支付#你有没有想买的电器却囊中羞涩？你是不是消费观念超前的人？扬州五星电器银联商务终端开通光大银行信用卡分期功能啦~~~~用稍许的利息就可以享受当下哦！[太开心] ','2013-05-20 11:10:15'),
	(27,'http://weibo.com/3447776930/zxyCLCYJy',2147483647,26,'青岛LaterOnClub',1,1,0,0,0,NULL,NULL,'http://ww4.sinaimg.cn/thumbnail/cd80e6a2tw1e4uk1gpt8hj20hs0notds.jpg','青岛','山东',0,'台东婚纱街 五星电器对面 大叔韩国料理 强力推荐！！！','2013-05-20 10:30:26'),
	(28,'http://weibo.com/2275124761/zxxhkv9LM',2147483647,27,'千金688',1,1,0,0,0,NULL,NULL,NULL,'盐城','江苏',0,' 补贴是一场相逢 2013年5月31日 国家补贴，政策的利好 是短暂的狂 欢 节能补贴的终极盛宴 是我们送给自己的礼物 你可以不在乎几百补贴 但可别怪我没有告诉你 国家发改委明确表示，节能补贴过后，不 会再有国家家电惠民政策，同时彩电必将涨价!! 5月31日前我们在五星电器与你相约!','2013-05-20 07:04:52'),
	(29,'http://weibo.com/2258726652/zxtp7pzyn',2147483647,4,'杭州五星电器',1,1,0,0,0,NULL,NULL,'http://ww4.sinaimg.cn/thumbnail/86a16efcjw1e4tx021e43j20cq13qgsb.jpg','杭州','浙江',0,'#五星电器星推荐#潮人就是我——五星电器3C特卖季火热进行中，现小编给你推荐几款3C潮品，可至您身边的五星电器选购~~~','2013-05-19 21:13:05'),
	(30,'http://weibo.com/1851283422/zxt7QwaJw',2147483647,28,'广州智造',1,1,0,0,0,NULL,NULL,'http://ww2.sinaimg.cn/thumbnail/6e5857dejw1e4tvrsjgqxj208w04gwek.jpg','广州','广东',0,'【传统企业做电商一周要闻5.11—5.17】受到电商、库存、业绩等因素的冲击，传统零售商们在不断的调整着各自的战略。优衣库加速海外扩张的步伐，耐克中华区与美国沃尔玛都将换帅，百思买旗下的五星电器也在布局线上业务等。http://t.cn/zTs4NnM  ','2013-05-19 20:30:31'),
	(31,'http://weibo.com/1667260624/zxsR5fWvy',2147483647,29,'我是泰山',1,1,6,2,0,NULL,NULL,NULL,'合肥','安徽',0,'@五星电器 你们不知道时间就是金钱吗，你们一而再，再而三的欺骗顾客，你们很爽吗？约好18号送货，却说因下雨推到19号，那也罢了，居然19号让我早上9点等到晚上19点，好，我也忍了，可你们送货只送一样，剩下的还要我再等一天。你们就这样服务吗?你让@苏宁 @国美 情何以堪?','2013-05-19 19:49:13'),
	(32,'http://weibo.com/3322750910/zxsujodmD',2147483647,30,'jl4ever1968',1,1,0,0,0,NULL,NULL,'http://ww3.sinaimg.cn/thumbnail/c60d27bejw1e4tsyfzkgaj20c70ejjsc.jpg','巴南区','重庆',0,'【百思买任命周猛为中国区总裁兼五星电器CEO】五星电器今天宣布，将由周猛担任公司的首席执行官（CEO），周猛同时被任命为五星电器母公司百思买的中国区总裁。他将负责五星电器的零售连锁，其在线及数字业务，还包括百思买移动正在试验中的中国业务。','2013-05-19 18:53:05'),
	(33,'http://weibo.com/3365513632/zxqNAAlcY',2147483647,31,'amber黄小瑞_2006',1,1,0,0,0,NULL,NULL,'http://ww1.sinaimg.cn/thumbnail/c899a9a0jw1e4tlhzqiujj20c70ejjsc.jpg','成都','四川',0,'【百思买任命周猛为中国区总裁兼五星电器CEO】五星电器今天宣布，将由周猛担任公司的首席执行官（CEO），周猛同时被任命为五星电器母公司百思买的中国区总裁。他将负责五星电器的零售连锁，其在线及数字业务，还包括百思买移动正在试验中的中国业务。','2013-05-19 14:35:07'),
	(34,'http://weibo.com/2828908891/zxqC8bmDF',2147483647,32,'火星花朵潘小潘',1,1,0,4,0,NULL,NULL,'http://ww3.sinaimg.cn/thumbnail/a89db95bjw1e4tkn5tplfj20ns0hswha.jpg','苏州','江苏',0,'朝阳路五星电器旁的老楼前阶段终于拆除了，让人舒心和放心，经历了漫天尘土后，路边的摊贩和来往的行人也留下了太多的“礼物”……天气热了，苍蝇蚊子也来凑热闹，给周边的商铺和居民带来了困扰，多次投诉无人管，昆山是文明城市，请关注居民的难处！@昆山电视台--新闻夜报 @昆山发布 @昆山日报','2013-05-19 14:06:51'),
	(35,'http://weibo.com/2106383120/zxpWGAgic',2147483647,33,'MikaWang855',1,1,0,10,0,NULL,NULL,'http://ww1.sinaimg.cn/thumbnail/7d8cdb10jw1e4thpitel8j20xc18g419.jpg','无锡','江苏',0,'今天这擦头师傅太牛x了，保利到胜利门五星电器一共4个红绿灯，一边数钱一边飙，才飙了2分钟[黑线]，每次换挡都是赛车级水准的神换挡…不得不服老呀… 我在这里:http://t.cn/zj9xzaD','2013-05-19 12:24:45'),
	(36,'http://weibo.com/2668760014/zxp1lebWb',2147483647,21,'一见钟芹相守一生',1,1,0,0,0,NULL,NULL,NULL,'盐城','江苏',0,'冰箱，一用就是12年，时刻不停工作，累计为你20万元食物提供保鲜；冰箱，占地0.5平，按房价1万元／平算，它占的地方就值0.5万。所以买冰箱是个大事，换台称心如意配得上房价的节能冰箱更是大事！还好节能末班车被你赶上了，即日起抢购美菱节能冰箱三重补贴，有限名额，快到五星电器抓住最后的机会吧！','2013-05-19 10:03:30'),
	(37,'http://weibo.com/2668760014/zxp0C1qPd',2147483647,21,'一见钟芹相守一生',1,1,0,0,0,NULL,NULL,NULL,'盐城','江苏',0,'三洋帝度洗衣机、冰箱千万大钜惠，国家补贴+工厂“满千返百”直补:享受国家节能补贴后，再享受工厂满1000元降100元活动，以此类推，盛宴狂欢，节能补贴最后的疯狂，错过本次，永无机会！  有购买意向请到您身边的五星电器！','2013-05-19 10:01:40'),
	(38,'http://weibo.com/2779969675/zxoVLwEPk',2147483647,34,'朩昜愷',1,1,0,0,0,NULL,NULL,NULL,'盐城','江苏',0,'冰箱，一用12年，不停工作，累计为你20万元食物提供保鲜；占地0.5平米，按房价1万元/平算，它占的地方就值0.5万元。所以，买冰箱是个大事，换台称心如意配得上房价的节能冰箱更是大事！还好，节能末班车被你赶上了，即日起抢购节能冰箱三重补贴，名额有限，快到阜宁五星电器抓住最后的节能补贴机会吧！','2013-05-19 09:49:46'),
	(39,'http://weibo.com/3325679392/zxnain1Cd',2147483647,35,'一段情只为迩画地为_2011',1,1,0,0,0,NULL,NULL,'http://ww1.sinaimg.cn/thumbnail/c639d720jw1e4t5ggz1jpj20c70ejjsc.jpg','信阳','河南',0,'【百思买任命周猛为中国区总裁兼五星电器CEO】五星电器今天宣布，将由周猛担任公司的首席执行官（CEO），周猛同时被任命为五星电器母公司百思买的中国区总裁。他将负责五星电器的零售连锁，其在线及数字业务，还包括百思买移动正在试验中的中国业务。','2013-05-19 05:20:03'),
	(40,'http://weibo.com/2258726652/zxkeRAVpj',2147483647,4,'杭州五星电器',1,1,0,0,0,NULL,NULL,'http://ww2.sinaimg.cn/thumbnail/86a16efcjw1e4ssjdcr8rj20cq13qgsb.jpg','杭州','浙江',0,'#五星电器星推荐#潮人就是我——五星电器3C特卖季火热进行中，现小编给你推荐几款3C潮品，可至您身边的五星电器选购~~~','2013-05-18 21:53:02'),
	(41,'http://weibo.com/1968233965/zxk4G7JYs',2147483647,36,'狐宝宝__Bobby',1,1,3,0,0,NULL,NULL,'http://ww3.sinaimg.cn/thumbnail/7550ddedjw1e4srt8efbhj20hs0oddh8.jpg','南京','江苏',0,'推广:位于河西新城市广场对面，五星电器楼上，自家连锁，千余场地，百余包间，足穴 指压  棋牌  商务会客的首选之地！预约热线:13739199616.','2013-05-18 21:28:00'),
	(42,'http://weibo.com/2965050865/zxjWWvC6v',2147483647,37,'五星陈建栋',1,1,0,1,0,NULL,NULL,'http://ww4.sinaimg.cn/thumbnail/b0bb15f1jw1e4sr2hcd1nj20da0hs75z.jpg','郑州','河南',0,'梦中的小街、幽静、深邃、安祥，看了就觉得舒服，正如我归巢的心境。[鼓掌][打哈气][嘘][月亮]，对了别忘了明天给老婆买个新洗衣机，碧沙岗五星电器总店，样机5折啊，来店找小陈店长，还有更多优惠[握手]13017683065最后一天甩卖啊[咖啡]','2013-05-18 21:08:56'),
	(43,'http://weibo.com/1497163844/zxjSL6Cyd',2147483647,38,'讨厌爱哭的我',1,1,0,0,1,NULL,NULL,NULL,'芜湖','安徽',0,'五星二楼韩姐，是不便宜但是手艺好，看你怎么选择了，一分钱一分货永远都是硬道理 //@大话芜湖:听讲五星电器二楼','2013-05-18 20:58:37'),
	(44,'http://weibo.com/2258726652/zxjQvjZIq',2147483647,4,'杭州五星电器',1,1,0,0,0,NULL,NULL,'http://ww4.sinaimg.cn/thumbnail/86a16efcjw1e4sqsxt1t9j20bo10dwke.jpg','杭州','浙江',0,'#五星电器星推荐#5月31日国家家电节能补贴全面截止！抢节能补贴末班车必来五星电器！错过这班省钱车，机会不再有！五星电器温馨提醒：国家家电节能补贴最高每台400元政策于5月31日结束，早买多省钱！未办理补贴的顾客，请您尽快带相关凭证至门店领取！现小编给你推荐几款节能产品~~~~','2013-05-18 20:53:01'),
	(45,'http://weibo.com/2038210611/zxivyyBXN',2147483647,39,'马鞍山翼部落',1,1,0,0,0,NULL,NULL,'http://ww2.sinaimg.cn/thumbnail/797ca033jw1e4skwbhwamj218g0xckfe.jpg','马鞍山','安徽',0,'五星电器的一个移动全球通用户在大家的共同努力下办理了合约计划！网络，资费，流量都是我们的优势！大家多一份执着，多一份自信，多一份诚意，就会有收获！@天翼-虎子 @MAS渠道中心 @卟想長大的成年人 @培宝妈','2013-05-18 17:28:42'),
	(46,'http://weibo.com/1737886187/zxgoHessB',2147483647,40,'童啾啾',1,1,0,2,0,NULL,NULL,'http://ww1.sinaimg.cn/thumbnail/679609ebjw1e4sbkut4m9j20lc0sgtdu.jpg','宁波','浙江',0,'五星电器的人渣明明乱停车还死活不肯来挪开，[怒][怒][怒][怒][怒]〜祝这个人渣全家不幸〜','2013-05-18 12:06:19'),
	(47,'http://weibo.com/1807594864/zxfPXa2ER',2147483647,41,'叶子龙free',1,1,0,0,1,NULL,NULL,NULL,'安庆','安徽',0,'生意好了，固然服务态度就差！//@安庆那些事: 怎么这么多人有意见？ //@西红柿炒番茄_Molly:对的！服务态度气死人！ //@文明人弹烟头Jack:尤其是五星电器边上那家ABC。//@安庆宠物帮:点个饭，等了N久，告诉我们厨房只有一个厨师，12点10分才给我们上~然后告诉我们12点30打烊，一碗煲仔饭吖，想烫死我吖','2013-05-18 10:40:42'),
	(48,'http://weibo.com/2302797265/zxf9WjxVC',2147483647,42,'李诚没有嘉',1,1,0,0,1,NULL,NULL,NULL,'安庆','安徽',0,'最大的意见就是没有美女服务员。 //@安庆那些事:怎么这么多人有意见？ //@西红柿炒番茄_Molly:对的！服务态度气死人！ //@文明人弹烟头Jack:尤其是五星电器边上那家ABC。。。 //@安庆那些事:回复@安庆宠物帮:','2013-05-18 08:57:13'),
	(49,'http://weibo.com/2965050865/zxexmB4w5',2147483647,37,'五星陈建栋',1,1,1,0,0,NULL,NULL,'http://ww3.sinaimg.cn/thumbnail/b0bb15f1jw1e4s3cdh831j20hs0dfq4e.jpg','郑州','河南',0,'【节能补贴倒计时】国家补贴政策将于5月底正式结束，今年有家电购买计划的亲们需抓住补贴末班车的最后机会，享受国家150—400元/台节能彩电的现金补贴。5月18-19日碧沙岗五星电器总店“节能补贴末班车+千款样机5折售＂活动中，快来抢购啦！我在碧沙岗公园西门对面67805026','2013-05-18 07:22:11'),
	(50,'http://weibo.com/1651511767/zxdblocGW',2147483647,43,'文明人弹烟头Jack',1,1,1,1,1,NULL,NULL,NULL,'安庆','安徽',0,'尤其是五星电器边上那家ABC。。。 //@安庆那些事:回复@安庆宠物帮:！！！ //@安庆宠物帮:点个饭，等了N久，告诉我们厨房只有一个厨师，12点10分才给我们上~然后告诉我们12点30打烊，一碗煲仔饭吖，想烫死我吖！！！ //@安庆那些事:有类似经历和感受的筒子没？','2013-05-18 03:55:11');

/*!40000 ALTER TABLE `weibo_statuses` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table weibo_users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `weibo_users`;

CREATE TABLE `weibo_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_origin_id` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `info_source_id` int(11) DEFAULT NULL,
  `screen_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `profile_image_url` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `status_count` int(11) NOT NULL,
  `follower_count` int(11) NOT NULL,
  `following_count` int(11) NOT NULL,
  `verified` tinyint(1) DEFAULT '0',
  `geo_info_city` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `geo_info_province` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `gender` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `index_weibo_users_on_info_source_id` (`info_source_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

LOCK TABLES `weibo_users` WRITE;
/*!40000 ALTER TABLE `weibo_users` DISABLE KEYS */;

INSERT INTO `weibo_users` (`id`, `user_origin_id`, `info_source_id`, `screen_name`, `profile_image_url`, `status_count`, `follower_count`, `following_count`, `verified`, `geo_info_city`, `geo_info_province`, `gender`)
VALUES
	(1,'1696300250',1,'辉爷是总攻','http://tp3.sinaimg.cn/1696300250/50/40014525362/0',370,223,111,0,'南京','江苏','f'),
	(2,'2636968650',1,'OMG你是Q','http://tp3.sinaimg.cn/2636968650/50/5619940149/0',42,87,62,0,'福州','福建','f'),
	(3,'1725401854',1,'flysky66','http://tp3.sinaimg.cn/1725401854/50/40003636128/0',153,43,79,0,'南京','江苏','f'),
	(4,'2258726652',1,'杭州五星电器','http://tp1.sinaimg.cn/2258726652/50/40022532799/1',1490,19216,83,1,'杭州','浙江','m'),
	(5,'1883869391',1,'南京五星电器','http://tp4.sinaimg.cn/1883869391/50/40022519038/1',3346,16175,1016,1,'南京','江苏','m'),
	(6,'1761874477',1,'五星刘娣Eliane','http://tp2.sinaimg.cn/1761874477/50/5662786870/0',2806,915,613,0,'南京','江苏','f'),
	(7,'1879439790',1,'汪志晓','http://tp3.sinaimg.cn/1879439790/50/40005189297/1',5599,477,334,0,'无锡','江苏','m'),
	(8,'1750024131',1,'奈何花落殇红颜','http://tp4.sinaimg.cn/1750024131/50/5663587417/0',2356,339,272,0,'南通','江苏','f'),
	(9,'3179664973',1,'环保华骄地板','http://tp2.sinaimg.cn/3179664973/50/40009686095/1',2795,909,2000,1,'成都','四川','m'),
	(10,'3302477951',1,'余洪飞3302477951','http://tp4.sinaimg.cn/3302477951/50/5657946296/0',251,91,255,0,'','其它','f'),
	(11,'2367108870',1,'辛辛辛辛_小辛','http://tp3.sinaimg.cn/2367108870/50/5660547951/0',4389,686,553,0,'郑州','河南','f'),
	(12,'2896573320',1,'南京花婆婆绘本馆','http://tp1.sinaimg.cn/2896573320/50/39999645940/0',1090,924,502,0,'南京','江苏','f'),
	(13,'1435830410',1,'南京小蜗牛','http://tp3.sinaimg.cn/1435830410/50/5611844064/0',5899,1296,525,0,'南京','江苏','f'),
	(14,'1870578244',1,'熊亚茹','http://tp1.sinaimg.cn/1870578244/50/1289066272/0',534,103,171,0,'济宁','山东','f'),
	(15,'3025322725',1,'MyLoft寡人','http://tp2.sinaimg.cn/3025322725/50/40010885380/1',150,206,225,0,'黑河','黑龙江','m'),
	(16,'2671717811',1,'丰一源陈志清','http://tp4.sinaimg.cn/2671717811/50/5627181972/1',474,531,1345,0,'深圳','广东','m'),
	(17,'2017927407',1,'晗涵viola','http://tp4.sinaimg.cn/2017927407/50/1299768370/0',314,95,77,0,'南京','江苏','f'),
	(18,'2022372735',1,'Belong_孙楠','http://tp4.sinaimg.cn/2022372735/50/40013187820/1',566,867,469,1,'南京','江苏','m'),
	(19,'1683205152',1,'张旭东南京','http://tp1.sinaimg.cn/1683205152/50/5645327027/1',21899,8386,1727,1,'南京','江苏','m'),
	(20,'2268832064',1,'常州五星电器','http://tp1.sinaimg.cn/2268832064/50/5662792123/1',518,49546,65,1,'常州','江苏','m'),
	(21,'2668760014',1,'一见钟芹相守一生','http://tp3.sinaimg.cn/2668760014/50/5639638568/1',780,238,267,0,'盐城','江苏','m'),
	(22,'1785493814',1,'Cecilia晓小','http://tp3.sinaimg.cn/1785493814/50/5653566324/0',598,548,166,0,'南京','江苏','f'),
	(23,'2911208041',1,'瑞祥商联卡-楽','http://tp2.sinaimg.cn/2911208041/50/5644993534/1',17,43,183,0,'南京','江苏','m'),
	(24,'1939076760',1,'四川五星电器','http://tp1.sinaimg.cn/1939076760/50/5662855867/0',963,5241,98,1,'成都','四川','f'),
	(25,'1750441861',1,'银联商务江苏分公司','http://tp2.sinaimg.cn/1750441861/50/5604996711/1',869,1300,485,1,'南京','江苏','m'),
	(26,'3447776930',1,'青岛LaterOnClub','http://tp3.sinaimg.cn/3447776930/50/22843046296/1',123,46,139,0,'青岛','山东','m'),
	(27,'2275124761',1,'千金688','http://tp2.sinaimg.cn/2275124761/50/5656408404/0',535,128,110,0,'盐城','江苏','f'),
	(28,'1851283422',1,'广州智造','http://tp3.sinaimg.cn/1851283422/50/5659421302/1',3177,473,763,1,'广州','广东','m'),
	(29,'1667260624',1,'我是泰山','http://tp1.sinaimg.cn/1667260624/50/40005607605/1',1319,302,206,0,'合肥','安徽','m'),
	(30,'3322750910',1,'jl4ever1968','http://tp3.sinaimg.cn/3322750910/50/40022996624/1',87,68,48,0,'巴南区','重庆','m'),
	(31,'3365513632',1,'amber黄小瑞_2006','http://tp1.sinaimg.cn/3365513632/50/40023524844/1',32,59,80,0,'成都','四川','m'),
	(32,'2828908891',1,'火星花朵潘小潘','http://tp4.sinaimg.cn/2828908891/50/5662003812/0',188,215,225,0,'苏州','江苏','f'),
	(33,'2106383120',1,'MikaWang855','http://tp1.sinaimg.cn/2106383120/50/40011502519/1',5956,1782,603,0,'无锡','江苏','m'),
	(34,'2779969675',1,'朩昜愷','http://tp4.sinaimg.cn/2779969675/50/5662937650/1',113,53,154,0,'盐城','江苏','m'),
	(35,'3325679392',1,'一段情只为迩画地为_2011','http://tp1.sinaimg.cn/3325679392/50/40023189255/1',183,108,213,0,'信阳','河南','m'),
	(36,'1968233965',1,'狐宝宝__Bobby','http://tp2.sinaimg.cn/1968233965/50/5664087042/0',2548,10062,270,0,'南京','江苏','f'),
	(37,'2965050865',1,'五星陈建栋','http://tp2.sinaimg.cn/2965050865/50/5658553413/1',74,97,354,0,'郑州','河南','m'),
	(38,'1497163844',1,'讨厌爱哭的我','http://tp1.sinaimg.cn/1497163844/50/5663861781/0',374,52,52,0,'芜湖','安徽','f'),
	(39,'2038210611',1,'马鞍山翼部落','http://tp4.sinaimg.cn/2038210611/50/5661239786/1',60,267,92,1,'马鞍山','安徽','m'),
	(40,'1737886187',1,'童啾啾','http://tp4.sinaimg.cn/1737886187/50/5653368056/0',1022,357,219,0,'宁波','浙江','f'),
	(41,'1807594864',1,'叶子龙free','http://tp1.sinaimg.cn/1807594864/50/40019666000/1',524,349,115,1,'安庆','安徽','m'),
	(42,'2302797265',1,'李诚没有嘉','http://tp2.sinaimg.cn/2302797265/50/5642668183/1',500,102,145,0,'安庆','安徽','m'),
	(43,'1651511767',1,'文明人弹烟头Jack','http://tp4.sinaimg.cn/1651511767/50/5660438473/1',3029,415,229,0,'安庆','安徽','m');

/*!40000 ALTER TABLE `weibo_users` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table wiki_post_analysis_categorizeds
# ------------------------------------------------------------

DROP TABLE IF EXISTS `wiki_post_analysis_categorizeds`;

CREATE TABLE `wiki_post_analysis_categorizeds` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `wiki_post_id` int(11) DEFAULT NULL,
  `label_id` int(11) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_wiki_post_analysis_categorizeds_on_wiki_post_id` (`wiki_post_id`),
  KEY `index_wiki_post_analysis_categorizeds_on_label_id` (`label_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



# Dump of table wiki_posts
# ------------------------------------------------------------

DROP TABLE IF EXISTS `wiki_posts`;

CREATE TABLE `wiki_posts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `wiki_user_screen_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `info_source_id` int(11) DEFAULT NULL,
  `keyword_id` int(11) DEFAULT NULL,
  `title` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `content` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `read_count` int(11) NOT NULL,
  `comment_count` int(11) NOT NULL,
  `answered` tinyint(1) DEFAULT '0',
  `urgency` int(11) DEFAULT '0',
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `index_wiki_posts_on_info_source_id` (`info_source_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

LOCK TABLES `wiki_posts` WRITE;
/*!40000 ALTER TABLE `wiki_posts` DISABLE KEYS */;

INSERT INTO `wiki_posts` (`id`, `url`, `wiki_user_screen_name`, `info_source_id`, `keyword_id`, `title`, `content`, `read_count`, `comment_count`, `answered`, `urgency`, `created_at`)
VALUES
	(1,'http://zhidao.baidu.com/question/553689403.html','rancan24',2,1,'从华联商厦到五星电器怎么走','',14,1,0,0,'2013-05-26 11:39:00'),
	(2,'http://zhidao.baidu.com/question/553407540.html','rancan24',2,1,'电脑问题，五星电器买的，怎么回事？','刚在五星电器买的戴尔比记本，打开后，右上方光驱部位有吱吱的声音，就像广播遇到信号干扰的声音，但不是很大，一打开某个软件声音就更大，我以为是光驱的，打开光驱还是有，请问是什么原因，今天才买的？',9,2,0,0,'2013-05-25 11:43:00'),
	(3,'http://zhidao.baidu.com/question/553024502.html','处刑者18号',2,1,'在五星电器买了电视机发票丢了还能领节能补贴么?以后维修怎么办啊?','',34,2,0,0,'2013-05-23 21:11:00'),
	(4,'http://zhidao.baidu.com/question/552060656.html','匿名',2,1,'410五一在五星电器买的windows 8的,i5_3337，一个上午就自动关机三次','开始是充着电在线听歌，关机了以为是睡眠，但怎么按都不亮，只好重启电源页面竟然又回到桌面了？没在意。后来看电影，又关机了，打电话给售后，让设置电源选项，设置过了看电影还是关机，郁闷。。。不敢看电影，浏览网页，不到一个小时又关机了！从早上开机到中午，三次了。下午去售后，售后让看电影检测看能够再显关机后维修。我都觉得搞笑，下午电脑什么情况都没发生。直接让我回家了，说看到关机再维修。有这样的售后麽？我电脑就是关机了才找维修呢，现在还必需得看到自己关机才给维修检测，那我还找售后做什么？自动关机自己扫描去？昨天还是关',12,1,0,0,'2013-05-20 14:57:00'),
	(5,'http://zhidao.baidu.com/question/552053349.html','jaurjer',2,1,'u410五一在五星电器买的，windows 8的,i5_3337，一个上午就自动关机三次','开始是充着电在线听歌，关机了以为是睡眠，但怎么按都不亮，只好重启电源页面竟然又回到桌面了？没在意。后来看电影，又关机了，打电话给售后，让设置电源选项，设置过了看电影还是关机，郁闷。。。不敢看电影，浏览网页，不到一个小时又关机了！从早上开机到中午，三次了。下午去售后，售后说让看电影检测看能够再显关机后维修。我都觉得搞笑，下午电脑什么情况都没发生。直接让我回家了，说看到关机再维修。有这样的售后麽？我电脑就是关机了才找维修呢，现在还必需得看到自己关机才给维修检测，那我还找售后做什么？自动关机自己扫描？昨天还是关',19,1,0,0,'2013-05-20 14:56:00'),
	(6,'http://zhidao.baidu.com/question/551338330.html','冷眼看你装AN',2,2,'百思买收购五星电器的资金贷款是谁提供的，其融资渠道是什么','',40,1,0,0,'2013-05-17 22:33:00'),
	(7,'http://zhidao.baidu.com/question/550670027.html','XUPEI19891114',2,1,'想知道: 南京市 从五星电器(尧化门卖场)到南京方基光电科技有限公司怎么坐公交','',33,1,0,0,'2013-05-15 17:03:00'),
	(8,'http://zhidao.baidu.com/question/550235342.html','listen314159',2,1,'你好，请问五星电器官网为什么一直打不开？','',20,2,0,0,'2013-05-14 10:06:00'),
	(9,'http://zhidao.baidu.com/question/548571686.html','段晓冉love',2,1,'苹果4s和4目前在舟山五星电器和新茂数码城的价格？最好是准确一点的','',43,2,1,0,'2013-05-08 22:32:00'),
	(10,'http://zhidao.baidu.com/question/546836000.html','远程助手',2,1,'关于五星电器的小伍在线','今年4月14日在五星电器买的手机，送的一年的小伍在线服务，服务各方面都很不错，但是我想问一下，在应用下载方面，有没有让用户自行下载应用的平台。',44,2,1,0,'2013-05-03 15:28:00'),
	(11,'http://zhidao.baidu.com/question/550235650.html','listen314159',2,2,'请问百思买是否有一项服务叫做WOW，和WOW+，具体是什么意思呢？','',43,1,0,0,'2013-05-14 10:06:00'),
	(12,'http://zhidao.baidu.com/question/550237647.html','listen314159',2,2,'百思买是否有一项服务叫WOW，（不是魔兽世界的WOW），只想知道这是干嘛的，为啥叫WOW呢.......','',50,1,1,0,'2013-05-14 09:56:00'),
	(13,'http://zhidao.baidu.com/question/549302584.html','匿名',2,2,'百思买存在的优势','',45,1,0,0,'2013-05-11 10:29:00'),
	(14,'http://zhidao.baidu.com/question/542761309.html','匿名',2,2,'百思买入股麦考林是真的吗','',97,3,0,0,'2013-04-19 21:06:00'),
	(15,'http://zhidao.baidu.com/question/541114988.html','wagagao',2,2,'百思买验厂怎样才能一次性通过','',89,1,1,0,'2013-04-14 17:14:00'),
	(16,'http://zhidao.baidu.com/question/539608357.html','匿名',2,2,'百思买瓷砖，这个瓷砖怎么样，我去看了下，效果挺好的，打听下，知道的告诉我。 我想买。','',158,1,1,0,'2013-04-09 17:02:00'),
	(17,'http://zhidao.baidu.com/question/539524291.html','panli2335',2,2,'百思买验厂如何申诉？','',87,1,1,0,'2013-04-09 12:36:00'),
	(18,'http://zhidao.baidu.com/question/538438227.html','匿名',2,2,'你好，我在百思买官网买IPHON5，请问可以寄到你们百思移动买门店吗','',127,1,0,0,'2013-04-07 13:23:00'),
	(19,'http://zhidao.baidu.com/question/536570662.html','喝不起通川大曲',2,2,'百思买网站里面的那个marketplace是什么意思？','',113,2,1,0,'2013-03-30 17:40:00'),
	(20,'http://zhidao.baidu.com/question/553687120.html','dmeil1327',2,3,'I want to buy some of PVC extrusion machine,which manufacturer is the best you know.','',28,3,0,0,'2013-05-26 11:32:00'),
	(21,'http://zhidao.baidu.com/question/551989590.html','lazygoat2',2,3,'美国bestbuy网络价格与实体店价格','偶然看到mac pro在on sale，最近有人去美国想托人带一个回来，但是不知道实体店价格是不是便宜？网上显示shipping 和 store pickup都是打勾的，所以这样的话实体店价格是和网络显示价格一样么？',35,1,0,0,'2013-05-20 09:10:00'),
	(22,'http://zhidao.baidu.com/question/542731851.html','403549390',2,3,'关于iphone5的退机纠纷，4月7号在南京溧水的best buy（前五星电器）花费5288购买一台白色联通裸机','当时开包后发现后置摄像头有灰，店员确定说是光圈不是灰，我就想先用着吧。5天后发现灰更明显了拿去调换，店里说他们现在不能换必须等他们下周1去南京的苹果售后鉴定换机，大概时间7到21天才能换。我提出退掉在换一台，店里要我自己跑南京售后，而且这个必须在7天之内，因为苹果是看激活时间的。<br />第二天我到南京去做了鉴定，工程师认定确实有灰，把机器收去了。等了4天后又跑南京取回来退机报告<br />因为这家店服务不好，我决定退机不想换了。然而店里负责的说不可以退，要我换一台。我非常坚持退，双方沟通了很久，最后店',161,7,1,0,'2013-04-19 19:36:00'),
	(23,'http://zhidao.baidu.com/question/539524075.html','jiaminglove21',2,3,'BestBuy验厂哪家顾问公司比较专业？','',85,1,1,0,'2013-04-09 12:35:00'),
	(24,'http://zhidao.baidu.com/question/536149343.html','匿名',2,3,'paypal如何支付bestbuy？','如题，我的paypal在支付<a href=\"http://www.bestbuy.com\" target=\"_blank\">www.bestbuy.com</a>时出现:此帐号不支持该国的交易要怎么样才能从bestbuy买东西？',117,2,1,0,'2013-03-29 12:48:00'),
	(25,'http://zhidao.baidu.com/question/533346188.html','momo88418',2,3,'BestBuy验厂如何申诉？？','',87,1,1,0,'2013-03-18 23:33:00'),
	(26,'http://zhidao.baidu.com/question/527707305.html','难得几回醉1',2,3,'我今后要去美国留学,请问我在国内买助听器便宜,还是在国外买便宜。我听说我best buy卖场 要便宜。','',176,8,1,0,'2013-02-25 22:43:00'),
	(27,'http://zhidao.baidu.com/question/527295739.html','13826437424',2,3,'问下在美国的bestbuy裏面有没有用於手提电脑散热用的风扇啊？有链接最好','',104,1,1,0,'2013-02-24 12:26:00'),
	(28,'http://zhidao.baidu.com/question/525484974.html','江村小屁孩',2,3,'本人在多伦多，今天去best buy 买了几张美服lol的点卡，都是五块的。','结果一冲进游戏里貌似是什么双倍的东西坑爹啊。。。楼主又不会英文也不想去退了！现在求解到底在太古附近那个mall能买到美服lol的点卡？顺便求加我QQ1767684639 帮忙看看我买的到底是什么！！',222,1,1,0,'2013-02-18 07:18:00'),
	(29,'http://zhidao.baidu.com/question/519560807.html','Mr·豆芽',2,3,'为什么开机这么慢，我在best buy买的新的什么都没装','',105,2,1,0,'2013-01-24 15:13:00'),
	(30,'http://zhidao.baidu.com/question/532688702.html','匿名',2,6,'百思买全球副总裁，五星电器CEO王健在今年3月份辞职了，职务由原来的副总裁宋镁担任，这事是真的吗？','',162,1,0,0,'2013-03-16 17:04:00'),
	(31,'http://zhidao.baidu.com/question/515548907.html','1453712342',2,4,'五星电器王建是什么学校毕业的','',105,1,0,0,'2013-01-11 15:42:00'),
	(32,'http://zhidao.baidu.com/question/515548719.html','1453712342',2,4,'五星电器王建什么地方人','',123,1,0,0,'2013-01-11 15:41:00'),
	(33,'http://zhidao.baidu.com/question/515548812.html','1453712342',2,4,'五星电器王建是做什么的','',106,1,0,0,'2013-01-11 15:41:00'),
	(34,'http://zhidao.baidu.com/question/515548608.html','1453712342',2,4,'五星电器王建什么职务','',92,1,0,0,'2013-01-11 15:41:00'),
	(35,'http://zhidao.baidu.com/question/515548512.html','1453712342',2,4,'五星电器王建什么学历','',105,1,0,0,'2013-01-11 15:40:00'),
	(36,'http://zhidao.baidu.com/question/485331831.html','davidkoree',2,4,'五星电器总裁王健参加伦敦奥运会火炬手传递了吗','',108,2,1,0,'2012-10-10 10:15:00');

/*!40000 ALTER TABLE `wiki_posts` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
