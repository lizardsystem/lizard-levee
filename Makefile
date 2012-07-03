all:

	echo "note: if this fails at lines starting with \"&\" and \"@\" characters, update less to the latest version:"
	echo "      # npm install less"
	lessc lizard_levee/static/lizard_levee/lizard_levee.less lizard_levee/static/lizard_levee/lizard_levee.css
#	 coffee -c lizard_levee/static/lizard_levee/levee.coffee
