Basic Usage
============
The basic usage of json_justify is shown here which is used to validate data from source

.. code-block:: python
	
	from json_justify import JsonManager
	from json_justify.fields import String,Number,Boolean,Array

	class Js(JsonManager):
		name = String("name")
		age = Number("age")
		male = Boolean("male")
		friends = Array("friends")

	data = {
		"name" : "john doe",
		"age" : 120,
		"male" : False,
		"friends" : ["Jelly","Kelly"]
		}
	# This will return True
	js = Js(data = data)
	data.is_valid()
    