//****************************************************************************************
$(function(){
	//改变接口名字，获取到服务提供者与调用方法LIST
	jQuery("#interfaceName").change(refresh_alias);
	jQuery("#interfaceName").change(refresh_method);
	
});


function refresh_alias(){
	jQuery.ajax({ 
		type:"GET", 
		url:"jQuerselectyalias", 
		data:"interfaceName="+jQuery("#interfaceName").val(), 
		success:refresh_alias_list
		}) 
		
}


function refresh_alias_list(data)
{	
	//alert(jQuery("#method_name").val());
	result = eval('(' + data + ')');
	jQuery("#method_name").html("");
	var size = result.length;
	if (size==0){
		jQuery("#method_name").append("<option  value=1><font size=\"10\">"+"没有查询到发布者信息"+"</font></option>")
		
	}else{
		for(i=0;i< size;i++)
		{
			//jQuery("#method_name").append("<option  value="+result[i].ip + result[i].port + result[i].alias+">"+"别名:"+result[i].alias+"\&nbsp;\&nbsp;\&nbsp;"+ "发布者:"+result[i].ip+":"+result[i].port+"</option>")
			jQuery("#method_name").append("<option  value="+result[i].ip +","+ result[i].port+","+ result[i].alias+">"+"别名:"+result[i].alias+"\&nbsp;\&nbsp;\&nbsp;"+ "发布者:"+result[i].ip+":"+result[i].port+"</option>")
		}
	}
}
//********************************************************************************************************************


function refresh_method(){
	jQuery.ajax({ 
		type:"GET", 
		url:"jQuerselectmethod", 
		data:"interfaceName="+jQuery("#interfaceName").val(), 
		success:refresh_method_list
		}) 
		
}


function refresh_method_list(data)
{	
	//alert(jQuery("#method_name").val());
	result = eval('(' + data + ')');
	jQuery("#quest").html("");
	var size = result.length;
	if (size==0){
		jQuery("#quest").append("<option  value=1><font size=\"10\">"+"没有查询到对应的方法"+"</font></option>")
		
	}else{
		for(i=0;i< size;i++)
		{
			jQuery("#quest").append("<option  value="+result[i]+">"+result[i]+"</option>")
		}
	}
}


//**********************************************************************************************
//获取到jsf输入的数据后，点击调用接口功能
function responsecontent(){
	//获取输入的数据
	//var interfaceName=document.getElementById("interfaceName").value;
	//var method_name=document.getElementById("method_name").value;
	//var quest=document.getElementById("quest").value;
	//var request_param=document.getElementById("request_param").value;
	jQuery.ajax({
		type:"GET", 
		url:"jQuerrequestjsf", 
		data:"interfaceName="+jQuery("#interfaceName").val()+"&"+"method_name="+jQuery("#method_name").val()+"&"+"quest="+jQuery("#quest").val()+"&"+"request_param="+jQuery("#request_param").val(), 
		success:refresh_request_jsf
		}) 
		
}


function refresh_request_jsf(data)
{	
	//alert(jQuery("#method_name").val());
	result = eval('(' + data + ')');
	jQuery("#response_param").html("");
	jQuery("#response_param").val(data)
	
}
//**********************************************************************************************


//**********************************************************************************************
//请求jmq, 广播到各个消费者
function responsJMQecontent(){

	jQuery.ajax({
		type:"GET", 
		url:"jQuerrequestjmq", 
		data:"topic="+jQuery("#topic").val()+"&"+"app="+jQuery("#app").val()+"&"+"request_param_jmq="+jQuery("#request_param_jmq").val(), 
		success:refresh_request_jsf_jmq
		}) 
		
}


function refresh_request_jsf_jmq(data)
{	
	//alert(jQuery("#method_name").val());
	//result = eval('(' + data + ')');
	jQuery("#response_param_jmq").html("");
	jQuery("#response_param_jmq").val(data)
	
}
//*************************************************************************************************





//**********************************************************************************************
//发送http请求
function responsHTTPecontent(){

	jQuery.ajax({
		type:"GET", 
		url:"jQuerrequesthttp", 
		data:"input_url="+jQuery("#input_url").val()+"&"+"protocal_type="+jQuery("#protocal_type").val()+"&"+"request_param_http="+jQuery("#request_param_http").val(), 
		success:refresh_request_http
		}) 
		
}


