define(["knockout", "text!./home.html"], function(ko, template) {

function HomeViewModel(route) {
	console.log( "HomeViewModel" )
	var self = this;

	this.init = function() {	   
		console.log("Home.init");
	};

	self.init();
}

 

  return { viewModel: HomeViewModel, template: template };

});
