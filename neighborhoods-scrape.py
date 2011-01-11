import mechanize

states = ["AL", "Alabama", "AK", "Alaska", "AZ", "Arizona", "AR", "Arkansas", "CA", "California", "CO", "Colorado", "CT", "Connecticut", "DE", "Delaware", "DC", "District Of Columbia", "FL", "Florida", "GA", "Georgia", "HI", "Hawaii", "ID", "Idaho", "IL", "Illinois", "IN", "Indiana", "IA", "Iowa", "KS", "Kansas", "KY", "Kentucky", "LA", "Louisiana", "ME", "Maine", "MD", "Maryland", "MA", "Massachusetts", "MI", "Michigan", "MN", "Minnesota", "MS", "Mississippi", "MO", "Missouri", "MT", "Montana", "NE", "Nebraska", "NV", "Nevada", "NH", "New Hampshire", "NJ", "New Jersey", "NM", "New Mexico", "NY", "New York", "NC", "North Carolina", "ND", "North Dakota", "OH", "Ohio", "OK", "Oklahoma", "OR", "Oregon", "PA", "Pennsylvania", "RI", "Rhode Island", "SC", "South Carolina", "SD", "South Dakota", "TN", "Tennessee", "TX", "Texas", "UT", "Utah", "VT", "Vermont", "VA", "Virginia", "WA", "Washington", "WV", "West Virginia", "WI", "Wisconsin", "WY", "Wyoming"]

debug = True

file = open("/tmp/communities.csv", "w")

for state in states:

    if state and len(state) == 2:
        url = "http://realestate.smarteragent.com/SA/BasicSearchPage.action?state=%s" % state
	if debug:
		print "\n"
		print "\n"
		print "Url: %s" % url
        br = mechanize.Browser()
        br.open(url)
        
        cities = []
        allforms = list(br.forms())
	if debug:
        	print "There are %d forms" % len(allforms)
        
        for i, form in enumerate(allforms):
            #print "--------------------"
            #print form
            #print "br.forms()[%d] br.select_form(name='%s')" % (i, form.name)
            br.form = allforms[i]  #  br.select_form(name=form.name) works only if name is not None
            
            # loop through the controls in the form
            for control in br.form.controls:
                # (could group the controls by type)
                #r = [ ]
                #r.append("  - type=%s, name=%s, value=%s, disabled=%s, readonly=%s" %  (control.type, control.name, br[control.name], control.disabled,  control.readonly))
        
                if control.name and control.name == "city":
                        for item in control.items:
                            if item and item.name:
                               cities.append(item.attrs['value'])
                    
       
	if debug: 
		print "Cities for State %s" % state
        	print cities
        
        for city in cities:
            if not city:
                continue
            url = "http://realestate.smarteragent.com/SA/BasicSearchPage.action?state=%s&city=%s" % (state, city.replace(' ', '+'))
	    if debug:
		print url
            br = mechanize.Browser()
            br.open(url)
        
            if not br:
                continue
        
            try:
                hoods = []
                allforms = list(br.forms())
                if not allforms:
                    continue
                #print "There are %d forms" % len(allforms)
                
                for i, form in enumerate(allforms):
                    #print "--------------------"
                    #print form
                    #print "br.forms()[%d] br.select_form(name='%s')" % (i, form.name)
                    br.form = allforms[i]  #  br.select_form(name=form.name) works only if name is not None
                    
                    # loop through the controls in the form
                    for control in br.form.controls:
                        # (could group the controls by type)
                        #r = [ ]
                        #r.append("  -  type=%s, name=%s, value=%s, disabled=%s, readonly=%s" %  (control.type,  control.name, br[control.name], control.disabled,  control.readonly))
                
                        if control.name and control.name == "neighborhood":
                                for item in control.items:
                                    if item and item.name:
                                       hoods.append(item.attrs['value'])
				       if item.attrs['value']:
					item.attrs['value'] = item.attrs['value'].replace('"',"")
				       	line = '"%s","%s","%s"\n' % (state, city, item.attrs['value'])
				       	if debug:
						print line
				       	file.write(line)
            except:
                pass
        
            #print city
            #print hoods

    
        
        """
        for i, form in enumerate(allforms):
            print "--------------------"
            print form
            print "br.forms()[%d] br.select_form(name='%s')" % (i, form.name)
            br.form = allforms[i]  #  br.select_form(name=form.name) works only if name is not None
            
            # loop through the controls in the form
            for control in br.form.controls:
                if not control.name:
                    print " - type=", (control.type)
                    continue
        
                # (could group the controls by type)
                r = [ ]
                r.append(" - type=%s, name=%s, value=%s, disabled=%s, readonly=%s" % \
                         (control.type, control.name, br[control.name], control.disabled, control.readonly))
                if control.type == 'radio':
                    for item in control.items:
                        r.append("    name=%s" % (item.name))
        
                if control.type == 'select':
                    for item in control.items:
                        r.append("     value=%s, labels=%s" % (str(item), [label.text  for label in item.get_labels()]))
                print "\n".join(r)
        
        r = [ "Links:" ]
        for link in br.links():
            r.append("   %s" % str(link))
        print "\n".join(r)
        """

file.close()
