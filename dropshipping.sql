-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 21, 2025 at 07:45 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dropshipping`
--

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 1,
  `added_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`id`, `user_id`, `product_id`, `quantity`, `added_at`) VALUES
(12, 3, 16, 1, '2025-04-08 15:02:28');

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`id`, `name`) VALUES
(3, 'Clothes'),
(4, 'Cosmetics'),
(1, 'Furniture'),
(5, 'Gadgets'),
(2, 'Vehicle');

-- --------------------------------------------------------

--
-- Table structure for table `chatbot_history`
--

CREATE TABLE `chatbot_history` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `message` text DEFAULT NULL,
  `is_bot` tinyint(1) DEFAULT NULL,
  `timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `chatbot_history`
--

INSERT INTO `chatbot_history` (`id`, `user_id`, `message`, `is_bot`, `timestamp`) VALUES
(1, 3, 'hi', 0, '2025-04-05 07:14:51'),
(2, 3, 'Hi customer! How can I help you today?', 1, '2025-04-05 07:14:51'),
(4, 3, 'hi', 0, '2025-04-05 07:16:46'),
(5, 3, 'Hi customer! How can I help you today?', 1, '2025-04-05 07:16:46'),
(6, 3, 'orders', 0, '2025-04-05 07:16:50'),
(7, 3, 'I\'m still learning. Try asking about your orders or popular products!', 1, '2025-04-05 07:16:50'),
(8, 3, 'my orders', 0, '2025-04-05 07:16:58'),
(9, 3, 'Here are your recent orders:\nOrder #3 – $100.00 – Status: Shipped\nOrder #2 – $240.00 – Status: Pending\nOrder #1 – $120.00 – Status: Pending', 1, '2025-04-05 07:16:58'),
(10, 3, 'which are the popular products?', 0, '2025-04-05 07:25:04'),
(11, 3, 'Hi customer! How can I help you today?', 1, '2025-04-05 07:25:04'),
(13, 3, 'hi', 0, '2025-04-05 07:30:29'),
(14, 3, 'Hi customer! How can I help you today?', 1, '2025-04-05 07:30:29'),
(15, 3, 'hi', 0, '2025-04-05 07:30:34'),
(16, 3, 'Hi customer! How can I help you today?', 1, '2025-04-05 07:30:34'),
(17, 3, 'hi', 0, '2025-04-05 07:33:20'),
(18, 3, 'Hi customer! How can I help you today?', 1, '2025-04-05 07:33:20'),
(19, 3, 'my orders', 0, '2025-04-05 07:33:25'),
(20, 3, 'Here are your recent orders:\nOrder #3 – $100.00 – Status: Shipped\nOrder #2 – $240.00 – Status: Pending\nOrder #1 – $120.00 – Status: Pending', 1, '2025-04-05 07:33:25'),
(22, 3, 'my orders', 0, '2025-04-05 07:33:38'),
(23, 3, 'Here are your recent orders:\nOrder #3 – $100.00 – Status: Shipped\nOrder #2 – $240.00 – Status: Pending\nOrder #1 – $120.00 – Status: Pending', 1, '2025-04-05 07:33:38'),
(24, 3, 'trending orders', 0, '2025-04-05 07:35:10'),
(25, 3, 'Check out these products:\ncar – $1000.00\nabc – $100.00\nuser2 – $120.00', 1, '2025-04-05 07:35:10'),
(26, 3, 'hi', 0, '2025-04-05 07:36:49'),
(27, 3, 'Hi customer! How can I help you today?', 1, '2025-04-05 07:36:49'),
(28, 3, 'my orders', 0, '2025-04-05 07:36:55'),
(29, 3, 'Here are your recent orders:\nOrder #3 – $100.00 – Status: Shipped\nOrder #2 – $240.00 – Status: Pending\nOrder #1 – $120.00 – Status: Pending', 1, '2025-04-05 07:36:55'),
(30, 3, 'trending orders', 0, '2025-04-05 07:36:58'),
(31, 3, 'Check out these products:\ncar – $1000.00\nabc – $100.00\nuser2 – $120.00', 1, '2025-04-05 07:36:58'),
(32, 3, 'tell me about abc', 0, '2025-04-05 07:37:09'),
(33, 3, 'abc – $100.00\nDescription: sdnkdcnk', 1, '2025-04-05 07:37:09'),
(34, 3, 'how to contact', 0, '2025-04-05 07:37:38'),
(35, 3, 'You can contact us at support@example.com or call 1-800-123-4567.', 1, '2025-04-05 07:37:38'),
(36, 3, 'give me order status', 0, '2025-04-05 07:37:49'),
(37, 3, 'Please provide a valid order number (e.g., \'status of order 123\').', 1, '2025-04-05 07:37:49'),
(38, 3, '1', 0, '2025-04-05 07:37:53'),
(39, 3, 'I\'m still learning. You can ask things like:\n- Show my orders\n- Status of order 101\n- Recommend popular products\n- Return policy\n- Contact info\n- Tell me about [product name]', 1, '2025-04-05 07:37:53'),
(40, 3, 'give me order status of 2', 0, '2025-04-05 07:38:11'),
(41, 3, 'Status of order #2: Pending.', 1, '2025-04-05 07:38:11'),
(42, 3, 'how long does shipping take', 0, '2025-04-05 07:39:55'),
(43, 3, 'Hi customer! How can I help you today?', 1, '2025-04-05 07:39:55'),
(44, 3, 'shipping', 0, '2025-04-05 07:39:58'),
(45, 3, 'Hi customer! How can I help you today?', 1, '2025-04-05 07:39:58'),
(46, 3, 'shipping', 0, '2025-04-05 07:40:02'),
(47, 3, 'Hi customer! How can I help you today?', 1, '2025-04-05 07:40:02'),
(48, 3, 'delivery time', 0, '2025-04-05 07:40:13'),
(49, 3, 'Standard shipping takes 3-5 business days. Express shipping options are available at checkout.', 1, '2025-04-05 07:40:13'),
(50, 3, 'hi', 0, '2025-04-05 07:42:48'),
(51, 3, 'Hi customer! How can I help you today?', 1, '2025-04-05 07:42:48'),
(52, 3, 'how are you?', 0, '2025-04-05 07:42:54'),
(53, 3, 'I\'m still learning. You can ask things like:\n- Show my orders\n- Status of order 101\n- Recommend popular products\n- Return policy\n- Contact info\n- Tell me about [product name]', 1, '2025-04-05 07:42:54'),
(54, 3, 'hi', 0, '2025-04-05 07:49:54'),
(55, 3, 'Hi customer! How can I help you today?', 1, '2025-04-05 07:49:54'),
(56, 3, 'hello', 0, '2025-04-05 07:49:59'),
(57, 3, 'Hi customer! How can I help you today?', 1, '2025-04-05 07:49:59'),
(58, 3, 'hello', 0, '2025-04-05 07:50:02'),
(59, 3, 'Hi customer! How can I help you today?', 1, '2025-04-05 07:50:02'),
(60, 3, 'hell', 0, '2025-04-05 07:50:06'),
(61, 3, 'I\'m still learning. You can ask things like:\n- Show my orders\n- Status of order 101\n- Recommend popular products\n- Return policy\n- Contact info\n- Tell me about [product name]', 1, '2025-04-05 07:50:06'),
(62, 3, 'fjkhsdcn', 0, '2025-04-05 07:50:08'),
(63, 3, 'I\'m still learning. You can ask things like:\n- Show my orders\n- Status of order 101\n- Recommend popular products\n- Return policy\n- Contact info\n- Tell me about [product name]', 1, '2025-04-05 07:50:08'),
(64, 3, 'hi', 0, '2025-04-05 07:50:40'),
(65, 3, 'Hi customer! How can I help you today?', 1, '2025-04-05 07:50:40'),
(66, 3, 'hi', 0, '2025-04-05 07:52:18'),
(67, 3, 'Hi customer! How can I help you today?', 1, '2025-04-05 07:52:18'),
(68, 3, 'my orders', 0, '2025-04-05 07:53:01'),
(69, 3, 'Here are your recent orders:\nOrder #3 – $100.00 – Status: Shipped\nOrder #2 – $240.00 – Status: Pending\nOrder #1 – $120.00 – Status: Pending', 1, '2025-04-05 07:53:01'),
(70, 3, 'whats the sttaus of order no 2', 0, '2025-04-05 07:53:11'),
(71, 3, 'I\'m still learning. You can ask things like:\n- Show my orders\n- Status of order 101\n- Recommend popular products\n- Return policy\n- Contact info\n- Tell me about [product name]', 1, '2025-04-05 07:53:11'),
(72, 3, 'whats the status of order 2', 0, '2025-04-05 07:53:18'),
(73, 3, 'Status of order #2: Pending.', 1, '2025-04-05 07:53:18'),
(74, 3, 'hi', 0, '2025-04-05 21:36:53'),
(75, 3, 'Hi customer! How can I help you today?', 1, '2025-04-05 21:36:53'),
(76, 3, 'whast the status of my order 1', 0, '2025-04-05 21:37:01'),
(77, 3, 'Status of order #1: Shipped.', 1, '2025-04-05 21:37:01'),
(78, 3, 'is sofa available?', 0, '2025-04-05 21:37:17'),
(79, 3, 'I\'m still learning. You can ask things like:\n- Show my orders\n- Status of order 101\n- Recommend popular products\n- Return policy\n- Contact info\n- Tell me about [product name]', 1, '2025-04-05 21:37:17'),
(80, 3, 'show my orders', 0, '2025-04-05 21:37:23'),
(81, 3, 'Here are your recent orders:\nOrder #3 – $100.00 – Status: Shipped\nOrder #2 – $240.00 – Status: Shipped\nOrder #1 – $120.00 – Status: Shipped', 1, '2025-04-05 21:37:23'),
(82, 3, 'recommend popular products', 0, '2025-04-05 21:37:32'),
(83, 3, 'Check out these products:\nuser2 – $120.00\nsofa – $120.00\nhello – $120.00', 1, '2025-04-05 21:37:32'),
(84, 3, 'hi', 0, '2025-04-06 11:23:01'),
(85, 3, 'Hi customer! How can I help you today?', 1, '2025-04-06 11:23:01'),
(86, 3, 'my orders', 0, '2025-04-06 11:23:06'),
(87, 3, 'Here are your recent orders:\nOrder #3 – $100.00 – Status: Shipped\nOrder #2 – $240.00 – Status: Shipped\nOrder #1 – $120.00 – Status: Shipped', 1, '2025-04-06 11:23:06'),
(88, 3, 'hi', 0, '2025-04-06 16:56:09'),
(89, 3, 'Hi customer! How can I help you today?', 1, '2025-04-06 16:56:09'),
(90, 3, 'my orders', 0, '2025-04-06 16:56:13'),
(91, 3, 'Here are your recent orders:\nOrder #3 – $100.00 – Status: Shipped\nOrder #2 – $240.00 – Status: Shipped\nOrder #1 – $120.00 – Status: Shipped', 1, '2025-04-06 16:56:13'),
(92, 3, 'hi', 0, '2025-04-06 22:38:22'),
(93, 3, 'Hi customer! How can I help you today?', 1, '2025-04-06 22:38:22'),
(94, 3, 'can u list my orders', 0, '2025-04-06 22:38:29'),
(95, 3, 'Here are your recent orders:\nOrder #5 – $9100.00 – Status: Delivered\nOrder #4 – $16400.00 – Status: Pending\nOrder #3 – $100.00 – Status: Shipped', 1, '2025-04-06 22:38:29'),
(96, 3, 'whats the status of order 2', 0, '2025-04-06 22:38:40'),
(97, 3, 'Status of order #2: Shipped.', 1, '2025-04-06 22:38:40'),
(98, 3, 'can you list some popular products?', 0, '2025-04-06 22:38:50'),
(99, 3, 'Check out these products:\nLaptop – $8000.00\nskincare – $400.00\nWatch – $700.00', 1, '2025-04-06 22:38:50'),
(100, 3, 'hi', 0, '2025-04-06 23:03:14'),
(101, 3, 'Hi customer! How can I assist you with products, orders, or your account today?', 1, '2025-04-06 23:03:14'),
(102, 3, 'list my orders', 0, '2025-04-06 23:03:41'),
(103, 3, 'Sorry, I encountered an unexpected issue while trying to understand that. Please try rephrasing, or contact support if the problem continues.', 1, '2025-04-06 23:03:41'),
(107, 3, '/help', 0, '2025-04-07 11:52:21'),
(108, 3, 'I can help with:\n- Show my orders\n- Status of order [ID]\n- Items in order [ID]\n- Cancel order [ID]\n- Recommend popular products\n- Tell me about [product name]\n- Show categories\n- Show products in [category]\n- Show my wishlist\n- Add [product] to wishlist\n- Remove [product] from wishlist\n- Show my cart\n- My profile\n- Shipping times\n- Return policy\n- Contact info', 1, '2025-04-07 11:52:21'),
(109, 3, 'show my orders', 0, '2025-04-07 11:52:26'),
(110, 3, 'Here are your recent orders:\nOrder #5 – $9100.00 – Delivered\nOrder #4 – $16400.00 – Pending\nOrder #3 – $100.00 – Shipped', 1, '2025-04-07 11:52:26'),
(111, 3, 'status of order 2', 0, '2025-04-07 11:52:33'),
(112, 3, 'Status of order #2: Shipped.', 1, '2025-04-07 11:52:33'),
(113, 3, 'items in order 2', 0, '2025-04-07 11:52:40'),
(114, 3, 'No items found for order #2.', 1, '2025-04-07 11:52:40'),
(115, 3, 'items in order 1', 0, '2025-04-07 11:52:48'),
(116, 3, 'No items found for order #1.', 1, '2025-04-07 11:52:48'),
(117, 3, 'items in order 3', 0, '2025-04-07 11:52:53'),
(118, 3, 'No items found for order #3.', 1, '2025-04-07 11:52:53'),
(119, 3, 'cancel order 1', 0, '2025-04-07 11:53:01'),
(120, 3, 'Order #1 cannot be canceled (current status: Shipped).', 1, '2025-04-07 11:53:01'),
(121, 3, 'recommend popular products', 0, '2025-04-07 11:53:12'),
(122, 3, 'Check out these products:\nLaptop – $8000.00\nskincare – $400.00\nWatch – $700.00', 1, '2025-04-07 11:53:12'),
(123, 3, 'tell me about laptop', 0, '2025-04-07 11:53:21'),
(124, 3, 'Laptop – $8000.00\nDescription: laptop', 1, '2025-04-07 11:53:21'),
(125, 3, 'show categories', 0, '2025-04-07 11:53:28'),
(126, 3, 'We have these categories:\nClothes\nCosmetics\nFurniture\nGadgets\nVehicle', 1, '2025-04-07 11:53:28'),
(127, 3, 'show products in clothes', 0, '2025-04-07 11:53:39'),
(128, 3, 'Products in clothes:\nDress – $300.00', 1, '2025-04-07 11:53:39'),
(129, 3, 'add dress to wishlist', 0, '2025-04-07 11:53:49'),
(130, 3, 'Could not find product \'dress to\'.', 1, '2025-04-07 11:53:49'),
(131, 3, 'add product dress to wishlist', 0, '2025-04-07 11:54:04'),
(132, 3, 'Could not find product \'product dress to\'.', 1, '2025-04-07 11:54:04'),
(133, 3, 'add product dress', 0, '2025-04-07 11:54:10'),
(134, 3, 'Sorry, I didn\'t understand. Type \'help\' to see all commands I support.', 1, '2025-04-07 11:54:10'),
(135, 3, 'add dress to wishlist', 0, '2025-04-07 11:54:26'),
(136, 3, 'Could not find product \'dress to\'.', 1, '2025-04-07 11:54:26'),
(137, 3, 'show my wishlist', 0, '2025-04-07 11:54:35'),
(138, 3, 'Your wishlist:\nWatch – $700.00\nLaptop – $8000.00', 1, '2025-04-07 11:54:35'),
(139, 3, 'add dress to wishlist', 0, '2025-04-07 11:54:42'),
(140, 3, 'Could not find product \'dress to\'.', 1, '2025-04-07 11:54:42'),
(141, 3, 'remove watch from wishlist', 0, '2025-04-07 11:54:53'),
(142, 3, 'Could not find product \'watch from\'.', 1, '2025-04-07 11:54:53'),
(143, 3, 'remove [watch] from wishlist', 0, '2025-04-07 11:55:06'),
(144, 3, 'Could not find product \'[watch] from\'.', 1, '2025-04-07 11:55:06'),
(145, 3, 'show my cart', 0, '2025-04-07 11:55:18'),
(146, 3, 'Your cart is empty.', 1, '2025-04-07 11:55:18'),
(147, 3, 'return policy', 0, '2025-04-07 11:55:28'),
(148, 3, 'You can return products within 14 days of delivery. Refunds process within 5-7 business days.', 1, '2025-04-07 11:55:28'),
(149, 3, 'contact info', 0, '2025-04-07 11:55:36'),
(150, 3, 'Contact us at support@example.com or call 1-800-123-4567.', 1, '2025-04-07 11:55:36'),
(151, 3, 'good morning', 0, '2025-04-07 11:57:24'),
(152, 3, 'Sorry, I didn\'t understand. Type \'help\' to see all commands I support.', 1, '2025-04-07 11:57:24'),
(153, 3, 'hi', 0, '2025-04-07 11:57:26'),
(154, 3, 'Hi customer! How can I assist you today?', 1, '2025-04-07 11:57:26'),
(155, 3, 'add watch to wishlist', 0, '2025-04-07 11:57:32'),
(156, 3, 'Added **watch** to your wishlist.', 1, '2025-04-07 11:57:32'),
(157, 3, 'show my wishlist', 0, '2025-04-07 11:57:39'),
(158, 3, 'Your wishlist:\nWatch – $700.00\nLaptop – $8000.00', 1, '2025-04-07 11:57:39'),
(159, 3, 'add dress to wishlist', 0, '2025-04-07 11:57:51'),
(160, 3, 'Added **dress** to your wishlist.', 1, '2025-04-07 11:57:51'),
(161, 3, 'show wishlist', 0, '2025-04-07 11:57:55'),
(162, 3, 'Your wishlist:\nDress – $300.00\nWatch – $700.00\nLaptop – $8000.00', 1, '2025-04-07 11:57:55'),
(163, 3, 'remove dress from wishlist', 0, '2025-04-07 11:58:20'),
(164, 3, 'Could not find product \'dress from\'.', 1, '2025-04-07 11:58:20'),
(165, 3, 'remove dress from wishlist', 0, '2025-04-07 12:01:32'),
(166, 3, 'Removed **dress** from your wishlist.', 1, '2025-04-07 12:01:32'),
(167, 3, 'show my wishlist', 0, '2025-04-07 12:01:36'),
(168, 3, 'Your wishlist:\nWatch – $700.00\nLaptop – $8000.00', 1, '2025-04-07 12:01:36'),
(169, 3, 'hi', 0, '2025-04-08 20:21:18'),
(170, 3, 'Hi customer! How can I assist you today?', 1, '2025-04-08 20:21:18'),
(171, 3, 'show me my orders', 0, '2025-04-08 20:21:23'),
(172, 3, 'Here are your recent orders:\nOrder #5 – $9100.00 – Delivered\nOrder #4 – $16400.00 – Pending\nOrder #3 – $100.00 – Shipped', 1, '2025-04-08 20:21:23'),
(173, 3, 'show me my wishlist', 0, '2025-04-08 20:21:28'),
(174, 3, 'Your wishlist:\nWatch – $700.00\nLaptop – $8000.00', 1, '2025-04-08 20:21:28'),
(175, 3, 'is dress availaible', 0, '2025-04-08 20:21:33'),
(176, 3, 'Sorry, I didn\'t understand. Type \'help\' to see all commands I support.', 1, '2025-04-08 20:21:33'),
(177, 3, 'help', 0, '2025-04-08 20:21:36'),
(178, 3, 'I can help with:\n- Show my orders\n- Status of order [ID]\n- Items in order [ID]\n- Cancel order [ID]\n- Recommend popular products\n- Tell me about [product name]\n- Show categories\n- Show products in [category]\n- Show my wishlist\n- Add [product] to wishlist\n- Remove [product] from wishlist\n- Show my cart\n- My profile\n- Shipping times\n- Return policy\n- Contact info', 1, '2025-04-08 20:21:36'),
(179, 3, 'tell me about laptop', 0, '2025-04-08 20:21:55'),
(180, 3, 'Laptop – $8000.00\nDescription: laptop', 1, '2025-04-08 20:21:55'),
(181, 3, 'status of order 2', 0, '2025-04-08 20:22:02'),
(182, 3, 'Status of order #2: Shipped.', 1, '2025-04-08 20:22:02'),
(183, 3, 'hi', 0, '2025-04-08 20:37:33'),
(184, 3, 'Hi customer! How can I assist you today?', 1, '2025-04-08 20:37:33'),
(185, 3, 'help', 0, '2025-04-08 20:37:38'),
(186, 3, 'I can help with:\n- Show my orders\n- Status of order [ID]\n- Items in order [ID]\n- Cancel order [ID]\n- Recommend popular products\n- Tell me about [product name]\n- Show categories\n- Show products in [category]\n- Show my wishlist\n- Add [product] to wishlist\n- Remove [product] from wishlist\n- Show my cart\n- My profile\n- Shipping times\n- Return policy\n- Contact info', 1, '2025-04-08 20:37:38'),
(187, 3, 'show my orders', 0, '2025-04-08 20:37:58'),
(188, 3, 'Here are your recent orders:\nOrder #6 – $8000.00 – Processing\nOrder #5 – $9100.00 – Pending\nOrder #4 – $16400.00 – Pending', 1, '2025-04-08 20:37:58'),
(189, 3, 'show my wishlist', 0, '2025-04-08 20:38:11'),
(190, 3, 'Your wishlist:\nWatch – $700.00\nLaptop – $8000.00', 1, '2025-04-08 20:38:11'),
(191, 3, 'show my cart', 0, '2025-04-08 20:38:26'),
(192, 3, 'Your cart is empty.', 1, '2025-04-08 20:38:26'),
(193, 3, 'help', 0, '2025-04-08 20:38:36'),
(194, 3, 'I can help with:\n- Show my orders\n- Status of order [ID]\n- Items in order [ID]\n- Cancel order [ID]\n- Recommend popular products\n- Tell me about [product name]\n- Show categories\n- Show products in [category]\n- Show my wishlist\n- Add [product] to wishlist\n- Remove [product] from wishlist\n- Show my cart\n- My profile\n- Shipping times\n- Return policy\n- Contact info', 1, '2025-04-08 20:38:36'),
(195, 3, 'tell me about laptop', 0, '2025-04-08 20:38:53'),
(196, 3, 'Laptop – $8000.00\nDescription: laptop', 1, '2025-04-08 20:38:53'),
(197, 3, 'show categories', 0, '2025-04-08 20:39:01'),
(198, 3, 'We have these categories:\nClothes\nCosmetics\nFurniture\nGadgets\nVehicle', 1, '2025-04-08 20:39:01'),
(199, 3, 'add skincare to wishlist', 0, '2025-04-08 20:39:31'),
(200, 3, 'Added **skincare** to your wishlist.', 1, '2025-04-08 20:39:31'),
(201, 3, 'remove skincare from wishlist', 0, '2025-04-08 20:39:46'),
(202, 3, 'Removed **skincare** from your wishlist.', 1, '2025-04-08 20:39:46'),
(203, 3, 'help', 0, '2025-04-08 20:39:56'),
(204, 3, 'I can help with:\n- Show my orders\n- Status of order [ID]\n- Items in order [ID]\n- Cancel order [ID]\n- Recommend popular products\n- Tell me about [product name]\n- Show categories\n- Show products in [category]\n- Show my wishlist\n- Add [product] to wishlist\n- Remove [product] from wishlist\n- Show my cart\n- My profile\n- Shipping times\n- Return policy\n- Contact info', 1, '2025-04-08 20:39:56'),
(205, 3, 'status of order 2', 0, '2025-04-08 20:40:16'),
(206, 3, 'Status of order #2: Shipped.', 1, '2025-04-08 20:40:16'),
(207, 3, 'hi', 0, '2025-04-09 18:30:45'),
(208, 3, 'Hi customer! How can I assist you today?', 1, '2025-04-09 18:30:45'),
(209, 3, 'show me my wishlist', 0, '2025-04-09 18:30:49'),
(210, 3, 'Your wishlist:\nWatch – $700.00\nLaptop – $8000.00', 1, '2025-04-09 18:30:49'),
(211, 3, 'hi', 0, '2025-04-13 12:02:38'),
(212, 3, 'Hi customer! How can I assist you today?', 1, '2025-04-13 12:02:38'),
(213, 3, 'show my orders', 0, '2025-04-13 12:02:44'),
(214, 3, 'Here are your recent orders:\nOrder #6 – $8000.00 – Processing\nOrder #5 – $9100.00 – Pending\nOrder #4 – $16400.00 – Pending', 1, '2025-04-13 12:02:44');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `status` enum('Pending','Processing','Shipped','Delivered','Cancelled') DEFAULT 'Pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `user_id`, `total_price`, `status`, `created_at`) VALUES
(1, 3, 120.00, 'Shipped', '2025-04-04 02:40:39'),
(2, 3, 240.00, 'Shipped', '2025-04-04 02:45:52'),
(3, 3, 100.00, 'Shipped', '2025-04-04 02:54:36'),
(4, 3, 16400.00, 'Pending', '2025-04-06 13:19:48'),
(5, 3, 9100.00, 'Pending', '2025-04-06 16:52:09'),
(6, 3, 8000.00, 'Processing', '2025-04-08 15:02:16');

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `product_id`, `quantity`, `price`) VALUES
(5, 4, 18, 2, 8000.00),
(6, 4, 17, 1, 400.00),
(7, 5, 18, 1, 8000.00),
(8, 5, 17, 2, 400.00),
(9, 5, 10, 1, 300.00),
(10, 6, 18, 1, 8000.00);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `video` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `seller_id` int(11) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `description`, `image`, `video`, `price`, `seller_id`, `category_id`) VALUES
(1, 'hello', 'ncdkjc', '/static/uploads/Screenshot_from_2025-04-02_18-32-54.png', '/static/uploads/vecteezy_hello-neon-light-title-animation-on-wall-great-for_23960299.mp4', 120.00, 1, NULL),
(10, 'Dress', 'Dress', '/static/uploads/URBAN-1_img19_out-Copy-scaled-1.jpg', '', 300.00, 4, 3),
(12, 'Earbuds', 'earbuds', '/static/uploads/boat_airdopes_91_blue.jpg', '/static/uploads/9130367-uhd_3840_2160_30fps.mp4', 200.00, 4, 5),
(14, 'Bed', 'bed', '/static/uploads/istockphoto-693197002-612x612.jpg', '', 3000.00, 4, 1),
(16, 'Watch', 'WATCH', '/static/uploads/prod2.jpg', '', 700.00, 4, 5),
(17, 'skincare', 'skincare', '/static/uploads/cosmetics.jpg', '', 400.00, 4, 4),
(18, 'Laptop', 'laptop', '/static/uploads/360_F_799572290_MMlAtIsJxdLK8mg9gVPDQoYvHuF24T2j.jpg', '', 8000.00, 4, 5);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(200) NOT NULL,
  `role` varchar(20) NOT NULL DEFAULT 'Customer',
  `is_blocked` tinyint(1) DEFAULT 0,
  `last_login` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `role`, `is_blocked`, `last_login`) VALUES
(1, 'abc', 'dbhsb@gmail.com', '$2b$12$fLUGNTxx/4CiA6K4MjY6geoxZ3tVSaK5sfgCCdGGIcA11W.g9ltYa', 'Admin', 0, NULL),
(2, 'user2', 'SHAIKHAAYESHA26@GMAIL.COM', '$2b$12$vcvVGRMK5vz0yhnxC3.YVuxuMOWy5NezV/vOUqypdiVcUu.YhYDrq', 'Seller', 0, NULL),
(3, 'customer', 'customer@gmail.com', '$2b$12$pT1w8jzx3vGcS0btqYr4qegEbA7z5yUoLrOOOwaeoxhHlJm0OUW6O', 'Customer', 0, '2025-04-13 12:18:27'),
(4, 'seller', 'seller@gmail.com', '$2b$12$qzQzUsOfMi8HdVYLV9efauILEqsvUZrtvWQ1FLMHAmK13dkzn9ZUm', 'Seller', 0, '2025-04-13 12:03:46'),
(5, 'admin', 'admin@gmail.com', '$2b$12$RGOzUA3wUL/KAYls1/8oa.8qZwmY9M5ZwDjGblXQ8QKDcdQ3zLQOq', 'Admin', 0, '2025-04-13 12:10:23'),
(6, 'ayesha', 'ayesha@gmail.com', '$2b$12$I9cr2Jn7hhSA3MmHem5ofeZ8Llhp/ph.bhHTSn.Z2wXblyyQK5Ai6', 'Customer', 0, '2025-04-06 22:16:43');

-- --------------------------------------------------------

--
-- Table structure for table `wishlist`
--

CREATE TABLE `wishlist` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `wishlist`
--

INSERT INTO `wishlist` (`id`, `user_id`, `product_id`, `created_at`) VALUES
(5, 3, 18, '2025-04-06 11:15:57'),
(6, 3, 16, '2025-04-06 11:26:37');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `chatbot_history`
--
ALTER TABLE `chatbot_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD KEY `seller_id` (`seller_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `wishlist`
--
ALTER TABLE `wishlist`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`,`product_id`),
  ADD KEY `product_id` (`product_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `chatbot_history`
--
ALTER TABLE `chatbot_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=215;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `wishlist`
--
ALTER TABLE `wishlist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `chatbot_history`
--
ALTER TABLE `chatbot_history`
  ADD CONSTRAINT `chatbot_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`seller_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `products_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`);

--
-- Constraints for table `wishlist`
--
ALTER TABLE `wishlist`
  ADD CONSTRAINT `wishlist_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `wishlist_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
