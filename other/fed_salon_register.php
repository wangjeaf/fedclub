<html>
<body>
<?php

// 获取referer，判断是否来自于fed.renren.com
$referer = $_SERVER['HTTP_REFERER'];

if (is_from_renren_blog($referer) == false) {
	write_message_and_goto("旁门已关，请走正门~ :-)", "http://fed.renren.com");
	return;
}

date_default_timezone_set('PRC');
$send_mail_to_user = false;

$file_name = "fed_salon_registered.txt";
$seperator = 'S#E$P%E&R*A!T_O@R';

$username = $_POST["username"];
$company = $_POST["company"];
$mobile = $_POST["mobile"];
$email = $_POST["email"];
$introduction = $_POST["introduction"];

# 先尝试连接数据库，如果连接不成功，则使用文件存储
$conn = false;
try {
	$conn = open_mysql_connection("10.2.74.100:3306", "salon", "111111", "salon");
} catch (Exception $e) {
}

if (is_not_empty($username) == false) {
	write_message("请填写您的尊姓大名，以便我们认识您！");
//} else if (is_mobile($mobile) == false) {
//	write_message("请填写正确的手机号，以便我们联系您！");
} else if (is_email($email) == false) {
	write_message("请填写正确的邮箱地址，以便我们联系您！");
//} else if (is_not_empty($introduction) == false) {
//	write_message("请填写您的丰功伟绩，以便我们了解您！");
} else if (is_user_email_registered($conn, $email)){
	write_message("您的邮箱已经注册过啦，请换一个更NB的邮箱吧！");
} else {
	$date = date("Y-m-d H:i:s");
	$translated = preg_split('/\r\n/', $introduction);
	$trans_array = join($translated, ',');

	// 保存记录，先判断是否成功连接数据库
	if ($conn != false) {
		save_record_to_db($conn, $username, $company, $mobile, $email, $trans_array, $date);
		// 暂时仍然将记录保存在文件中
		save_record_to_file($username, $company, $mobile, $email, $trans_array, $date);
		$conn.mysql_close();
	} else {
		save_record_to_file($username, $company, $mobile, $email, $trans_array, $date);
	}

	send_email_to_manager($username, $company, $mobile, $email, $trans_array, $date);
	if ($send_mail_to_user) {
		send_welcome_email_to_user($username, $email);
	}
}

function open_mysql_connection($host, $user, $pass, $db) {
	$conn = mysql_connect($host, $user, $pass) or die ("Could not connect:".mysql_error());
	$program_char = "utf8";
	$conn.mysql_select_db($db);
	mysql_set_charset($program_char, $conn); 
	return $conn;
}

function get_md5($str) {
	//$str = "FED_Salon_wangjeaf@gmail.com";
	return substr(md5($str), 0, 6);
}

// 把新注册用户的信息放入文件存储
function save_record_to_db($conn, $username, $company, $mobile, $email, $introduction, $register_time) {
	$barcode = get_md5("S2012E01" . "_" . "$email");

	if ($register_time == "") {
		$register_time = date("Y-m-d H:i:s");
	}

	mysql_query("INSERT INTO salon_user (salon_id, name, mobile, email, company, introduction, register_time, status, barcode) VALUES (1, '$username', '$mobile', '$email', '$company', '$introduction', '$register_time', 0, '$barcode')");
}

// 给用户发送欢迎邮件
function send_welcome_email_to_user($username, $email) {
	$to = $email;

	// set time zone to People's Republic of China
	date_default_timezone_set('PRC');
	$date = date("Y-m-d H:i:s");

	$headers  = 'MIME-Version: 1.0' . "\r\n";
	$headers .= 'Content-type: text/html; charset=utf-8' . "\r\n";
	$headers .= "To: $to \r\n";
	$headers .= 'From: no-reply.fed@renren-inc.com' . "\r\n";

	$subject = "欢迎 $username 参加人人网FED技术沙龙~~";
	$subject = "=?UTF-8?B?".base64_encode($subject)."?=";

	$content = "<html><head><meta charset='utf-8'></head><body>";
	$content .= "<p>" . $username . "，您好：</p>";
	$content .= "<p style='margin-left:2em;'>欢迎您注册\"人人网FED技术沙龙\"！</p>";
	$content .= "<p style='margin-left:2em;'>您的申请我们已经收到，我们将通过电子邮件或电话的方式与您取得联系。</p>";
	$content .= "<p style='margin-left:2em;'>请您耐心等候，谢谢~</p>";
	$content .= "---------------<p>人人 FED @ $date</p></body></html>";

	mail($to, $subject, $content, $headers);
}

function get_registered_users_from_db($conn, $content) {
	$content .= '<table border=2>';
	$content .= "<thead><tr style='font-weight:bold;'><td>姓名</td><td>公司</td><td>手机</td><td>邮箱</td><td>自我介绍</td><td>注册时间</td></tr></thead><tbody>";

	$result = mysql_query("select * from salon_user", $conn);
	$row = mysql_fetch_object($result);
	while($row) { 
		$username = $row->name;
		$company = $row->company;
		$mobile = $row->mobile;
		$email = $row->email;
		$introduction = $row->introduction;
		$date = $row->register_time;

		if ($username != "") {
			$content .= "<tr>";
			$content .= "<td>$username</td>";
			$content .= "<td>$company</td>";
			$content .= "<td>$mobile</td>";
			$content .= "<td>$email</td>";
			if (strlen($introduction) > 30) {
				$content .= "<td>" . substr($introduction, 0, 30) . "...</td>";
			} else {
				$content .= "<td>$introduction</td>";
			}
			$content .= "<td>$date</td>";
			$content .= "</tr>";
		}
		$row = mysql_fetch_object($result);
	} 
	$content .= '</tbody></table>';

	return $content;
}

