//Show Hide
function SHIDb(id){var element = document.getElementById(id); if(element.style.display == 'none'){element.style.display = 'block';} else{element.style.display = 'none';}}
function SHIDi(id){var element = document.getElementById(id); if(element.style.display == 'none'){element.style.display = 'inline';} else{element.style.display = 'none';}}
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
//Strings
	function isString(aString){return typeof aString == 'string';}
	function isEqualString(aString,bString){return new String(aString).valueOf() == new String(bString).valueOf()}
//Mobile
	function isMobile(){return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);}
//XMLDis
	function loadXMLDoc(filename){if (window.XMLHttpRequest){xhttp=new XMLHttpRequest();} else {xhttp=new ActiveXObject("Microsoft.XMLHTTP");} xhttp.open("GET",filename,false); xhttp.send(); return xhttp.responseXML;}

function DecAsciiShiftCypherEnDecode(Shift,Str){
	if(Shift>0){Shift = Shift - Math.floor(Shift/255)*255;}
	if(Shift<0){Shift = Shift - Math.ceil(Shift/255)*255;}
	var StrInt; var newStr="";
	for(var i=0;i<Str.length;i++){
		StrInt = Str.charCodeAt(i) + Shift;
		if(StrInt>255){StrInt=StrInt-255;}
		if(StrInt<0){StrInt=StrInt+255;}
		newStr = newStr+String.fromCharCode(StrInt)
		}
	return newStr;
	}



//This Site
var XMLView="XMLView.html";
var XMLListing="XMLListing.html";
var XMLGenerator="XMLGenerator.html";

function AssignRefArray(xmlFile){return loadXMLDoc(xmlFile).getElementsByTagName("Ref");}
function GetRef(){
	var Num;
	if(document.getElementById("NumIdIn").value.indexOf("/") != -1){Num = parseInt(document.getElementById("NumIdIn").value.substring(0,document.getElementById("NumIdIn").value.indexOf("/")),"10")-1;}
	else{Num = parseInt(document.getElementById("NumIdIn").value,"10")-1;}
	return AssignRefArray(document.getElementById("URLIdIn").value)[Num];
	}


var TrElementNotes;
	function MoreNotes(){
		var noteArray = document.getElementsByClassName("note");
		var NextNum = parseInt(noteArray[noteArray.length-1].parentNode.parentNode.getAttribute("id").substring(4),10)+1;
		NoteTrElement(NextNum);
		if(!isEqualString(noteArray[noteArray.length-1].value,"")){document.getElementById("NoteTable").appendChild(TrElementNotes);}
		}
	function DeleteNote(id){document.getElementById("NoteTable").removeChild(document.getElementById(id));}
	function NoteTrElement2(Value){
		var inputElement = TrElementNotes.childNodes[0].childNodes[0];
		var ValueAttribute = document.createAttribute("value");ValueAttribute.value =Value;inputElement.setAttributeNode(ValueAttribute);
		}
	function NoteTrElement(NextNum){
		TrElementNotes = document.createElement("tr");
			var idAttribute = document.createAttribute("id");
				idAttribute.value ="note"+NextNum;
				TrElementNotes.setAttributeNode(idAttribute);
			var TDElement = document.createElement("td");
				var inputElement = document.createElement("input");
					var ClassAttribute = document.createAttribute("class");
						ClassAttribute.value ="note";
						inputElement.setAttributeNode(ClassAttribute);
					var OnChangeAttribute = document.createAttribute("onchange");
						OnChangeAttribute.value ="MoreNotes()";
						inputElement.setAttributeNode(OnChangeAttribute);
					var TypeAttribute = document.createAttribute("type");
						TypeAttribute.value ="text";
						inputElement.setAttributeNode(TypeAttribute);
					var PlaceHolderAttribute = document.createAttribute("placeholder");
						PlaceHolderAttribute.value ="Note detailing blah blah blah... ";
						inputElement.setAttributeNode(PlaceHolderAttribute);
					TDElement.appendChild(inputElement);
				TrElementNotes.appendChild(TDElement);	
			var TDElement2 = document.createElement("td");
				var aElement = document.createElement("a");
					var hrefAttribute = document.createAttribute("href");
					hrefAttribute.value ="#";
					aElement.setAttributeNode(hrefAttribute);
					var supElement = document.createElement("sup");
						var ClassAttribute2 = document.createAttribute("class");
							ClassAttribute2.value ="red";
							supElement.setAttributeNode(ClassAttribute2);
						var OnClickAttribute = document.createAttribute("onclick");
							OnClickAttribute.value ="DeleteNote("+"'"+"note"+NextNum+"'"+")";
							supElement.setAttributeNode(OnClickAttribute);
						var xText = document.createTextNode("\u2718");
							supElement.appendChild(xText);
						aElement.appendChild(supElement);
					TDElement2.appendChild(aElement);
				TrElementNotes.appendChild(TDElement2);	
		}

