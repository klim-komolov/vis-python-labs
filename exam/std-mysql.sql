-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: std-mysql
-- Время создания: Июн 14 2024 г., 19:37
-- Версия сервера: 5.7.26-0ubuntu0.16.04.1
-- Версия PHP: 8.1.15

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `std_2572_exam`
--
CREATE DATABASE IF NOT EXISTS `std_2572_exam` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `std_2572_exam`;

-- --------------------------------------------------------

--
-- Структура таблицы `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('5ceb0f3d0030');

-- --------------------------------------------------------

--
-- Структура таблицы `book`
--

CREATE TABLE `book` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `year` int(11) NOT NULL,
  `publisher` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `pages` int(11) NOT NULL,
  `cover_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `book`
--

INSERT INTO `book` (`id`, `title`, `description`, `year`, `publisher`, `author`, `pages`, `cover_id`) VALUES
(9, 'Великий Гэтсби', 'Роман, написанный американским писателем Ф. Скоттом Фицджеральдом.', 1925, 'Скрибнер', 'Ф. Скотт Фицджеральд', 215, 1),
(17, 'Мастер и Маргарита', 'Книга пропитана мистикой, верой, любовью. ', 1967, 'Политех', 'Михаил Булгаков', 500, 13),
(18, 'Чемодан (сборник) ', 'Сергей Довлатов - один из наиболее популярных и читаемых русских писателей конца XX - начала XXI века. Его повести, рассказы и записные книжки переведены на множество языков, экранизированы, изучаются в школе и вузах. \"Заповедник\", \"Зона\", \"Иностранка\", \"Наши\", \"Чемодан\" - эти и другие удивительно смешные и пронзительно печальные довлатовские вещи давно стали классикой. \"Отморозил пальцы ног и уши головы\", \"выпил накануне - ощущение, как будто проглотил заячью шапку с ушами\", \"алкоголизм излечим - пьянство - нет\" - шутки Довлатова запоминаешь сразу и на всю жизнь, а книги перечитываешь десятки раз. Они никогда не надоедают.', 2007, 'Азбука-классика', 'Сергей Довлатов', 800, 14),
(19, 'Преступление и наказание ', 'Одно из «краеугольных» произведений русской и мировой литературы, включенный во все школьные и университетские программы, неоднократно экранизированный роман Достоевского «Преступление и наказание» ставит перед читателем важнейшие нравственно-мировоззренческие вопросы — о вере, совести, грехе и об искуплении через страдание. Опровержение преступной «идеи-страсти», «безобразной мечты», завладевшей умом Родиона Раскольникова в самом «умышленном» и «фантастическом» городе на свете, составляет основное содержание этой сложнейшей, соединившей в себе несколько различных жанров книги. Задуманный как «психологический отчет одного преступления», роман Достоевского предстал перед читателем грандиозным художественно-философским исследованием человеческой природы, христианской трагедией о смерти и воскресении души.', 2013, 'Азбука-Аттикус', 'Фёдор Достоевский ', 350, 15),
(20, 'Война и мир', 'ВОЙНА И МИР Л.Н.Толстого — книга на все времена. Кажется, что она существовала всегда, настолько знакомым кажется текст, едва мы открываем первые страницы романа, настолько памятны многие его эпизоды: охота и святки, первый бал Наташи Ростовой, лунная ночь в Отрадном, князь Андрей в сражении при Аустерлице... Сцены \"мирной\", семейной жизни сменяются картинами, имеющими значение для хода всей мировой истории, но для Толстого они равноценны, связаны в едином потоке времени. Каждый эпизод важен не только для развития сюжета, но и как одно из бесчисленных проявлений жизни, которая насыщена в каждом своем моменте и которую учит любить Толстой.', 2014, 'Азбука ', 'Лев Толстой', 5000, 16),
(21, 'Евгений Онегин ', '\"Читали ли вы \"Онегина\"? Каков вам кажется \"Оне­гин\"? Что вы скажете об \"Онегине\"? Вот вопросы, по­вторяемые беспрестанно в кругу литераторов и русских читателей\", - отмечал после выхода в свет второй главы романа писатель, предприимчивый издатель и, кстати, герой многочисленных эпиграмм Пушкина Фаддей Бул-гарин. Уже давно ЕВГЕНИЯ ОНЕГИНА не принято оцени­вать. Говоря словами того же Булгарина, он \"написан сти­хами Пушкина. Этого довольно\". Зато иллюстраторы до сих пор радуют читателей разными художественными ин­терпретациями романа в стихах. Один из первых циклов рисунков к ЕВГЕНИЮ ОНЕГИНУ создал Павел Соколов, которого современники называли \"творцом Татьяны\". А через полвека огромной популярностью пользовалось великолепное издание одной из лучших российских ти­пографий - \"Товарищества Р.Голике и А.Вильборг\", поставщика Императорского двора, с акварелями Елены Самокиш-Судковской.', 2014, 'Издательский Дом Мещерякова', 'Александр Пушкин ', 250, 17),
(22, 'Собачье сердце ', 'В повести \"Собачье сердце\", написанной в первые послереволюционные годы, автор, используя элементы фантастики, рисует тщетную попытку создать \"нового\" человека вопреки его природным инстинктам и устремлениям.\n', 2001, 'Дрофа', 'Михаил Булгаков', 123, 18),
(23, 'Приключения Шерлока Холмса (сборник)', 'Перу английского писателя, публициста и журналиста Артура Конан Дойла принадлежат исторические, приключенческие, фантастические романы и труды по спиритизму, но в мировую литературу он вошел как создатель самого Великого Сыщика всех времен и народов - Шерлока Холмса. Благородный и бесстрашный борец со Злом, обладатель острого ума и необыкновенной наблюдательности, с помощью своего дедуктивного метода сыщик решает самые запутанные головоломки, зачастую спасая этим человеческие жизни. Он гениально перевоплощается, обладает актерским даром и умеет поставить эффектную точку в конце каждого блестяще проведенного им расследования.', 2013, 'Эксмо', 'Артур Конан Дойл ', 973, 19),
(24, 'Идиот ', '\"Идиот\". Роман, в котором творческие принципы Достоевского воплощаются в полной мере, а удивительное владение сюжетом достигает подлинного расцвета. Яркая и почти болезненно талантливая история несчастного князя Мышкина, неистового Парфена Рогожина и отчаявшейся Настасьи Филипповны, много раз экранизированная и поставленная на сцене, и сейчас завораживает читателя...', 2010, 'АСТ, Харвест, АСТ Москва', 'Фёдор Достоевский', 500, 20),
(25, 'Двенадцать стульев', 'Авторская редакция знаменитого романа Ильи Ильфа и Евгения Петрова, восстановленная Александрой Ильиничной Ильф. В текст романа возвращены фрагменты, опубликованные в журнале \"30 дней\" и в первом издании, в том числе две главы и несколько значительных эпизодов, которые по вкусовым или цензурным соображениям были опущены при последующих переизданиях, а также включен ряд фрагментов из рукописного и машинописного вариантов романа.', 2004, 'Ильфиада ', 'Илья Ильф, Евгений Петров', 1000, 21),
(26, 'Герой нашего времени', '`Герой нашего времени` - роман гениального поэта и писателя-классика XIX века М.Ю.Лермонтова.', 2000, 'Детская литература', 'Михаил Лермонтов', 700, 22),
(27, 'Рассказы', 'Антон Павлович Чехов - один из величайших писателей и драматургов не только отечественной, но и мировой литературы, тончайший психолог, ироничный юморист, непревзойденный певец загадочной русской души во всем се эмоциональном диапазоне, в котором от смешного до драматического - всего один шаг. В сборник вошли наиболее известные повести и рассказы Чехова - произведения забавные и трагические, порой прозрачно-поэтические, порой саркастично-едкие.\n', 2009, 'АСТ', 'Антон Чехов', 2000, 23),
(28, 'Братья Карамазовы ', 'Последний, самый объемный и один из наиболее известных романов Ф.М.Достоевского обращает читателя к вневременным нравственно-философским вопросам о грехе, воздаянии, сострадании и милосердии. Книга, которую сам писатель определил как \"роман о богохульстве и опровержении его\", явилась попыткой \"решить вопрос о человеке\", \"разгадать тайну\" человека, что, по Достоевскому, означало \"решить вопрос о Боге\". Сквозь призму истории провинциальной семьи Карамазовых автор повествует об извечной борьбе Божественного и дьявольского в человеческой душе. Один из самых глубоких в мировой литературе опытов отражения христианского сознания, БРАТЬЯ КАРАМАЗОВЫ стали в XX веке объектом парадоксальных философских и психоаналитических интерпретаций.', 2014, 'Азбука, Азбука-Аттикус', 'Фёдор Достоевский ', 390, 24),
(29, 'Маленький принц', 'Философская сказка о любви и дружбе, о долге и верности, о нетерпимости к злу.', 2000, 'Детская литература. Москва', 'Антуан де Сент-Экзюпери', 600, 25);

