<?php 
	$user_email = "mail@companyname.com";
	
	if($_SERVER['REQUEST_METHOD'] == "POST"){

		$email = htmlspecialchars($_POST['sc_email']);
		$subject = isset($sc_subject) ? htmlspecialchars($sc_subject) : "ShopMe. Newsletter";

		try{

			if(!filter_var($email, FILTER_VALIDATE_EMAIL)) throw new Exception("Your email address is incorrect!");

		}
		catch(Exception $e){

			echo $e->getMessage();
			die();
		}

		try{

			$headers = 'From: shopme@example.com' . "\r\n" .
		   			 	'Reply-To: shopme@example.com' . "\r\n";
		   	$msg = "Email address: $email";

			if(mail($user_email, $subject, $msg, $headers)) throw new Exception("Your email address has been successfully sent!");
			else throw new Exception("Connection to server is failed!");

		}
		catch(Exception $e){

			echo $e->getMessage();

		}

	}
	
?>