function get_registered_users_from_file($content) {
	global $file_name;
	global $seperator;

	$fp = fopen($file_name, "r"); 
	$content .= '<table border=2>';
	$content .= "<thead><tr style='font-weight:bold;'><td>姓名</td><td>公司</td><td>手机</td><td>邮箱</td><td>自我介绍</td><td>注册时间</td></tr></thead>";
	while(! feof($fp)) { 
		$record = fgets($fp);
		list ($username, $company, $mobile, $email, $introduction, $date) = explode($seperator, $record);
		if ($username != "") {
			$content .= "<tr>";
			$content .= "<td>$username</td>";
			$content .= "<td>$company</td>";
			$content .= "<td>$mobile</td>";
			$content .= "<td>$email</td>";
			if (strlen($introduction) > 30) {
				$content .= "<td>" . substr($introduction, 0, 30) . "...</td>";
			} else {
				$content .= "<td>$introduction</td>";
			}
			$content .= "<td>$date</td>";
			$content .= "</tr>";
		}
	} 
	$content .= '</table>';
	fclose($fp); 

	return $content;
}

// 将用户的信息发送到管理员
function send_email_to_manager($username, $company, $mobile, $email, $introduction, $date) {
	global $conn;
	//$to = 'jingwei.li@renren-inc.com,zhifu.wang@renren-inc.com';
	$to = 'jingwei.li@renren-inc.com';

	// set time zone to People's Republic of China
	date_default_timezone_set('PRC');

	$headers  = 'MIME-Version: 1.0' . "\r\n";
	$headers .= 'Content-type: text/html; charset=utf-8' . "\r\n";
	$headers .= "To: $to \r\n";
	$headers .= 'From: no-reply.fed@renren-inc.com' . "\r\n";

	$subject = "$username 注册了人人FED技术沙龙";
	$subject = "=?UTF-8?B?".base64_encode($subject)."?=";

	$content = '<table border=2>';
	$content .= '<tr><td>姓名：</td>'."<td>$username</td>";
	$content .= '<tr><td>公司名称：</td>'."<td>$company</td>";
	$content .= '<tr><td>手机：</td>'."<td>$mobile</td>";
	$content .= '<tr><td>邮箱：</td>'."<td>$email</td>";
	$content .= '<tr><td>自我介绍：</td>'."<td>$introduction</td>";
	$content .= "<tr><td>注册时间：</td><td>$date</td>";
	$content .= '</table>';

	if ($conn == false) {
		$content .= "<br><br>已注册用户信息统计：\n";
		$content = get_registered_users_from_file($content);
	} else {
		$content .= "<br><br>已注册用户信息在10.2.74.100上的mysql中查看即可\n";
		//$content = get_registered_users_from_db($conn, $content);
	}

	$result = mail($to, $subject, $content, $headers);

	if($result) {
		write_message("您的信息已经提交，谢谢您的参与，请敬候佳音~");
	}
}

// 请求是否来自人人blog，避免外部进入
function is_from_renren_blog($referer) {
	if (ereg('^http:\/\/fed\.renren\.com', $referer)) {
		return true;
	} else {
		return false;
	}
}

// 是否非空的校验
function is_not_empty($msg) {
	if (strlen(trim($msg)) == "0") {
		return false;
	}
	return true;
}

// 是否是电子邮箱的校验
function is_email($email) {
	if(ereg("^[_\.0-9A-Za-z-]+@([0-9A-Za-z][0-9A-Za-z-]+\.)+[a-z]{2,3}$",$email)){
		return true;
	}else{
		return false;
	}
}

// 是否是手机的校验
function is_mobile($mobile) {
	if(strlen($mobile) != "11") {
		return false;
	}
	if(ereg("^[0-9]{11}$",$mobile)){
		return true;
	} else {
		return false;
	}
}

// 用js打印消息$msg
function write_message($msg) {
	echo '<html><head><meta charset="utf-8"/></head><body><script type="text/javascript">alert("' . $msg  . '");window.history.back();</script></body></html>';
}

// 用js打印消息$msg，并且转入$url对应的页面
function write_message_and_goto($msg, $url) {
	echo '<html><head><meta charset="utf-8"/></head><body><script type="text/javascript">alert("' . $msg  . '");window.location.href="' . $url . '";</script></body></html>';
}

// 把新注册用户的信息放入文件存储
function save_record_to_file($username, $company, $mobile, $email, $introduction, $date) {
	global $file_name;
	global $seperator;
	$fp = fopen($file_name, "a+"); 
	fwrite($fp, "$username$seperator$company$seperator$mobile$seperator$email$seperator$introduction$seperator$date\n"); 
	fclose($fp); 
}

// 判断当前注册的email是否注册过
function is_user_email_registered($conn, $new_email) {
	if ($conn != false) {
		$result = mysql_query("select * from salon_user where email='" . $new_email . "'", $conn);
		if(mysql_fetch_object($result)) {
			return true;
		} else {
			return false;
		}
	} else {
		global $file_name;
		global $seperator;
		if (file_exists($file_name) && is_readable($file_name)) {
			$boolean = false;
			$fp = fopen($file_name, "r"); 
			while(! feof($fp)) { 
				$record = fgets($fp);
				list ($username, $company, $mobile, $email, $introduction) = explode($seperator, $record);
				if (trim($email) == trim($new_email)) {
					$boolean = true;
				}
				//echo $username . $company . $mobile . $email . $introduction;
			} 
			fclose($fp); 
			return $boolean;
		}
	}
}

?>
</body>
</html>