-- --------------------------------------------------------

--
-- Структура таблицы `books_genres`
--

CREATE TABLE `books_genres` (
  `book_id` int(11) NOT NULL,
  `genre_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `books_genres`
--

INSERT INTO `books_genres` (`book_id`, `genre_id`) VALUES
(17, 1),
(20, 1),
(23, 1),
(25, 1),
(26, 1),
(27, 1),
(28, 1),
(29, 1),
(9, 2),
(22, 2),
(24, 2),
(25, 2),
(27, 2),
(18, 3),
(21, 3),
(22, 3),
(25, 3),
(26, 3),
(27, 3),
(29, 3),
(19, 4),
(23, 4),
(25, 4),
(26, 4),
(27, 4);

-- --------------------------------------------------------

--
-- Структура таблицы `collection`
--

CREATE TABLE `collection` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `collection`
--

INSERT INTO `collection` (`id`, `name`, `user_id`) VALUES
(3, 'test1', 3);

-- --------------------------------------------------------

--
-- Структура таблицы `collection_books`
--

CREATE TABLE `collection_books` (
  `collection_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `collection_books`
--

INSERT INTO `collection_books` (`collection_id`, `book_id`) VALUES
(3, 9),
(3, 20);

-- --------------------------------------------------------

--
-- Структура таблицы `cover`
--

CREATE TABLE `cover` (
  `id` int(11) NOT NULL,
  `file_name` varchar(255) NOT NULL,
  `mime_type` varchar(255) NOT NULL,
  `md5_hash` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `cover`
--

INSERT INTO `cover` (`id`, `file_name`, `mime_type`, `md5_hash`) VALUES
(1, 'book.jpg', 'image/jpeg', 'd41d8cd98f00b204e9800998ecf8427e'),
(12, '2.jpeg', 'image/jpeg', '0f0a4fe6dde7db025f54143262fa629d'),
(13, '14.jpg', 'image/jpeg', '2bc0b13219a5ec6d01cffc876c6a8d45'),
(14, '9.jpg', 'image/jpeg', '0d0d2d125b9c8105a2229dc61dba89e3'),
(15, '3.jpg', 'image/jpeg', 'a43eb6fdb30b9bf1b70dad61d5360a48'),
(16, '13.jpg', 'image/jpeg', 'c16651d50a9097e7ebbff186342d4d66'),
(17, '2.jpg', 'image/jpeg', '4ec2406e82bbc5bd35addcd05f1209e2'),
(18, '4.jpg', 'image/jpeg', 'a876792b678f8d0b963b85ca62cb18cf'),
(19, '5.jpg', 'image/jpeg', '8cfef6edb977ff2e272ba2bf0a22e8da'),
(20, '6.jpg', 'image/jpeg', '5095c4f65e73c19764de26dcb4d1e1ec'),
(21, '7.jpg', 'image/jpeg', 'dc1bed5c0b57ef7433e6a802d837dab9'),
(22, '8.jpg', 'image/jpeg', 'a89506b2d3661b83abbdab96699e87ca'),
(23, '10.jpg', 'image/jpeg', 'fa2973afddaf396d3d31f5b38fb1cc6f'),
(24, '11.jpg', 'image/jpeg', 'd8102830160ceeb34f36dad823992d06'),
(25, '12.jpg', 'image/jpeg', '34eb2d4152879112797807ecfeb08827');

-- --------------------------------------------------------

--
-- Структура таблицы `genre`
--

CREATE TABLE `genre` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `genre`
--

INSERT INTO `genre` (`id`, `name`) VALUES
(3, 'Биография'),
(2, 'Наука'),
(1, 'Фантастика'),
(4, 'Фэнтези');

-- --------------------------------------------------------

--
-- Структура таблицы `review`
--

CREATE TABLE `review` (
  `id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `rating` int(11) NOT NULL,
  `text` text NOT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `review`
--

INSERT INTO `review` (`id`, `book_id`, `user_id`, `rating`, `text`, `created_at`) VALUES
(2, 9, 1, 5, '5/5', '2024-06-13 20:20:52'),
(3, 20, 1, 5, 'Роман, не побоюсь этого слова, легендарный, но долгое время не мог к нему подступиться. В школе интереса не было, так, урывками, а потом объём отпугивал. Как выяснилось, зря. Толстой великолепный рассказчик. Несмотря на глубину и широту повествования, текст на всем протяжении романа постоянно увлекал за собой, не давая заскучать. По содержанию Война и мир - это художественно-философское произведение. С художественной точки зрения Льву Николаевичу удалось воссоздать эпоху и вплести в неё живой сюжет с полнокровными и разносторонними героями. Описание событий войны зачастую даётся глазами какого-либо героя, что делает его органичной частью сюжета.\n', '2024-06-14 19:28:27');

-- --------------------------------------------------------

--
-- Структура таблицы `role`
--

CREATE TABLE `role` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `role`
--

INSERT INTO `role` (`id`, `name`, `description`) VALUES
(1, 'admin', 'Administrator with full access'),
(2, 'moderator', 'Moderator with limited access'),
(3, 'user', 'Regular user');

-- --------------------------------------------------------

--
-- Структура таблицы `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `login` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `middle_name` varchar(255) DEFAULT NULL,
  `role_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `user`
--

INSERT INTO `user` (`id`, `login`, `password_hash`, `last_name`, `first_name`, `middle_name`, `role_id`) VALUES
(1, 'admin', 'pbkdf2:sha256:260000$n2Y0SbDiTAJVexEn$f091831776cb4bf8440b80fdd12d34bf64158546fc9ab629b0d557971a875a98', 'Admin', 'Admin', NULL, 1),
(2, 'moderator', 'pbkdf2:sha256:260000$YhQlKsAMsiWKfz0N$7c78c2ea6dcebaa436798004ec984229d999cec0433397b947b4d37549340871', 'Mod', 'Moderator', NULL, 2),
(3, 'user', 'pbkdf2:sha256:260000$Rzu5OnG6kN1PgNNF$b86ff61f6490fa75c0092f83e0deb16feb5fa1f026ed74036b36dafc54bbf4f2', 'User', 'Regular', NULL, 3);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Индексы таблицы `book`
--
ALTER TABLE `book`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cover_id` (`cover_id`);

--
-- Индексы таблицы `books_genres`
--
ALTER TABLE `books_genres`
  ADD PRIMARY KEY (`book_id`,`genre_id`),
  ADD KEY `genre_id` (`genre_id`);

--
-- Индексы таблицы `collection`
--
ALTER TABLE `collection`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Индексы таблицы `collection_books`
--
ALTER TABLE `collection_books`
  ADD PRIMARY KEY (`collection_id`,`book_id`),
  ADD KEY `book_id` (`book_id`);

--
-- Индексы таблицы `cover`
--
ALTER TABLE `cover`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `genre`
--
ALTER TABLE `genre`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Индексы таблицы `review`
--
ALTER TABLE `review`
  ADD PRIMARY KEY (`id`),
  ADD KEY `book_id` (`book_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Индексы таблицы `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `login` (`login`),
  ADD KEY `role_id` (`role_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `book`
--
ALTER TABLE `book`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT для таблицы `collection`
--
ALTER TABLE `collection`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `cover`
--
ALTER TABLE `cover`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT для таблицы `genre`
--
ALTER TABLE `genre`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `review`
--
ALTER TABLE `review`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `role`
--
ALTER TABLE `role`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `book`
--
ALTER TABLE `book`
  ADD CONSTRAINT `book_ibfk_1` FOREIGN KEY (`cover_id`) REFERENCES `cover` (`id`) ON DELETE CASCADE;

--
-- Ограничения внешнего ключа таблицы `books_genres`
--
ALTER TABLE `books_genres`
  ADD CONSTRAINT `books_genres_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `books_genres_ibfk_2` FOREIGN KEY (`genre_id`) REFERENCES `genre` (`id`) ON DELETE CASCADE;

--
-- Ограничения внешнего ключа таблицы `collection`
--
ALTER TABLE `collection`
  ADD CONSTRAINT `collection_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Ограничения внешнего ключа таблицы `collection_books`
--
ALTER TABLE `collection_books`
  ADD CONSTRAINT `collection_books_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`),
  ADD CONSTRAINT `collection_books_ibfk_2` FOREIGN KEY (`collection_id`) REFERENCES `collection` (`id`);

--
-- Ограничения внешнего ключа таблицы `review`
--
ALTER TABLE `review`
  ADD CONSTRAINT `review_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `review_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;

--
-- Ограничения внешнего ключа таблицы `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `user_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
