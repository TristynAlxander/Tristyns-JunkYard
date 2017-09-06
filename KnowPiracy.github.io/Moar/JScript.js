
//Show Hide
function SHIDb(id){var element = document.getElementById(id); if(element.style.display == 'none'){element.style.display = 'block';} else{element.style.display = 'none';}}
function SHIDi(id){var element = document.getElementById(id); if(element.style.display == 'none'){element.style.display = 'inline';} else{element.style.display = 'none';}}
function SHIDt(id){var element = document.getElementById(id); if(element.style.display == 'none'){element.style.display = 'table';} else{element.style.display = 'none';}}
function SHCi(ClassName) {var elementArray = document.getElementsByClassName(ClassName); var i; for(i=0;i<elementArray.length;i++){if (elementArray[i].style.display  == "none"){elementArray[i].style.display  = "inline";} else{elementArray[i].style.display  = "none";}}}
function SHCb(ClassName) {var elementArray = document.getElementsByClassName(ClassName); var i; for(i=0;i<elementArray.length;i++){if (elementArray[i].style.display  == "none"){elementArray[i].style.display  = "block";} else{elementArray[i].style.display  = "none";}}}
function altSHb(id1,id2){var element1 = document.getElementById(id1); var element2 = document.getElementById(id2); if(element1.style.display == 'none' && element2.style.display == 'block'){element1.style.display = 'block';element2.style.display = 'none'} else{element1.style.display = 'none'; element2.style.display = 'block';}}

function altSHi(id1,id2){var element1 = document.getElementById(id1); var element2 = document.getElementById(id2); if(element1.style.display == 'none' && element2.style.display == 'inline'){element1.style.display = 'inline';element2.style.display = 'none'} else{element1.style.display = 'none'; element2.style.display = 'inline';}}
function SHIDbCheck(HideID,CheckID){var HideElement = document.getElementById(HideID); var CheckElement = document.getElementById(CheckID); if(CheckElement.checked){HideElement.style.display = 'block';} else{HideElement.style.display = 'none';}}
function SHCbCheck(HideClass,CheckID){var CheckElement = document.getElementById(CheckID);var HideElements = document.getElementsByClassName(HideClass); var i; for(i=0; i<HideElements.length; i=i+1){if(CheckElement.checked){HideElements[i].style.display = 'block';} else{HideElements[i].style.display = 'none';}}}
function SHIDiCheck(HideID,CheckID){var HideElement = document.getElementById(HideID); var CheckElement = document.getElementById(CheckID); if(CheckElement.checked){HideElement.style.display = 'inline';} else{HideElement.style.display = 'none';}}
function SHCiCheck(HideClass,CheckID){var CheckElement = document.getElementById(CheckID);var HideElements = document.getElementsByClassName(HideClass); var i; for(i=0; i<HideElements.length; i=i+1){if(CheckElement.checked){HideElements[i].style.display = 'inline';} else{HideElements[i].style.display = 'none';}}}
function SHbNext(CurrentElement){var next = CurrentElement.nextElementSibling;if(next.style.display == 'none'){next.style.display = 'block';}else{next.style.display = 'none';}}
function SHiNext(CurrentElement){var next = CurrentElement.nextElementSibling;if(next.style.display == 'none'){next.style.display = 'inline';}else{next.style.display = 'none';}}
function SHbPNext(CurrentElement){var next = CurrentElement.parentNode.nextElementSibling;if(next.style.display == 'none'){next.style.display = 'block';}else{next.style.display = 'none';}}
function SHiPNext(CurrentElement){var next = CurrentElement.parentNode.nextElementSibling;if(next.style.display == 'none'){next.style.display = 'inline';}else{next.style.display = 'none';}}
// CheckBoks
function UncheckC(ClassName){var elementArray = document.getElementsByClassName(ClassName); var i; for(var i=0;i<elementArray.length;i++){elementArray[i].checked = false;}}
function CheckID(id){document.getElementById(id).checked= true;}
function UncheckID(id){document.getElementById(id).checked = false;}