function refresh_request_http(data)
{	
	//alert(jQuery("#method_name").val());
	//result = eval('(' + data + ')');
	jQuery("#response_param_http").html("");
	jQuery("#response_param_http").val(data)
	
}
//*************************************************************************************************





//**********************************通过adb获取到手机的自动化信息**********************************

function response_iphone_info(){

	jQuery.ajax({
		type:"GET", 
		url:"jQuerrequestiphoneinfo", 
		data:"package_name="+jQuery("#package_name").val(),
		success:refresh_request_iphone_info
		}) 
		
}


function refresh_request_iphone_info(data)
{	
	//alert(jQuery("#method_name").val());
	//result = eval('(' + data + ')');
	jQuery("#response_param_iphoneinfo").html("");
	jQuery("#response_param_iphoneinfo").val(data)
	
}




//*************************************************************************************************




//*********************************通过adb命令批量安装apk安装包************************************

function response_install(){
	//Common.confirm()
	jQuery.ajax({
		type:"GET", 
		url:"jQuerrequestinstall", 
		data:"package_name_install="+jQuery("#package_name_install").val(),
		success:refresh_response_install
		}) 
		
}


function refresh_response_install(data)
{	
	//jQuery("#install_btn").html("");
	//jQuery("#install_btn>span:first").text(data);
	//jQuery("#install_btn").innerHTML(data)
	jQuery("#setstatus").text(data);
}




//*************************************************************************************************






//*********************************生成OOM任务*****************************************************

function response_checkOOM_task(){

	jQuery.ajax({
		type:"GET", 
		url:"jQuerrequestcheckoomtask", 
		data:"package_id="+jQuery("#package_id").val()+"&"+"execut_phone_id="+jQuery("#execut_phone_id").val(),
		success:refresh_response_OOM
		}) 
		
}


function refresh_response_OOM(data)
{	 
   //$("#flsh_list").html(dates);//要刷新的div 
   window
	$.get("/monkey",function(data){
		var html=$("#flsh_list",data);
		$("#flsh_list").html(html);
	});
}	

//*************************************************************************************************






//*******************************    稳定性测试部分    ***********************************************

function response_checkcrash_task(){

	jQuery.ajax({
		type:"GET", 
		url:"jQuerrequestcheckcrashtask",
		data:"package_id_2="+jQuery("#package_id_2").val()+"&"+"execut_phone_id_2="+jQuery("#execut_phone_id_2").val(),
		success:refresh_response_crash
		}) 
		
}


function refresh_response_crash(data)
{	 
   //$("#flsh_list_two").html(dates);//要刷新的div 
   window
	$.get("/monkey",function(data){
		var html=$("#flsh_list_two",data);
		$("#flsh_list_two").html(html);
	});
}	

//*****************************************END****************************************************





//*********************************   深度兼容性测试部分   *********************************************
function response_checkBestTest(){

	jQuery.ajax({
		type:"GET", 
		url:"jQuerrequestcheckBestTest",
		data:"check_package_name="+jQuery("#check_package_name").val()+"&"+"check_install="+jQuery("#check_install").val(),
		success:refresh_response_checkBestTest
		}) 
		
}


function refresh_response_checkBestTest(data)
{	 
   //$("#flsh_list_two").html(dates);//要刷新的div 
   window
	$.get("/monkey",function(data){
		var html=$("#flsh_list_three",data);
		$("#flsh_list_three").html(html);
	});
}	



//***************************************END****************************************************




//*********************************   生成自动化执行脚本   *********************************************
function response_checkScriptTest(){

	jQuery.ajax({
		type: "GET",
		url: "jQuerrequestScriptTest",
		data: "auto_package_name=" + jQuery("#auto_package_name").val()+"&" + "run_iphone=" + jQuery("#run_iphone").val() + "&" + "auto_script=" + jQuery("#auto_script").val(),
		success: refresh_response_checkScript
		})

}


function refresh_response_checkScript(data)
{
   window
	$.get("/monkey",function(data){
		var html=$("#flsh_script_list",data);
		$("#flsh_script_list").html(html);
	});
}

//***************************************   END   ****************************************************



//通过checkbox选中信息，获取执行用例列表信息
function cpk(){
  var obj=document.getElementsByName('selected');
  var s='';
  for(var i=0; i<obj.length; i++){
    if(obj[i].checked) s+=obj[i].value+',';
  }

  if(s==''){
        sAlert('亲,请选择要执行的用例');
        return false;
  }
  window.open("/jqueryjsftotal?jsfcase="+s);
}