var SpanElementTags;
	function MoreTags(){
		var tagArray = document.getElementsByClassName("tag");
		var NextNum = parseInt(tagArray[tagArray.length-1].parentNode.getAttribute("id").substring(3),10)+1;
		TagSpanElement(NextNum)
		if(!isEqualString(tagArray[tagArray.length-1].value,"")){document.getElementById("TagDiv").appendChild(SpanElementTags);}
		}
	function DeleteTag(id){document.getElementById("TagDiv").removeChild(document.getElementById(id));}
	function TagSpanElement2(Value){
		var inputElement = SpanElementTags.childNodes[0];
		var ValueAttribute = document.createAttribute("value");ValueAttribute.value =Value;inputElement.setAttributeNode(ValueAttribute);
		}
	function TagSpanElement(NextNum){
		SpanElementTags = document.createElement("span");
			var idAttribute = document.createAttribute("id");
				idAttribute.value ="tag"+NextNum;
				SpanElementTags.setAttributeNode(idAttribute);
			var inputElement = document.createElement("input");
				var ClassAttribute = document.createAttribute("class");
					ClassAttribute.value ="tag";
					inputElement.setAttributeNode(ClassAttribute);
				var OnChangeAttribute = document.createAttribute("onchange");
					OnChangeAttribute.value ="MoreTags()";
					inputElement.setAttributeNode(OnChangeAttribute);
				var TypeAttribute = document.createAttribute("type"); 
					TypeAttribute.value ="text"; 
					inputElement.setAttributeNode(TypeAttribute);
				var PlaceHolderAttribute = document.createAttribute("placeholder");
					PlaceHolderAttribute.value ="+Tag";
					inputElement.setAttributeNode(PlaceHolderAttribute);
				SpanElementTags.appendChild(inputElement);
			var aElement = document.createElement("a");
				var hrefAttribute = document.createAttribute("href");
				hrefAttribute.value ="#";
				aElement.setAttributeNode(hrefAttribute);
				var supElement = document.createElement("sup");
					var ClassAttribute2 = document.createAttribute("class");
						ClassAttribute2.value ="red";
						supElement.setAttributeNode(ClassAttribute2);
					var OnClickAttribute = document.createAttribute("onclick");
						OnClickAttribute.value ="DeleteTag("+"'"+"tag"+NextNum+"'"+")";
						supElement.setAttributeNode(OnClickAttribute);
					var xText = document.createTextNode("\u2718"); 
						supElement.appendChild(xText); 
					aElement.appendChild(supElement);
				SpanElementTags.appendChild(aElement);
		}

