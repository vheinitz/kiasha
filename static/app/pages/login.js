define(["knockout", "text!./login.html"], function(ko, template) {

function Model(route) {
	console.log( "Model" )
	var self = this;
	this.user = ko.observable('');
	this.password = ko.observable('');
    this.error = ko.observable(null);

	this.doLogin = function ( ) {
	    console.log("doLogin ", self.user(), self.password() );

		  $.ajax({
			type : "POST",
			url : "/api/user/login",
			data: JSON.stringify({ user: this.user(), password: this.password() }, null, '\t'),
			contentType: 'application/json;charset=UTF-8',
			success: function(data) {
				console.log("doLogin finished: ", data );
				j =  JSON.parse(data);
				console.log("doLogin finished: ", j.result, " ",j.session );
				if (j.result == 'OK')
				{
					app_share.session( j.session );
                    app_share.main_view("home");
                    self.error(null)
				}
				else
                {
					self.error( "Username or password wrong!" )
                    app_share.session( null );
                }
		        
			}
		});  	    	  
	};

	this.doRegister = function ( ) {
	    console.log("doRegister ");	    	  
	};

	this.init = function() {	   
		console.log("Login.init");
		app_share.session( "dbg_admin" );
        app_share.main_view("survey_list");

	};

	self.init();
}

 

  return { viewModel: Model, template: template };

});
