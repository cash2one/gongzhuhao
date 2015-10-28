checkRegex = function(dest,pattern,notEmpty){
	if(dest.length == 0){
		return !notEmpty ? false : true;
	}
	return pattern.test(dest);
};

checkSpecialChar = function (str){
	var pattern = /[^A-Za-z0-9&,\-\._\*@\(\)\s\!\#\&\$\%\^\'\/]/;
	if(str == ""){
		return false;
	}
	
	if(str.search(pattern) != -1){
		return true;
	}
	
	return false;
	
}

getErrorMsg = function(width, item){
	if(width == 0){
		return "<div class='error'>" + item + "不能为空</div>";
	}
	
	return "<div class='error' style='width:" + width + "px;'>'" + item + "'不能为空</div>";
}

getErrorMsgClass = function(width, item, classs){
	var _error =  "<div class='error " + classs;
	if(width != 0) 
		_error += "' style='width:" + width + "px;'>" 
	_error += item + "不能为空</div>";
	return _error;
}

getNormalErrorMsg = function(width, item, message){
	if(width == 0)
  	return "<div class='error'>" + item + " " +  message +  "</div>";
  return "<div class='error' style='width:" + width+ "px;'>" + item + " " +  message +  "</div>";
}

checkField=function(field, notEmpty, fieldName, err, output){
	field = field.replace(/^\s+/,"").replace(/\s+$/,"");	
	if(field.length == 0){
		if(!notEmpty){
			if(output){
				var msg = "<div class='error'>" +fieldName + "不能为空</div>";
				err.after(msg);
			}
			return false;
		}else{
			return true;
		}
	}
	if(checkSpecialChar(field)){
		if(output){
			var msg = getErrorMsg(0, fieldName);
			err.after(msg);
		}
		return false;
	}
	return true;
}

checkPhone = function(phone, notEmpty){
	phone = phone.replace(/^\s+/,"").replace(/\s+$/,"");
	if(phone.length == 0){
		return !notEmpty ? false : true;
	}
	return checkRegex(phone,/^[+]{0,1}(\d){1,3}[ ]?([-]?((\d)|[ ]){1,12})+$/,notEmpty);
};

checkQQ = function(qq, notEmpty){
	qq = qq.replace(/^\s+/,"").replace(/\s+$/,"");
	if(qq.length == 0){
		return !notEmpty ? false : true;
	}
	return checkRegex(qq,/^\s*[.0-9]{5,11}\s*$/,notEmpty);
};


checkPwd = function(pwd, notEmpty){
	pwd = pwd.replace(/^\s+/,"").replace(/\s+$/,"");
	if(pwd.length == 0){
		return !notEmpty ? false : true;
	}
	return checkRegex(pwd,/^[a-zA-Z]\w{5,17}$/,notEmpty);
};

isNumber = function(num, notEmpty){
	num = num.replace(/^\s+/,"").replace(/\s+$/,"");
	if(num.length == 0){
		return !notEmpty ? false : true;
	}
	return checkRegex(num,/^[0-9]+$/,notEmpty);	
}
