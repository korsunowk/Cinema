$(document).ready(function(){

	function createMap(bilets, rowId, seatId){
		for (i=0;i<bilets.length-1;i++)
			{
				console.log(bilets[i]+'='+bilets[i].split(',')[0]+";"+bilets[i].split(',')[1])
				if (bilets[i].split(',')[0] == rowId && bilets[i].split(',')[1]== seatId)
					return true;
			}
		return false;
	}

	function getCookie(name) {
			  var cookieValue = null;
			  if (document.cookie && document.cookie != '') {
					var cookies = document.cookie.split(';');
			  for (var i = 0; i < cookies.length; i++) {
				   var cookie = jQuery.trim(cookies[i]);
			  // Does this cookie string begin with the name we want?
			  if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				  break;
				 }
			  }
		  }
	 return cookieValue;
	}

    $(".cssload-container").hide();
	var red_bilets = $('#red_bilet').val().split(';');
	var black_bilets = $('#black_bilet').val().split(';');
	a = 0;

	var csrftoken = getCookie('csrftoken');
	var bilets = new Array();

	var placeNumber = 1;
	var ryad = 1;
	var placesMap = new Array();
	var testStr='';

	for (rowId=1; rowId<10;rowId++)
	{
		for(seatId=1; seatId<16;seatId++)
		{
			if (createMap(red_bilets,rowId,seatId))
				testStr+="R";
			else if (createMap(black_bilets,rowId,seatId))
				testStr+="B";
			else
				testStr+='x';
		}
		placesMap.push(testStr);
		testStr='';
	}

	for (rowId in placesMap) {
		var row = document.createElement("tr");
		row.className = "image_center";
	    for (place in placesMap[rowId]) {
			btn = document.createElement("button"); 
			btn.className = "placeButton";
		if (placesMap[rowId][place] == 'x') {
			btn.innerHTML = placeNumber++;
			if (placeNumber == 16) placeNumber = 1;
		}
		else if (placesMap[rowId][place] == 'R'){
			btn.innerHTML = placeNumber++;
			btn.className = "blackButton";
			if (placeNumber == 16) placeNumber = 1;

		}
		else if (placesMap[rowId][place] == 'B'){
			btn.innerHTML = placeNumber++;
			btn.className = "blackButton";
			if (placeNumber == 16) placeNumber = 1;

		}
		else {
		    btn.style.visibility = "hidden";
		 }
		btn.id = ryad;
		row.appendChild(btn);    
	   }
	ryad++;
	$("#myzal").append(row);
	 }

    var placeNumber = 1;
	var placesMap2 = new Array();

	var idealMap = "x-xx-xx-xx-xx-x";
	var placesssssss = ['1','0','2','3','0','4','5','0','6','7','0','8','9','0','10'];

	for(seatId=0; seatId<15;seatId++)
	{

		if (idealMap[seatId]=='-')
		{
			testStr+='-';
		}
		else if (createMap(red_bilets,'10',placesssssss[seatId]))
		{
			testStr+="R";
		}

		else if (createMap(black_bilets,'10',placesssssss[seatId]))
		{
			testStr+="B";
		}
		else
		{
			testStr+='x';
		}

	}
	placesMap2.push(testStr);

	for (rowId in placesMap2) {
		var row = document.createElement("tr");
		row.className = "image_center";
	    for (place in placesMap2[rowId]) {
			btn = document.createElement("button");
			btn.className = "placeButton2";

		if (placesMap2[rowId][place] == 'x') {
			btn.innerHTML = placeNumber++;
		}
		else if (placesMap2[rowId][place] == 'R'){
			btn.innerHTML = placeNumber++;
			btn.className = "blackButton";
		}
		else if (placesMap2[rowId][place] == 'B'){
			btn.innerHTML = placeNumber++;
			btn.className = "blackButton";

		}
		else {
		    btn.style.visibility = "hidden";
		 }
		btn.id =  10;
		row.appendChild(btn);
	   }
		$("#vipzal").append(row);
	}

	$(".placeButton,.placeButton2").click(function(){
		placeColor = $(this).css('backgroundColor');
		
		if (placeColor != 'rgb(255, 0, 0)')
		{
			$(this).css("background","red");
			ryad = $(this).attr('id');
			mesto = $(this).html();
			if ($(this).attr('class') == 'placeButton')
				price = $("#hid1").attr('value');
			else 
				price = $("#hid2").attr('value');
			
			if (a<13)
			{			
				$(".korzina").append('<tr><td class="ryad_td">Ряд: '+ryad+', Место: '+mesto+'</td><td class="second_td2">'+price+' грн.</td></tr>');
				bilets.push(ryad+":"+mesto+":"+price);
			}
			else 
				alert('За раз можно купить максимум 10 билетов.');
			a+=1;
			summa = $("#summa").html();
			
			$("#summa").html(Number(summa) + Number(price));
		}
	});
	
	$("#cancel").click(function(){
		bilets = new Array();
		location.reload()
	});

	$('.buy_false').click(function(){
		alert('Для покупки билета авторизируйтесь на сайте.')
	});

	$('.buy').click(test_buy);
	function test_buy() {
		if (confirm('Вы уверены?'))
		{
            $(".cssload-container").show();
			var my_bilets ='';
			for(i=0;i<bilets.length;i++)
			{
				my_bilets+=bilets[i] +',';
			}
			$.ajax({
				type: "POST",
				url: "/buy/seans/seans_id="+$("#seans_id").val()+'/',
					csrfmiddlewaretoken : csrftoken,
				data:{
					tikets: my_bilets,
					usluga: 'buy',
					seans_id: $("#seans_id").val(),
				},
				dataType: "html",
				cache: false,
				success: function(data){
					if (data == 'ok'){
                        $(".cssload-container").hide();
						location.reload();
						alert("Покупка прошла успешно.");
					}
				}
		   });
		}

	}

	$('.bron').click(test_bron);
	function test_bron() {
		if (confirm('Вы уверены?'))
		{
			$(".cssload-container").show();
			var my_bilets ='';
			for(i=0;i<bilets.length;i++)
			{
				my_bilets+=bilets[i] +',';
			}
			$.ajax({
				type: "POST",
				url: "/buy/seans/seans_id="+$("#seans_id").val()+'/',
				data:{
					csrfmiddlewaretoken : csrftoken,
					tikets: my_bilets,
					usluga: 'bron',
					seans_id: $("#seans_id").val(),
				},
				dataType: "html",
				cache: false,
				success: function(data){
					if (data == 'ok'){
						$(".cssload-container").hide();
						location.reload();
						alert("Бронирование прошло успешно.");
					}
				}
		   });
		}

	}
	$('.bron_false').click(function(){
		alert('Для бронирования билета авторизируйтесь на сайте.')
	});
});


