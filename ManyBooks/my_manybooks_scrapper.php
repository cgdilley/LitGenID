<?php
	
	$consolidated = "";	//this will contain the consolidated data
	$from = (isset($_GET['from'])) ? (int)$_GET['from'] : 1;	//starting page number
	$to = (isset($_GET['to'])) ? (int)$_GET['to'] : 5;			//ending page number
	if(isset($_GET['cat']))
		$category = $_GET['cat']."/";
	else
		die('Category not set!');
	//fetching data for all pages
	for($i = $from; $i <= $to ; $i++)
	{
		$url = "http://manybooks.net/categories/".$category.$i."/en";
		$output = file_get_contents($url);	//store the contents of the page in $output
		$strpos_begin = $strpos_end = 0;
		$consolidated .= $output;	//consolidating data of all pages together
		$consolidated .= '
';
	}
	
?>
<head>
	<script src="https://code.jquery.com/jquery-3.1.0.slim.min.js" > </script>
	<script type="text/javascript">
	//once our php script runs completely and has displayed the html on the page, we'll need to sanitize the data to display it according to our needs!
		$(document).ready(function (){
			
			
			var x = document.querySelectorAll("[class='table']");	//there is only one div on the page with the class "table", which lists all the books.
			var allinnerhtml = '';	//initializing our variable which will contain the final data
			for (var i=0;i<x.length;i++) {
				allinnerhtml += x[i].innerHTML;
			}
			allinnerhtml = allinnerhtml.trim();	//trimming out any extra spaces.
			
			allinnerhtml = allinnerhtml.replace(/\n/g, "<br>");		//replacing all new line characters with a break tag
			allinnerhtml = allinnerhtml.trim();	//trimming out any extra spaces.
			//since, we have replaced new line with the <br> tag, we now have consecutive <br> tags, let's replace them with a single <br> tag
			allinnerhtml = allinnerhtml.replace(/<br><br>/g, '<br>');	
			
			allinnerhtml = allinnerhtml.replace(/<br>/g, '||');	//replacing <br> tags with double pipe sign
			
			
			document.body.innerHTML = allinnerhtml;	//setting the document body with our sanitized variable - (more sanitization to be performed ahead)
			
			
			$('img').remove();	//remove all images
			$('em').remove();	//remove descriptions	-	the <em> element contained images of all the books
			allinnerhtml = document.body.innerHTML;		//now fetch the document's inner HTML and update our variable with it.
			
			//as long as we have four consecutive pipe signs in our data, replace them with double pipe signs, until all are replaced till end of document
			while(allinnerhtml.indexOf("||||") > -1)
				allinnerhtml = allinnerhtml.replace("||||", '||');
			
			//as long as we have "||		" in our data, replace it with empty characters, until all are replaced till end of document
			while(allinnerhtml.indexOf("||		") > -1)
				allinnerhtml = allinnerhtml.replace("||		", '');
			
			document.body.innerHTML = allinnerhtml;		//replace the body with our further sanitized data
			
			var y = document.getElementsByTagName('a');		//fetching all anchor elements in our 'updated' document
			
			//running the loop for each anchor element.
			for (var i=0;i<y.length;i++) {
				
				var actualbookname = y[i].innerHTML;	//this will be the actual book name - getting the innerHTML from the anchor element
				var booklink = y[i].getAttribute('href');	//fetching the link from the 'href' attribute of this anchor element
				var bookname_start = booklink.lastIndexOf('/');	//starting point reference for getting the book name (not the actual name, but the book reference used in all the links on the site)
				var bookname_end = booklink.lastIndexOf('.html'); //ending point reference for getting the book name (not the actual name, but the book reference used in all the links on the site)
				var bookname = booklink.substring(bookname_start + 1, bookname_end); //getting the reference book name (not the actual name, but the book reference used in all the links on the site)
				var link = 'http://manybooks.net/send/1:text:.txt:text/' + bookname + '/'+ bookname + '.txt'; //building the download link for the book
				//now finally, we replace this book with the data that WE want to display..
				//it will be displayed in the format	-	"BookName||BookDownloadLink||Author Name"
				$(y[i]).replaceWith( actualbookname + '||<a href="' + link + '">' + link + '</a>' ); 
				
			}
		});
	</script>
</head>
<body>
<?php
	echo $consolidated;	//this is the html of all the pages that php has strafed through - (unsanitized)
?>
</body>