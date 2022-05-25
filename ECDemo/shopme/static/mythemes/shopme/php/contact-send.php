<?php 
	$user_email = "mail@companyname.com";
	
	if($_SERVER['REQUEST_METHOD'] == "POST"){

		extract($_POST);

		$name = htmlspecialchars($cf_name);
		$email = htmlspecialchars($cf_email);
		$message = htmlspecialchars($cf_message);
		$subject = isset($cf_subject) ? htmlspecialchars($cf_subject) : "ShopMe. Contact form";
		$cf_order_number = !empty($cf_order_number) ? 'Order number: ' . htmlspecialchars($cf_order_number) . "\n" : '';
		$tmpName = $_FILES['cf_attachment']['tmp_name'];
		$fileType = $_FILES['cf_attachment']['type'];
		$fileName = $_FILES['cf_attachment']['name'];
	
		if ($_FILES && file($tmpName)) { 

		  $file = fopen($tmpName,'rb'); 
		  $data = fread($file,filesize($tmpName)); 
		  fclose($file); 
		 
		  $randomVal = md5(time()); 
		  $mimeBoundary = "==Multipart_Boundary_x{$randomVal}x"; 
		 
		  $headers = "\nMIME-Version: 1.0\n"; 
		  $headers .= "Content-Type: multipart/mixed;\n" ;
		  $headers .= " boundary=\"{$mimeBoundary}\""; 
		 
		  $message = "This is a multi-part message in MIME format.\n\n" . 
		  "--{$mimeBoundary}\n" . 
		  "Content-Type: text/plain; charset=\"iso-8859-1\"\n" . 
		  "Content-Transfer-Encoding: 7bit\n\n" . 
		  $message . "\n\n"; 
		 
		  $data = chunk_split(base64_encode($data)); 
		 
		  $message .= "--{$mimeBoundary}\n" . 
		  "Content-Type: {$fileType};\n" . 
		  " name=\"{$fileName}\"\n" . 
		  "Content-Transfer-Encoding: base64\n\n" . 
		  $data . "\n\n" . 
		  "--{$mimeBoundary}--\n";
		}

		try{

			if(!filter_var($email, FILTER_VALIDATE_EMAIL)) throw new Exception("Your email address is incorrect!");

		}
		catch(Exception $e){

			echo $e->getMessage();
			die();

		}

		try{

			$headers .= 'From: shopme@example.com' . "\r\n" .
		   			 	'Reply-To: shopme@example.com' . "\r\n";
		   	$msg = "Name: $name\n$cf_order_number" . "Email address: $email\nMessage: $message";

			if(mail($user_email, $subject, $msg, $headers)) throw new Exception("Your message has been successfully sent!");
			else throw new Exception("Connection to server is failed!");

		}
		catch(Exception $e){

			echo $e->getMessage();

		}

	}
	
?>