/* Other  */	/* Other  */	/* Other  */	/* Other  */	/* Other  */	/* Other  */
//Src
	function Src(id,html){document.getElementById(id).setAttribute("src",html);}
	/*MathJax Dependent*/ 
	function SrcAll(SrcImg,SrcMath,str){
		var imgNode=document.getElementById(SrcImg);
		var mathNode=document.getElementById(SrcMath);
			if(str.indexOf("$$") == 0 && str.lastIndexOf("$$") == str.length - 2){
				mathNode.innerHTML = str;
				mathNode.style.display = 'block';
				imgNode.style.display = 'none';
				MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
				}
			else{
				Src(SrcImg,str);
				imgNode.style.display = 'block';
				mathNode.style.display = 'none';
			}
		}
// onKeyPress
	function Enter(event){var keyCode = event.which || event.keyCode;if (keyCode == 13){return true;} else return false;}
//ENTITIES		Note: document.body.innerHTML is supposedly a bad way to do this, so is onload
	function ProcessEntities(filename){var file = loadXMLDoc(filename);var ENTITYlist = file.getElementsByTagName("ENTITY");var i;for(i=0; i<ENTITYlist.length; i=i+1){var name = "&amp;" + ENTITYlist[i].getAttribute("name")+";";var content = ENTITYlist[i].childNodes[0].nodeValue;var regex = new RegExp(name,"g");document.body.innerHTML = document.body.innerHTML.replace( regex, content);}}
//Strings
	function isString(aString){return typeof aString == 'string';}
	function isEqualString(aString,bString){return new String(aString).valueOf() == new String(bString).valueOf()}
//Mobile (Note regex is supposedly a bad way to do this)
	function isMobile(){return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);}
//XMLDis
	function loadXMLDoc(filename){if (window.XMLHttpRequest){xhttp=new XMLHttpRequest();} else {xhttp=new ActiveXObject("Microsoft.XMLHTTP");} xhttp.open("GET",filename,false); xhttp.send(); return xhttp.responseXML;}
		
