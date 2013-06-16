from xml.dom import minidom
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
		self.hm_from_dpid = {}
  
  def indent(self, elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            self.indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
  
  def prettify(self, elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")
    
  def modify_by_cmd(self, xml_path_rule):
    """Modify the rule xml file according to newly rxed xml_path_rule
    """
    lst = self.rule_dict_rxed_cmd_from_sch(xml_path_rule)
    print 'lst: ', lst
    
    for session in lst:
      for child in self.root:
        if child.get('number') == session:
          self.root.remove(child) #old sch for session is deleted
          #write the new session xml rule
          new_session = ET.Element('session')
          new_session.set('number', session)
          for conn in lst[session]:
            new_conn = ET.SubElement(new_session, 'connection')
            new_conn.set('dpid', conn[0])
            new_conn.set('from', conn[1])
            new_type = ET.SubElement(new_conn, 'type')
            new_type.text = lst[session][conn]['typ']
            new_wcs = ET.SubElement(new_conn, 'wildcards')
            new_wcs.set('src_ip',lst[session][conn]['wc_dict']['src_ip'])
            new_wcs.set('dst_ip',lst[session][conn]['wc_dict']['dst_ip'])
            new_rule = ET.SubElement(new_conn, 'rule')
            if new_type.text == 'forward':
              new_rule.set('fport', lst[session][conn]['rule_dict']['fport'])
              new_rule.set('duration', lst[session][conn]['rule_dict']['duration'])
            elif new_type.text == 'modify_forward':
              new_rule.set('fport', lst[session][conn]['rule_dict']['fport'])
              new_rule.set('duration', lst[session][conn]['rule_dict']['duration'])
              new_rule.set('new_dst_ip', lst[session][conn]['rule_dict']['new_dst_ip'])
              new_rule.set('new_dst_mac', lst[session][conn]['rule_dict']['new_dst_mac'])
            
          self.root.append((new_session))
          self.indent(self.root,0)
          self.tree.write(self.xmlfile_url)
          return
          
  def rule_dict_rxed_cmd_from_sch(self, xml_path_rule):
    lst = {}
    root = ET.fromstring(xml_path_rule)
    for child in root:
      print "child.get('number'): ", child.get('number')
      session_number = child.get('number')
      lst[session_number] = {}
      for conn in child.iter('connection'):
        dpid = conn.get('dpid')
        fromm = conn.get('from')
        tup = dpid, fromm

        typ = conn.find('type').text
        ip = conn.find('wildcards')
        wc_dict = {}
        wc_dict['src_ip'] = ip.get('src_ip')
        wc_dict['dst_ip'] = ip.get('dst_ip')

        rule = conn.find('rule')
        rule_dict = {}
        if typ == 'forward':
          rule_dict['fport'] = rule.get('fport')
          rule_dict['duration'] = rule.get('duration')
        elif typ == 'modify_forward':
          rule_dict['new_dst_ip'] = rule.get('new_dst_ip')
          rule_dict['new_dst_mac'] = rule.get('new_dst_mac')
          rule_dict['fport'] = rule.get('fport')
          rule_dict['duration'] = rule.get('duration')
        else:
          print 'Unrecognized rule type'

        lst[session_number][tup] = { 'typ': typ, 'wc_dict': wc_dict, 'rule_dict': rule_dict}

    return lst  
  
  def rule_dict_for_session (self, session_number):
  	lst = {}
  	for child in self.root:
  		#print child.tag, child.attrib
  		if child.get('number') == session_number:
  			#conns = child.find('dpid')
  			for conn in child.iter('connection'):
					dpid = conn.get('dpid')
					fromm = conn.get('from')
					tup = dpid, fromm
					
					typ = conn.find('type').text
					ip = conn.find('wildcards')
					wc_dict = {}
					wc_dict['src_ip'] = ip.get('src_ip')
					wc_dict['dst_ip'] = ip.get('dst_ip')
					
					rule = conn.find('rule')
					rule_dict = {}
					if typ == 'forward':
						rule_dict['fport'] = rule.get('fport')
						rule_dict['duration'] = rule.get('duration')
					elif typ == 'modify_forward':
						rule_dict['new_dst_ip'] = rule.get('new_dst_ip')
						rule_dict['new_dst_mac'] = rule.get('new_dst_mac')
						rule_dict['fport'] = rule.get('fport')
						rule_dict['duration'] = rule.get('duration')
					else:
						print 'Unrecognized rule type'
					
					lst[tup] = { 'typ': typ, 'wc_dict': wc_dict, 'rule_dict': rule_dict}
					
		return lst
	
  def rule_dict_for_session_I (self, session_number):	
    lst = {}
    for child in self.root:
      if child.get('number') == session_number:
        for conn in child.iter('connection'):
          dpid = conn.get('dpid')
					
          typ = conn.find('type').text
          ip = conn.find('wildcards')
          wc_dict = {}
          wc_dict['src_ip'] = ip.get('src_ip')
          wc_dict['dst_ip'] = ip.get('dst_ip')

          rule = conn.find('rule')
          rule_dict = {}
          if typ == 'forward':
					  rule_dict['fport'] = rule.get('fport')
					  rule_dict['duration'] = rule.get('duration')
          elif typ == 'modify_forward':
            rule_dict['new_dst_ip'] = rule.get('new_dst_ip')
            rule_dict['new_dst_mac'] = rule.get('new_dst_mac')
            rule_dict['fport'] = rule.get('fport')
            rule_dict['duration'] = rule.get('duration')
          else:
            print 'Unrecognized rule type'

          if dpid in self.hm_from_dpid:
            print 'it is in'
            self.hm_from_dpid[dpid] = self.hm_from_dpid[dpid] + 1;
          else:
            self.hm_from_dpid[dpid] = 0

          tup = dpid, self.hm_from_dpid[dpid]
          lst[tup] = { 'typ': typ, 'wc_dict': wc_dict, 'rule_dict': rule_dict}

    return lst
		
def main():
  my_p = RuleParser("scheduling.xml")
  """
  rule_dict = my_p.rule_dict_for_session_I('1')
  for k,v in rule_dict.iteritems():
  	print k, "- ", v, "\n"
  
  print my_p.hm_from_dpid
  """
  xml_path_rule = '<scheduling><session number="1"><connection dpid="11" from="10.0.0.2"><type>forward</type><wildcards src_ip="10.0.0.2" dst_ip="10.0.0.1"/><rule fport="2" duration="50"/></connection><connection dpid="1" from="10.0.0.2"><type>modify_forward</type><wildcards src_ip="10.0.0.2" dst_ip="10.0.0.1"/><rule new_dst_ip="10.0.0.11" new_dst_mac="00:00:00:00:01:01" fport="4" duration="50"/></connection><connection dpid="1" from="10.0.0.11"><type>forward</type><wildcards src_ip="10.0.0.11" dst_ip="10.0.0.21"/><rule fport="2" duration="50"/></connection><connection dpid="2" from="10.0.0.21"><type>forward</type><wildcards src_ip="10.0.0.21" dst_ip="10.0.0.1"/><rule fport="4" duration="50"/></connection><connection dpid="12" from="10.0.0.21"><type>forward</type><wildcards src_ip="10.0.0.21" dst_ip="10.0.0.1"/><rule fport="3" duration="50"/></connection></session></scheduling>'
  #print my_p.rule_dict_rxed_cmd_from_sch(xml_path_rule)
  
  my_p.modify_by_cmd(xml_path_rule)
  
if __name__ == "__main__":
  main()



