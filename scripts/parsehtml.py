import os
import re

websitePath = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
outputPath = os.path.join(websitePath, 'data.html')

# Save data
fout = open(outputPath, 'w')

def save(str):
	print str
	fout.write(str + '\n')

#####################
# Google scholar
#####################

try:
	p = re.compile('.*Citations</a></td><td class="gsc_rsb_std">([0-9]+).*')
	f = os.path.join(websitePath, 'downloaded/googlescholar_giuliomarin.html')
	with open(f, 'r') as fid:
		content = fid.read()
		numcit = p.search(content)
		if numcit is not None:
			save('<div>numcit: <numcit>%s</numcit></div>' % numcit.group(1))
except:
	print 'Error processing google scholar'

#####################
# Runtastic
#####################

try:
	f = os.path.join(websitePath, 'downloaded/runtastic_giuliomarin.html')
	with open(f, 'r') as fid:
		state = [0]
		for line in fid.readlines():
			if state[0] or ('This month' in line):
				if not state[0]:
					state[0] = 1
					state.append(0)
				if state[1] or ('value' in line):
					if not state[1]:
						state[1] = 1
						state.append(1)
						continue
					if state[2]:
						save('<div>activitiesmonth: <activitiesmonth>%s</activitiesmonth></div>' % line.strip())
						break

	with open(f, 'r') as fid:
		state = [0]
		for line in fid.readlines():
			if state[0] or ('This year' in line):
				if not state[0]:
					state[0] = 1
					state.append(0)
				if state[1] or ('Distance' in line):
					if not state[1]:
						state[1] = 1
						state.append(0)
					if state[2] or ('value' in line):
						if not state[2]:
							state[2] = 1
							state.append(1)
							continue
						if state[3]:
							vals = line.strip().split()
							dist = vals[0]
							unit = vals[1].split('>')[1].split('<')[0]
							save('<div>distyear: <distyear>%s %s</distyear></div>' % (dist, unit))
							break

	fout.close()
except:
	print 'Error processing runtastic'
