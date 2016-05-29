define(["knockout", "text!./users.html"], function(ko, template ) {

	var User = function( model, data) {
		//console.log( "User", JSON.stringify(data) );
		var self = this;	
		this.model = model;	
		this.data = data;
		this.select = function() {
			console.log("select:" + self.data.id);
			self.model.selectUser( self )	
		}.bind(this);
        
	}	
	
 	function UsersViewModel()
	{
	    console.log("UsersViewModel");
	    var self = this;
		this.Users = ko.observableArray();

		

		console.log("Pages", app_share.app_pages);

		this.init = function() {	   
			self.listUsers();
			console.log( "init" );
		};

		this.listUsers = function( )
		{
			console.log( "listUsers " );
			$.post('/users','{"session":"ABCDEFG"}', function(data) {
				//console.log( "listUsers ... ", data );
				js =  JSON.parse(data);
				//console.log( js.length, "================================" );
				//console.log( js );
				//console.log( "============================================" );
				
				self.Users([]);
				
				for(var di in js)
				{
					//self.Users.push({id:js.devices[dev], type:"HELIOS", info:"Floor 001" });
					self.Users.push(new User(self, js[di]));
					//console.log( "INSTR:", di, data[di].first_name, data[di].photo_200 );
				}
				//setTimeout(self.listUsers.bind(self), 3000);
			});
		};

		this.selectUser = function ( user) {
		    console.log("selectUser ", user.data.id);
		    app_share.user_id(user.data.id)
		    app_share.main_view('user');		  
		};

		this.init();
	}

  return { viewModel: UsersViewModel, template: template };

});
