"""
	TODO: some xml experiment
"""
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class RuleParser (object):
  def __init__ (self, xmlfile_url):
    self.xmlfile_url=xmlfile_url
    self.tree = ET.parse(xmlfile_url)
    #self.node_tree = self.tree.getiterator('node')
    self.root = self.tree.getroot()
    
  def rule_list_for_session (self, session_number):
  	for child in self.root:
  		#print child.tag, child.attrib
  		if child.get('number') == session_number:
  			lst = []
  			conns = child.find('dpid')
  			for conn in child.iter('connection'):
					dpid = conn.get('dpid')
					typ = conn.find('type').text
					ip = conn.find('wildcards')
					wcsl = []
					wcsl.append(ip.get('src_ip'))
					wcsl.append(ip.get('dst_ip'))
					
					rule = conn.find('rule')
					rulel = []
					if typ == 'forward':
						rulel.append(rule.get('fport'))
						rulel.append(rule.get('duration'))
					elif typ == 'modify_forward':
						rulel.append(rule.get('new_dst_ip'))
						rulel.append(rule.get('new_dst_mac'))
						rulel.append(rule.get('fport'))
						rulel.append(rule.get('duration'))
					else:
						print 'Unrecognized rule type'
						
					rule = [dpid, typ, wcsl, rulel]
					lst.append(rule)
		return lst
def main():
  my_p = RuleParser("scheduling.xml")
  rule_list = my_p.rule_list_for_session('1')
  for rule in rule_list:
  	print rule

if __name__ == "__main__":
  main()



