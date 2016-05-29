define(["knockout", "text!./survey_list.html"], function(ko, template ) {

	var Item = function( model, data) {
		//console.log( "Item", JSON.stringify(data) );
		var self = this;	
		this.model = model;	
		this.data = data;
		this.edit = function() {
			console.log("select:" + self.data.id);
			self.model.edit( self )	
		}.bind(this);
		
		this.remove = function() {
			console.log("remove:" + self.data.id);
			self.model.remove( self )	
		}.bind(this);
        
	}	
	
 	function Model()
	{
	    console.log("Items Model");
	    var self = this;
		this.Items = ko.observableArray();
		this.error = ko.observable(null);
		this.create_mode = ko.observable(0);
		
		this.new_name = ko.observable(null);

		

		console.log("Pages", app_share.app_pages);

		this.init = function() {	   
			self.list();
			console.log( "init" );
		};

		this.list = function( )
		{
			console.log( "listItems " );
			$.post('/api/survey/list','{"session":"%s"}'%app_share.session(), function(data) {
				//console.log( "listItems ... ", data );
				js =  JSON.parse(data);
				
				console.log( js );
				
				self.Items([]);
				
				/*for(var di in js)
				{
					self.Items.push(new Item(self, js[di]));
				}*/				
			});
		};

		this.edit = function ( Item) {
		    //app_share.main_view_args(Item.data.id)
		    app_share.main_view('Item');		  
		};
		
		this.remove = function ( Item) {
			console.log("add: ", Item.data );
		    $.ajax({
				type : "POST",
				url : "/api/survey/" + Item.data.survey_id + "/delete" ,
				data: JSON.stringify(
					{ session: app_share.session()						
					}, null, '\t'),
				contentType: 'application/json;charset=UTF-8',
				success: function(data) {
					console.log("add: ", data );
					j =  JSON.parse(data);
					if (j.result == 'OK')
					{
						self.list()
					}
					else
					{
						self.error( "ERROR" + j.reason )
					}
					
				}
			}); 		  
		};
		
		this.create_mode_on = function ( ) {
			self.create_mode(1);
		}
	
		this.add = function ( ) {
			$.ajax({
				type : "POST",
				url : "/api/survey/add",
				data: JSON.stringify(
					{ 
						session: app_share.session(), 
						survey_name: self.new_name(), 
						survey_info: 'survey_instructions',
						survey_instructions: 'survey_instructions',
						survey_help: ''
					}, null, '\t'),
				contentType: 'application/json;charset=UTF-8',
				success: function(data) {
					console.log("add: ", data );
					j =  JSON.parse(data);
					console.log("add: ", j.result, " ",j.data );
					j.data.survey_name = self.new_name();
					if (j.result == 'OK')
					{
						console.log("add: ", j.result, " ",j.data );
						self.error(null)
						self.Items.push(new Item(self, j.data));
						self.create_mode(0);
						self.new_name('');
					}
					else
					{
						self.error( "ERROR" + j.reason )
					}
					
				}
			});  	  
				
		    //self.Items.push(new Item(self, {name:self.new_name()} ));	  
		};

		this.init();
	}

  return { viewModel: Model, template: template };

});
