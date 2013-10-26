from pylab import *
import numpy.numarray as na

class PerfPlotter(object):
  def __init__(self, actual_res_dict):
    self.plot_head_margin = 0.3
    self.actual_res_dict = actual_res_dict
  
  def show_sching_result(self, s_info_dict, res_info_dict):
    figure(num=1, figsize=(8, 10))
    #
    font = {'size': 10}
    matplotlib.rc('font', **font)
    #
    subplot(311)
    self.plot_session_allocation(s_info_dict)
    subplot(312)
    self.plot_session_perfs(s_info_dict)
    subplot(313)
    self.plot_res_assignment(res_info_dict)
    #
    show()
  
  def save_sching_result(self, s_info_dict, res_info_dict):
    figure(num=1, figsize=(25, 10))
    #
    font = {'size': 10}
    matplotlib.rc('font', **font)
    #
    subplot(311)
    self.plot_session_allocation(s_info_dict)
    subplot(312)
    self.plot_session_perfs(s_info_dict)
    subplot(313)
    self.plot_res_assignment(res_info_dict)
    #
    #Sching dec will be save to a file with name formed by active session #'s
    fname = ''
    for s_id in s_info_dict:
      fname += str(s_id)
    savefig('sching_decs/%s.png' % fname)
  
  def plot_session_allocation(self, s_info_dict):
    width=0.4 #bar width
    sid_len = len(s_info_dict)
    base_info_list = ["bw", "proc", "dur", "n", "stor"]
    bil_len = len(base_info_list)
    x_len = bil_len*sid_len
    #
    def extract_sching_result_plot_data():
      #Assuming s_info_dict and base_info_list are in-sync
      xlocations = {}
      for i in range(0, bil_len):
        xlocations[i] = na.array([x*bil_len+i for x in range(0, sid_len)])+self.plot_head_margin
      #
      data = {'bw':[], 'proc':[], 'dur':[], 'n':[], 'stor':[]}
      for s_id in s_info_dict:
        for base_info in base_info_list:
          data[base_info].append(s_info_dict[s_id][base_info])
      return [data, xlocations]
    #
    [data, xlocations] = extract_sching_result_plot_data()
    #print 'data: ', data
    #print 'xlocations: ', xlocations
    #
    fc_set = ['#9999ff', 'green', '#ff9999', 'k', 'm', 'y', 'c']
    count = 0
    for base_info in base_info_list:
      bar(xlocations[count], data[base_info], width=width, facecolor=fc_set[count], edgecolor='white')
      for j in range(0,sid_len):
        text(xlocations[count][j]+width/2, data[base_info][j]+0.5, \
             '%.2f' % data[base_info][j], \
             ha='center', va= 'bottom', fontsize=9)
      count += 1
    #separating session allocs by vertical lines
    count -= 1
    for i in range(0, sid_len-1):
      mx = (xlocations[count][i]+xlocations[0][i+1])/2 + width/2
      my = axis()[3]/2
      #
      axvline(x = mx)
      text(mx+0.2, my, 'S'+`i+1`, ha='center', va= 'bottom', fontsize=9)
      if i == 0:
        text(0.2, my, 'S'+`i`, ha='center', va= 'bottom', fontsize=9)
      
    """
    #writing session id under the info bar sections
    for i in range(0,sid_len):
      text(self.plot_head_margin+bil_len*(0.3+1*i), -0.08*axis()[3], 'S'+`i`)
    """
    #yticks(range(0,  8))
    # x-axis labeling
    xticks(arange(x_len)+self.plot_head_margin+width/2, base_info_list*sid_len)
    xlim(0, x_len+width*2)
    title("Session Res Alloc")
    gca().get_xaxis().tick_bottom()
    gca().get_yaxis().tick_left()
    #show()
    
  def plot_session_perfs(self, s_info_dict):
    x_scal=0.3
    y_scal=0.1
    base_info_list = ["hard_pi", "soft_pi", "trans_time", "tt", "m_u", "m_p", "x_u", "x_p"]
    bil_len = len(base_info_list)
    sid_len = len(s_info_dict)
    x_len = bil_len*sid_len
    #
    def extract_session_perf_plot_data():
      #Assuming s_info_dict and base_info_list are in-sync
      #xlocations = na.array(range(sid_len))+self.plot_head_margin
      #
      data = {'hard_pi':[], 'soft_pi':[],
              'trans_time':[], 'tt':[],
              'm_u':[], 'm_p':[],
              'x_u':[], 'x_p':[]
             }
      for s_id in s_info_dict:
        for base_info in base_info_list:
          data[base_info].append(s_info_dict[s_id][base_info])
      return data
    #
    data = extract_session_perf_plot_data()
    fc_set = ['#9999ff', 'green', '#ff9999', 'k', 'm', 'y', 'c']
    for i in range(0, bil_len):
      for j in range(0,sid_len):
        text((j+1)*x_scal, (i+1)*y_scal, \
             '%s: %.2f' % (base_info_list[i],data[base_info_list[i]][j] ), \
             ha='center', va= 'bottom', fontsize=9)
    #separating session allocs by vertical lines
    for i in range(0, sid_len-1):
      mx = (i+1)*x_scal+x_scal/2
      my = axis()[3]/2
      #
      axvline(x = mx)
      text(mx+0.05, my, 'S'+`i+1`, ha='center', va= 'bottom', fontsize=9, weight='bold')
      if i == 0:
        text(0.05, my, 'S'+`i`, ha='center', va= 'bottom', fontsize=9, weight='bold')
    #yticks(range(0,  8))
    #ylim(0, axis()[3]*1.2)
    xlim(0, (sid_len+1)*x_scal)
    title("Session Hard & Soft Perfs")
    gca().get_xaxis().tick_bottom()
    gca().get_yaxis().tick_left()
    
  def plot_res_assignment(self, res_info_dict):
    width=0.4 #bar width
    rid_len = len(res_info_dict)
    num_links = self.actual_res_dict['overview']['last_link_index'] + 1
    num_itrs = rid_len-num_links
    x_len = num_links + 2*num_itrs
    #
    def extract_res_assignment_plot_data():
      xlocations = {'bws':None, 'procs':None, 'stors':None}
      xlocations['bws'] = na.array(range(num_links))+self.plot_head_margin
      xlocations['procs'] = self.plot_head_margin + num_links + \
      na.array( range(0, 2*num_itrs, 2))
      xlocations['stors'] = self.plot_head_margin + num_links + \
      na.array( range(1, 2*num_itrs+1, 2))
      #
      data = {'link_bws_actual':[0]*num_links, 'link_bws_cap':[0]*num_links,
              'itr_procs_actual':[0]*num_itrs, 'itr_procs_cap':[0]*num_itrs,
              'itr_stors_actual':[0]*num_itrs, 'itr_stors_model':[0]*num_itrs,
              'itr_stors_cap':[0]*num_itrs}
      id_info_map = self.actual_res_dict['id_info_map']
      for res_id in range(0,rid_len):
        if res_id < num_links: #res is link
          data['link_bws_actual'][res_id] = res_info_dict[res_id]['bw']
          data['link_bws_cap'][res_id] = float(id_info_map[res_id]['bw_cap'])
        else: #res is itr
          id_ = res_id-num_links
          data['itr_procs_actual'][id_] = res_info_dict[res_id]['proc']
          data['itr_procs_cap'][id_] = float(id_info_map[res_id]['proc_cap'])
          #
          data['itr_stors_actual'][id_] = res_info_dict[res_id]['stor_actual']
          data['itr_stors_model'][id_] = res_info_dict[res_id]['stor_model']
          data['itr_stors_cap'][id_] = float(id_info_map[res_id]['stor_cap'])
      return [data, xlocations]
    #
    [data, xlocations] = extract_res_assignment_plot_data()
    #print 'data: ', data
    #print 'xlocations: ', xlocations
    #
    fc_set = ['#9999ff', '#ff9999', 'green', 'k', 'm', 'y', 'c']
    xtick_locs = []
    xtick_strs = []
    #
    bw_bars = bar(xlocations['bws'], data['link_bws_actual'], width=width, facecolor=fc_set[0], edgecolor='white', label="bw")
    bar(xlocations['bws'], data['link_bws_cap'], width=width, facecolor=fc_set[0], fill=False)
    for j in range(0,num_links):
      text(xlocations['bws'][j]+width/2, data['link_bws_actual'][j]+0.5, \
           '%i' % data['link_bws_actual'][j], \
           ha='center', va= 'bottom', fontsize=9)
      xtick_strs.append('L%i' % j)
    xtick_locs.extend(xlocations['bws']+width/2)
    #
    proc_bars = bar(xlocations['procs'], data['itr_procs_actual'], width=width, facecolor=fc_set[1], edgecolor='white', label="proc")
    bar(xlocations['procs'], data['itr_procs_cap'], width=width, facecolor=fc_set[1], fill=False)
    for j in range(0,num_itrs):
      text(xlocations['procs'][j]+width/2, data['itr_procs_actual'][j]+0.5, \
           '%i' % data['itr_procs_actual'][j], \
           ha='center', va= 'bottom', fontsize=9)
      xtick_strs.append('T%i' % j)
    xtick_locs.extend(xlocations['procs']+width/2+0.5)
    #
    stor_bars = bar(xlocations['stors'], data['itr_stors_actual'], width=width, facecolor=fc_set[2], edgecolor='white', label="stor")
    bar(xlocations['stors'], data['itr_stors_cap'], width=width, facecolor=fc_set[2], fill=False)
    for j in range(0,num_itrs):
      text(xlocations['stors'][j]+width/2, data['itr_stors_actual'][j]+0.5, \
           '%i' % data['itr_stors_actual'][j], \
           ha='center', va= 'bottom', fontsize=9)
    legend() #labeling by legend
    #yticks(range(0,  8))
    # x-axis labeling
    xticks(xtick_locs, xtick_strs)
    xlim(0, x_len+width*2)
    title("Resource Occupation - Cap")
    gca().get_xaxis().tick_bottom()
    gca().get_yaxis().tick_left()
    #show()
    
def main():
  pass

if __name__ == "__main__":
  main()
