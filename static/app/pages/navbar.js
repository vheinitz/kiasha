define(['knockout', 'text!./navbar.html'], function(ko, template) {

  function NavBarViewModel(params) {
      app_share.main_view("login");
      this.route = params.route;

	  this.page_topics = function ()
      {
          console.log("page_topics");
          app_share.main_view("topics");
      }

      this.page_home = function () {

          console.log("page_home ");
          app_share.main_view("home");
      }
      
      this.page_surveys = function () {

          console.log("page_surveys ");
          app_share.main_view("survey_list");
      }
      
     
      this.doLogout = function ( ) {
        console.log("doLogout ", app_share.session() );
        
        $.ajax({
                type : "POST",
                url : "/api/user/logout",
                data: JSON.stringify({ session: app_share.session() }, null, '\t'),
                contentType: 'application/json;charset=UTF-8',
                success: function(data) {
                    j =  JSON.parse(data);
                    console.log("doLogin finished: ", j.result );
                    app_share.session( null );
                    app_share.main_view("login");
                    if (j.result !== 'OK')
                    {
                        console.log("TODO Logout error" );
                    }
                }    
           }); 
    };
  }



  return { viewModel: NavBarViewModel, template: template };
});
