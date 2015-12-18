{% extends "templates/base.html" %}

{% block content %}
	<form id='add-reservation' role='form' method='POST' action='/createreservation'>
	    <div class='container-fluid'>
    		<div class='form-group col-lg-12'>
    			You will make an reservation to resource: 
    			"<strong>{{ resource.name|truncate(75,True) }}</strong>" 
    		</div>
	    	<div class='form-group col-lg-12'>
	    		<label for="title">Nickname:</label>
	    		<input type="text" class="form-control" maxlength="256" name="name" placeholder="Name prefered to be called">
	  		</div>
	  	
	  		<input type="hidden" class="form-control" name="rid" value="{{ resource.key.id() }}">

	  		<div class='form-group col-lg-12'>
	  			<label for="title">Description:</label>
	  			<textarea class="form-control" rows="6" placeholder='Your full answer here' name='description' id='review'></textarea>
	  		</div>
		
	    	<div class='form-group col-lg-12'>
	    		<button type="button" class='btn btn-primary' onclick="location.href='/view?rid={{ resource.key.id() }}'">Cancel</button>
	  		<input type='submit' class='btn btn-primary' value='Submit' />
  			</div>
  		</div>
    </form>
{% endblock %}