//This site Onclick
	function SetSNLink(){
		var x=document.getElementById("SNIn").value;
		var link=document.getElementById("SNLink");
		var AccArea=document.getElementById("BlankAccount");
		switch(x){
			case "Anime-Planet":	AccArea.setAttribute("title","For Anime");		link.setAttribute("onclick","");	link.setAttribute("href","http://www.anime-planet.com/users/TrystynAlxander");				break;
			case "Change":			AccArea.setAttribute("title","");				link.setAttribute("onclick","");	link.setAttribute("href","https://www.change.org/u/78285940");								break;
			case "Degreed":			AccArea.setAttribute("title","");				link.setAttribute("onclick","");	link.setAttribute("href","https://degreed.com/trystynalxander/");							break;
			case "DeviantArt":		AccArea.setAttribute("title","My Images");		link.setAttribute("onclick","");	link.setAttribute("href","http://trystynalxander.deviantart.com/");							break;
			case "Facebook":		AccArea.setAttribute("title","");				link.setAttribute("onclick","");	link.setAttribute("href","https://www.facebook.com/trystyn.alxander");						break;
			case "Flickr":			AccArea.setAttribute("title","");				link.setAttribute("onclick","");	link.setAttribute("href","https://www.flickr.com/people/133087115@N05");					break;
			case "GoodReads":		AccArea.setAttribute("title","For Quotes");		link.setAttribute("onclick","");	link.setAttribute("href","https://goodreads.com/TrystynAlxander");							break;
			case "Google+":			AccArea.setAttribute("title","");				link.setAttribute("onclick","");	link.setAttribute("href","https://plus.google.com/+TrystynAlxander_PoI");					break;
			case "Gist":			AccArea.setAttribute("title","");				link.setAttribute("onclick","");	link.setAttribute("href","https://gist.github.com/TristynAlxander/");						break;
			case "GitHub":			AccArea.setAttribute("title","");				link.setAttribute("onclick","");	link.setAttribute("href","https://github.com/TristynAlxander");								break;
			case "IMDb":			AccArea.setAttribute("title","For Media");		link.setAttribute("onclick","");	link.setAttribute("href","http://www.imdb.com/user/ur48157496/");							break;
			case "Imgur":			AccArea.setAttribute("title","My Memes");		link.setAttribute("onclick","");	link.setAttribute("href","http://trystynalxander.imgur.com");							break;
			case "Instructables":	AccArea.setAttribute("title","");				link.setAttribute("onclick","");	link.setAttribute("href","http://www.instructables.com/member/TrystynAlxander/");							break;
			case "Linkedin":		AccArea.setAttribute("title","");				link.setAttribute("onclick","");	link.setAttribute("href","http://www.linkedin.com/in/TristynAlxander");						break;
			case "Memrise":			AccArea.setAttribute("title","");				link.setAttribute("onclick","");	link.setAttribute("href","http://www.memrise.com/user/TrystynAlxander/");					break;
			case "Mendeley":		AccArea.setAttribute("title","");				link.setAttribute("onclick","");	link.setAttribute("href","https://www.mendeley.com/profiles/tristyn-alxander/");			break;
			case "Mozilla":			AccArea.setAttribute("title","");				link.setAttribute("onclick","");	link.setAttribute("href","https://addons.mozilla.org/en-US/firefox/user/TrystynAlxander/");	break;
			case "MySpace":			AccArea.setAttribute("title","");				link.setAttribute("onclick","");	link.setAttribute("href","https://myspace.com/trystyn.alxander");							break;
			case "Reddit":			AccArea.setAttribute("title","");				link.setAttribute("onclick","");	link.setAttribute("href","http://www.reddit.com/user/TrystynAlxander/");					break;
			case "SoundCloud":		AccArea.setAttribute("title","");				link.setAttribute("onclick","");	link.setAttribute("href","https://soundcloud.com/trystynalxander");							break;
			case "StumbleUpon":		AccArea.setAttribute("title","");				link.setAttribute("onclick","");	link.setAttribute("href","http://www.stumbleupon.com/stumbler/trystynalxander/");			break;
			case "Tumblr":			AccArea.setAttribute("title","");				link.setAttribute("onclick","");	link.setAttribute("href","https://www.tumblr.com/blog/trystynalxander");					break;
			case "Twitter":			AccArea.setAttribute("title","");				link.setAttribute("onclick","");	link.setAttribute("href","https://twitter.com/TrystynAlxander");							break;
			case "Wikipedia":		AccArea.setAttribute("title","");				link.setAttribute("onclick","");	link.setAttribute("href","https://en.wikipedia.org/wiki/User:TrystynAlxander");				break;
			case "Youtube":			AccArea.setAttribute("title","");				link.setAttribute("onclick","");	link.setAttribute("href","https://www.youtube.com/c/TrystynAlxander_PoI");					break;
			default: AccArea.setAttribute("title",""); link.setAttribute("onclick","document.getElementById('myframe').src='index.html'"); link.setAttribute("href",""); break;
		}
		}
	function startTime() {
		var now = new Date();
		var dead = new Date(2077,01,11,0,0,0);
		NDay = now.getYear()*365.242*24*60*60 + now.getMonth()*30.4368*24*60*60 + now.getDate()*24*60*60+now.getHours()*60*60+now.getMinutes()*60+now.getSeconds();
		DDay = dead.getYear()*365.242*24*60*60 + dead.getMonth()*30.4368*24*60*60 + dead.getDate()*24*60*60+dead.getHours()*60*60+dead.getMinutes()*60+dead.getSeconds();
		UDay = Math.round(DDay - NDay);
			document.getElementById('time').innerHTML = UDay;
			var t = setTimeout(function(){startTime()},500);
		}
	function Insignia(){
		var myframe = document.getElementById('myframe');
		var inframe = (myframe.contentWindow || myframe.contentDocument);
		if (inframe.document){inframe = inframe.document;} 
		var title = inframe.getElementsByTagName('title')[0].innerHTML; 
		
		var element1 = document.getElementById('Insignia'); 
		var element2 = document.getElementById('PirateInsignia'); 
		
		if(title.indexOf('Pirate') != -1){
			element1.style.display = 'none';
			element2.style.display = 'inline';}
		else{
			element1.style.display = 'inline';
			element2.style.display = 'none';
			}
		} 