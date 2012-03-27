<html>
<head>
	<meta charset='gbk' />
</head>
<body>
<?php
	$file_name = "fed_salon_registered.txt";
	$seperator = 'S#E$P%E&R*A!T_O@R';
	$salon_name = 'S2012E01';
	$salon_id = 1;

	function open_mysql_connection() {
		$conn = mysql_connect("10.2.74.100:3306", "salon", "111111" ) or die ("Could not connect:".mysql_error());
		$program_char = "utf8";
		$conn.mysql_select_db("salon");
		mysql_set_charset($program_char, $conn); 
		return $conn;
	}

	function get_md5($str) {
		//$str = "FED_Salon_wangjeaf@gmail.com";
		return substr(md5($str), 0, 6);
	}

	// 把新注册用户的信息放入文件存储
	function save_record_to_db($conn, $username, $company, $mobile, $email, $introduction, $register_time) {
		global $salon_id;
		global $salon_name;

		$barcode = get_md5("$salon_name" . "_" . "$email");

		if ($register_time == "") {
			$register_time = '2012-3-26 10:00:00';
		}

		mysql_query("INSERT INTO salon_user (salon_id, name, mobile, email, company, introduction, register_time, status, barcode) VALUES ($salon_id, '$username', '$mobile', '$email', '$company', '$introduction', '$register_time', 0, '$barcode')");

	}

	function exports_data_from_file() {
		global $file_name;
		global $seperator;

		$conn = open_mysql_connection();
		$fp = fopen($file_name, "r");
		while(! feof($fp)) { 
			$record = fgets($fp);
			list ($username, $company, $mobile, $email, $introduction, $register_time) = explode($seperator, $record);
			if ($username != "") {
				save_record_to_db($conn, $username, $company, $mobile, $email, $introduction, $register_time);
			}
		} 
		$conn.mysql_close();
		fclose($fp);
	}
	exports_data_from_file();
?>

</body>
</html>