var TrElementVars;
	function MoreVars(){
		var VarArray = document.getElementsByClassName("var");
		var VarExplanationArray = document.getElementsByClassName("varExp");
		var NextNum = parseInt(VarArray[VarArray.length-1].parentNode.parentNode.getAttribute("id").substring(3),10)+1;
		VarTrElement(NextNum)
		if((!isEqualString(VarArray[VarArray.length-1].value,"")) || (!isEqualString(VarExplanationArray[VarExplanationArray.length-1].value,"")) ){document.getElementById("VarTable").appendChild(TrElementVars);}
		}
	function DeleteVar(id){document.getElementById("VarTable").removeChild(document.getElementById(id));}
	function VarTrElement2p1(Value){
		var inputElement = TrElementVars.childNodes[0].childNodes[0];
		var ValueAttribute = document.createAttribute("value");ValueAttribute.value =Value;inputElement.setAttributeNode(ValueAttribute);
		}
	function VarTrElement2p2(Value){
		var inputElement = TrElementVars.childNodes[1].childNodes[0];
		var ValueAttribute = document.createAttribute("value");ValueAttribute.value =Value;inputElement.setAttributeNode(ValueAttribute);
		}
	function VarTrElement(NextNum){
		TrElementVars = document.createElement("tr");
			var idAttribute = document.createAttribute("id");
				idAttribute.value ="var"+NextNum;
				TrElementVars.setAttributeNode(idAttribute);
			var TDElement1 = document.createElement("td");
				var inputElement1 = document.createElement("input");
					var ClassAttribute1 = document.createAttribute("class");
						ClassAttribute1.value ="var";
						inputElement1.setAttributeNode(ClassAttribute1);
					var PlaceHolderAttribute1 = document.createAttribute("placeholder");
						PlaceHolderAttribute1.value ="V";
						inputElement1.setAttributeNode(PlaceHolderAttribute1);
					var OnChangeAttribute1 = document.createAttribute("onchange");
						OnChangeAttribute1.value ="MoreVars()";
						inputElement1.setAttributeNode(OnChangeAttribute1);
					var TypeAttribute1 = document.createAttribute("type");
						TypeAttribute1.value ="text";
						inputElement1.setAttributeNode(TypeAttribute1);
					TDElement1.appendChild(inputElement1);
				TrElementVars.appendChild(TDElement1);
			var TDElement2 = document.createElement("td");
				var inputElement2 = document.createElement("input");
					var ClassAttribute2 = document.createAttribute("class");
						ClassAttribute2.value ="varExp";
						inputElement2.setAttributeNode(ClassAttribute2);
					var PlaceHolderAttribute2 = document.createAttribute("placeholder");
						PlaceHolderAttribute2.value =" A measurement of blah blah blah...";
						inputElement2.setAttributeNode(PlaceHolderAttribute2);
					var OnChangeAttribute2 = document.createAttribute("onchange");
						OnChangeAttribute2.value ="MoreVars()";
						inputElement2.setAttributeNode(OnChangeAttribute2);
					var TypeAttribute2 = document.createAttribute("type");
						TypeAttribute2.value ="text";
						inputElement2.setAttributeNode(TypeAttribute2);
					TDElement2.appendChild(inputElement2);
				TrElementVars.appendChild(TDElement2);
				var TDElement3 = document.createElement("td");
					var aElement = document.createElement("a");
						var hrefAttribute = document.createAttribute("href");
						hrefAttribute.value ="#";
						aElement.setAttributeNode(hrefAttribute);
						var supElement = document.createElement("sup");
							var ClassAttribute3 = document.createAttribute("class");
								ClassAttribute3.value ="red";
								supElement.setAttributeNode(ClassAttribute3);
							var OnClickAttribute = document.createAttribute("onclick");
								OnClickAttribute.value ="DeleteVar("+"'"+"var"+NextNum+"'"+")";
								supElement.setAttributeNode(OnClickAttribute);
							var xText = document.createTextNode("\u2718");
								supElement.appendChild(xText); 
							aElement.appendChild(supElement);
						TDElement3.appendChild(aElement);
					TrElementVars.appendChild(TDElement3);
		}

