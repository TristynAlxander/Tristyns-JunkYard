function loadMathToNode(math_node, math_url){																					// Load math_node from MathURL
	
	
	var xml_http;																											//
	if(window.XMLHttpRequest){xml_http = new XMLHttpRequest();} else {xml_http = new ActiveXObject("Microsoft.XMLHTTP");}		// XML Request
	xml_http.onreadystatechange = function(){if(xml_http.readyState == 4 && xml_http.status == 200){								//
																																//
		var is_derivation = math_url.length > 15 && math_url.substr(math_url.length-14,14) === "derivation.eqn";					//
		// Make & Append Math																									// Make & Append Math
		var math_box = parseMath(xml_http,is_derivation);									//
		math_node.appendChild(math_box);																								//
																																	//
		}};																														//
	xml_http.open("GET", math_url, true);																						//
	xml_http.send();																											//
	}																														//

function parseMath(xml_http,is_derivation){																								// Verify Equation Version
	var equation_xml = xml_http.responseXML.documentElement;																			//
	if(equation_xml.getAttribute("version") === "1.0"){return parseMathV1(xml_http,is_derivation);}												// Parse for proper version. 
	}																															//

function parseMathV1(xml_http,is_derivation){																				// Version 1 Parser
																																//
	equation_xml = xml_http.responseXML.documentElement;																				// Get Doc Element: Equation.
																																//
	//<table class="math_box">																										// Make Table (see left)
	var math_box = document.createElement("table");																					//
	if(is_derivation){math_box.setAttribute("class", "math_box left_align");}															// 
	else{math_box.setAttribute("class", "math_box");}																					//
	math_box.style.display = "inline-table";																							//
	
	make_header();
	make_body();
	
	function make_header(){
		//<thead><tr><td colspan=6 id="mathTitle">	MathTitle	</td></tr></thead>													// Make Table Head (see left)
		//<thead>																														// Make Head Element (see left)
		var table_head = document.createElement("thead");																					//
		math_box.appendChild(table_head);																									//
																																			//
		//<tr>																															// Make Table Row  (see left)
		var table_row_head = document.createElement("tr");																					//
		table_head.appendChild(table_row_head);																								//
																																			//
		//<td colspan=6 id="mathTitle">																									// Make Table Down  (see left)
		var table_down_head = document.createElement("td");																					//
		table_down_head.setAttribute("class", "math_title");																				//
		table_down_head.setAttribute("colspan", "6");																						//
		table_row_head.appendChild(table_down_head);																						//
																																			//
		// Txt Node																														// Make Text Node
		var math_title = document.createTextNode(equation_xml.getAttribute("name"));														//
		table_down_head.appendChild(math_title);																							//
		}
	
	function make_body(){
		//<tbody><tr><td colspan=6 id="LateX">		LaTeX		</td></tr></tbody>													// Make LateX Display (see left)
		//<tbody>																														// Make Table Body (see left)
		var table_body = document.createElement("tbody");																						//
		math_box.appendChild(table_body);																											//
																																			//
		//<tr>																															// Make Table Row (see left)
		var table_row_body = document.createElement("tr");																							//
		table_body.appendChild(table_row_body);																											//
																																			//
		//<td colspan=6 id="LateX">																										// Make Table Down (see left)
		var table_down_body = document.createElement("td");																							//
		if(is_derivation){table_down_body.setAttribute("class", "LateX tex2jax_ignore");}														// MathJax ignores these
		else{table_down_body.setAttribute("class", "LateX");}																						//
		table_down_body.setAttribute("colspan", "6");																								//
		table_row_body.appendChild(table_down_body);																											//
																																			//
		// MathJax Txt Node																												// Make MathJax Compatible Txt Node. 
		var math_latex_str = "";																												// Empty String
		latex_list = equation_xml.getElementsByTagName("LaTeX");																					// Get all LaTeX
		for(var i=0; i<latex_list.length;i++){																								// Add LaTex
			if(math_latex_str === ""){math_latex_str = latex_list[i].childNodes[0].nodeValue;}														// if empty, no break space
			else{math_latex_str = math_latex_str +"\\" + latex_list[i].childNodes[0].nodeValue;}													// else, separate with break space 
			}																																	//
		math_latex_str="\\["+math_latex_str+"\\]";																								// Declare LaTeX Environment
		var math_latex = document.createTextNode(math_latex_str);																				// Create TxtNode
		table_down_body.appendChild(math_latex);																										// Append Txt Node

		}

	



	// Create Table Footer for Variables																						// Create Table Footer for Variables (see below)
	//<tfoot class="VarArea">
	//		<tr class="label_row">	<td><span class="symbol">Symbols</span><input type="checkbox" title="Symbols"></td>		<td><span class="math_object">Math&nbsp;Objects</span><input type="checkbox" title="Math Objects"></td>	<td><span class="unit">Unit</span><input type="checkbox" title="Units"></td>	<td>Variable&nbsp;Names<input type="checkbox"></td>		</tr>
	//		<tr class="">			<td>					 Symbols						  					  </td>		<td>						 Math      Objects													 </td>	<td>				   Units										   </td>	<td>Variable&nbsp;Names						  </td>		</tr>
	//		...
	//</tfoot class="VarArea">
																																	//
	// <tfoot class="VarArea">																										// Make Footer (see left)
	var table_foot = document.createElement("tfoot");																						//
	table_foot.setAttribute("class", "VarArea");																								//
	math_box.appendChild(table_foot);																											//
																																		//
																																		//
		make_lable_row();
		make_var_rows();
		make_assumption_footer();
		make_var_collapser();
	
	function make_lable_row(){
		// <tr class="label_row">																											// Make Title Row (first row)
		var table_row_foot_label = document.createElement("tr");																							//
		table_row_foot_label.setAttribute("class", "label_row");																							//
		table_row_foot_label.style.display = "none";																										// default display = none
		table_foot.appendChild(table_row_foot_label);																											//
		
		make_symbol_column();
		make_math_object_column();
		make_unit_column();
		make_name_column();
		
		function make_symbol_column(){
			// <td><span class="symbol">Symbols</span><input type="checkbox" title="Symbols"></td>													// Make Symbol Column (see left)
			var table_down_foot_symbol = document.createElement("td");																								//
			table_row_foot_label.appendChild(table_down_foot_symbol);																											//
																																						//
			// <span class="symbol">Symbols</span>																										// Make Symbol Span  (see left)
			var span_symbol = document.createElement("span");																									//
			span_symbol.setAttribute("class","symbol");																										//
			table_down_foot_symbol.appendChild(span_symbol);																												//
			// Make Text node																																// Make Text Node
			var text_node_symbol = document.createTextNode("Symbol");																									// 
			span_symbol.appendChild(text_node_symbol);																													//
																																								// 
			// <input type="checkbox" title="Symbols">																									// Make Checkbox (see left)
			var input_symbol = document.createElement("input");																									//
			input_symbol.setAttribute("type","checkbox");																											//
			input_symbol.checked = true;																															// default checked
			input_symbol.setAttribute("title","Symbols");																											//
			input_symbol.addEventListener("click"   , function(){ShowHideCheckbox(this,"symbol")}, false);															// Show Hide Listener
			table_down_foot_symbol.appendChild(input_symbol);																													//
			}
		
		function make_math_object_column(){
			// <td><span class="math_object">Math&nbsp;Objects</span><input type="checkbox" title="Math Objects"></td>								// Make Math Object Column (see left)
			var table_down_math_object = document.createElement("td");																								//
			table_row_foot_label.appendChild(table_down_math_object);																											//
																																						//
			// <span class="math_object">Math&nbsp;Objects</span>																						// Make MathObject span (see left)
			var span_math_object = document.createElement("span");																									//
			span_math_object.setAttribute("class","math_object");																									//
			table_down_math_object.appendChild(span_math_object);																													//
			// Make Text Node																																// Make Text Node
			var text_node_math_object = document.createTextNode("Math\u00A0Object");																						//
			span_math_object.appendChild(text_node_math_object);																													//
																																								//
			// <input type="checkbox" title="Math Objects">																								// Make Checkbox (see left)
			var input_math_object = document.createElement("input");																										//
			input_math_object.setAttribute("type","checkbox");																											//
			input_math_object.checked = false;																															// default unchecked
			input_math_object.setAttribute("title","Math Objects");																										//
			input_math_object.addEventListener("click", function(){ShowHideCheckbox(this,"math_object")}, false);														// Show Hide Listener
			table_down_math_object.appendChild(input_math_object);																														//
			}
		
		function make_unit_column(){
			// <td><span class="unit">Unit</span><input type="checkbox" title="Units"></td>															// Make Unite Column (see left)
			var table_down_unit = document.createElement("td");																									//
			table_row_foot_label.appendChild(table_down_unit);																											//
																																						//
			// <span class="unit">Unit</span>																											// Make Unit Span (see left)
			var span_unit = document.createElement("span");																									//
			span_unit.setAttribute("class","unit");																											//
			table_down_unit.appendChild(span_unit);																													//
			// Make Text Node																																// Make Text Node
			var text_node_unit = document.createTextNode("Unit");																										//
			span_unit.appendChild(text_node_unit);																														//
																																								//
			// <input type="checkbox" title="Units">																									// Make Checkbox (see left)
			var input_unit = document.createElement("input");																										//
			input_unit.setAttribute("type","checkbox");																											//
			input_unit.checked = true;																																// default checked
			input_unit.setAttribute("title","Units");																												//
			input_unit.addEventListener("click", function(){ShowHideCheckbox(this,"unit")}, false);																// Show Hide Listener
			table_down_unit.appendChild(input_unit);																														//
			
			}
		
		function make_name_column(){
			//<td>Variable&nbsp;Names<input type="checkbox"></td>
			var table_down_name = document.createElement("td");
			table_row_foot_label.appendChild(table_down_name);
			
			//Span
			var span_name = document.createElement("span");
			span_name.setAttribute("class","VarName");
			table_down_name.appendChild(span_name);
			var text_node_name = document.createTextNode("Variable\u00A0Name");
			span_name.appendChild(text_node_name);
			
			//<input type="checkbox">
			var input_name = document.createElement("input");
			input_name.setAttribute("type","checkbox");
			input_name.setAttribute("title","Variable Names");
			input_name.addEventListener("click"   , function(){ShowHideCheckbox(this,"VarName")}, false);
			input_name.checked = true;
			table_down_name.appendChild(input_name);
			}
		
		}
	
	function make_var_rows(){
		//<tr class="Var">
		var_list = equation_xml.getElementsByTagName("Variables")[0].getElementsByTagName("Var");
		for(var i=0;i<var_list.length;i++){
			
			//<tr class="Var">
			var table_row_var = document.createElement("tr");
			table_row_var.setAttribute("class", "Var");
			table_foot.appendChild(table_row_var);
				
			//<td><span>\( symbol \)</span></td>
			var TDVarSym = document.createElement("td");
			TDVarSym.setAttribute("class","popUp_Trigger");
			table_row_var.appendChild(TDVarSym);
			var SPVarSym = document.createElement("span");
			SPVarSym.setAttribute("class","symbol");
			TDVarSym.appendChild(SPVarSym);
			
			var VarSymStrArray = var_list[i].getAttribute("symbol").split(", ")
			var VarSymStr = document.createTextNode("\\("+VarSymStrArray[0]+"\\)");
			if(VarSymStrArray.length > 1){
				TDVarSym.setAttribute("class","popUp_Trigger");
				var AltVarTable = document.createElement("table");
				AltVarTable.setAttribute("class","popUp_Content");
				TDVarSym.appendChild(AltVarTable);
				for(var j=1; j<VarSymStrArray.length; j++){
					var AltVarSymStr = document.createTextNode("\\("+VarSymStrArray[j]+"\\)");
					var AltVarTD     = document.createElement("td");
						AltVarTD.appendChild(AltVarSymStr);
					var AltVarTR     = document.createElement("tr");
						AltVarTR.appendChild(AltVarTD);
					AltVarTable.appendChild(AltVarTR);
					}
				}
			SPVarSym.appendChild(VarSymStr);
				
			//<td>math_object</td>
			var TDVarMO = document.createElement("td");
			table_row_var.appendChild(TDVarMO);
			var SPVarMO = document.createElement("span");
			SPVarMO.setAttribute("class","math_object");
			TDVarMO.appendChild(SPVarMO);
			
			var VarMOStr = document.createTextNode(var_list[i].getAttribute("math_object").replace(/ /g,"\u00A0"));			// To do Remove RegEx
			SPVarMO.appendChild(VarMOStr);
				
			//<td>unit</td>
			var TDVarU = document.createElement("td");
			table_row_var.appendChild(TDVarU);
			var SPVarU = document.createElement("span");
			SPVarU.setAttribute("class","unit");
			TDVarU.appendChild(SPVarU);
			
			var VarUStrArray = var_list[i].getAttribute("unit").split(", ")
			var VarUStr = document.createTextNode("\\("+VarUStrArray[0]+"\\)");
			if(VarUStrArray.length > 1){
				TDVarU.setAttribute("class","popUp_Trigger");
				var AltVarTable = document.createElement("table");
				AltVarTable.setAttribute("class","popUp_Content");
				TDVarU.appendChild(AltVarTable);
				for(var j=1; j<VarUStrArray.length; j++){
					var AltVarSymStr = document.createTextNode("\\("+VarUStrArray[j]+"\\)");
					var AltVarTD     = document.createElement("td");
						AltVarTD.appendChild(AltVarSymStr);
					var AltVarTR     = document.createElement("tr");
						AltVarTR.appendChild(AltVarTD);
					AltVarTable.appendChild(AltVarTR);
					}
				}
			SPVarU.appendChild(VarUStr);
			
			//<td>name</td>
			var TDVarName = document.createElement("td");
			table_row_var.appendChild(TDVarName);
			var SPVarName = document.createElement("span");
			SPVarName.setAttribute("class","VarName");
			TDVarName.appendChild(SPVarName);
			
			var VarNameStrArray = var_list[i].getAttribute("name").split(", ")
			var VarNameStr = document.createTextNode(VarNameStrArray[0].replace(/ /g,"\u00A0"));						// To do Remove RegEx
			if(VarNameStrArray.length > 1){
				TDVarName.setAttribute("class","popUp_Trigger");
				var AltVarTable = document.createElement("table");
				AltVarTable.setAttribute("class","popUp_Content");
				TDVarName.appendChild(AltVarTable);
				for(var j=1; j<VarNameStrArray.length; j++){
					var AltVarSymStr = document.createTextNode(VarNameStrArray[j].replace(/ /g,"\u00A0"));				// To do Remove RegEx
					var AltVarTD     = document.createElement("td");
						AltVarTD.appendChild(AltVarSymStr);
					var AltVarTR     = document.createElement("tr");
						AltVarTR.appendChild(AltVarTD);
					AltVarTable.appendChild(AltVarTR);
					}
				}
			
			SPVarName.appendChild(VarNameStr);
				
			}
		}
	
	function make_assumption_footer(){
		assumption_list = equation_xml.getElementsByTagName("Assumptions")[0].getElementsByTagName("Ass");
		for(var i=0;i<assumption_list.length;i++){
			
			//TR
			var table_row_ass = document.createElement("tr");
			table_row_ass.setAttribute("class", "Ass");
			table_row_ass.setAttribute("colspan", "4");
			table_foot.appendChild(table_row_ass);
			
			//TD
			var table_down_ass = document.createElement("td");
			table_down_ass.setAttribute("colspan", "4");
			table_row_ass.appendChild(table_down_ass);
			
			//Bold
			var bold_ass = document.createElement("b");
			table_down_ass.appendChild(bold_ass);
			
			assumption_number_str="Assumption "+(i+1)+": ";
			var text_node_ass_num = document.createTextNode(assumption_number_str);
			bold_ass.appendChild(text_node_ass_num);
			
			
			var text_node_ass = document.createTextNode(assumption_list[i].getAttribute("text"));
			table_down_ass.appendChild(text_node_ass);
			
			}
		}
	
	function make_var_collapser(){
		//<tr class="Collapser">
		var TRfootCollapser = document.createElement("tr");
		TRfootCollapser.setAttribute("class", "Collapser");
		TRfootCollapser.addEventListener("click"   , function(){collapseVariables(this)}, false);
		table_foot.appendChild(TRfootCollapser);
		//<td>
		var TDfootCollapser = document.createElement("td");
		TDfootCollapser.setAttribute("colspan", "4");
		TRfootCollapser.appendChild(TDfootCollapser);
		//Text
		var collapserText = document.createTextNode("\u21F2");
		TDfootCollapser.appendChild(collapserText);
		}
		
	return math_box;
	}
function collapseVariables(tr){
	var footer = tr.parentNode;
	var var_list = footer.getElementsByClassName("Var");
	var assumption_list = footer.getElementsByClassName("Ass");
	var label_row = footer.getElementsByClassName("label_row")[0];
	if(label_row.style.display === "none"){
		label_row.style.display = "table-row";
		for(var i=0;i<var_list.length;i++){
			var_list[i].style.display = "table-row";
			}
		for(var i=0;i<assumption_list.length;i++){
			assumption_list[i].style.display = "table-row";
			}
		}
	else{
		label_row.style.display = "none";
		for(var i=0;i<var_list.length;i++){
			var_list[i].style.display = "none";
			}
		for(var i=0;i<assumption_list.length;i++){
			assumption_list[i].style.display = "none";
			}
		}
	}
function ShowHideCheckbox(input,myClass){
	myClassList = input.parentNode.parentNode.parentNode.getElementsByClassName(myClass);
	if(input.checked){	for(var i = 0; i<myClassList.length;i++){myClassList[i].style.display = "inline";}}
	else{				for(var i = 0; i<myClassList.length;i++){myClassList[i].style.display = "none";  }}
	}
