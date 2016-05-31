define(["knockout", "text!./survey.html"], function(ko, template ) {

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
	    console.log("Survey data Model");
	    var self = this;
		this.Items = ko.observableArray();
		this.error = ko.observable(null);
		this.create_mode = ko.observable(0);
		
		this.survey_name = ko.observable(null);
		this.survey_info = ko.observable(null);
		this.survey_instructions = ko.observable(null);
		this.survey_help = ko.observable(null);
		this.survey_id = ko.observable(null);
		

		this.init = function() {	   
			self.survey_id( app_share.main_view_args[0].survey_id )
			self.survey_name( app_share.main_view_args[0].survey_name )
			self.getData();
			//console.log( "init ID", self.survey_id(), app_share.main_view_args );
		};
		
		this.getData = function( )
		{			
			console.log( "getData " );
			$.ajax({
				type : "POST",
				url : "/api/survey/" + self.survey_id() + "/select",
				data: JSON.stringify(
					{ session: app_share.session()						
					}, null, '\t'),
				contentType: 'application/json;charset=UTF-8',
				success: function(data) {					
					j =  JSON.parse(data);
					console.log("JSON: ", j );
					if (j.result == 'OK')
					{
						self.survey_id( j.data.survey_id )
						self.survey_name( j.data.survey_name )
						self.survey_info( j.data.survey_info )
						self.survey_instructions( j.data.survey_instructions )
						self.survey_help( j.data.survey_help )
					}
					else
					{
						self.error( "ERROR" + j.reason )
					}					
				}
			}); 	
			
		};
		
		this.list = function( )
		{			
			console.log( "listItems " );
			$.ajax({
				type : "POST",
				url : "/api/survey/list",
				data: JSON.stringify(
					{ session: app_share.session()						
					}, null, '\t'),
				contentType: 'application/json;charset=UTF-8',
				success: function(data) {					
					j =  JSON.parse(data);
					console.log("JSON: ", j );
					if (j.result == 'OK')
					{
						self.Items([])
						for(var di in j.data)
						{
							self.Items.push(new Item(self, j.data[di]));
						}
					}
					else
					{
						self.error( "ERROR" + j.reason )
					}					
				}
			}); 	
			
		};

		this.edit = function ( Item) {
		    app_share.main_view_args([Item.data.suevey_id])
		    app_share.main_view('Survey');		  
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
	
		this.save = function ( ) {
			
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
