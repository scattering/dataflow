var tracks = (function ($) {
// local functions/variables

// Put app specific properties (functions or variables) here.  The property
// p will be accessible outside as site.p.
return {

deleteExperiment: function(experimentname, experimentid, projectid, url) {
    // Send alert to have user confirm deletion.
    var choice = confirm("Are you sure you want to delete experiment:  "  + experimentname + "?");
    if (choice == true) {
	// Delete the project via Ajax request
	$.ajax({
	    url: url, // '/myProjects/editProject/'+projectid+'/',
	    type: 'POST',
	    data: {'experiment_id' : experimentid},
	    success: function(response, a, b, c) {
		//projectid is not in scope here; calling another function that has it.
		successfunction();
	    }
	});
	successfunction = function () {
	    inputs = $('input');
	    //skip first and last inputs -- only care about the projects
	    for (var i = 1; i < inputs.length - 1; ++i) {
		if (parseInt(inputs[i].getAttribute('id')) === experimentid) {
		    $(inputs[i].parentElement).remove(); //removes the list <li> element for deleted project
		    break;
		}
	    }
	};
    } else { /*// Do nothing; they did not want to delete the project. */ }
};

deleteProject: function(projectname, projectid, url) {
    // Send alert to have user confirm deletion.
    var choice = confirm("Are you sure you want to delete project:  "  + projectname + "?");
    if (choice == true) {
	// Delete the project via Ajax request
	$.ajax({
	    url: url, // '/myProjects/',
	    type: 'POST',
	    data: {'project_id' : projectid},
	    success: function(response) {
		//projectid is not in scope here; calling another function that has it.
		successfunction();
	    }
	});
	successfunction = function () {
	    inputs = $('input');
	    //skip first and last inputs -- only care about the projects
	    for (var i = 1; i < inputs.length - 1; ++i) {
		if (parseInt(inputs[i].getAttribute('id')) === projectid) {
		    $(inputs[i].parentElement).remove(); //removes the list <li> element for deleted project
		    break;
		}
	    }
	};
    } else { /* Do nothing; they did not want to delete the project. */ }
},


shareProject: function(userid, projectname, projectid, url) {
    // Prompt user for collaborator's email.
    var collaborator_email = prompt("With whom do you want to share Project: " + projectname + "? Enter their email: ", "");

    // Does a null check if they cancel and a length test to check if they entered something.
    // Do a better validation for a valid email here or perhaps in the URL reverse lookup regex?
    if (collaborator_email == null) {
	// Do nothing - they canceled the prompt.
    } else if (collaborator_email.length > 0) {
	$.ajax({
	    url: url, // '/project/collaborate/',
	    type: 'POST',
	    data: {'collaborator_email': collaborator_email, 'user_id' : userid, 'project_id' : projectid},
	    success: function(response) {
		successfunction(response);
	    },
	    failure: function() {
		alert("Failed to contact server. Unable to process request.");
	    }
	});
	successfunction = function (response) {
	    //NOTE: doesn't reach success function in local testing... email fails
	    alert("An email has been sent to " + collaborator_email);
	};
    } else {
	alert("No email was provided.");
    }
} //,

})(jQuery));