function DTD(){return "<?xml version=\"1.0\"?>\n<!DOCTYPE Ref42 [\n<!ELEMENT Ref42 (Ref*)>\n<!ELEMENT Ref (Src,Var*,Notes*,Tags?)>\n<!ELEMENT Src EMPTY>\n<!ELEMENT Var (#PCDATA)>\n<!ELEMENT Notes (#PCDATA)>\n<!ELEMENT Tags (tag+)>\n<!ELEMENT tag (#PCDATA)>\n\n<!ATTLIST Ref title CDATA #IMPLIED>\n<!ATTLIST Src src CDATA #IMPLIED>\n<!ATTLIST Var id CDATA #REQUIRED>\n]>\n\n"}
function XMLGeneratorN(){
	
	var dtd = DTD();
	
	var title= '<Ref42>\n' + '\t<Ref title="'+document.getElementById("MainTitle").value.replace(/&/g,"&amp;").replace(/\"/g,"&#34;").replace(/\</g,"&#60;").replace(/\>/g,"&#62;")+'">\n'; 
	var img = '\t\t<Src src="'+document.getElementById("SrcIn").value.replace(/&/g,"&amp;").replace(/\"/g,"&#34;").replace(/\</g,"&#60;").replace(/\>/g,"&#62;")+'"/>\n';

	var VarArray = document.getElementsByClassName("var");
	var VarExArray = document.getElementsByClassName("varExp");
	var i; var vars="";
	for(i=0;i<VarArray.length;i=i+1){if( !isEqualString(VarArray[i].value,"") && !isEqualString(VarExArray[i].value,""))
		{vars = vars + '\t\t<Var id="'+VarArray[i].value.replace(/&/g,"&amp;").replace(/\"/g,"&#34;").replace(/\</g,"&#60;").replace(/\>/g,"&#62;")+'">'+VarExArray[i].value.replace(/&/g,"&amp;").replace(/\"/g,"&#34;").replace(/\</g,"&#60;").replace(/\>/g,"&#62;")+'</Var>\n';}}
	
	var noteArray = document.getElementsByClassName("note");
	var j; var notes=""; 
	for(j=0;j<noteArray.length;j=j+1){if(!isEqualString(noteArray[j].value,""))
		{notes = notes + '\t\t<Notes>'+noteArray[j].value.replace(/&/g,"&amp;").replace(/\"/g,"&#34;").replace(/\</g,"&#60;").replace(/\>/g,"&#62;")+'</Notes>\n';}}
	
	var tagArray = document.getElementsByClassName("tag");
	var k; var tags=""; 
	for(k=0;k<tagArray.length;k=k+1){if(!isEqualString(tagArray[k].value,"")){tags = tags + '\t\t\t<tag>'+tagArray[k].value.replace(/&/g,"&amp;").replace(/\"/g,"&#34;").replace(/\</g,"&#60;").replace(/\>/g,"&#62;")+'</tag>\n';}}
	
	var AllTags = '\t\t<Tags>\n'+tags+'\t\t</Tags>\n'+"\t</Ref>\n"+"</Ref42>";
	
	return (dtd+title+img+vars+notes+AllTags);
	}
function XMLGenerator1(){
	var dtd = DTD();
	
	var title= '<Ref42>\n' + '<Ref title="'+document.getElementById("MainTitle").value.replace(/&/g,"&amp;").replace(/\"/g,"&#34;").replace(/\</g,"&#60;").replace(/\>/g,"&#62;")+'">'; 
	var img = '<Src src="'+document.getElementById("SrcIn").value.replace(/&/g,"&amp;").replace(/\"/g,"&#34;").replace(/\</g,"&#60;").replace(/\>/g,"&#62;")+'"/>';
	
	var VarArray = document.getElementsByClassName("var");
	var VarExArray = document.getElementsByClassName("varExp");
	var i; var vars="";
	for(i=0;i<VarArray.length;i=i+1){if( !isEqualString(VarArray[i].value,"") && !isEqualString(VarExArray[i].value,""))
		{vars = vars + '<Var id="'+VarArray[i].value.replace(/&/g,"&amp;").replace(/\"/g,"&#34;").replace(/\</g,"&#60;").replace(/\>/g,"&#62;")+'">'+VarExArray[i].value.replace(/&/g,"&amp;").replace(/\"/g,"&#34;").replace(/\</g,"&#60;").replace(/\>/g,"&#62;")+'</Var>';}}
	
	var noteArray = document.getElementsByClassName("note");
	var j; var notes=""; 
	for(j=0;j<noteArray.length;j=j+1){if(!isEqualString(noteArray[j].value,""))
		{notes = notes + '<Notes>'+noteArray[j].value.replace(/&/g,"&amp;").replace(/\"/g,"&#34;").replace(/\</g,"&#60;").replace(/\>/g,"&#62;")+'</Notes>';}}
	
	var tagArray = document.getElementsByClassName("tag");
	var k; var tags=""; 
	for(k=0;k<tagArray.length;k=k+1){if(!isEqualString(tagArray[k].value,"")){tags = tags + '<tag>'+tagArray[k].value.replace(/&/g,"&amp;").replace(/\"/g,"&#34;").replace(/\</g,"&#60;").replace(/\>/g,"&#62;")+'</tag>';}}
	
	var AllTags = '<Tags>'+tags+'</Tags>'+"</Ref>\n"+"</Ref42>";
	
	return (dtd+title+img+vars+notes+AllTags);
	}

//LoadMore
function SetTitle(){document.getElementById("MainTitle").innerHTML = GetRef().getAttribute("title");}
function LoadTitle(){document.getElementById("MainTitle").value = GetRef().getAttribute("title");}


function SetSrc(){
	var nodeArray = GetRef().childNodes;var i; 
	for(i=0;i<nodeArray.length;i=i+1){if(isEqualString(nodeArray[i].nodeName,"Src")){break;}}
	var str = nodeArray[i].getAttribute("src");
	var imgNode=document.getElementById("SrcImg");
	SrcAll("SrcImg","SrcMath",str);
	}
function LoadSrc(){
	var nodeArray = GetRef().childNodes; var i; 
	for(i=0;i<nodeArray.length;i=i+1){if(isEqualString(nodeArray[i].nodeName,"Src")){break;}}
	document.getElementById('SrcIn').value = nodeArray[i].getAttribute("src");
	var str = nodeArray[i].getAttribute("src");
	SrcAll("SrcImg","SrcMath",str);
	}

function GetTags(){
	var nodeArray = GetRef().childNodes; var i; 
	for(i=0;i<nodeArray.length;i=i+1){if(isEqualString(nodeArray[i].nodeName,"Tags")){break;}}
	var NodeArrayOfTags = nodeArray[i].childNodes; 
	var j;var TagStrList=""; 
	for(j=0;j<NodeArrayOfTags.length;j=j+1){
		if(NodeArrayOfTags[j].nodeType==1){
			var TagName = NodeArrayOfTags[j].childNodes[0].nodeValue; 
			TagStrList=TagStrList+TagName +", ";
			}
		}
	document.getElementById("TagDiv").innerHTML = TagStrList;//This has to be appended!!
	}
function LoadTags(){
	var nodeArray = GetRef().childNodes; 
	var i; for(i=0;i<nodeArray.length;i=i+1){if(isEqualString(nodeArray[i].nodeName,"Tags")){break;}}
	var NodeArrayOfTags = nodeArray[i].childNodes; 
	var j; for(j=0;j<NodeArrayOfTags.length;j=j+1){
	if(NodeArrayOfTags[j].nodeType==1){
			var TagName = NodeArrayOfTags[j].childNodes[0].nodeValue; 
			var NextNum = parseInt(document.getElementsByClassName("tag")[document.getElementsByClassName("tag").length-1].parentNode.getAttribute("id").substring(3),10)+1;
			TagSpanElement(NextNum);TagSpanElement2(TagName);
			document.getElementById("TagDiv").appendChild(SpanElementTags);
			}
		}
	}

function GetVars(){
	var nodeArray = GetRef().childNodes; 
	var VarStrList=""; 
	var i; for(i=0;i<nodeArray.length;i=i+1){if(isEqualString(nodeArray[i].nodeName,"Var")){
		VarStrList=VarStrList+"<tr><td class=\"var\">"+nodeArray[i].getAttribute("id")+": </td>";
		VarStrList=VarStrList+"<td CLASS=\"varExp\">"+nodeArray[i].childNodes[0].nodeValue+"</td></tr>";
		}} 
	VarStrList="<table id=\"VarTable\" class=\"fat plrbox\"><tr><td colspan=2 class=\"MiniTitle\">&nbsp;Variables</td></tr>"+VarStrList+"</table>"; 
	return VarStrList;}
function LoadVars(){
	var nodeArray = GetRef().childNodes; 
	var i; for(i=0;i<nodeArray.length;i=i+1){if(isEqualString(nodeArray[i].nodeName,"Var")){
		var NextNum = parseInt(document.getElementsByClassName("Var")[document.getElementsByClassName("Var").length-1].parentNode.parentNode.getAttribute("id").substring(3),10)+1;
		var IdValue = nodeArray[i].getAttribute("id");
		var Value = nodeArray[i].childNodes[0].nodeValue;
		VarTrElement(NextNum);VarTrElement2p1(IdValue);VarTrElement2p2(Value);
		document.getElementById("VarTable").appendChild(TrElementVars);
	}}}

function GetNotes(){
	var NodeArrayOfRef = GetRef().childNodes;
	var NoteStrList=""; 
	var i; for(i=0;i<NodeArrayOfRef.length;i=i+1){if(isEqualString(NodeArrayOfRef[i].nodeName,"Notes")){
	NoteStrList=NoteStrList+"<tr><td class=\"note\">\u2022\u00A0"+NodeArrayOfRef[i].childNodes[0].nodeValue+"</td></tr>";
	}}
	NoteStrList="<table id=\"NoteTable\" class=\"fat plrbox\"><tr><td class=\"MiniTitle\">&nbsp;Notes</td></tr>"+NoteStrList+"</table>"; 
	return NoteStrList;}
function LoadNotes(){
	var nodeArray = GetRef().childNodes; 
	var i; for(i=0;i<nodeArray.length;i=i+1){if(isEqualString(nodeArray[i].nodeName,"Notes")){
	var NextNum = parseInt(document.getElementsByClassName("note")[document.getElementsByClassName("note").length-1].parentNode.parentNode.getAttribute("id").substring(4),10)+1;
	var Value = nodeArray[i].childNodes[0].nodeValue;
	NoteTrElement(NextNum); NoteTrElement2(Value);
	document.getElementById("NoteTable").appendChild(TrElementNotes);
	}}}

function GetVarNotes(){
	var VarsAndNotes="<tr><td>"+GetVars(); 
	if(isMobile()){VarsAndNotes=VarsAndNotes+"</td></tr><tr><td>";} 
	else {VarsAndNotes=VarsAndNotes+"</td><td>";}
	VarsAndNotes=VarsAndNotes+GetNotes(); 
	VarsAndNotes=VarsAndNotes+"</td></tr>";
	document.getElementById("VarNoteTable").innerHTML = VarsAndNotes;}

function XMLGetter(event){if(Enter(event)){SetTitle();SetSrc();GetTags();GetVarNotes();MathJax.Hub.Queue(['Typeset',MathJax.Hub]);}}
function XMLLoader(event){if(Enter(event)){LoadTitle(); LoadSrc(); LoadTags(); LoadVars();LoadNotes();}}

function refLister(){
	var xml = document.getElementById("URLIdIn").value;
	var refArray = AssignRefArray(xml);
	var i; for(i=0;i < refArray.length;i=i+1){
		var title=refArray[i].getAttribute("title");
		nodeArray = refArray[i].childNodes;  
		var j; for(j=0;j<nodeArray.length;j=j+1){if(isEqualString(nodeArray[j].nodeName,"Tags")){break;}}
		var NodeArrayOfTags = nodeArray[j].childNodes; 
		var k;var TagStrList=""; 
		for(k=0;k<NodeArrayOfTags.length;k=k+1){if(NodeArrayOfTags[k].nodeType==1){var TagName = NodeArrayOfTags[k].childNodes[0].nodeValue; TagStrList=TagStrList+TagName +", ";}}
		var TrElement = document.createElement("tr");
			var TDElement1 = document.createElement("td");
				var AElement = document.createElement("a")
					var LinkAttribute = document.createAttribute("href");
					LinkAttribute.value = XMLView+"?XML="+encodeURIComponent(xml)+"&Num="+i;
					AElement.setAttributeNode(LinkAttribute);
					var titleNode = document.createTextNode(title);
						AElement.appendChild(titleNode);
					TDElement1.appendChild(AElement);
				TrElement.appendChild(TDElement1);
				
			var TDElement2 = document.createElement("td");
				var tagNode = document.createTextNode(TagStrList);
					TDElement2.appendChild(tagNode);
				var ClassAttribute1 = document.createAttribute("class");
					ClassAttribute1.value ="tag";
					TDElement2.setAttributeNode(ClassAttribute1);
				TrElement.appendChild(TDElement2);
		
		document.getElementById("RefListTable").appendChild(TrElement);
		}}

function ViewOnLoad(){
	if(location.search.indexOf("?") != -1){
	var xml = decodeURIComponent(location.search.substring(location.search.indexOf("?XML=")+5,location.search.indexOf("&")));
	var Num = parseInt(location.search.substring(location.search.indexOf("&Num=")+5),10)+1;	
	document.getElementById("NumIdIn").value = Num;
	document.getElementById("URLIdIn").value = xml;
	SetTitle();SetSrc();GetTags();GetVarNotes();
	MathJax.Hub.Queue(['Typeset',MathJax.Hub]);
	}}
function ListOnLoad(){if(location.search.indexOf("?") != -1){
	var xml=location.search;
	
	if(xml.indexOf("&") != -1){
		var loc = decodeURIComponent(xml.substring(xml.indexOf("?XML=")+5,xml.indexOf("&")));
		document.getElementById("URLIdIn").value = loc;
		refLister();
		xml = xml.substring(xml.indexOf("&"));
		}
	else{
		var loc = decodeURIComponent(xml.substring(xml.indexOf("?XML=")+5));
		document.getElementById("URLIdIn").value = loc;
		refLister();
		xml="";
		}
	
	
	
	while(xml.indexOf("&") != -1){
		if(xml.indexOf("&",xml.indexOf("&")+1) != -1){
			loc = decodeURIComponent(xml.substring(xml.indexOf("&XML=")+5,xml.indexOf("&",xml.indexOf("&")+1)));
			document.getElementById("URLIdIn").value = loc;
			refLister();
			xml = xml.substring(xml.indexOf("&",xml.indexOf("&")+1));
			}
		else{
			loc = decodeURIComponent(xml.substring(xml.indexOf("&XML=")+5))
			document.getElementById("URLIdIn").value = loc;
			refLister();
			xml = "";
			}
		}
	}}

function LocToVal(element){
var input = element.nextElementSibling.children[0];
if(!input.value == ""){input.value="";}
else{input.value = input.getAttribute("placeholder");}
}

function OpenLink(){
	var XMLLocs = document.getElementsByClassName("XMLLocations");
	LinkAdd=""; var i; 
	for(i=0; i<XMLLocs.length;i=i+1){if(!isEqualString(XMLLocs[i].value,"")){LinkAdd=LinkAdd+"&XML="+XMLLocs[i].value;}}
	LinkAdd=LinkAdd.replace("&","?");
	var Link=XMLListing+LinkAdd;
	document.getElementById("xmlList").innerHTML="<a href=\""+Link+"\">[Listing]</a>";
	window.location=Link;
}

